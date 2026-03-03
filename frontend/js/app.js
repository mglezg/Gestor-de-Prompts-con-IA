// ─────────────────────────────────────────────────────────
//  Prompt Manager — app.js
// ─────────────────────────────────────────────────────────
const API = '/api';
let state = {
  projects: [],
  prompts: [],
  tags: [],
  currentView: 'dashboard',
  currentProjectFilter: null,
  currentPromptId: null,
  tagFilter: null,
  comparingA: null,
  comparingB: null,
  editingProjectId: null,
  selectedIcon: '📁',
  selectedColor: '#3b82f6',
  modelTargets: [],
  criteria: {}
};

// ── API HELPERS ───────────────────────────────────────────
async function api(path, options = {}) {
  try {
    const res = await fetch(API + path, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Error desconocido' }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return await res.json();
  } catch (e) {
    toast(e.message, 'error');
    throw e;
  }
}

// ── TOAST ─────────────────────────────────────────────────
function toast(msg, type = 'info', duration = 3000) {
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type]||'ℹ'}</span><span>${msg}</span>`;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => el.remove(), duration);
}

// ── NAVIGATION ────────────────────────────────────────────
function setView(view, extra = {}) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));

  const el = document.getElementById(`view-${view}`);
  if (el) el.classList.add('active');

  const nav = document.querySelector(`.sidebar-item[data-view="${view}"]`);
  if (nav) nav.classList.add('active');

  const titles = {
    dashboard: 'Dashboard',
    prompts: extra.projectName ? `📁 ${extra.projectName}` : 'Todos los prompts',
    editor: extra.title || 'Editor de prompt',
    compare: 'Comparar prompts',
    criteria: 'Guía de criterios',
    settings: 'Configuración'
  };
  document.getElementById('topbar-title').textContent = titles[view] || view;
  state.currentView = view;

  if (view === 'dashboard') loadDashboard();
  if (view === 'prompts') loadPrompts();
  if (view === 'compare') loadCompareSelectors();
  if (view === 'criteria') renderCriteria();
  if (view === 'settings') loadSettings();
}

function goBackFromEditor() {
  setView(state.currentProjectFilter !== null ? 'prompts' : 'prompts');
}

// ── INIT ──────────────────────────────────────────────────
async function init() {
  await loadMeta();
  await loadProjects();
  loadDashboard();
  setupSidebarNav();
  checkApiKeyStatus();
}

async function loadMeta() {
  try {
    state.modelTargets = await api('/analysis/model-targets');
    state.criteria = await api('/analysis/criteria');
    state.tags = await api('/prompts/meta/tags');
  } catch(e) {}
}

function setupSidebarNav() {
  document.querySelectorAll('.sidebar-item[data-view]').forEach(item => {
    item.addEventListener('click', () => {
      state.currentProjectFilter = null;
      setView(item.dataset.view);
    });
  });
}

// ── PROJECTS ──────────────────────────────────────────────
async function loadProjects() {
  state.projects = await api('/projects/').catch(() => []);
  renderProjectSidebar();
  updateStats();
}

function renderProjectSidebar() {
  const list = document.getElementById('project-list');
  if (!state.projects.length) {
    list.innerHTML = `<div style="padding:8px 10px;font-size:12px;color:var(--text-muted);">Sin proyectos aún</div>`;
    return;
  }
  list.innerHTML = state.projects.map(p => `
    <div class="sidebar-item" onclick="filterByProject(${p.id},'${escHtml(p.name)}')" ondblclick="openProjectModal(${p.id})">
      <span class="project-dot" style="background:${p.color}"></span>
      <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escHtml(p.icon)} ${escHtml(p.name)}</span>
      <span class="badge">${p.prompt_count}</span>
    </div>
  `).join('');
}

function filterByProject(id, name) {
  state.currentProjectFilter = id;
  setView('prompts', { projectName: name });
}

// ── DASHBOARD ─────────────────────────────────────────────
async function loadDashboard() {
  await loadProjects();
  const prompts = await api('/prompts/?').catch(() => []);
  state.prompts = prompts;

  document.getElementById('stat-prompts').textContent = prompts.length;
  document.getElementById('stat-projects').textContent = state.projects.length;
  document.getElementById('stat-tags').textContent = state.tags.length;
  document.getElementById('badge-total').textContent = prompts.length;

  // Recent prompts
  const recentEl = document.getElementById('recent-prompts-list');
  const recent = prompts.slice(0, 6);
  recentEl.innerHTML = recent.length
    ? recent.map(p => promptMiniCard(p)).join('')
    : '<div class="empty-state"><p>Aún no tienes prompts</p></div>';

  // Projects in dashboard
  const projEl = document.getElementById('dashboard-projects');
  projEl.innerHTML = state.projects.length
    ? state.projects.map(p => `
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);cursor:pointer;" onclick="filterByProject(${p.id},'${escHtml(p.name)}')">
          <div style="width:8px;height:8px;border-radius:50%;background:${p.color};flex-shrink:0;"></div>
          <span style="font-size:13px;flex:1;">${escHtml(p.icon)} ${escHtml(p.name)}</span>
          <span class="text-muted text-mono">${p.prompt_count} prompts</span>
        </div>
      `).join('')
    : '<div class="empty-state"><p>Sin proyectos</p><button class="btn btn-secondary btn-sm" onclick="openProjectModal()">Crear proyecto</button></div>';
}

function promptMiniCard(p) {
  const proj = state.projects.find(x => x.id === p.project_id);
  return `
    <div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);cursor:pointer;" onclick="openEditor(${p.id})">
      ${proj ? `<div style="width:6px;height:6px;border-radius:50%;background:${proj.color};flex-shrink:0;"></div>` : ''}
      <div style="flex:1;min-width:0;">
        <div style="font-size:13px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escHtml(p.title)}</div>
        <div style="font-size:11px;color:var(--text-muted);font-family:var(--mono);">${proj ? escHtml(proj.name) : 'Sin proyecto'} · v${p.current_version}</div>
      </div>
    </div>
  `;
}

function updateStats() {
  document.getElementById('stat-projects').textContent = state.projects.length;
}

// ── PROMPTS LIST ──────────────────────────────────────────
async function loadPrompts() {
  let url = '/prompts/?';
  if (state.currentProjectFilter !== null) url += `project_id=${state.currentProjectFilter}&`;
  if (state.tagFilter) url += `tags=${encodeURIComponent(state.tagFilter)}&`;

  const prompts = await api(url).catch(() => []);
  state.prompts = prompts;

  // Update title
  if (state.currentProjectFilter !== null) {
    const p = state.projects.find(x => x.id === state.currentProjectFilter);
    document.getElementById('prompts-view-title').textContent = p ? `${p.icon} ${p.name}` : 'Proyecto';
  } else {
    document.getElementById('prompts-view-title').textContent = 'Todos los prompts';
  }

  // Tags filter bar
  const bar = document.getElementById('tag-filter-bar');
  bar.innerHTML = `<span class="filter-tag ${!state.tagFilter ? 'active' : ''}" onclick="setTagFilter(null)">Todos</span>`;
  state.tags.forEach(t => {
    bar.innerHTML += `<span class="filter-tag ${state.tagFilter === t ? 'active' : ''}" onclick="setTagFilter('${escHtml(t)}')">${escHtml(t)}</span>`;
  });

  // Render cards
  const grid = document.getElementById('prompts-grid');
  if (!prompts.length) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1;">
        <div class="empty-icon">⚡</div>
        <p>No hay prompts aquí todavía</p>
        <button class="btn btn-primary btn-sm" onclick="openNewPromptModal()">+ Crear primer prompt</button>
      </div>`;
    return;
  }
  grid.innerHTML = prompts.map(p => promptCard(p)).join('');
}

