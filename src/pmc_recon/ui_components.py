"""UI Design Components, Dark/Light Mode Themes, and Regal Visual Assets for PMC Recon.
Complies with SRP and keeps all source files strictly under 350 lines.
"""

def get_theme_css() -> str:
    """Return dark-mode and light-mode compatible CSS with regal civic styling."""
    return """
<style>
    /* Theme-Adaptive Variables */
    :root {
        --civic-navy: #0F172A;
        --civic-gold: #D97706;
        --civic-royal: #1E3A8A;
        --card-bg: rgba(255, 255, 255, 0.95);
        --card-border: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #475569;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --civic-navy: #F8FAFC;
            --civic-gold: #FBBF24;
            --civic-royal: #60A5FA;
            --card-bg: rgba(30, 41, 59, 0.85);
            --card-border: rgba(255, 255, 255, 0.12);
            --text-primary: #F8FAFC;
            --text-secondary: #CBD5E1;
        }
    }

    /* Streamlit Dark Mode Auto-Adaptation */
    [data-testid="stAppViewContainer"] {
        color: var(--text-primary);
    }

    /* Regal Header Banner */
    .regal-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E3A8A 100%);
        border: 1px solid rgba(217, 119, 6, 0.35);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .regal-banner h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .regal-tagline {
        color: #FCD34D !important;
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }

    /* Bento Grid Card View */
    .bento-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .bento-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }
    .bento-card h3 {
        color: var(--text-primary) !important;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .bento-card p {
        color: var(--text-secondary) !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Discrepancy Story Cards with Dark Mode Support */
    .anomaly-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
        border: 1px solid var(--card-border);
    }
    .anomaly-card h4 {
        margin-top: 0;
        font-size: 1.15rem;
        font-weight: 700;
    }
    .card-r1 { border-left: 5px solid #3B82F6; }
    .card-r3 { border-left: 5px solid #F59E0B; }
    .card-r6 { border-left: 5px solid #EF4444; }

    /* Animated Video Simulation Mockup */
    .video-hero {
        position: relative;
        background: radial-gradient(circle at 50% 50%, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(217, 119, 6, 0.4);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: #F8FAFC;
        margin-bottom: 2rem;
        overflow: hidden;
    }
    .video-pulse {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.8s infinite;
        margin-right: 6px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
</style>
"""

def render_regal_banner() -> str:
    """Return HTML for the regal municipal heraldry and system pulse."""
    return """
<div class="regal-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🏛️ पुणे महानगरपालिका • Pune Municipal Corporation</h1>
            <div class="regal-tagline">
                ⚖️ Public Procurement Reconciliation & Forensic Expenditure Audit System
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.1); border: 1px solid rgba(251,191,36,0.4); padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
            <span class="video-pulse"></span> SYSTEM STATUS: ACTIVE (141 ZONES MONITORED)
        </div>
    </div>
</div>
"""

def render_intro_video_walkthrough() -> str:
    """Return a rich animated civic visual briefing introducing the system."""
    return """
<div class="video-hero">
    <div style="font-size: 0.85rem; letter-spacing: 0.15em; color: #FCD34D; font-weight: 700; text-transform: uppercase;">
        🎬 60-Second Civic Briefing Walkthrough
    </div>
    <h2 style="color: #FFFFFF !important; font-size: 1.8rem; margin: 0.5rem 0 1rem 0; font-weight: 800;">
        How Pune's ₹ 2,077.43 Cr Water Supply Budget Gets Verified
    </h2>
    <div style="max-width: 780px; margin: 0 auto; color: #CBD5E1; font-size: 1.05rem; line-height: 1.6;">
        Every year, PMC publishes budget books in <b>Marathi</b> (308 pages) and tender notices in <b>English</b>.
        Watch this interactive command center cross-reference both datasets in real-time, catching additions slips,
        mirror gaps, and impossible pipeline lengths with zero false accusations.
    </div>
    <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <span style="background: rgba(37,99,235,0.3); border: 1px solid #3B82F6; padding: 6px 14px; border-radius: 8px; font-size: 0.9rem;">
            💧 141 Municipal Water Zones
        </span>
        <span style="background: rgba(245,158,11,0.3); border: 1px solid #F59E0B; padding: 6px 14px; border-radius: 8px; font-size: 0.9rem;">
            🔍 3 Deterministic Forensic Invariants
        </span>
        <span style="background: rgba(16,185,129,0.3); border: 1px solid #10B981; padding: 6px 14px; border-radius: 8px; font-size: 0.9rem;">
            🔒 SHA-256 Tamper-Proof Lineage
        </span>
    </div>
</div>
"""
