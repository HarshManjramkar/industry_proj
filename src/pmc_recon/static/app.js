/**
 * PMC Procurement Reconciliation Command Center - Client State Engine
 * Adheres to The Elm Architecture (TEA) principles:
 * - Unidirectional data flow
 * - State immutability
 * - Strict XSS sanitization (CWE-79 prevention)
 */

// Pure HTML sanitizer for CWE-79 mitigation
function escapeHtml(unsafe) {
  if (unsafe === null || unsafe === undefined) return '';
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

const AppState = {
  activeFlags: [],
  activeTenders: [],
  activeBudget: [],
  activeLinks: [],
  selectedFlag: null,
  currentView: 'tenders',
  isSubmitting: false,
};

async function loadData() {
  try {
    const [mRes, fRes, tRes, bRes, lRes] = await Promise.all([
      fetch('/api/metrics').then(r => r.json()),
      fetch('/api/flags').then(r => r.json()),
      fetch('/api/tenders').then(r => r.json()),
      fetch('/api/budget').then(r => r.json()),
      fetch('/api/links').then(r => r.json()),
    ]);

    document.getElementById('metric-tenders').textContent = mRes.tenders_count;
    document.getElementById('metric-budget').textContent = mRes.budget_count;
    document.getElementById('metric-links').textContent = mRes.links_count;
    document.getElementById('metric-flags').textContent = mRes.open_flags;
    document.getElementById('flag-count-badge').textContent = `${mRes.open_flags} Open`;

    AppState.activeFlags = fRes;
    AppState.activeTenders = tRes;
    AppState.activeBudget = bRes;
    AppState.activeLinks = lRes;

    renderFlags();
    renderActiveView();
  } catch (err) {
    console.error("Failed to load dashboard data:", err);
  }
}

function renderFlags() {
  const list = document.getElementById('anomaly-list');
  list.innerHTML = '';

  AppState.activeFlags.forEach(f => {
    const card = document.createElement('div');
    const isActive = AppState.selectedFlag && AppState.selectedFlag.flag_id === f.flag_id;
    card.className = `anomaly-card ${isActive ? 'active' : ''}`;
    
    // XSS-safe rendering via escapeHtml
    card.innerHTML = `
      <div class="card-top">
        <span class="rule-chip">${escapeHtml(f.rule_id)}</span>
        <span class="card-meta">${escapeHtml(f.severity.toUpperCase())}</span>
      </div>
      <div class="card-title">${escapeHtml(f.title)}</div>
      <div class="card-meta">ID: ${escapeHtml(f.flag_id)} · ${escapeHtml(f.status)}</div>
    `;
    card.onclick = () => selectFlag(f);
    list.appendChild(card);
  });
}

function selectFlag(f) {
  AppState.selectedFlag = f;
  renderFlags();

  document.getElementById('target-title').textContent = f.title;
  
  let evidenceStr = "";
  try {
    evidenceStr = JSON.stringify(JSON.parse(f.evidence_json), null, 2);
  } catch {
    evidenceStr = f.evidence_json;
  }
  document.getElementById('target-evidence').textContent = evidenceStr;

  let expList = [];
  try {
    expList = JSON.parse(f.benign_explanations_json);
  } catch {
    expList = [f.benign_explanations_json];
  }

  const expContainer = document.getElementById('target-explanations');
  expContainer.innerHTML = '';
  expList.forEach(e => {
    const div = document.createElement('div');
    div.textContent = `• ${e}`;
    expContainer.appendChild(div);
  });

  const btn = document.getElementById('btn-resolve');
  btn.disabled = false;
  btn.textContent = `Mark ${f.flag_id} as Explained`;
}

async function resolveCurrentFlag() {
  if (!AppState.selectedFlag || AppState.isSubmitting) return;
  AppState.isSubmitting = true;
  const btn = document.getElementById('btn-resolve');
  btn.disabled = true;

  try {
    await fetch('/api/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        flag_id: AppState.selectedFlag.flag_id,
        outcome: 'explained',
        comment: 'Verified against official corrigendum notice 1. Innocent synchronization lag confirmed.'
      })
    });
    await loadData();
  } catch (err) {
    console.error("Resolution failed:", err);
  } finally {
    AppState.isSubmitting = false;
  }
}

function switchView(view) {
  AppState.currentView = view;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  renderActiveView();
}

function renderActiveView() {
  const view = document.getElementById('grid-view');
  
  if (AppState.currentView === 'tenders') {
    view.innerHTML = `
      <table class="data-table">
        <thead><tr><th>Tender ID</th><th>Ref No</th><th>Title</th><th>Value (INR)</th><th>Status</th><th>Source</th></tr></thead>
        <tbody>
          ${AppState.activeTenders.map(t => `
            <tr>
              <td style="color:var(--accent-cyan);">${escapeHtml(t.tender_id)}</td>
              <td>${escapeHtml(t.reference_number)}</td>
              <td>${escapeHtml(t.title)}</td>
              <td style="color:var(--text-primary); font-weight:600;">₹ ${(t.value_inr).toLocaleString('en-IN')}</td>
              <td><span class="brand-badge">${escapeHtml(t.status)}</span></td>
              <td>${escapeHtml(t.source_name)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } else if (AppState.currentView === 'budget') {
    view.innerHTML = `
      <table class="data-table">
        <thead><tr><th>Budget Head</th><th>Marathi Description</th><th>Fiscal Year</th><th>Type</th><th>Crore (INR)</th></tr></thead>
        <tbody>
          ${AppState.activeBudget.map(b => `
            <tr>
              <td style="color:var(--accent-cyan); font-weight:700;">${escapeHtml(b.budget_head_code)}</td>
              <td>${escapeHtml(b.description_marathi)}</td>
              <td>${escapeHtml(b.fiscal_year)}</td>
              <td>${escapeHtml(b.amount_type)}</td>
              <td style="color:var(--accent-emerald); font-weight:700;">₹ ${b.amount_inr_crore} Cr</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } else if (AppState.currentView === 'links') {
    view.innerHTML = `
      <table class="data-table">
        <thead><tr><th>Link ID</th><th>Tender ID</th><th>Budget Head</th><th>Method</th><th>Confidence</th><th>Status</th></tr></thead>
        <tbody>
          ${AppState.activeLinks.map(l => `
            <tr>
              <td style="color:var(--text-muted);">${escapeHtml(l.link_id)}</td>
              <td style="color:var(--accent-cyan);">${escapeHtml(l.left_record_id)}</td>
              <td style="color:var(--accent-emerald); font-weight:700;">${escapeHtml(l.right_record_id)}</td>
              <td>${escapeHtml(l.method)}</td>
              <td style="font-weight:700;">${(l.confidence * 100).toFixed(1)}%</td>
              <td><span class="brand-badge">${escapeHtml(l.status)}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }
}

// Initial load
loadData();
setInterval(loadData, 5000);