function promptCard(p) {
  const proj = state.projects.find(x => x.id === p.project_id);
  const color = proj ? proj.color : 'var(--accent)';
  const tags = (p.tags || []).slice(0,3).map(t => `<span class="tag">${escHtml(t)}</span>`).join('');
  return `
    <div class="prompt-card" style="--project-color:${color}" onclick="openEditor(${p.id})">
      <div class="prompt-card-title">${escHtml(p.title)}</div>
      <div class="prompt-card-content">${escHtml(p.content)}</div>
      <div class="prompt-card-meta">
        ${tags}
        <span class="version-badge">v${p.current_version}</span>
        <span class="model-badge">${p.model_target}</span>
      </div>
    </div>`;
}

function setTagFilter(tag) {
  state.tagFilter = tag;
  loadPrompts();
}

// ── EDITOR ────────────────────────────────────────────────
async function openEditor(promptId) {
  const prompt = await api(`/prompts/${promptId}`).catch(() => null);
  if (!prompt) return;
  state.currentPromptId = promptId;

  document.getElementById('editor-title').value = prompt.title;
  document.getElementById('editor-content').value = prompt.content;
  document.getElementById('editor-tags').value = (prompt.tags || []).join(', ');
  document.getElementById('editor-change-note').value = '';

  // Populate project select
  const projSel = document.getElementById('editor-project');
  projSel.innerHTML = '<option value="">Sin proyecto</option>' +
    state.projects.map(p => `<option value="${p.id}" ${p.id === prompt.project_id ? 'selected' : ''}>${escHtml(p.icon)} ${escHtml(p.name)}</option>`).join('');

  // Populate model select
  const modelSel = document.getElementById('editor-model');
  modelSel.innerHTML = state.modelTargets.map(m =>
    `<option value="${m}" ${m === prompt.model_target ? 'selected' : ''}>${m}</option>`).join('');

  updateWordCount();
  document.getElementById('analysis-content').innerHTML = `<div class="empty-state"><div class="empty-icon">🔬</div><p>Haz clic en "Analizar" para evaluar la calidad</p><button class="btn btn-secondary btn-sm" onclick="analyzeCurrentPrompt()">Analizar ahora</button></div>`;
  document.getElementById('analysis-history').innerHTML = '<div class="empty-state"><p>Sin análisis previos</p></div>';

  setView('editor', { title: prompt.title });
  loadAnalysisHistory(promptId);
}

