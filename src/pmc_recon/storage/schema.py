"""Database DDL schemas for PMC Procurement Reconciliation storage.
Defines immutable tables for raw documents, tender versions, and review audit trails.
"""

SQLITE_SCHEMA_DDL = """
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
"""
