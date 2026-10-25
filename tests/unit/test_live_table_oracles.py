"""ATDD Test Oracles for Epic 6: Live In-Flight Table Discrepancy & Invariant Engine.
Verifies real-time deterministic mathematical and integrity scans on public data tables
without requiring an LLM or bot, with zero defamatory language.
"""

import pytest
from pmc_recon.models.entities import FlagSeverity
from pmc_recon.ingest.table_validator import (
    LiveTableValidator,
    TableDiscrepancyType,
    TableValidationReport,
)


def test_oracle_table_totality_invariant_detection():
    """Scenario: Live table totality validation detects arithmetic discrepancy in subtotals.
    Given budget or tender items summing to 266.12 Cr but table total stating 265.72 Cr
    When LiveTableValidator.validate_totality is executed
    Then an arithmetic variance discrepancy is flagged with the exact 0.40 Cr variance.
    """
    validator = LiveTableValidator()
    
    rows = [
        {"item": "Street lighting capital works", "amount_crore": 80.90},
        {"item": "Street lighting revenue maintenance", "amount_crore": 185.22},
    ]
    stated_total = 265.72  # Stated total is less by 0.40 Cr
    
    discrepancies = validator.validate_totality(
        rows=rows,
        value_key="amount_crore",
        stated_total=stated_total,
        context_label="Electrical Dept Budget Table"
    )
    
    assert len(discrepancies) == 1
    d = discrepancies[0]
    assert d.discrepancy_type == TableDiscrepancyType.TOTALITY_MISMATCH
    assert d.rule_id == "R3-Table"
    assert "arithmetic" in d.title.lower()
    assert abs(d.delta - 0.40) < 0.001
    assert d.severity == FlagSeverity.MEDIUM
    assert "Typographical entry slip" in d.benign_explanation or "rounding" in d.benign_explanation.lower()


def test_oracle_table_totality_invariant_clean():
    """Scenario: Totality check passes cleanly when sum equals stated total."""
    validator = LiveTableValidator()
    rows = [
        {"item": "Baner DMA works", "amount_crore": 10.50},
        {"item": "Balewadi DMA works", "amount_crore": 15.50},
    ]
    stated_total = 26.00
    discrepancies = validator.validate_totality(rows, "amount_crore", stated_total, "Clean DMA Works")
    assert len(discrepancies) == 0


def test_oracle_table_chronology_invariant_detection():
    """Scenario: Chronological validation detects inverted publishing vs closing vs opening dates.
    Given tender row with closing date before publication date or opening date before closing
    When LiveTableValidator.validate_chronology is executed
    Then a chronology inversion discrepancy is flagged.
    """
    validator = LiveTableValidator()
    
    rows = [
        {
            "tender_id": "PMCP/WTR/2026/042",
            "published_date": "2026-11-01",
            "closing_date": "2026-11-15",
            "opening_date": "2026-11-16",
        },
        {
            "tender_id": "PMCP/WTR/2026/043",
            "published_date": "2026-11-20",
            "closing_date": "2026-11-10",  # Inverted: closing before publishing
            "opening_date": "2026-11-22",
        },
        {
            "tender_id": "PMCP/WTR/2026/044",
            "published_date": "2026-11-01",
            "closing_date": "2026-11-25",
            "opening_date": "2026-11-20",  # Inverted: opening before closing
        }
    ]
    
    discrepancies = validator.validate_chronology(
        rows=rows,
        id_key="tender_id",
        published_key="published_date",
        closing_key="closing_date",
        opening_key="opening_date"
    )
    
    assert len(discrepancies) == 2
    types = [d.discrepancy_type for d in discrepancies]
    assert TableDiscrepancyType.CHRONOLOGY_INVERSION in types
    for d in discrepancies:
        assert "chronological" in d.title.lower()
        assert "corrigendum" in d.benign_explanation.lower() or "administrative" in d.benign_explanation.lower()