function openNewPromptModal() {
  const modal = document.getElementById('modal-prompt');
  document.getElementById('modal-prompt-title').textContent = 'Nuevo prompt';
  document.getElementById('modal-prompt-name').value = '';
  document.getElementById('modal-prompt-content').value = '';
  document.getElementById('modal-prompt-tags').value = '';
  document.getElementById('modal-prompt-desc').value = '';
  document.getElementById('modal-prompt-note').value = 'Versión inicial';

  // Populate selects
  const projSel = document.getElementById('modal-prompt-project');
  projSel.innerHTML = '<option value="">Sin proyecto</option>' +
    state.projects.map(p => `<option value="${p.id}" ${p.id === state.currentProjectFilter ? 'selected' : ''}>${escHtml(p.icon)} ${escHtml(p.name)}</option>`).join('');

  const modelSel = document.getElementById('modal-prompt-model');
  modelSel.innerHTML = state.modelTargets.map(m => `<option value="${m}">${m}</option>`).join('');

  modal.querySelector('.btn-primary').textContent = 'Crear prompt';
  modal.querySelector('.btn-primary').onclick = submitPromptModal;
  openModal('modal-prompt');
}

async function submitPromptModal() {
  const title = document.getElementById('modal-prompt-name').value.trim();
  const content = document.getElementById('modal-prompt-content').value.trim();
  if (!title || !content) { toast('Título y contenido son obligatorios', 'error'); return; }

  const tags = document.getElementById('modal-prompt-tags').value
    .split(',').map(t => t.trim()).filter(Boolean);

  const data = {
    title,
    content,
    description: document.getElementById('modal-prompt-desc').value,
    project_id: document.getElementById('modal-prompt-project').value || null,
    model_target: document.getElementById('modal-prompt-model').value || 'general',
    tags,
    change_note: document.getElementById('modal-prompt-note').value || 'Versión inicial'
  };

  const created = await api('/prompts/', { method: 'POST', body: JSON.stringify(data) }).catch(() => null);
  if (!created) return;

  toast(`Prompt "${title}" creado`, 'success');
  closeModal('modal-prompt');
  await loadMeta();
  await loadProjects();
  openEditor(created.id);
}

