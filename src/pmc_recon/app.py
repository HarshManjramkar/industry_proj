"""Interactive Demonstration Dashboard for PMC Procurement Reconciliation.
Provides human-in-the-loop inspection of sources, runs, linked records, raised flags,
and live public government portal crawling with cryptographic proof verification.
"""

from unittest.mock import MagicMock
import pandas as pd
import streamlit as st

from pmc_recon.ingest.crawler_service import CrawlerDemoService
from pmc_recon.storage.db import DatabaseEngine
from tests.fixtures.mock_data import MOCK_MAHATENDERS_HTML

st.set_page_config(page_title="PMC Procurement Reconciliation", page_icon="🏛️", layout="wide")

st.title("🏛️ Pune Municipal Corporation (PMC) Procurement Reconciliation")
st.markdown("*Accounts & Water Supply Expenditure Verification System*")

db = DatabaseEngine()
crawler_service = CrawlerDemoService(db=db)

# Metrics overview
col1, col2, col3, col4, col5 = st.columns(5)
with db._get_connection() as conn:
    tenders_count = conn.execute("SELECT COUNT(*) FROM tenders").fetchone()[0]
    budget_count = conn.execute("SELECT COUNT(*) FROM budget_lines").fetchone()[0]
    links_count = conn.execute("SELECT COUNT(*) FROM entity_links").fetchone()[0]
    flags_count = conn.execute("SELECT COUNT(*) FROM flags WHERE status = 'open'").fetchone()[0]
    raw_docs_count = conn.execute("SELECT COUNT(*) FROM raw_documents").fetchone()[0]

col1.metric("Ingested Tenders", tenders_count)
col2.metric("Budget Lines", budget_count)
col3.metric("Cross-Source Links", links_count)
col4.metric("Open Anomaly Flags", flags_count)
col5.metric("Raw Payloads (SHA-256)", raw_docs_count)

tabs = st.tabs([
    "🚨 Anomaly Flag Queue",
    "🔗 Entity Link Explorer",
    "📋 Tenders & Diffs",
    "📊 Budget Allocations",
    "🌐 Live Govt Crawler Demo"
])

with tabs[0]:
    st.subheader("Discrepancy Flags Requiring Human Review")
    with db._get_connection() as conn:
        flags_df = pd.read_sql("SELECT flag_id, rule_id, title, severity, status, created_at FROM flags", conn)
    if not flags_df.empty:
        st.dataframe(flags_df, use_container_width=True)
    else:
        st.info("No active flags raised. Invariants satisfied.")

with tabs[1]:
    st.subheader("Cross-Dataset Links (Tender ↔ Budget Line)")
    with db._get_connection() as conn:
        links_df = pd.read_sql("SELECT * FROM entity_links", conn)
    st.dataframe(links_df, use_container_width=True)

with tabs[2]:
    st.subheader("Active & Historical Tenders (Official + Mirror)")
    with db._get_connection() as conn:
        tenders_df = pd.read_sql(
            "SELECT tender_id, reference_number, title, value_inr, status, source_name FROM tenders",
            conn
        )
    st.dataframe(tenders_df, use_container_width=True)

with tabs[3]:
    st.subheader("Accounts Budget Reference Lines (FY 2025-26 & 2026-27)")
    with db._get_connection() as conn:
        budget_df = pd.read_sql(
            "SELECT budget_head_code, description_marathi, amount_inr_crore, fiscal_year, amount_type FROM budget_lines",
            conn
        )
    st.dataframe(budget_df, use_container_width=True)

