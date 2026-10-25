"""Service layer for the Live Government Crawler Demo.
Encapsulates crawl orchestration, rate limiting adherence, and cryptographic lineage verification.
"""

import hashlib
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import requests

from pmc_recon.ingest.polite_crawler import PoliteCrawler
from pmc_recon.storage.db import DatabaseEngine


@dataclass
class CrawlResult:
    """Structured result returned by the crawler service for UI presentation."""
    status_code: int
    url: str
    doc_id: str
    content_hash: str
    size_bytes: int
    storage_path: str
    user_agent: str
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    cache_control: Optional[str] = None
    payload_preview: str = ""
    error_message: Optional[str] = None


class CrawlerDemoService:
    """Orchestrates live crawling and provides cryptographic lineage audit routines."""

    def __init__(self, db: DatabaseEngine, request_interval_sec: float = 2.0):
        self.db = db
        self.crawler = PoliteCrawler(
            raw_store=db,
            request_interval_sec=request_interval_sec
        )

    def run_live_crawl(
        self,
        url: str,
        run_id: Optional[str] = None,
        session: Optional[requests.Session] = None
    ) -> CrawlResult:
        """Execute a polite crawl and prepare inspection metadata for the dashboard."""
        active_run_id = run_id or f"ui_crawl_{int(time.time())}"
        fetch_res = self.crawler.fetch_url(
            url=url,
            run_id=active_run_id,
            session=session
        )

        if not fetch_res:
            return CrawlResult(
                status_code=500,
                url=url,
                doc_id="",
                content_hash="",
                size_bytes=0,
                storage_path="",
                user_agent=self.crawler.user_agent,
                error_message="Network unreachable or connection timed out."
            )

        if fetch_res.get("status_code") != 200:
            return CrawlResult(
                status_code=fetch_res["status_code"],
                url=url,
                doc_id="",
                content_hash="",
                size_bytes=0,
                storage_path="",
                user_agent=self.crawler.user_agent,
                error_message=f"HTTP server responded with status {fetch_res['status_code']}."
            )

        doc_id = fetch_res["raw_doc_id"]
        content_hash = fetch_res["content_hash"]
        raw_text = fetch_res.get("content", "")

        # Retrieve file path and size from database
        storage_path = ""
        size_bytes = 0
        with self.db._get_connection() as conn:
            row = conn.execute(
                "SELECT storage_path, size_bytes FROM raw_documents WHERE doc_id = ?",
                (doc_id,)
            ).fetchone()
            if row:
                storage_path = row["storage_path"]
                size_bytes = row["size_bytes"]

        return CrawlResult(
            status_code=200,
            url=url,
            doc_id=doc_id,
            content_hash=content_hash,
            size_bytes=size_bytes,
            storage_path=storage_path,
            user_agent=self.crawler.user_agent,
            etag=fetch_res.get("etag"),
            last_modified=fetch_res.get("last_modified"),
            cache_control=fetch_res.get("cache_control"),
            payload_preview=raw_text[:2000]
        )

    def verify_disk_lineage(self, doc_id: str) -> Dict[str, Any]:
        """Cryptographically re-hash disk file to prove mathematical immutability (Theorem 1)."""
        with self.db._get_connection() as conn:
            row = conn.execute(
                "SELECT storage_path, content_hash, size_bytes FROM raw_documents WHERE doc_id = ?",
                (doc_id,)
            ).fetchone()

        if not row:
            return {
                "verified": False,
                "error": f"Document ID '{doc_id}' not found in registry."
            }

        stored_hash = row["content_hash"]
        file_path = self.db.raw_dir / row["storage_path"]

        if not file_path.exists():
            return {
                "verified": False,
                "error": f"Raw payload file missing on disk at '{file_path}'."
            }

        with open(file_path, "rb") as f:
            disk_bytes = f.read()

        computed_hash = hashlib.sha256(disk_bytes).hexdigest()
        is_identical = (computed_hash == stored_hash)

        return {
            "verified": is_identical,
            "doc_id": doc_id,
            "stored_hash": stored_hash,
            "computed_hash": computed_hash,
            "size_bytes": len(disk_bytes),
            "file_path": str(file_path)
        }