async function savePrompt() {
  if (!state.currentPromptId) return;
  const title = document.getElementById('editor-title').value.trim();
  const content = document.getElementById('editor-content').value.trim();
  if (!title || !content) { toast('Título y contenido son obligatorios', 'error'); return; }

  const tags = document.getElementById('editor-tags').value
    .split(',').map(t => t.trim()).filter(Boolean);
  const changeNote = document.getElementById('editor-change-note').value || 'Actualización';

  const data = {
    title,
    content,
    project_id: document.getElementById('editor-project').value || null,
    model_target: document.getElementById('editor-model').value || 'general',
    tags,
    change_note: changeNote
  };

  await api(`/prompts/${state.currentPromptId}`, { method: 'PUT', body: JSON.stringify(data) });
  toast('Prompt guardado', 'success');
  document.getElementById('editor-change-note').value = '';
  await loadMeta();
  await loadProjects();
}

function onEditorInput() {
  updateWordCount();
}

function updateWordCount() {
  const content = document.getElementById('editor-content').value;
  const words = content.trim() ? content.trim().split(/\s+/).length : 0;
  document.getElementById('editor-word-count').textContent = `${words} palabras`;
}

// ── ANALYSIS ──────────────────────────────────────────────
async function analyzeCurrentPrompt() {
  const content = state.currentPromptId
    ? document.getElementById('editor-content').value
    : null;
  if (!content || !content.trim()) { toast('El prompt está vacío', 'error'); return; }

  const analysisEl = document.getElementById('analysis-content');
  analysisEl.innerHTML = `<div class="loading-overlay"><div class="spinner"></div><span>Analizando con IA...</span></div>`;

  const payload = state.currentPromptId
    ? { prompt_id: state.currentPromptId }
    : { content };

  const result = await api('/analysis/analyze', { method: 'POST', body: JSON.stringify(payload) }).catch(() => null);
  if (!result) { analysisEl.innerHTML = '<div class="empty-state"><p>Error al analizar</p></div>'; return; }

  renderAnalysisResult(result, analysisEl);
  if (state.currentPromptId) loadAnalysisHistory(state.currentPromptId);
}

