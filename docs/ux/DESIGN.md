---
status: final
version: 1.0.0
last_updated: "2026-10-25"
tokens:
  colors:
    primary: "#0F172A"       # Deep Civic Slate
    brand_blue: "#2563EB"    # Public Trust Blue
    surface_bg: "#F8FAFC"    # Soft Editorial Off-White
    card_bg: "#FFFFFF"       # Crisp White Card Surface
    card_border: "#E2E8F0"   # Subtle Slate Border
    text_main: "#0F172A"     # High Legibility Text
    text_muted: "#475569"    # Subtitle Slate Gray
    accent_green: "#059669"  # Verified / Legitimate
    accent_amber: "#D97706"  # Addition Slip / Typo Warning
    accent_rose: "#DC2626"   # Outlier Anomaly Spike
  typography:
    font_headings: "Inter, system-ui, -apple-system, sans-serif"
    font_body: "Inter, system-ui, -apple-system, sans-serif"
    font_numbers: "system-ui, -apple-system, monospace"
    size_hero: "2.25rem"
    size_h1: "1.75rem"
    size_h2: "1.35rem"
    size_body: "1rem"
    size_caption: "0.875rem"
  rounded:
    sm: "4px"
    md: "8px"
    lg: "12px"
    pill: "9999px"
  spacing:
    container_padding: "1.5rem"
    card_padding: "1.25rem"
    element_gap: "0.75rem"
---

# DESIGN.md — Visual Identity for Pune Civic Reconciliation

## 1. Brand & Style Philosophy
Public procurement data is historically opaque, bureaucratic, and technically alienating. The design philosophy of this portal is **Radical Civic Transparency for Everyday Citizens**.

It trades dry database consoles for an authoritative, clean, and reassuring visual language inspired by modern investigative publications (ProPublica, The Pudding, Financial Times Visual Journalism).

### Visual Pillars:
1. **Calm Authority over Panic:** Discrepancies are highlighted in informative amber and warm indigo—never screaming red banners that induce fear or imply malicious wrongdoing.
2. **Generous Visual Breathing Room:** High information density achieved through hierarchical cards and interactive charts, not walls of cramped text.
3. **Tabular Numerals & Clear Rupee Units:** Standardized Indian currency denominations (Crores and Lakhs) with explicit comma grouping.

---

## 2. Color Palette & Semantic Roles

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| `primary` | `#0F172A` | Hero titles, primary headers, dark accents |
| `brand_blue` | `#2563EB` | Active tabs, primary buttons, clickable filters |
| `surface_bg` | `#F8FAFC` | Dashboard background canvas |
| `card_bg` | `#FFFFFF` | Information cards and container backgrounds |
| `card_border` | `#E2E8F0` | Subtle, clean separation borders |
| `text_main` | `#0F172A` | Body prose, table values, metric digits |
| `text_muted` | `#475569` | Explanatory captions, dates, helper footnotes |
| `accent_green` | `#059669` | Verified audit matches, legitimate calculations |
| `accent_amber` | `#D97706` | Mathematical variances, arithmetic addition slips |
| `accent_rose` | `#DC2626` | Statistical outliers, typographical errors (450 km) |

---

## 3. Typography & Micro-Hierarchy

- **Hero Title (`2.25rem` / `800 Weight`):** Anchors the page as an official, independent municipal audit portal.
- **Section Headers (`1.35rem` / `700 Weight`):** Numbered questions guiding the user sequentially (e.g., *"1. What Public Data Did We Crawl?"*).
- **Metric Cards (`1.75rem` / `700 Weight`):** Crisp numbers paired with single-sentence context tooltips.
- **Explanatory Prose (`1rem` / `400 Weight`):** High contrast, 1.5 line height for effortless reading.

---

## 4. Components & Surface Styling

### A. The Civic Story Card
Containers styled with `background: #FFFFFF`, `border: 1px solid #E2E8F0`, `box-shadow: 0 1px 3px rgba(0,0,0,0.05)`, and a `4px` colored left accent border indicating data tier.

### B. The Discrepancy Breakdown Pill
Badges with subtle pastel backgrounds and bold text (e.g. `₹ 40 Lakh Slip`, `Hampel Z-Score 3.85`, `Bilingual Match 100%`).

### C. Visual Comparative Graphs
Clean bar charts contrasting:
- Capital vs Revenue Budget Allocations.
- Peer Pipeline Lengths vs Lohegaon 450 km Outlier.
- Official Portal vs Mirror Portal Valuations.

---

## 5. Do's and Don'ts

### Do's:
- Always translate technical terms into civic impact (e.g., explain that *450 km pipeline* would stretch across the state of Maharashtra).
- Frame every anomaly alongside its pre-approved benign explanation checklist.
- Keep the user in the browser at all times—zero terminal interaction.

### Don'ts:
- Never expose raw database IDs (`doc_b4f9...`), unparsed JSON blobs, or YAML server dumps to laymen.
- Never use accusatory words like "fraud", "scam", or "corruption".
- Never display uncapped fractional numbers (always round to ₹ Crores / Lakhs).
