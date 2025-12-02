// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Service
const api = {
    // Health check
    async healthCheck() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    },

    // Get sample data
    async getSampleData() {
        try {
            const response = await fetch(`${API_BASE_URL}/sample-data`);
            const result = await response.json();
            return result.data;
        } catch (error) {
            console.error('Failed to fetch sample data:', error);
            throw error;
        }
    },

    // Upload file
    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Upload failed');
            }
            
            return result.data;
        } catch (error) {
            console.error('File upload failed:', error);
            throw error;
        }
    },

    // Summarize hosts
    async summarizeHosts(hosts, summaryType = 'detailed') {
        try {
            const response = await fetch(`${API_BASE_URL}/summarize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    hosts: hosts,
                    summary_type: summaryType
                })
            });

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Summarization failed');
            }
            
            return result.data;
        } catch (error) {
            console.error('Summarization failed:', error);
            throw error;
        }
    }
};