function renderAnalysisResult(result, container) {
  const score = result.overall_score;
  const color = scoreColor(score);
  const criteriaNames = {
    clarity: 'Claridad', specificity: 'Especificidad', structure: 'Estructura',
    format: 'Formato', context: 'Contexto', examples: 'Ejemplos'
  };

  const bars = Object.entries(result.criteria_scores).map(([k, v]) => `
    <div class="criteria-bar">
      <div class="criteria-bar-header">
        <span>${criteriaNames[k] || k}</span>
        <span style="color:${scoreColor(v)};font-family:var(--mono);">${v.toFixed(0)}</span>
      </div>
      <div class="criteria-bar-track">
        <div class="criteria-bar-fill" style="width:${v}%;background:${scoreColor(v)};"></div>
      </div>
    </div>`).join('');

  const suggestions = (result.suggestions || []).map(s => `
    <div class="suggestion-item priority-${s.priority}">
      <div class="suggestion-criterion">${s.criterion} · ${s.priority}</div>
      <div class="suggestion-issue">${escHtml(s.issue)}</div>
      <div class="suggestion-text">${escHtml(s.suggestion)}</div>
    </div>`).join('');

  const strengths = (result.strengths || []).map(s => `
    <div class="strength-item">${escHtml(s)}</div>`).join('');

  container.innerHTML = `
    <div style="text-align:center;margin-bottom:18px;">
      <div style="display:inline-flex;flex-direction:column;align-items:center;gap:6px;">
        <svg width="90" height="90" viewBox="0 0 90 90" style="transform:rotate(-90deg)">
          <circle cx="45" cy="45" r="38" fill="none" stroke="var(--bg-elevated)" stroke-width="7"/>
          <circle cx="45" cy="45" r="38" fill="none" stroke="${color}" stroke-width="7"
            stroke-dasharray="${2*Math.PI*38}" stroke-dashoffset="${2*Math.PI*38*(1-score/100)}"
            stroke-linecap="round"/>
        </svg>
        <div style="position:absolute;display:inline-flex;flex-direction:column;align-items:center;transform:translateY(-62px);">
          <div style="font-family:var(--display);font-size:22px;font-weight:700;color:${color};">${score.toFixed(0)}</div>
          <div style="font-size:10px;color:var(--text-muted);">/ 100</div>
        </div>
      </div>
      <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">${result.model_used === 'heuristic' ? 'Análisis heurístico' : '✨ Análisis con IA'}</div>
    </div>
    <div style="font-size:12px;color:var(--text-secondary);line-height:1.6;margin-bottom:16px;padding:10px;background:var(--bg-overlay);border-radius:var(--radius-sm);">${escHtml(result.summary)}</div>
    <div style="margin-bottom:14px;">${bars}</div>
    ${strengths ? `<div style="margin-bottom:14px;"><div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:8px;letter-spacing:0.8px;text-transform:uppercase;">Fortalezas</div>${strengths}</div>` : ''}
    ${suggestions ? `<div><div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:8px;letter-spacing:0.8px;text-transform:uppercase;">Sugerencias</div>${suggestions}</div>` : ''}
  `;
}

async function loadAnalysisHistory(promptId) {
  const analyses = await api(`/analysis/prompt/${promptId}`).catch(() => []);
  const el = document.getElementById('analysis-history');
  if (!analyses.length) {
    el.innerHTML = '<div class="empty-state"><p>Sin análisis previos</p></div>';
    return;
  }
  el.innerHTML = analyses.slice(0, 5).map((a, i) => `
    <div style="padding:10px;background:var(--bg-overlay);border-radius:var(--radius-sm);margin-bottom:8px;cursor:pointer;" onclick="showHistoricAnalysis(${i})">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
        <span style="font-size:12px;font-family:var(--mono);color:${scoreColor(a.overall_score)};font-weight:700;">${a.overall_score.toFixed(0)}/100</span>
        <span style="font-size:10px;color:var(--text-muted);">v${a.prompt_version} · ${formatDate(a.created_at)}</span>
      </div>
      <div style="font-size:11px;color:var(--text-secondary);">${escHtml(a.summary.slice(0,80))}...</div>
    </div>
  `).join('');

  // Store for reference
  el._analyses = analyses;
}

function showHistoricAnalysis(i) {
  const el = document.getElementById('analysis-history');
  if (!el._analyses) return;
  renderAnalysisResult(el._analyses[i], document.getElementById('analysis-content'));
  switchAnalysisTab('analysis', document.querySelector('.tab'));
}

function switchAnalysisTab(tab, el) {
  document.querySelectorAll('.analysis-panel .tab').forEach(t => t.classList.remove('active'));
  if(el) el.classList.add('active');
  document.getElementById('analysis-content').style.display = tab === 'analysis' ? '' : 'none';
  document.getElementById('analysis-history').style.display = tab === 'history' ? '' : 'none';
}

// ── VERSION HISTORY ───────────────────────────────────────
async function openVersionHistory() {
  if (!state.currentPromptId) return;
  const versions = await api(`/prompts/${state.currentPromptId}/versions`).catch(() => []);
  const el = document.getElementById('modal-versions-content');

  if (!versions.length) {
    el.innerHTML = '<div class="empty-state"><p>Sin versiones guardadas</p></div>';
  } else {
    el.innerHTML = versions.map(v => `
      <div class="version-item">
        <div class="version-num">v${v.version_number}</div>
        <div class="version-info">
          <div class="version-note">${escHtml(v.change_note || v.title)}</div>
          <div class="version-date">${formatDate(v.created_at)}</div>
        </div>
        <button class="btn btn-ghost btn-sm" onclick="previewVersion(${v.version_number}, \`${escJs(v.content)}\`)">Ver</button>
        <button class="btn btn-secondary btn-sm" onclick="restoreVersion(${v.version_number})">Restaurar</button>
      </div>
    `).join('');
  }
  openModal('modal-versions');
}

function previewVersion(vnum, content) {
  toast(`Vista previa v${vnum} (no guardada)`, 'info');
  document.getElementById('editor-content').value = content;
  updateWordCount();
  closeModal('modal-versions');
}

async function restoreVersion(vnum) {
  if (!confirm(`¿Restaurar versión ${vnum}? Esto creará una nueva versión.`)) return;
  await api(`/prompts/${state.currentPromptId}/restore/${vnum}`, { method: 'POST' });
  toast(`Versión ${vnum} restaurada como nueva versión`, 'success');
  closeModal('modal-versions');
  openEditor(state.currentPromptId);
}

// ── COMPARE ───────────────────────────────────────────────
async function loadCompareSelectors() {
  const prompts = await api('/prompts/?').catch(() => []);
  const options = prompts.map(p => `<option value="${p.id}">${escHtml(p.title)}</option>`).join('');
  ['compare-a', 'compare-b'].forEach(id => {
    const sel = document.getElementById(id);
    sel.innerHTML = '<option value="">Selecciona un prompt...</option>' + options;
  });
  state._comparePrompts = prompts;
}

async function loadComparePrompt(side) {
  const selId = side === 'a' ? 'compare-a' : 'compare-b';
  const contentId = side === 'a' ? 'compare-content-a' : 'compare-content-b';
  const id = document.getElementById(selId).value;
  if (!id) {
    document.getElementById(contentId).textContent = 'Selecciona un prompt';
    return;
  }
  const p = await api(`/prompts/${id}`).catch(() => null);
  if (p) {
    document.getElementById(contentId).textContent = p.content;
    if (side === 'a') state.comparingA = p;
    else state.comparingB = p;
  }
}

async function runComparison() {
  const idA = document.getElementById('compare-a').value;
  const idB = document.getElementById('compare-b').value;
  if (!idA || !idB) { toast('Selecciona ambos prompts', 'error'); return; }
  if (idA === idB) { toast('Selecciona prompts diferentes', 'error'); return; }

  const resultsEl = document.getElementById('compare-results');
  resultsEl.innerHTML = '<div class="loading-overlay" style="grid-column:1/-1;"><div class="spinner"></div><span>Analizando ambos prompts...</span></div>';

  const [ra, rb] = await Promise.all([
    api('/analysis/analyze', { method: 'POST', body: JSON.stringify({ prompt_id: parseInt(idA) }) }),
    api('/analysis/analyze', { method: 'POST', body: JSON.stringify({ prompt_id: parseInt(idB) }) })
  ]).catch(() => [null, null]);

  if (!ra || !rb) { resultsEl.innerHTML = ''; return; }

  const winner = ra.overall_score > rb.overall_score ? 'A' : rb.overall_score > ra.overall_score ? 'B' : 'Empate';

  resultsEl.innerHTML = `
    <div class="card">
      <div class="card-header">
        <div class="card-title">Prompt A ${winner === 'A' ? '🏆' : ''}</div>
        <span style="font-family:var(--mono);font-size:13px;color:${scoreColor(ra.overall_score)};font-weight:700;">${ra.overall_score.toFixed(0)}/100</span>
      </div>
      <div class="card-body">${compareBarSet(ra.criteria_scores)}</div>
    </div>
    <div class="card">
      <div class="card-header">
        <div class="card-title">Prompt B ${winner === 'B' ? '🏆' : ''}</div>
        <span style="font-family:var(--mono);font-size:13px;color:${scoreColor(rb.overall_score)};font-weight:700;">${rb.overall_score.toFixed(0)}/100</span>
      </div>
      <div class="card-body">${compareBarSet(rb.criteria_scores)}</div>
    </div>
  `;
}

function compareBarSet(scores) {
  const names = { clarity:'Claridad', specificity:'Especificidad', structure:'Estructura', format:'Formato', context:'Contexto', examples:'Ejemplos' };
  return Object.entries(scores).map(([k, v]) => `
    <div class="criteria-bar">
      <div class="criteria-bar-header"><span>${names[k]||k}</span><span style="color:${scoreColor(v)};font-family:var(--mono);">${v.toFixed(0)}</span></div>
      <div class="criteria-bar-track"><div class="criteria-bar-fill" style="width:${v}%;background:${scoreColor(v)};"></div></div>
    </div>`).join('');
}

// ── CRITERIA GUIDE ────────────────────────────────────────
function renderCriteria() {
  const el = document.getElementById('criteria-guide-content');
  if (!Object.keys(state.criteria).length) {
    el.innerHTML = '<div class="empty-state"><p>Cargando...</p></div>';
    api('/analysis/criteria').then(c => {
      state.criteria = c;
      renderCriteria();
    });
    return;
  }
  el.innerHTML = Object.entries(state.criteria).map(([k, c]) => `
    <div class="criteria-guide-item">
      <div class="criteria-guide-name">${c.name} <span style="color:var(--text-muted);font-weight:400;font-size:10px;">(peso: ${(c.weight*100).toFixed(0)}%)</span></div>
      <div class="criteria-guide-desc" style="margin-bottom:8px;">${c.description}</div>
      ${c.tips.map(t => `<div style="font-size:11px;color:var(--text-secondary);margin-bottom:3px;padding-left:10px;border-left:2px solid var(--accent);">→ ${t}</div>`).join('')}
    </div>
  `).join('');
}

// ── PROJECTS MODAL ────────────────────────────────────────
function openProjectModal(editId = null) {
  state.editingProjectId = editId;
  const isEdit = editId !== null;
  const proj = isEdit ? state.projects.find(p => p.id === editId) : null;

  document.getElementById('modal-project-title').textContent = isEdit ? 'Editar proyecto' : 'Nuevo proyecto';
  document.getElementById('modal-project-name').value = proj ? proj.name : '';
  document.getElementById('modal-project-desc').value = proj ? proj.description : '';
  document.getElementById('modal-project-delete').style.display = isEdit ? '' : 'none';

  state.selectedIcon = proj ? proj.icon : '📁';
  state.selectedColor = proj ? proj.color : '#3b82f6';

  // Highlight selected color
  document.querySelectorAll('.color-swatch').forEach(s => {
    s.classList.toggle('selected', s.dataset.color === state.selectedColor);
  });

  openModal('modal-project');
}

function selectIcon(el) {
  state.selectedIcon = el.title;
  document.querySelectorAll('#icon-picker span').forEach(s => s.style.outline = 'none');
  el.style.outline = '2px solid var(--accent)';
  el.style.borderRadius = '4px';
}

function selectColor(el) {
  state.selectedColor = el.dataset.color;
  document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
  el.classList.add('selected');
}

async function submitProjectModal() {
  const name = document.getElementById('modal-project-name').value.trim();
  if (!name) { toast('El nombre es obligatorio', 'error'); return; }

  const data = {
    name,
    description: document.getElementById('modal-project-desc').value,
    icon: state.selectedIcon,
    color: state.selectedColor
  };

  if (state.editingProjectId) {
    await api(`/projects/${state.editingProjectId}`, { method: 'PUT', body: JSON.stringify(data) });
    toast('Proyecto actualizado', 'success');
  } else {
    await api('/projects/', { method: 'POST', body: JSON.stringify(data) });
    toast(`Proyecto "${name}" creado`, 'success');
  }

  closeModal('modal-project');
  await loadProjects();
  if (state.currentView === 'dashboard') loadDashboard();
}

async function deleteCurrentProject() {
  if (!state.editingProjectId) return;
  const proj = state.projects.find(p => p.id === state.editingProjectId);
  if (!confirm(`¿Eliminar el proyecto "${proj?.name}"? Los prompts no se borrarán.`)) return;

  await api(`/projects/${state.editingProjectId}`, { method: 'DELETE' });
  toast('Proyecto eliminado', 'success');
  closeModal('modal-project');
  state.currentProjectFilter = null;
  await loadProjects();
  setView('prompts');
}

// ── SETTINGS ──────────────────────────────────────────────
async function loadSettings() {
  checkApiKeyStatus();
}

async function checkApiKeyStatus() {
  const status = await api('/analysis/config/api-key-status').catch(() => ({ configured: false }));
  const dot = document.getElementById('api-dot');
  const dotSettings = document.getElementById('api-dot-settings');
  const text = document.getElementById('api-key-status-text');

  if (dot) dot.classList.toggle('active', status.configured);
  if (dotSettings) dotSettings.classList.toggle('active', status.configured);
  if (text) text.textContent = status.configured ? `Configurada (${status.preview})` : 'No configurada';
}

async function saveApiKey() {
  const key = document.getElementById('api-key-input').value.trim();
  await api('/analysis/config/api-key', { method: 'POST', body: JSON.stringify({ api_key: key }) });
  toast('API key guardada', 'success');
  document.getElementById('api-key-input').value = '';
  checkApiKeyStatus();
}

async function clearApiKey() {
  await api('/analysis/config/api-key', { method: 'POST', body: JSON.stringify({ api_key: '' }) });
  toast('API key eliminada', 'info');
  checkApiKeyStatus();
}

// ── EXPORT / IMPORT ───────────────────────────────────────
async function exportPrompts() {
  let url = '/api/prompts/export/json';
  if (state.currentProjectFilter) url += `?project_id=${state.currentProjectFilter}`;

  const data = await fetch(url).then(r => r.json());
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `prompts-export-${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  toast('Prompts exportados', 'success');
}

async function importPrompts(input) {
  const file = input.files[0];
  if (!file) return;
  const text = await file.text();
  let data;
  try { data = JSON.parse(text); } catch(e) { toast('Archivo JSON inválido', 'error'); return; }

  const result = await api('/prompts/import/json', { method: 'POST', body: JSON.stringify(data) }).catch(() => null);
  if (result) {
    toast(`${result.imported} prompts importados`, 'success');
    input.value = '';
    await loadMeta();
    await loadProjects();
    loadPrompts();
  }
}

// ── SEARCH ────────────────────────────────────────────────
let searchTimeout;
async function onGlobalSearch(val) {
  clearTimeout(searchTimeout);
  if (!val.trim()) {
    if (state.currentView === 'prompts') loadPrompts();
    return;
  }
  searchTimeout = setTimeout(async () => {
    setView('prompts');
    const prompts = await api(`/prompts/?search=${encodeURIComponent(val)}`).catch(() => []);
    const grid = document.getElementById('prompts-grid');
    document.getElementById('prompts-view-title').textContent = `Resultados para "${val}"`;
    grid.innerHTML = prompts.length
      ? prompts.map(p => promptCard(p)).join('')
      : `<div class="empty-state" style="grid-column:1/-1;"><p>Sin resultados para "${escHtml(val)}"</p></div>`;
  }, 300);
}

// ── MODALS ────────────────────────────────────────────────
function openModal(id) {
  document.getElementById(id).classList.add('open');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}
// Close on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
});

// ── UTILS ─────────────────────────────────────────────────
function escHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function escJs(str) {
  return String(str||'').replace(/\\/g,'\\\\').replace(/`/g,'\\`').replace(/\$/g,'\\$');
}
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('es-ES', { day:'2-digit', month:'short', year:'numeric' });
}
function scoreColor(score) {
  if (score >= 90) return '#10b981';
  if (score >= 75) return '#6ee7b7';
  if (score >= 60) return '#fbbf24';
  if (score >= 40) return '#f97316';
  return '#ef4444';
}

// ── BOOT ──────────────────────────────────────────────────
init();
