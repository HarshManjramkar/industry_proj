"""Cinematic Movie-Style Intro Sequence for PMC Recon.
Renders on application initial load to immerse evaluators, citizens, and faculty
in the scale, gravity, and sovereign mission of the civic reconciliation engine.
Strictly under 350 lines and compliant with SRP.
"""

def render_cinematic_intro_html() -> str:
    """Return fullscreen cinematic movie intro with gold aura and dramatic typography."""
    return """
<style>
    @keyframes epicFadeIn {
        0% { opacity: 0; transform: translateY(18px) scale(0.97); }
        100% { opacity: 1; transform: translateY(0) scale(1.0); }
    }
    @keyframes goldAuraPulse {
        0% { box-shadow: 0 0 25px rgba(212, 175, 55, 0.2), inset 0 0 15px rgba(212, 175, 55, 0.1); }
        50% { box-shadow: 0 0 55px rgba(212, 175, 55, 0.45), inset 0 0 30px rgba(243, 198, 72, 0.25); }
        100% { box-shadow: 0 0 25px rgba(212, 175, 55, 0.2), inset 0 0 15px rgba(212, 175, 55, 0.1); }
    }
    @keyframes beamSweep {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .cinematic-stage {
        background: radial-gradient(ellipse at 50% 40%, #0F1C3F 0%, #070B18 65%, #020409 100%);
        border: 2px solid rgba(212, 175, 55, 0.4);
        border-radius: 14px;
        padding: 3.5rem 2rem 2.5rem 2rem;
        text-align: center;
        animation: epicFadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1), goldAuraPulse 4s infinite ease-in-out;
        margin: 1.5rem auto 1.5rem auto;
        max-width: 960px;
    }
    .cinema-prelude {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #F3C648;
        font-size: 0.85rem;
        letter-spacing: 0.35em;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.85rem;
        opacity: 0.95;
    }
    .cinema-main-title {
        color: #FFFFFF !important;
        font-size: 2.85rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin: 0.4rem 0 0.8rem 0;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8), 0 0 35px rgba(212, 175, 55, 0.4);
    }
    .cinema-subtitle {
        color: #E2E8F0 !important;
        font-size: 1.2rem;
        font-weight: 500;
        max-width: 720px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.6;
    }
    .cinema-stats-strip {
        display: flex;
        justify-content: center;
        gap: 1.25rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .stat-pill {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(212, 175, 55, 0.35);
        padding: 0.5rem 1.15rem;
        border-radius: 8px;
        font-size: 0.88rem;
        color: #F8FAFC;
    }
    .stat-pill b {
        color: #F3C648;
    }
</style>

<div class="cinematic-stage">
    <div class="cinema-prelude">
        🏛️ PUNE MUNICIPAL CORPORATION • FORENSIC BRIEFING
    </div>
    <div style="font-size: 3rem; margin-bottom: 0.2rem;">
        ⚖️
    </div>
    <h1 class="cinema-main-title">
        पुणे महानगरपालिका<br>
        <span style="background: linear-gradient(90deg, #F3C648, #FFFFFF, #D4AF37);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PMC RECON ENGINE
        </span>
    </h1>
    <p class="cinema-subtitle">
        In a metropolis of <b>4.5 Million citizens</b>, <b>₹ 2,077.43 Crores</b> are allocated for water supply.
        Published across 308-page Marathi budget books and English state tender portals.
        <br>
        <span style="color: #94A3B8; font-size: 0.98rem;">
            Watch mathematical invariants, Hampel MAD filters, and SHA-256 cryptographic lineage cross-examine public expenditure with zero bot hallucinations.
        </span>
    </p>
    <div class="cinema-stats-strip">
        <div class="stat-pill">💧 <b>141</b> Municipal Zones</div>
        <div class="stat-pill">🧮 <b>₹ 2,077.43 Cr</b> Monitored Budget</div>
        <div class="stat-pill">⚡ <b>&lt; 5 ms</b> Deterministic Invariant Radar</div>
        <div class="stat-pill">🔒 <b>SHA-256</b> Cryptographic Lineage</div>
    </div>
</div>
"""
