/* ═══════════════════════════════════════════════════════════
   Slang Translator — Frontend Logic
   ═══════════════════════════════════════════════════════════ */

const API = '';

const EXAMPLES = [
  "bro is cooked no cap",
  "scene kya hai bhai",
  "ngl that movie was mid fr fr",
  "wagwan bruv innit",
  "jhakaas performance thi yaar",
  "she understood the assignment",
  "that's sick lowkey",
  "full tight hai bhai",
  "he's got mad rizz tbh",
  "I'm deadass shook rn",
];

// ── Init ──────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  loadLanguages();
  loadStats();
  loadDictionary();
  renderExamples();
});

// ── Tabs ──────────────────────────────────────────────────

function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('content-' + btn.dataset.tab).classList.add('active');
    });
  });
}

// ── Examples ──────────────────────────────────────────────

function renderExamples() {
  const pBox = document.getElementById('pipelineExamples');
  const nBox = document.getElementById('normalizeExamples');
  EXAMPLES.forEach(ex => {
    [pBox, nBox].forEach(box => {
      const chip = document.createElement('button');
      chip.className = 'example-chip';
      chip.textContent = ex;
      chip.onclick = () => {
        const isP = box === pBox;
        document.getElementById(isP ? 'pipelineInput' : 'normalizeInput').value = ex;
      };
      box.appendChild(chip);
    });
  });
}

// ── Load Languages ────────────────────────────────────────

async function loadLanguages() {
  try {
    const res = await fetch(API + '/api/languages');
    const json = await res.json();
    const sel = document.getElementById('targetLang');
    const langs = json.data.popular;
    for (const [code, name] of Object.entries(langs)) {
      const opt = document.createElement('option');
      opt.value = code;
      opt.textContent = name;
      if (code === 'hi') opt.selected = true;
      sel.appendChild(opt);
    }
  } catch (e) {
    console.error('Failed to load languages:', e);
  }
}

// ── Load Stats ────────────────────────────────────────────

async function loadStats() {
  try {
    const res = await fetch(API + '/api/stats');
    const json = await res.json();
    document.getElementById('statTotal').textContent = json.data.total_entries;
  } catch (e) {
    console.error('Failed to load stats:', e);
  }
}

// ── Pipeline (Full Translate) ─────────────────────────────

async function runPipeline() {
  const text = document.getElementById('pipelineInput').value.trim();
  const lang = document.getElementById('targetLang').value;
  if (!text) return;

  const btn = document.getElementById('pipelineBtn');
  btn.classList.add('loading');
  btn.disabled = true;

  try {
    const res = await fetch(API + '/api/pipeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, target_lang: lang }),
    });
    const json = await res.json();
    const d = json.data.pipeline_summary;

    const flow = document.getElementById('pipelineFlow');
    flow.innerHTML = `
      <div class="pipeline-step">
        <div class="step-label">① Original Input (Slang)</div>
        <div class="step-text">${escHtml(d.input)}</div>
      </div>
      <div class="pipeline-arrow">↓</div>
      <div class="pipeline-step">
        <div class="step-label">② Normalized English</div>
        <div class="step-text">${escHtml(d.normalized_english)}</div>
      </div>
      <div class="pipeline-arrow">↓</div>
      <div class="pipeline-step">
        <div class="step-label">③ Translated (${escHtml(d.target_language)})</div>
        <div class="step-text translated">${escHtml(d.final_translation)}</div>
      </div>
    `;

    const meta = document.getElementById('pipelineMeta');
    meta.innerHTML = `
      <span class="meta-tag tone">Tone: ${d.tone_detected}</span>
      <span class="meta-tag region">Region: ${d.region_detected}</span>
      <span class="meta-tag confidence">Confidence: ${(d.confidence * 100).toFixed(0)}%</span>
    `;

    document.getElementById('pipelineResult').classList.add('visible');
  } catch (e) {
    alert('Error: ' + e.message);
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

// ── Normalize Only ────────────────────────────────────────

async function runNormalize() {
  const text = document.getElementById('normalizeInput').value.trim();
  if (!text) return;

  const btn = document.getElementById('normalizeBtn');
  btn.classList.add('loading');
  btn.disabled = true;

  try {
    const res = await fetch(API + '/api/normalize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const json = await res.json();
    const d = json.data;

    const flow = document.getElementById('normalizeFlow');
    flow.innerHTML = `
      <div class="pipeline-step">
        <div class="step-label">Original</div>
        <div class="step-text">${escHtml(d.original)}</div>
      </div>
      <div class="pipeline-arrow">↓</div>
      <div class="pipeline-step">
        <div class="step-label">Standard English</div>
        <div class="step-text translated">${escHtml(d.normalized)}</div>
      </div>
    `;

    const meta = document.getElementById('normalizeMeta');
    meta.innerHTML = `
      <span class="meta-tag method">Method: ${d.method}</span>
      <span class="meta-tag tone">Tone: ${d.tone}</span>
      <span class="meta-tag region">Region: ${d.region}</span>
      <span class="meta-tag confidence">Confidence: ${(d.confidence * 100).toFixed(0)}%</span>
      ${d.slang_detected ? `<span class="meta-tag tone">Detected: ${escHtml(d.slang_detected)}</span>` : ''}
    `;

    document.getElementById('normalizeResult').classList.add('visible');
  } catch (e) {
    alert('Error: ' + e.message);
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

// ── Dictionary ────────────────────────────────────────────

let allDictEntries = [];

async function loadDictionary() {
  try {
    const res = await fetch(API + '/api/dictionary');
    const json = await res.json();
    allDictEntries = json.data;
    renderFilters();
    renderDict(allDictEntries);
    document.getElementById('dictSearch').addEventListener('input', filterDict);
  } catch (e) {
    console.error('Failed to load dictionary:', e);
  }
}

function renderFilters() {
  const regions = [...new Set(allDictEntries.map(e => e.region))];
  const bar = document.getElementById('filterBar');
  const allBtn = document.createElement('button');
  allBtn.className = 'filter-btn active';
  allBtn.textContent = 'All';
  allBtn.onclick = () => { setActiveFilter(allBtn); renderDict(allDictEntries); };
  bar.appendChild(allBtn);

  const flags = { india: '🇮🇳', us: '🇺🇸', uk: '🇬🇧', australia: '🇦🇺', internet: '🌐', general: '🌍' };
  regions.forEach(r => {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.textContent = (flags[r] || '') + ' ' + r.charAt(0).toUpperCase() + r.slice(1);
    btn.onclick = () => {
      setActiveFilter(btn);
      renderDict(allDictEntries.filter(e => e.region === r));
    };
    bar.appendChild(btn);
  });
}

function setActiveFilter(active) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  active.classList.add('active');
}

function filterDict() {
  const q = document.getElementById('dictSearch').value.toLowerCase();
  const filtered = allDictEntries.filter(e =>
    e.slang.toLowerCase().includes(q) || e.meaning.toLowerCase().includes(q)
  );
  renderDict(filtered);
}

function renderDict(entries) {
  const grid = document.getElementById('dictGrid');
  grid.innerHTML = entries.map(e => `
    <div class="dict-card">
      <div class="slang">"${escHtml(e.slang)}"</div>
      <div class="meaning">${escHtml(e.meaning)}</div>
      <div class="tags">
        <span>${e.region}</span>
        <span>${e.tone}</span>
      </div>
    </div>
  `).join('');
}

// ── Helpers ───────────────────────────────────────────────

function escHtml(s) {
  if (!s) return '';
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
