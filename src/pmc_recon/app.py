"""Interactive Demonstration Dashboard for PMC Procurement Reconciliation.
Provides human-in-the-loop inspection of sources, runs, linked records, and raised flags.
"""

import streamlit as st
import pandas as pd
from pmc_recon.storage.db import DatabaseEngine
from pmc_recon.models.entities import FlagStatus, ReviewDecision

st.set_page_config(page_title="PMC Procurement Reconciliation", page_icon="🏛️", layout="wide")

st.title("🏛️ Pune Municipal Corporation (PMC) Procurement Reconciliation")
st.markdown("*Accounts & Water Supply Expenditure Verification System*")

db = DatabaseEngine()

# Metrics overview
col1, col2, col3, col4 = st.columns(4)
with db._get_connection() as conn:
    tenders_count = conn.execute("SELECT COUNT(*) FROM tenders").fetchone()[0]
    budget_count = conn.execute("SELECT COUNT(*) FROM budget_lines").fetchone()[0]
    links_count = conn.execute("SELECT COUNT(*) FROM entity_links").fetchone()[0]
    flags_count = conn.execute("SELECT COUNT(*) FROM flags WHERE status = 'open'").fetchone()[0]

col1.metric("Ingested Tenders", tenders_count)
col2.metric("Budget Lines", budget_count)
col3.metric("Cross-Source Links", links_count)
col4.metric("Open Anomaly Flags", flags_count)

tabs = st.tabs(["🚨 Anomaly Flag Queue", "🔗 Entity Link Explorer", "📋 Tenders & Diffs", "📊 Budget Allocations"])

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
        tenders_df = pd.read_sql("SELECT tender_id, reference_number, title, value_inr, status, source_name FROM tenders", conn)
    st.dataframe(tenders_df, use_container_width=True)

with tabs[3]:
    st.subheader("Accounts Budget Reference Lines (FY 2025-26 & 2026-27)")
    with db._get_connection() as conn:
        budget_df = pd.read_sql("SELECT budget_head_code, description_marathi, amount_inr_crore, fiscal_year, amount_type FROM budget_lines", conn)
    st.dataframe(budget_df, use_container_width=True)
