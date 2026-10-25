"""Cinematic Movie-Style Intro Sequence for PMC Recon.
Auto-transitions after 5 seconds or on click anywhere, with smooth 0.9s cinematic fade.
No buttons required. Strictly under 350 lines and compliant with SRP.
"""

def render_cinematic_intro_html() -> str:
    """Return fullscreen overlay with auto 5s timer and click-anywhere transition."""
    return """
<style>
    @keyframes epicFadeIn {
        0% { opacity: 0; transform: translateY(22px) scale(0.96); }
        100% { opacity: 1; transform: translateY(0) scale(1.0); }
    }
    @keyframes goldAuraPulse {
        0% { box-shadow: 0 0 25px rgba(212, 175, 55, 0.25), inset 0 0 15px rgba(212, 175, 55, 0.1); }
        50% { box-shadow: 0 0 65px rgba(212, 175, 55, 0.5), inset 0 0 30px rgba(243, 198, 72, 0.25); }
        100% { box-shadow: 0 0 25px rgba(212, 175, 55, 0.25), inset 0 0 15px rgba(212, 175, 55, 0.1); }
    }
    @keyframes progressCountdown {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    #cinematicIntroOverlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        background: radial-gradient(ellipse at 50% 45%, #0E1D44 0%, #070C1D 65%, #020409 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        user-select: none;
        transition: opacity 0.9s cubic-bezier(0.16, 1, 0.3, 1), transform 0.9s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .cinematic-stage {
        background: rgba(10, 18, 41, 0.85);
        border: 2px solid rgba(212, 175, 55, 0.45);
        border-radius: 16px;
        padding: 3.5rem 3rem 2.5rem 3rem;
        text-align: center;
        animation: epicFadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1), goldAuraPulse 4s infinite ease-in-out;
        max-width: 960px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
    }
    .cinema-prelude {
        color: #F3C648;
        font-size: 0.85rem;
        letter-spacing: 0.35em;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.85rem;
    }
    .cinema-main-title {
        color: #FFFFFF !important;
        font-size: 3.0rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin: 0.4rem 0 0.8rem 0;
        text-shadow: 0 4px 25px rgba(0, 0, 0, 0.9), 0 0 35px rgba(212, 175, 55, 0.45);
    }
    .cinema-subtitle {
        color: #E2E8F0 !important;
        font-size: 1.2rem;
        font-weight: 500;
        max-width: 760px;
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
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.35);
        padding: 0.5rem 1.15rem;
        border-radius: 8px;
        font-size: 0.88rem;
        color: #F8FAFC;
    }
    .stat-pill b {
        color: #F3C648;
    }
    .cinema-hint {
        color: #94A3B8;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        margin-top: 1rem;
        text-transform: uppercase;
    }

    .countdown-bar-container {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100vw;
        height: 3px;
        background: rgba(212, 175, 55, 0.2);
    }
    .countdown-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #F3C648, #D4AF37, #38BDF8);
        animation: progressCountdown 5s linear forwards;
    }
</style>

<div id="cinematicIntroOverlay" onclick="dismissCinematicIntro()">
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
            <span style="color: #94A3B8; font-size: 0.98rem;">
                Mathematical invariants, Hampel MAD filters, and SHA-256 cryptographic lineage cross-examine public expenditure with zero bot hallucinations.
            </span>
        </p>
        <div class="cinema-stats-strip">
            <div class="stat-pill">💧 <b>141</b> Municipal Zones</div>
            <div class="stat-pill">🧮 <b>₹ 2,077.43 Cr</b> Monitored Budget</div>
            <div class="stat-pill">⚡ <b>&lt; 5 ms</b> Deterministic Invariant Radar</div>
            <div class="stat-pill">🔒 <b>SHA-256</b> Cryptographic Lineage</div>
        </div>
        <div class="cinema-hint">
            ⏳ Entering command center automatically in 5s • Click anywhere to enter immediately
        </div>
    </div>
    <div class="countdown-bar-container">
        <div class="countdown-bar-fill"></div>
    </div>
</div>

<script>
function dismissCinematicIntro() {
    const el = document.getElementById('cinematicIntroOverlay');
    if (el && el.style.display !== 'none') {
        el.style.opacity = '0';
        el.style.transform = 'scale(1.04)';
        setTimeout(() => {
            el.style.display = 'none';
        }, 900);
    }
}
// Automatically trigger transition after 5 seconds
setTimeout(dismissCinematicIntro, 5000);
</script>
"""