with tabs[4]:
    st.subheader("🌐 Public Government Portal Polite Crawler & Lineage Verification")
    st.info(
        "Demonstrates live HTTP acquisition from public portals under strict **NFR-01 Politeness** "
        "(User-Agent declaration, 2.0s rate limiter, ETag conditional headers) and **Theorem 1 Cryptographic Preimage Lineage**."
    )

    portal_choice = st.selectbox(
        "Select Target Public Portal for Live Demonstration:",
        [
            "mahatenders.gov.in (National Informatics Centre e-Procurement Portal)",
            "pmc.gov.in (Pune Municipal Corporation Official Portal)",
            "Verified Offline Replay (Zero Network Delay Fallback)"
        ]
    )

    if st.button("🚀 Trigger Polite Crawl (Zero Terminal Required)", type="primary"):
        with st.spinner("Executing polite fetch with NFR-01 compliance..."):
            if "mahatenders" in portal_choice:
                target_url = "https://mahatenders.gov.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page"
                crawl_result = crawler_service.run_live_crawl(url=target_url)
            elif "pmc.gov" in portal_choice:
                target_url = "https://pmc.gov.in"
                crawl_result = crawler_service.run_live_crawl(url=target_url)
            else:
                # Offline replay session
                target_url = "https://mahatenders.gov.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page"
                mock_sess = MagicMock()
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.content = MOCK_MAHATENDERS_HTML.encode("utf-8")
                mock_resp.text = MOCK_MAHATENDERS_HTML
                mock_resp.headers = {"ETag": '"sha256-verified-etag-2026"'}
                mock_sess.get.return_value = mock_resp
                crawl_result = crawler_service.run_live_crawl(
                    url=target_url,
                    run_id="replay_demo_run",
                    session=mock_sess
                )

        if crawl_result.error_message:
            st.warning(f"Fetch Notice: {crawl_result.error_message}")
            st.caption("Tip: Select 'Verified Offline Replay' if venue/hotspot Wi-Fi filters Indian gov domains.")
        else:
            st.success("✅ Fetch Succeeded! Payload cryptographically sealed in content-addressed storage.")
            c1, c2, c3 = st.columns(3)
            c1.metric("HTTP Response Status", f"{crawl_result.status_code} OK")
            c2.metric("Size on Disk", f"{crawl_result.size_bytes:,} bytes")
            c3.metric("Document Reference", crawl_result.doc_id)

            st.markdown("#### 🔒 Lineage & Safeguards Verification")
            st.code(
                f"• Target URL: {crawl_result.url}\n"
                f"• Invariant Theorem 1 SHA-256 Hash: {crawl_result.content_hash}\n"
                f"• Disk Storage Path: data/raw_store/{crawl_result.storage_path}\n"
                f"• Header User-Agent: {crawl_result.user_agent}\n"
                f"• Conditional ETag: {crawl_result.etag or 'N/A'}",
                language="yaml"
            )

            with st.expander("👁️ View Captured Raw HTML Preimage (Verbatim Payload Preview)"):
                st.code(crawl_result.payload_preview, language="html")

    st.markdown("---")
    st.subheader("🔬 Tamper-Proof Cryptographic Lineage Auditor (Theorem 1)")
    with db._get_connection() as conn:
        raw_docs_df = pd.read_sql(
            "SELECT doc_id, run_id, content_hash, size_bytes, storage_path, fetched_at FROM raw_documents ORDER BY fetched_at DESC",
            conn
        )

    if not raw_docs_df.empty:
        st.dataframe(raw_docs_df, use_container_width=True)

        selected_doc = st.selectbox("Select Stored Document to Re-Verify Against Disk:", raw_docs_df["doc_id"].tolist())
        if st.button("🔍 Cryptographically Re-Verify Selected Document"):
            audit = crawler_service.verify_disk_lineage(selected_doc)
            if audit.get("verified"):
                st.success(
                    f"✅ **Theorem 1 Mathematical Proof Confirmed!**\n\n"
                    f"File bytes read from disk at `{audit['file_path']}` ({audit['size_bytes']} bytes) "
                    f"produce the exact SHA-256 hash stored in the database:\n\n"
                    f"`{audit['computed_hash']}`"
                )
            else:
                st.error(f"❌ Verification Failure: {audit.get('error')}")
    else:
        st.info("No raw documents in database yet.")
