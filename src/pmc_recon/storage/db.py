"""Database schema and storage engine for PMC Procurement Reconciliation.
Provides immutable raw document storage and versioned record snapshots.
"""

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from pmc_recon.models.entities import RawDocument, TenderRecord, BudgetLine, ChangeEvent, EntityLink, Flag, ReviewDecision


class DatabaseEngine:
    def __init__(self, db_path: str = "pmc_recon.db", raw_dir: str = "data/raw_store"):
        self.db_path = db_path
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                base_url TEXT NOT NULL,
                owner_dept TEXT NOT NULL,
                access_method TEXT NOT NULL,
                terms_status TEXT NOT NULL,
                crawl_frequency TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS raw_documents (
                doc_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                storage_path TEXT NOT NULL,
                content_hash TEXT UNIQUE NOT NULL,
                size_bytes INTEGER NOT NULL,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tenders (
                tender_id TEXT PRIMARY KEY,
                reference_number TEXT NOT NULL,
                title TEXT NOT NULL,
                department_chain TEXT NOT NULL,
                published_date TEXT,
                closing_date TEXT,
                opening_date TEXT,
                value_inr REAL NOT NULL,
                fee_inr REAL,
                emd_inr REAL,
                status TEXT NOT NULL,
                corrigenda_count INTEGER DEFAULT 0,
                source_name TEXT NOT NULL,
                raw_doc_id TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tender_versions (
                version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tender_id TEXT NOT NULL,
                snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attributes_json TEXT NOT NULL,
                version_hash TEXT NOT NULL,
                FOREIGN KEY (tender_id) REFERENCES tenders(tender_id)
            );

            CREATE TABLE IF NOT EXISTS budget_lines (
                budget_head_code TEXT,
                fiscal_year TEXT,
                description_marathi TEXT NOT NULL,
                description_english TEXT,
                department TEXT NOT NULL,
                amount_type TEXT NOT NULL,
                amount_inr_crore REAL NOT NULL,
                source_file TEXT NOT NULL,
                PRIMARY KEY (budget_head_code, fiscal_year, amount_type)
            );

            CREATE TABLE IF NOT EXISTS change_events (
                change_id TEXT PRIMARY KEY,
                record_id TEXT NOT NULL,
                record_type TEXT NOT NULL,
                change_type TEXT NOT NULL,
                changed_fields_json TEXT NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS entity_links (
                link_id TEXT PRIMARY KEY,
                left_record_id TEXT NOT NULL,
                right_record_id TEXT NOT NULL,
                method TEXT NOT NULL,
                confidence REAL NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS flags (
                flag_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                benign_explanations_json TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS reviews (
                review_id TEXT PRIMARY KEY,
                flag_id TEXT NOT NULL,
                reviewer TEXT NOT NULL,
                outcome TEXT NOT NULL,
                comment TEXT NOT NULL,
                reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flag_id) REFERENCES flags(flag_id)
            );
            """)

    def save_raw_payload(self, run_id: str, payload_bytes: bytes, filename_prefix: str = "payload") -> RawDocument:
        content_hash = hashlib.sha256(payload_bytes).hexdigest()
        doc_id = f"doc_{content_hash[:12]}"
        storage_rel_path = f"{run_id}_{filename_prefix}_{doc_id}.bin"
        storage_full_path = self.raw_dir / storage_rel_path

        if not storage_full_path.exists():
            with open(storage_full_path, "wb") as f:
                f.write(payload_bytes)

        raw_doc = RawDocument(
            doc_id=doc_id,
            run_id=run_id,
            storage_path=str(storage_rel_path),
            content_hash=content_hash,
            size_bytes=len(payload_bytes),
        )

        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR IGNORE INTO raw_documents (doc_id, run_id, storage_path, content_hash, size_bytes, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (raw_doc.doc_id, raw_doc.run_id, raw_doc.storage_path, raw_doc.content_hash, raw_doc.size_bytes, raw_doc.fetched_at.isoformat()))
        return raw_doc

    def upsert_tender(self, tender: TenderRecord) -> Optional[ChangeEvent]:
        tender_json = tender.model_dump_json()
        version_hash = hashlib.sha256(tender_json.encode("utf-8")).hexdigest()

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM tenders WHERE tender_id = ?", (tender.tender_id,))
            existing = cur.fetchone()

            change_event: Optional[ChangeEvent] = None
            if not existing:
                cur.execute("""
                INSERT INTO tenders (tender_id, reference_number, title, department_chain, published_date,
                                    closing_date, opening_date, value_inr, fee_inr, emd_inr, status,
                                    corrigenda_count, source_name, raw_doc_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (tender.tender_id, tender.reference_number, tender.title, tender.department_chain,
                      str(tender.published_date) if tender.published_date else None,
                      str(tender.closing_date) if tender.closing_date else None,
                      str(tender.opening_date) if tender.opening_date else None,
                      tender.value_inr, tender.fee_inr, tender.emd_inr, tender.status.value,
                      tender.corrigenda_count, tender.source_name, tender.raw_doc_id))
                change_event = ChangeEvent(
                    change_id=f"chg_new_{tender.tender_id}_{version_hash[:8]}",
                    record_id=tender.tender_id,
                    record_type="tender",
                    change_type="new",
                    changed_fields=json.loads(tender.model_dump_json())
                )
            else:
                # Compare for field changes
                diffs = {}
                for field in ["value_inr", "closing_date", "status", "corrigenda_count"]:
                    old_val = existing[field]
                    new_val = getattr(tender, field)
                    if hasattr(new_val, "value"):
                        new_val = new_val.value
                    if str(old_val) != str(new_val):
                        diffs[field] = {"old": old_val, "new": new_val}

                if diffs:
                    cur.execute("""
                    UPDATE tenders SET value_inr = ?, closing_date = ?, status = ?,
                                      corrigenda_count = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE tender_id = ?
                    """, (tender.value_inr, str(tender.closing_date) if tender.closing_date else None,
                          tender.status.value, tender.corrigenda_count, tender.tender_id))
                    change_event = ChangeEvent(
                        change_id=f"chg_mod_{tender.tender_id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                        record_id=tender.tender_id,
                        record_type="tender",
                        change_type="modified",
                        changed_fields=diffs
                    )

            # Record version snapshot
            cur.execute("""
            INSERT INTO tender_versions (tender_id, attributes_json, version_hash)
            VALUES (?, ?, ?)
            """, (tender.tender_id, tender_json, version_hash))

            if change_event:
                cur.execute("""
                INSERT OR REPLACE INTO change_events (change_id, record_id, record_type, change_type, changed_fields_json, detected_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (change_event.change_id, change_event.record_id, change_event.record_type,
                      change_event.change_type.value, json.dumps(change_event.changed_fields), change_event.detected_at.isoformat()))

        return change_event

    def insert_budget_line(self, line: BudgetLine) -> None:
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO budget_lines (budget_head_code, fiscal_year, description_marathi,
                                                description_english, department, amount_type,
                                                amount_inr_crore, source_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (line.budget_head_code, line.fiscal_year, line.description_marathi,
                  line.description_english, line.department, line.amount_type.value,
                  line.amount_inr_crore, line.source_file))

    def insert_flag(self, flag: Flag) -> None:
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO flags (flag_id, rule_id, title, severity, evidence_json,
                                         benign_explanations_json, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (flag.flag_id, flag.rule_id, flag.title, flag.severity.value,
                  json.dumps(flag.evidence), json.dumps(flag.benign_explanations),
                  flag.status.value, flag.created_at.isoformat()))

    def record_review(self, review: ReviewDecision) -> None:
        with self._get_connection() as conn:
            conn.execute("""
            INSERT INTO reviews (review_id, flag_id, reviewer, outcome, comment, reviewed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (review.review_id, review.flag_id, review.reviewer, review.outcome.value,
                  review.comment, review.reviewed_at.isoformat()))
            conn.execute("UPDATE flags SET status = ? WHERE flag_id = ?", (review.outcome.value, review.flag_id))
