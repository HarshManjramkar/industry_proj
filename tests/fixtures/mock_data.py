"""Test fixtures for Track A (Budget XLS) and Track B (Tender HTML/JSON).
Provides realistic mock data representing PMC Accounts and Water Supply.
"""

from typing import List, Dict, Any

# Mock raw payload for PMC budget lines (representing row RI11A101 and peers)
MOCK_BUDGET_ROWS: List[Dict[str, Any]] = [
    {
        "budget_head_code": "RI11A101",
        "description_marathi": "पाणी पुरवठा वितरण व्यवस्था सक्षमीकरण (वाघोली, लोहगाव)",
        "department": "Water Supply",
        "fiscal_year": "2025-26",
        "actual_amount_crore": 42.50,
        "estimate_amount_crore": 50.00,
        "source_file": "PMC_Budget_2025_26_Accounts.xlsx"
    },
    {
        "budget_head_code": "RI11A102",
        "description_marathi": "नवीन समाविष्ट गावांसाठी जलशुद्धीकरण प्रकल्प व मुख्य जलवाहिनी",
        "department": "Water Supply",
        "fiscal_year": "2025-26",
        "actual_amount_crore": 125.75,
        "estimate_amount_crore": 140.00,
        "source_file": "PMC_Budget_2025_26_Accounts.xlsx"
    },
    {
        "budget_head_code": "EL05B201",
        "description_marathi": "विद्युत विभाग पथदिवे देखभाल दुरुस्ती",
        "department": "Electrical",
        "fiscal_year": "2025-26",
        "actual_amount_crore": 80.90,
        "estimate_amount_crore": 90.00,
        "source_file": "PMC_Budget_2025_26_Accounts.xlsx"
    }
]

# Mock tender HTML from official portal (mahatenders.gov.in)
MOCK_MAHATENDERS_HTML = """
<!DOCTYPE html>
<html>
<head><title>Pune Municipal Corporation - Active Tenders</title></head>
<body>
<table id="activeTendersTable" class="table">
  <thead>
    <tr>
      <th>Tender ID</th>
      <th>Ref No</th>
      <th>Work Title</th>
      <th>Department</th>
      <th>Closing Date</th>
      <th>Estimated Value</th>
      <th>Corrigendum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PMCP/WTR/2026/042</td>
      <td>PMC-WS-2026-T42</td>
      <td>Laying of trunk water pipeline in Lohegaon Wagholi zone</td>
      <td>Pune Municipal Corporation/Water Supply</td>
      <td>2026-11-15</td>
      <td>₹ 18,50,00,000</td>
      <td>0</td>
    </tr>
    <tr>
      <td>PMCP/WTR/2026/043</td>
      <td>PMC-WS-2026-T43</td>
      <td>DMA meter installation and distribution strengthening Baner</td>
      <td>Pune Municipal Corporation/Water Supply</td>
      <td>2026-11-20</td>
      <td>₹ 4,25,00,000</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</body>
</html>
"""

# Mock mirror payload (publicservicesmap.in / tenders.infralens.in)
# Notice: Mirror has a discrepancy on PMCP/WTR/2026/042 (Value shows 19.20 Cr instead of 18.50 Cr) -> R1 trigger!
MOCK_MIRROR_PAYLOAD = {
    "portal": "publicservicesmap.in",
    "fetched_at": "2026-10-25T12:00:00Z",
    "tenders": [
        {
            "id": "PMCP/WTR/2026/042",
            "reference": "PMC-WS-2026-T42",
            "title": "Laying of trunk water pipeline in Lohegaon Wagholi zone",
            "dept": "Water Supply Department",
            "closing_date": "2026-11-15",
            "tender_value_inr": 192000000.0, # 19.20 Cr (Mismatch from official 18.50 Cr)
            "status": "active"
        },
        {
            "id": "PMCP/WTR/2026/043",
            "reference": "PMC-WS-2026-T43",
            "title": "DMA meter installation and distribution strengthening Baner",
            "dept": "Water Supply Department",
            "closing_date": "2026-11-20",
            "tender_value_inr": 42500000.0,
            "status": "active"
        }
    ]
}
