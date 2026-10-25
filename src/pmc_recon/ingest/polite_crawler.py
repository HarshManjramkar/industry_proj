"""Polite Web Crawler & Content-Addressed Fetcher for Public Procurement Portals.
Implements NFR-01 (Politeness, Rate-limiting, User-Agent identification) and FR-03/FR-04.
"""

import time
import urllib.parse
from typing import Optional, Dict, Any
import requests
from pmc_recon.storage.interfaces import RawDocumentStore


class PoliteCrawler:
    """Polite HTTP crawler adhering strictly to PDR Section 10 & NFR-01."""

    def __init__(
        self,
        raw_store: RawDocumentStore,
        request_interval_sec: float = 2.0,
        user_agent: str = "PMCProcurementReconciliationBot/1.0 (+research@pmc-recon.org)",
        timeout_sec: float = 10.0
    ):
        self.raw_store = raw_store
        self.request_interval_sec = request_interval_sec
        self.user_agent = user_agent
        self.timeout_sec = timeout_sec
        self.last_request_time: Dict[str, float] = {}

    def _respect_rate_limit(self, domain: str) -> None:
        """Enforces at least request_interval_sec delay between consecutive host hits."""
        now = time.time()
        last_time = self.last_request_time.get(domain, 0.0)
        elapsed = now - last_time
        if elapsed < self.request_interval_sec:
            time.sleep(self.request_interval_sec - elapsed)
        self.last_request_time[domain] = time.time()

    def fetch_url(
        self,
        url: str,
        run_id: str,
        session: Optional[requests.Session] = None,
        etag: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch page with rate limiting, User-Agent identity, and conditional headers."""
        domain = urllib.parse.urlparse(url).netloc
        self._respect_rate_limit(domain)

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/json,*/*",
        }
        if etag:
            headers["If-None-Match"] = etag

        http = session or requests.Session()
        try:
            response = http.get(url, headers=headers, timeout=self.timeout_sec)
        except requests.RequestException:
            return None

        # Return unchanged signal on 304 Not Modified
        if response.status_code == 304:
            return {"status_code": 304, "unchanged": True}

        if response.status_code != 200:
            return {"status_code": response.status_code, "error": True}

        payload_bytes = response.content
        raw_doc = self.raw_store.save_raw_payload(
            run_id=run_id,
            payload_bytes=payload_bytes,
            filename_prefix=domain.replace(".", "_")
        )

        return {
            "status_code": 200,
            "content": response.text,
            "raw_doc_id": raw_doc.doc_id,
            "content_hash": raw_doc.content_hash,
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "cache_control": response.headers.get("Cache-Control")
        }
