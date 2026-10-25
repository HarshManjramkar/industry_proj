---
status: final
version: 1.0.0
last_updated: "2026-10-25"
foundation:
  framework: "Streamlit 1.40+ (Python 3.12)"
  design_system_ref: "docs/ux/DESIGN.md"
  target_user: "Civic Watchdogs, Citizens, Evaluators, Journalists (Layman Focus)"
---

# EXPERIENCE.md — Behavioral & Interaction Architecture

## 1. Foundation & Mental Model
The layman mental model follows a **4-Beat Narrative Arc**:
1. **The Context:** What public money are we looking at? (Pune's ₹2,077 Cr Water Supply Budget across 141 zones).
2. **The Acquisition:** Where did the data come from? (Official Marathi budget PDFs, State e-Tenders, and Mirror Watchdogs).
3. **The Investigation:** What didn't add up? (₹40 Lakh math slip, ₹70 Lakh mirror variance, 450 km pipe typo).
4. **The Live Proof:** Can I verify it myself right now? (1-click polite crawl + instant cryptographic audit).

---

## 2. Information Architecture (Layman-First 5-Tab Layout)

```
[ Hero Banner & Live System Health Pulse ]
[ Top KPI Row: ₹2,077 Cr Budget | 141 Zones | 2 Active Contracts | 3 Verified Slips ]
  │
  ├── 🔍 Tab 1: "What Are We Crawling?" (Source Transparency & Scope Defense)
  │    ├── 3 Source Origin Cards (Budget PDF, e-Tenders, Watchdog Mirror)
  │    └── "Why Water Supply and NOT Election?" Accordion Drawer
  │
  ├── 🚨 Tab 2: "The 3 Verified Discrepancies" (Forensic Stories)
  │    ├── Story 1: The ₹40 Lakh Budget Addition Slip (Rule R3)
  │    ├── Story 2: The ₹70 Lakh Tender Value Gap (Rule R1)
  │    └── Story 3: The 450 km Impossible Pipeline (Rule R6)
  │
  ├── 📊 Tab 3: "Visual Graphs & Comparisons" (Visual Evidence)
  │    ├── Chart A: Budget Split (Capital ₹802 Cr vs Revenue ₹1,274 Cr)
  │    ├── Chart B: The 450 km Outlier Bar Chart (Red Spike)
  │    ├── Chart C: Tender Valuation Gap Bar Chart (₹18.5 Cr vs ₹19.2 Cr)
  │    └── Chart D: Addition Math Check Bar Chart (₹265.72 Cr vs ₹266.12 Cr)
  │
  ├── 🔗 Tab 4: "Marathi ↔ English Project Linker" (Language Decoder)
  │    ├── Marathi Budget Head RI11A101 Decoder Card
  │    └── Interactive Tender-to-Budget Match Table
  │
  └── 🌐 Tab 5: "Live Public Portal Ingestion" (Zero-Terminal Interactive Audit)
       ├── 1-Click "Fetch Public Portal Data" Action
       ├── Live Extracted Records Table
       └── Forensic Integrity Re-Verification Button
```

---

## 3. Voice and Tone (Microcopy Guidelines)
- **Objective, Not Sensational:** Use *"Mathematical addition slip"*, *"Cross-portal synchronization variance"*, *"Typographical entry outlier"*.
- **Empowering, Not Puzzling:** Instead of *"SHA-256 Preimage Hash verified"*, say *"Tamper-Proof Digital Fingerprint Confirmed (100% Unaltered)"*.
- **Local Pune Context:** Ground every metric in Pune geography (*"Wagholi-Lohegaon water distribution"*, *"Baner DMA meter installation"*).

---

## 4. Key User Journeys

### Journey 1: The Faculty Evaluator (Speed & Proof)
1. **Entry:** Lands on dashboard; immediately reads the ₹2,077 Cr monitored budget and 141 zones.
2. **Context:** Clicks Tab 1; sees that PMC has no municipal election budget line and why Water Supply was chosen.
3. **Evidence:** Clicks Tab 3; instantly smiles at the visual 450 km pipeline outlier spike chart.
4. **Climax Beat:** Clicks Tab 5; runs the live crawler and cryptographic verification in 3 seconds with zero terminal access.

### Journey 2: The Civic Journalist (Story & Accountability)
1. **Entry:** Wants to know where public funds in Wagholi/Lohegaon are going.
2. **Language Bridge:** Opens Tab 4; sees how Marathi budget code `RI11A101` translates to English tender `PMCP/WTR/2026/042`.
3. **Variance Check:** Opens Tab 2; downloads evidence of the ₹70 Lakh mirror discrepancy and ₹40 Lakh presentation math slip.

---

## 5. Accessibility Floor & Responsive Behavior
- **WCAG 2.1 AA Contrast:** All text passes 4.5:1 contrast against `#FFFFFF` or `#F8FAFC`.
- **Zero Scroll Traps:** All dataframes use `width="stretch"` with fixed pagination.
- **Instant Fallback (Airplane / Bad Wi-Fi Mode):** The live crawler includes a `Verified Offline Replay` option that guarantees a seamless demonstration even if venue Wi-Fi blocks `.gov.in` servers.
