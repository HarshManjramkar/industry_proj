"""UI Design Components, Zero-Scroll Viewport Tokens, and Regal Heraldry for PMC Recon.
Strictly under 350 lines, adhering to SRP, high-contrast dark/light adaptability,
and zero page-level scrolling layout constraints.
"""


def get_theme_css() -> str:
    """Return CSS that locks page-level scrolling and establishes regal civic aesthetics."""
    return """
<style>
    /* Viewport-Locking & Root Zero-Scroll Rules */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
        background-color: #080D1A !important;
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.2rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* High-Density Regal Civic Top HUD */
    .regal-top-hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, #0A1128 0%, #101B3B 50%, #0D162E 100%);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 8px;
        padding: 0.45rem 1rem;
        margin-bottom: 0.4rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    .hud-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .hud-title {
        color: #FFFFFF !important;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin: 0;
        line-height: 1.2;
    }
    .hud-subtitle {
        color: #F3C648 !important;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .hud-ticker {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(11, 19, 43, 0.7);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 6px;
        padding: 0.25rem 0.75rem;
    }
    .ticker-item {
        font-size: 0.78rem;
        color: #CBD5E1;
    }
    .ticker-item b {
        color: #F8FAFC;
    }
    .ticker-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 6px #10B981;
    }

    /* HIGH-CONTRAST TAB BAR & LABELS */
    div[role="radiogroup"] {
        background: #0E172E !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 8px !important;
        padding: 0.35rem 0.75rem !important;
        margin-bottom: 0.4rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }
    div[role="radiogroup"] label,
    div[role="radiogroup"] label p,
    div[role="radiogroup"] label span,
    div[role="radiogroup"] label div,
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label * {
        color: #F8FAFC !important;
        font-size: 0.90rem !important;
        font-weight: 600 !important;
    }
    div[role="radiogroup"] label:has(input:checked) *,
    div[role="radiogroup"] label[data-checked="true"] * {
        color: #F3C648 !important;
        font-weight: 800 !important;
    }

    /* All Form and Widget Labels (Selectboxes, text areas, inputs) */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    label[data-testid="stWidgetLabel"] {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Inputs, Selectboxes, and Textarea background + text contrast */
    textarea,
    input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background-color: #0E172E !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 6px !important;
        font-family: monospace !important;
        font-size: 0.85rem !important;
    }

    /* Toggle label contrast */
    div[data-testid="stToggle"] label,
    div[data-testid="stToggle"] label * {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        font-size: 0.90rem !important;
    }

    /* Headings & Captions */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #94A3B8 !important;
        font-size: 0.84rem !important;
    }

    /* INDEPENDENT SCROLLABLE CARD CONTAINERS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0E172E !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        scrollbar-width: thin !important;
        scrollbar-color: #D4AF37 #0B132B !important;
        padding: 0.65rem 0.85rem !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div::-webkit-scrollbar {
        width: 8px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div::-webkit-scrollbar-thumb {
        background-color: #D4AF37 !important;
        border-radius: 4px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div::-webkit-scrollbar-track {
        background-color: #0B132B !important;
    }

    /* Anomaly Cards */
    .anomaly-card {
        background: #0A1128 !important;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.75rem;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .anomaly-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 1.0rem;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    .anomaly-card p {
        color: #E2E8F0 !important;
        font-size: 0.86rem;
        line-height: 1.45;
        margin: 0.2rem 0;
    }
    .card-r1 { border-left: 4px solid #38BDF8 !important; }
    .card-r3 { border-left: 4px solid #F59E0B !important; }
    .card-r6 { border-left: 4px solid #F87171 !important; }

    /* Radar Results Header Box */
    .radar-summary-box {
        background: linear-gradient(135deg, #0B142B 0%, #131F3F 100%);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 8px;
        padding: 0.75rem 0.85rem;
        margin-bottom: 0.75rem;
    }
    .radar-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .radar-pass { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #10B981; }
    .radar-alert { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #F59E0B; }
    .radar-outlier { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; }
</style>
"""


def render_regal_banner() -> str:
    """Return HTML for the high-density top command HUD with royal Maratha heraldry."""
    return """
<div class="regal-top-hud">
    <div class="hud-brand">
        <span style="font-size: 1.6rem;">🏛️</span>
        <div>
            <div class="hud-title">पुणे महानगरपालिका • Pune Municipal Corporation</div>
            <div class="hud-subtitle">⚖️ Deterministic Civic Expenditure Reconciliation Command Center</div>
        </div>
    </div>
    <div class="hud-ticker">
        <div class="ticker-item"><span class="ticker-pulse"></span> <b>STATUS:</b> ACTIVE</div>
        <div class="ticker-item">| <b>WATER BUDGET:</b> ₹ 2,077.43 Cr</div>
        <div class="ticker-item">| <b>ZONES:</b> 141</div>
        <div class="ticker-item">| <b>LINEAGE:</b> SHA-256 PRE-IMAGE</div>
    </div>
</div>
"""


def render_intro_video_walkthrough() -> str:
    """Return a rich animated SVG/HTML5 civic briefing visual walkthrough."""
    return """
<div style="background: radial-gradient(circle at 50% 50%, #152243 0%, #0A1128 100%);
            border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 8px; padding: 0.9rem;
            margin-bottom: 0.6rem; text-align: center;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div style="text-align: left;">
            <span style="background: rgba(212,175,55,0.2); color: #F3C648; font-size: 0.72rem;
                         font-weight: 800; padding: 2px 7px; border-radius: 4px; letter-spacing: 0.08em;">
                🎬 60-SECOND CIVIC BRIEFING THEATER
            </span>
            <div style="color: #FFFFFF; font-size: 1.05rem; font-weight: 700; margin-top: 0.2rem;">
                Cross-Checking Pune's ₹ 2,077.43 Cr Water Infrastructure Without Bot Guesses
            </div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <span style="background: rgba(56,189,248,0.15); border: 1px solid #38BDF8; color: #38BDF8;
                         padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                Track A: Marathi Budget
            </span>
            <span style="background: rgba(245,158,11,0.15); border: 1px solid #F59E0B; color: #F59E0B;
                         padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                Track B: English Tenders
            </span>
            <span style="background: rgba(16,185,129,0.15); border: 1px solid #10B981; color: #10B981;
                         padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                Deterministic Radar
            </span>
        </div>
    </div>
</div>
"""


def render_radar_header(execution_time_ms: float, rows_count: int, tamper_hash: str) -> str:
    """Render summary banner for in-flight table scan."""
    return f"""
<div class="radar-summary-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <span class="radar-badge radar-pass">⚡ IN-FLIGHT RADAR ACTIVE</span>
            <span style="color: #CBD5E1; font-size: 0.85rem; margin-left: 0.5rem;">
                Inspected <b>{rows_count} table rows</b> in <b>{execution_time_ms} ms</b>
            </span>
        </div>
        <div style="font-family: monospace; font-size: 0.75rem; color: #94A3B8;">
            SHA-256: {tamper_hash[:16]}...
        </div>
    </div>
</div>
"""
