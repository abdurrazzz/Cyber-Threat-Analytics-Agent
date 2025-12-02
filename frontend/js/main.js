// Main Application Logic

let currentHostData = null;

// DOM Elements
const loadSampleBtn = document.getElementById('load-sample-btn');
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');
const analyzeBtn = document.getElementById('analyze-btn');
const summaryTypeSelect = document.getElementById('summary-type');
const retryBtn = document.getElementById('retry-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkAPIHealth();
});

// Initialize Event Listeners
function initializeEventListeners() {
    loadSampleBtn.addEventListener('click', handleLoadSample);
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    analyzeBtn.addEventListener('click', handleAnalyze);
    retryBtn.addEventListener('click', handleRetry);
}

// Check API Health
async function checkAPIHealth() {
    try {
        const health = await api.healthCheck();
        console.log('API Health:', health);
    } catch (error) {
        console.error('API is not available:', error);
        showError('Unable to connect to the backend API. Please ensure the Flask server is running.');
    }
}

// Handle Load Sample Data
async function handleLoadSample() {
    try {
        clearError();
        loadSampleBtn.disabled = true;
        loadSampleBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        
        const data = await api.getSampleData();
        currentHostData = data.hosts;
        
        displayDataPreview(currentHostData);
        
        loadSampleBtn.disabled = false;
        loadSampleBtn.innerHTML = '<i class="fas fa-database"></i> Load Sample Data';
    } catch (error) {
        loadSampleBtn.disabled = false;
        loadSampleBtn.innerHTML = '<i class="fas fa-database"></i> Load Sample Data';
        showError('Failed to load sample data: ' + error.message);
    }
}

// Handle File Upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    try {
        clearError();
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        
        const data = await api.uploadFile(file);
        currentHostData = data.hosts;
        
        displayDataPreview(currentHostData);
        
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-file-upload"></i> Upload JSON File';
        
        // Reset file input
        fileInput.value = '';
    } catch (error) {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-file-upload"></i> Upload JSON File';
        fileInput.value = '';
        showError('Failed to upload file: ' + error.message);
    }
}

// Display Data Preview
function displayDataPreview(hosts) {
    const previewSection = document.querySelector('.preview-section');
    const dataPreview = document.getElementById('data-preview');
    const hostCount = document.getElementById('host-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    // Clear previous preview
    dataPreview.innerHTML = '';
    
    // Show only first 5 hosts for preview
    const previewHosts = hosts.slice(0, 5);
    
    previewHosts.forEach((host, index) => {
        dataPreview.appendChild(createHostPreview(host, index));
    });
    
    if (hosts.length > 5) {
        const moreDiv = document.createElement('div');
        moreDiv.style.textAlign = 'center';
        moreDiv.style.padding = '10px';
        moreDiv.style.color = '#6c757d';
        moreDiv.textContent = `... and ${hosts.length - 5} more hosts`;
        dataPreview.appendChild(moreDiv);
    }
    
    hostCount.textContent = `${hosts.length} host${hosts.length !== 1 ? 's' : ''}`;
    analyzeBtn.style.display = 'block';
    previewSection.style.display = 'block';
    
    // Hide results section
    hideSection('results-section');
    
    // Scroll to preview
    setTimeout(() => scrollToElement(previewSection), 100);
}

// Handle Analyze
async function handleAnalyze() {
    if (!currentHostData || currentHostData.length === 0) {
        showError('No host data available to analyze');
        return;
    }
    
    try {
        clearError();
        
        // Hide preview and show loading
        hideSection('preview-section');
        hideSection('results-section');
        showSection('loading-section');
        
        // Scroll to loading section
        const loadingSection = document.querySelector('.loading-section');
        scrollToElement(loadingSection);
        
        // Get summary type
        const summaryType = summaryTypeSelect.value;
        
        // Call API
        const result = await api.summarizeHosts(currentHostData, summaryType);
        
        // Display results
        displayResults(result);
        
        // Hide loading and show results
        hideSection('loading-section');
        showSection('results-section');
        
        // Scroll to results
        const resultsSection = document.querySelector('.results-section');
        setTimeout(() => scrollToElement(resultsSection), 100);
        
    } catch (error) {
        hideSection('loading-section');
        showError('Analysis failed: ' + error.message);
    }
}

// Display Results
function displayResults(result) {
    // Summary - render markdown
    const summaryContent = document.getElementById('summary-content');
    summaryContent.innerHTML = marked.parse(result.summary);
    
    // Key Insights
    const insightsList = document.getElementById('insights-list');
    insightsList.innerHTML = '';
    
    if (result.key_insights && result.key_insights.length > 0) {
        result.key_insights.forEach(insight => {
            const li = document.createElement('li');
            // Render markdown in insights too
            li.innerHTML = marked.parse(insight);
            insightsList.appendChild(li);
        });
    }
    
    // Risk Assessment - render markdown
    const riskAssessment = document.getElementById('risk-assessment');
    riskAssessment.innerHTML = marked.parse(result.risk_assessment || 'No specific risks identified');
    
    // Statistics
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '';
    
    if (result.stats) {
        statsContent.appendChild(createStatsCards(result.stats));
    }
    
    // Metadata
    const processingTime = document.getElementById('processing-time');
    const timestamp = document.getElementById('analysis-timestamp');
    
    if (result.processing_time) {
        processingTime.textContent = `Processed in ${formatProcessingTime(result.processing_time)}`;
    }
    
    if (result.timestamp) {
        timestamp.textContent = formatTimestamp(result.timestamp);
    }
}

// Handle Retry
function handleRetry() {
    clearError();
    
    if (currentHostData) {
        showSection('preview-section');
    }
}