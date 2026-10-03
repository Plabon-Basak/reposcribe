let currentAnalysis = null;
let currentReadme = null;

const repoUrlInput = document.getElementById('repo-url');
const analyzeBtn = document.getElementById('analyze-btn');
const generateBtn = document.getElementById('generate-btn');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');

const inputSection = document.getElementById('input-section');
const analysisSection = document.getElementById('analysis-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const qualitySection = document.getElementById('quality-section');

const errorDiv = document.getElementById('error');
const analysisContent = document.getElementById('analysis-content');
const loadingText = document.getElementById('loading-text');
const copyStatus = document.getElementById('copy-status');

const markdownOutput = document.getElementById('markdown-output');
const previewContent = document.getElementById('preview-content');

const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

function showError(msg) {
    errorDiv.textContent = msg;
}

function clearError() {
    errorDiv.textContent = '';
}

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(tc => tc.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(`${tab.dataset.tab}-tab`).classList.add('active');
        if (tab.dataset.tab === 'preview') {
            renderPreview();
        }
    });
});

function renderPreview() {
    if (!currentReadme) {
        previewContent.innerHTML = '';
        return;
    }
    if (typeof marked !== 'undefined') {
        previewContent.innerHTML = marked.parse(currentReadme);
        if (typeof DOMPurify !== 'undefined') {
            previewContent.innerHTML = DOMPurify.sanitize(previewContent.innerHTML);
        }
    } else {
        previewContent.textContent = currentReadme;
    }
}

analyzeBtn.addEventListener('click', async () => {
    clearError();
    const url = repoUrlInput.value.trim();
    if (!url) {
        showError('Please enter a GitHub repository URL.');
        return;
    }

    analysisSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    qualitySection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    loadingText.textContent = 'Analyzing repository...';

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await res.json();
        loadingSection.classList.add('hidden');
        if (!res.ok) {
            showError(data.error || 'Analysis failed.');
            return;
        }
        currentAnalysis = data.analysis;
        displayAnalysis(currentAnalysis);
        analysisSection.classList.remove('hidden');
    } catch (e) {
        loadingSection.classList.add('hidden');
        showError('Analysis failed. Please try again.');
    }
});

function displayAnalysis(analysis) {
    let html = '<ul>';
    html += `<li><strong>Name:</strong> ${escapeHtml(analysis.name || 'N/A')}</li>`;
    html += `<li><strong>Owner/Repo:</strong> ${escapeHtml(analysis.owner || '')}/${escapeHtml(analysis.repo || '')}</li>`;
    html += `<li><strong>Description:</strong> ${escapeHtml(analysis.description || 'N/A')}</li>`;
    html += `<li><strong>Default Branch:</strong> ${escapeHtml(analysis.default_branch || 'main')}</li>`;
    html += `<li><strong>Language:</strong> ${escapeHtml(analysis.language || 'N/A')}</li>`;
    html += `<li><strong>Languages:</strong> ${(analysis.languages || []).map(escapeHtml).join(', ') || 'N/A'}</li>`;
    html += `<li><strong>Topics:</strong> ${(analysis.topics || []).map(escapeHtml).join(', ') || 'N/A'}</li>`;
    html += `<li><strong>Important Files:</strong> ${(analysis.important_files || []).map(escapeHtml).join(', ') || 'N/A'}</li>`;
    html += `<li><strong>Structure (first 100):</strong> ${(analysis.structure || []).map(escapeHtml).join(', ') || 'N/A'}</li>`;
    html += '</ul>';
    analysisContent.innerHTML = html;
}

generateBtn.addEventListener('click', async () => {
    if (!currentAnalysis) return;
    analysisSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    qualitySection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    loadingText.textContent = 'Generating README with Gemma...';
    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ analysis: currentAnalysis })
        });
        const data = await res.json();
        loadingSection.classList.add('hidden');
        if (!res.ok) {
            showError(data.error || 'README generation failed.');
            return;
        }
        currentReadme = data.readme;
        markdownOutput.value = currentReadme;
        resultSection.classList.remove('hidden');
        const previewTab = document.querySelector('.tab[data-tab="preview"]');
        previewTab.click();
    } catch (e) {
        loadingSection.classList.add('hidden');
        showError('README generation failed. Please try again.');
    }
});

copyBtn.addEventListener('click', async () => {
    if (!currentReadme) return;
    try {
        await navigator.clipboard.writeText(currentReadme);
        copyStatus.textContent = 'Copied!';
        setTimeout(() => copyStatus.textContent = '', 2000);
    } catch (e) {
        copyStatus.textContent = 'Copy failed';
        setTimeout(() => copyStatus.textContent = '', 2000);
    }
});

downloadBtn.addEventListener('click', async () => {
    if (!currentReadme) return;
    try {
        const res = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ readme: currentReadme })
        });
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'README.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error('Download failed', e);
    }
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
"