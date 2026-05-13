/* ════════════════════════════════════════════════════════════════
   main.js — HireAI Resume Screener
   Shared utilities for index.html and main.html
   Covers: theme toggle, drag-and-drop, score bar animation,
           candidate/history search filters, file clear
   ════════════════════════════════════════════════════════════════ */


/* ── THEME SYSTEM ────────────────────────────────────────────── */

/* Runs once at script load: restores saved theme preference */
(function initTheme() {
  const saved = localStorage.getItem('hireai-theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
  }
})();

function toggleTheme() {
  const html    = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next    = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('hireai-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeIcon');
  if (!icon) return;
  icon.className = theme === 'light' ? 'fas fa-sun' : 'fas fa-moon';
}


/* ── DRAG AND DROP FILE UPLOAD ───────────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {
  const dropZone  = document.getElementById('dropZone');
  const fileInput = document.getElementById('resumeFiles');
  if (!dropZone || !fileInput) return;   /* Only present on index.html */

  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', function () {
    dropZone.classList.remove('drag-over');
  });

  dropZone.addEventListener('drop', function (e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    fileInput.files = e.dataTransfer.files;
    handleFileSelection(fileInput.files);
  });

  fileInput.addEventListener('change', function () {
    handleFileSelection(this.files);
  });
});

/* Updates the visible file list after selection or drop */
function handleFileSelection(files) {
  const fileList     = document.getElementById('fileList');
  const fileCountBar = document.getElementById('fileCountBar');
  const fileCountTxt = document.getElementById('fileCountText');

  if (!fileList) return;
  fileList.innerHTML = '';

  const pdfs = Array.from(files).filter(function (f) {
    return f.type === 'application/pdf';
  });

  if (pdfs.length === 0) {
    fileList.innerHTML = '<p style="color:var(--score-low);font-size:.8rem;padding:6px 0;">Only PDF files are accepted.</p>';
    if (fileCountBar) fileCountBar.style.display = 'none';
    return;
  }

  pdfs.forEach(function (file) {
    const item = document.createElement('div');
    item.className = 'file-item';
    const size = file.size > 1048576
      ? (file.size / 1048576).toFixed(1) + ' MB'
      : (file.size / 1024).toFixed(0) + ' KB';
    item.innerHTML =
      '<span class="file-item-name"><i class="fas fa-file-pdf"></i> ' + file.name + '</span>' +
      '<span class="file-item-size">' + size + '</span>';
    fileList.appendChild(item);
  });

  if (fileCountBar) {
    fileCountBar.style.display = 'flex';
    fileCountTxt.textContent = pdfs.length + ' file' + (pdfs.length !== 1 ? 's' : '') + ' selected';
  }
}

/* Resets file input and clears visible list */
function clearFiles() {
  const fileInput    = document.getElementById('resumeFiles');
  const fileList     = document.getElementById('fileList');
  const fileCountBar = document.getElementById('fileCountBar');
  if (fileInput)    fileInput.value = '';
  if (fileList)     fileList.innerHTML = '';
  if (fileCountBar) fileCountBar.style.display = 'none';
}


/* ── SCORE BAR ANIMATION ──────────────────────────────────────── */

/* Animates score-bar-fill widths from 0% → target on page load */
function animateScoreBars() {
  document.querySelectorAll('.score-bar-fill').forEach(function (fill) {
    const target = fill.style.width;
    fill.style.width = '0%';
    setTimeout(function () { fill.style.width = target; }, 80);
  });
}


/* ── CANDIDATE SEARCH FILTER (results table) ─────────────────── */

function filterCandidates() {
  const query = document.getElementById('candidateSearch').value.toLowerCase();
  document.querySelectorAll('.candidate-row').forEach(function (row) {
    const name = row.getAttribute('data-name') || '';
    row.style.display = name.includes(query) ? '' : 'none';
  });
}


/* ── HISTORY SEARCH FILTER ────────────────────────────────────── */

function filterHistory() {
  const query = document.getElementById('historySearch').value.toLowerCase();
  document.querySelectorAll('.history-card').forEach(function (card) {
    const title = card.getAttribute('data-title') || '';
    card.style.display = title.includes(query) ? 'flex' : 'none';
  });
}
