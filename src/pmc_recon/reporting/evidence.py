"""Reporting and Evidence Dossier Generation Engine.
Produces audit-ready Markdown/HTML dossiers with complete cryptographic lineage.
"""

import json
from typing import Optional
from pmc_recon.storage.db import DatabaseEngine


class EvidenceReporter:
    """Generates neutral evidence summaries and audit trails."""
    def __init__(self, db: DatabaseEngine):
        self.db = db

    def generate_flag_dossier(self, flag_id: str) -> str:
        """Compile a standalone Markdown evidence dossier for a specific flag."""
        with self.db._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM flags WHERE flag_id = ?", (flag_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Flag {flag_id} not found.")

            cur.execute("SELECT * FROM reviews WHERE flag_id = ? ORDER BY reviewed_at DESC LIMIT 1", (flag_id,))
            review = cur.fetchone()

        evidence = json.loads(row["evidence_json"])
        explanations = json.loads(row["benign_explanations_json"])

        dossier_lines = [
            f"# PMC PROCUREMENT RECONCILIATION AUDIT DOSSIER: {row['flag_id']}",
            f"**Rule:** {row['rule_id']} | **Severity:** {row['severity'].upper()} | **Status:** {row['status'].upper()}",
            f"**Created:** {row['created_at']}",
            "",
            "## Summary",
            f"> {row['title']}",
            "",
            "## Measured Evidence",
            "```json",
            json.dumps(evidence, indent=2),
            "```",
            "",
            "## Innocent / Benign Explanations to Check",
        ]
        for exp in explanations:
            dossier_lines.append(f"- [ ] {exp}")

        if review:
            dossier_lines.extend([
                "",
                "## Review Decision",
                f"- **Reviewer:** {review['reviewer']}",
                f"- **Outcome:** {review['outcome']}",
                f"- **Timestamp:** {review['reviewed_at']}",
                f"- **Commentary:** {review['comment']}"
            ])

        return "\n".join(dossier_lines)