def test_oracle_table_hampel_outlier_detection():
    """Scenario: Real-time Hampel/MAD statistical filter identifies extreme physical or financial outliers.
    Given peer water pipeline lengths [24.0, 32.5, 45.0, 16.5, 77.0, 450.0]
    When LiveTableValidator.validate_outliers is executed
    Then the 450.0 km row is flagged with modified Z-score > 3.5.
    """
    validator = LiveTableValidator()
    
    rows = [
        {"sector": "Baner", "length_km": 24.0},
        {"sector": "Kothrud", "length_km": 32.5},
        {"sector": "Hadapsar", "length_km": 45.0},
        {"sector": "Katraj", "length_km": 16.5},
        {"sector": "Sinhagad", "length_km": 77.0},
        {"sector": "Lohegaon", "length_km": 450.0},
    ]
    
    discrepancies = validator.validate_outliers(
        rows=rows,
        id_key="sector",
        metric_key="length_km",
        threshold_z=3.5
    )
    
    assert len(discrepancies) == 1
    d = discrepancies[0]
    assert d.discrepancy_type == TableDiscrepancyType.STATISTICAL_OUTLIER
    assert d.rule_id == "R6-Table"
    assert d.row_identifier == "Lohegaon"
    assert d.measured_values["observed_value"] == 450.0
    assert d.measured_values["modified_z_score"] > 3.5
    assert d.severity == FlagSeverity.HIGH


def test_oracle_table_duplicate_notice_conflict_detection():
    """Scenario: Detects duplicate tender IDs within the same table with conflicting valuations.
    Given two entries for PMCP/WTR/2026/042 with 18.50 Cr and 19.20 Cr
    When LiveTableValidator.validate_duplicate_conflicts is executed
    Then a conflicting duplicate notice discrepancy is flagged.
    """
    validator = LiveTableValidator()
    
    rows = [
        {"tender_id": "PMCP/WTR/2026/042", "title": "Lohegaon trunk", "value_cr": 18.50},
        {"tender_id": "PMCP/WTR/2026/043", "title": "Baner DMA", "value_cr": 4.25},
        {"tender_id": "PMCP/WTR/2026/042", "title": "Lohegaon trunk revised", "value_cr": 19.20},
    ]
    
    discrepancies = validator.validate_duplicate_conflicts(
        rows=rows,
        id_key="tender_id",
        compare_keys=["value_cr"]
    )
    
    assert len(discrepancies) == 1
    d = discrepancies[0]
    assert d.discrepancy_type == TableDiscrepancyType.DUPLICATE_NOTICE_CONFLICT
    assert d.row_identifier == "PMCP/WTR/2026/042"
    assert "divergence" in d.title.lower() or "conflict" in d.title.lower()


def test_oracle_full_html_table_in_flight_scan():
    """Scenario: Full in-flight live HTML table scan executes within milliseconds with zero LLM.
    Given raw HTML table containing tenders and subtotal summary
    When validator.scan_html_table is executed
    Then a typed TableValidationReport is produced containing deterministic findings and zero defamatory words.
    """
    validator = LiveTableValidator()
    
    html = """
    <table id="testTenders">
      <thead>
        <tr>
          <th>Tender ID</th>
          <th>Work Description</th>
          <th>Closing Date</th>
          <th>Estimated Value (INR)</th>
          <th>Pipe Length (km)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>PMCP/WTR/2026/042</td>
          <td>Lohegaon Trunk Pipeline</td>
          <td>2026-11-15</td>
          <td>18,50,00,000</td>
          <td>450.0</td>
        </tr>
        <tr>
          <td>PMCP/WTR/2026/043</td>
          <td>Baner DMA Network</td>
          <td>2026-11-20</td>
          <td>4,25,00,000</td>
          <td>24.0</td>
        </tr>
        <tr>
          <td>PMCP/WTR/2026/044</td>
          <td>Katraj Booster Station</td>
          <td>2026-11-18</td>
          <td>3,80,00,000</td>
          <td>18.5</td>
        </tr>
      </tbody>
    </table>
    """
    
    report: TableValidationReport = validator.scan_html_table(html)
    assert report.total_rows_inspected == 3
    assert len(report.columns_inspected) >= 4
    assert report.execution_time_ms < 50.0  # Instant deterministic evaluation
    assert len(report.tamper_hash) == 64
    
    # Assert neutral language across all reports
    for item in report.discrepancies:
        text = f"{item.title} {item.benign_explanation}".lower()
        for forbidden in ["fraud", "corruption", "scam", "illegal", "criminal", "guilty"]:
            assert forbidden not in text
