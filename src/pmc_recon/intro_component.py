"""Cinematic Movie-Style Intro Sequence for PMC Recon.
Renders fullscreen theatrical sequence with gold aura and automatic transition.
Strictly under 350 lines and compliant with SRP.
"""


def render_cinematic_intro_html() -> str:
    """Return fullscreen theatrical intro sequence with smooth timed fade."""
    return """
<style>
    @keyframes cinemaFade {
        0% { opacity: 0; transform: scale(0.96); }
        15% { opacity: 1; transform: scale(1.0); }
        75% { opacity: 1; transform: scale(1.0); }
        100% { opacity: 0; transform: scale(1.03); }
    }

    @keyframes goldAuraGlow {
        0% { box-shadow: 0 0 30px rgba(212, 175, 55, 0.25), inset 0 0 15px rgba(212, 175, 55, 0.1); }
        50% { box-shadow: 0 0 65px rgba(212, 175, 55, 0.55), inset 0 0 35px rgba(243, 198, 72, 0.25); }
        100% { box-shadow: 0 0 30px rgba(212, 175, 55, 0.25), inset 0 0 15px rgba(212, 175, 55, 0.1); }
    }

    @keyframes timelineFill {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    .cinematic-fullscreen {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 99999999 !important;
        background: radial-gradient(ellipse at 50% 45%, #0E1D44 0%, #070C1D 65%, #020409 100%) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        animation: cinemaFade 3.5s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        box-sizing: border-box !important;
        padding: 2rem !important;
    }

    .cinematic-stage {
        background: rgba(10, 18, 41, 0.94) !important;
        border: 2px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 16px !important;
        padding: 3.5rem 3rem 2.8rem 3rem !important;
        text-align: center !important;
        animation: goldAuraGlow 3s infinite ease-in-out !important;
        max-width: 960px !important;
        box-shadow: 0 12px 50px rgba(0, 0, 0, 0.85) !important;
    }
    .cinema-prelude {
        color: #F3C648 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.35em !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        margin-bottom: 0.85rem !important;
    }
    .cinema-main-title {
        color: #FFFFFF !important;
        font-size: 2.9rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.15 !important;
        margin: 0.4rem 0 0.8rem 0 !important;
        text-shadow: 0 4px 25px rgba(0, 0, 0, 0.9), 0 0 35px rgba(212, 175, 55, 0.45) !important;
    }
    .cinema-subtitle {
        color: #E2E8F0 !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        max-width: 760px !important;
        margin: 0 auto 1.8rem auto !important;
        line-height: 1.6 !important;
    }
    .cinema-stats-strip {
        display: flex !important;
        justify-content: center !important;
        gap: 1.25rem !important;
        flex-wrap: wrap !important;
    }
    .stat-pill {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        padding: 0.5rem 1.15rem !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        color: #F8FAFC !important;
    }
    .stat-pill b {
        color: #F3C648 !important;
    }

    .countdown-bar-container {
        position: absolute !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 4px !important;
        background: rgba(212, 175, 55, 0.2) !important;
    }
    .countdown-bar-fill {
        height: 100% !important;
        background: linear-gradient(90deg, #F3C648, #D4AF37, #38BDF8) !important;
        animation: timelineFill 3.5s linear forwards !important;
    }
</style>

<div class="cinematic-fullscreen">
    <div class="cinematic-stage">
        <div class="cinema-prelude">
            🏛️ PUNE MUNICIPAL CORPORATION • CIVIC FORENSIC PROLOGUE
        </div>
        <div style="font-size: 3.2rem; margin-bottom: 0.2rem;">
            ⚖️
        </div>
        <h1 class="cinema-main-title">
            पुणे महानगरपालिका<br>
            <span style="background: linear-gradient(90deg, #F3C648 0%, #FFFFFF 50%, #D4AF37 100%);
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                PMC RECON COMMAND CENTER
            </span>
        </h1>
        <p class="cinema-subtitle">
            In a metropolis of <b>4.5 Million citizens</b>, <b>₹ 2,077.43 Crores</b> are allocated for water supply.
            Published across 308-page Marathi budget books and English state tender portals.
            <br>
            <span style="color: #94A3B8; font-size: 0.95rem;">
                Mathematical invariants, Hampel MAD filters, and SHA-256 cryptographic lineage cross-examine public expenditure with zero bot hallucinations.
            </span>
        </p>
        <div class="cinema-stats-strip">
            <div class="stat-pill">💧 <b>141</b> Municipal Zones</div>
            <div class="stat-pill">🧮 <b>₹ 2,077.43 Cr</b> Monitored Budget</div>
            <div class="stat-pill">⚡ <b>&lt; 5 ms</b> Deterministic Invariant Radar</div>
            <div class="stat-pill">🔒 <b>SHA-256</b> Cryptographic Lineage</div>
        </div>
    </div>
    <div class="countdown-bar-container">
        <div class="countdown-bar-fill"></div>
    </div>
</div>
"""
