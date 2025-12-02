// Utility Functions

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Format processing time
function formatProcessingTime(seconds) {
    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(0)}ms`;
    }
    return `${seconds.toFixed(2)}s`;
}

// Create host preview HTML
function createHostPreview(host, index) {
    const hostDiv = document.createElement('div');
    hostDiv.className = 'host-item';
    
    const details = [];
    
    // Add ports
    if (host.ports && host.ports.length > 0) {
        details.push(`<span><strong>Ports:</strong> ${host.ports.join(', ')}</span>`);
    }
    
    // Add protocols
    if (host.protocols && host.protocols.length > 0) {
        details.push(`<span><strong>Protocols:</strong> ${host.protocols.join(', ')}</span>`);
    }
    
    // Add location
    if (host.city && host.country) {
        details.push(`<span><strong>Location:</strong> ${host.city}, ${host.country}</span>`);
    } else if (host.country) {
        details.push(`<span><strong>Country:</strong> ${host.country}</span>`);
    }
    
    // Add organization
    if (host.organization) {
        details.push(`<span><strong>Org:</strong> ${host.organization}</span>`);
    }
    
    // Add hostname
    if (host.hostname) {
        details.push(`<span><strong>Hostname:</strong> ${host.hostname}</span>`);
    }
    
    // Add vulnerability count with color coding
    if (host.vulnerability_count > 0) {
        const vulnClass = host.has_critical_vulns ? 'critical-vuln' : 'has-vuln';
        details.push(`<span class="${vulnClass}"><strong>⚠️ Vulnerabilities:</strong> ${host.vulnerability_count}</span>`);
    }
    
    // Add malware detection
    if (host.malware_detected) {
        details.push(`<span class="malware-detected"><strong>🚨 Malware:</strong> ${host.malware_detected.name}</span>`);
    }
    
    // Add risk level badge
    let riskBadge = '';
    if (host.risk_level) {
        const riskClass = `risk-${host.risk_level}`;
        riskBadge = `<span class="risk-badge ${riskClass}">${host.risk_level.toUpperCase()} RISK</span>`;
    }
    
    hostDiv.innerHTML = `
        <div class="host-header">
            <div class="host-ip">${host.ip}</div>
            ${riskBadge}
        </div>
        <div class="host-details">
            ${details.join('')}
        </div>
    `;
    
    return hostDiv;
}

// Create statistics cards
function createStatsCards(stats) {
    const container = document.createElement('div');
    container.className = 'stats-grid';
    
    // Total hosts card
    const totalCard = document.createElement('div');
    totalCard.className = 'stat-card';
    totalCard.innerHTML = `
        <h4>Total Hosts</h4>
        <p>${stats.total_hosts || 0}</p>
    `;
    container.appendChild(totalCard);
    
    // Total vulnerabilities card
    if (stats.total_vulnerabilities !== undefined) {
        const vulnCard = document.createElement('div');
        vulnCard.className = 'stat-card stat-card-danger';
        vulnCard.innerHTML = `
            <h4>Total Vulnerabilities</h4>
            <p>${stats.total_vulnerabilities}</p>
        `;
        container.appendChild(vulnCard);
    }
    
    // Critical hosts card
    if (stats.critical_vulnerability_hosts !== undefined) {
        const criticalCard = document.createElement('div');
        criticalCard.className = 'stat-card stat-card-danger';
        criticalCard.innerHTML = `
            <h4>Critical Vulnerability Hosts</h4>
            <p>${stats.critical_vulnerability_hosts}</p>
        `;
        container.appendChild(criticalCard);
    }
    
    // Malware detected card
    if (stats.malware_detected_hosts !== undefined && stats.malware_detected_hosts > 0) {
        const malwareCard = document.createElement('div');
        malwareCard.className = 'stat-card stat-card-danger';
        malwareCard.innerHTML = `
            <h4>Malware Detected</h4>
            <p>${stats.malware_detected_hosts} host${stats.malware_detected_hosts !== 1 ? 's' : ''}</p>
        `;
        container.appendChild(malwareCard);
    }
    
    // Total services card
    if (stats.total_services !== undefined) {
        const servicesCard = document.createElement('div');
        servicesCard.className = 'stat-card';
        servicesCard.innerHTML = `
            <h4>Total Services</h4>
            <p>${stats.total_services}</p>
        `;
        container.appendChild(servicesCard);
    }
    
    // Countries card
    if (stats.top_countries && Object.keys(stats.top_countries).length > 0) {
        const countriesCard = document.createElement('div');
        countriesCard.className = 'stat-card';
        const countryList = Object.entries(stats.top_countries)
            .slice(0, 3)
            .map(([country, count]) => `<li><span>${country || 'Unknown'}</span><span>${count}</span></li>`)
            .join('');
        
        countriesCard.innerHTML = `
            <h4>Top Countries</h4>
            <ul class="stat-list">${countryList}</ul>
        `;
        container.appendChild(countriesCard);
    }
    
    // Organizations card
    if (stats.top_organizations && Object.keys(stats.top_organizations).length > 0) {
        const orgsCard = document.createElement('div');
        orgsCard.className = 'stat-card';
        const orgList = Object.entries(stats.top_organizations)
            .slice(0, 3)
            .map(([org, count]) => `<li><span>${org || 'Unknown'}</span><span>${count}</span></li>`)
            .join('');
        
        orgsCard.innerHTML = `
            <h4>Top Organizations</h4>
            <ul class="stat-list">${orgList}</ul>
        `;
        container.appendChild(orgsCard);
    }
    
    // Risk levels card
    if (stats.risk_levels && Object.keys(stats.risk_levels).length > 0) {
        const riskCard = document.createElement('div');
        riskCard.className = 'stat-card';
        const riskList = Object.entries(stats.risk_levels)
            .map(([level, count]) => {
                const riskClass = `risk-indicator-${level}`;
                return `<li class="${riskClass}"><span>${level.toUpperCase()}</span><span>${count}</span></li>`;
            })
            .join('');
        
        riskCard.innerHTML = `
            <h4>Risk Distribution</h4>
            <ul class="stat-list">${riskList}</ul>
        `;
        container.appendChild(riskCard);
    }
    
    return container;
}

// Show/hide sections
function showSection(sectionClass) {
    const section = document.querySelector(`.${sectionClass}`);
    if (section) {
        section.style.display = 'block';
    }
}

function hideSection(sectionClass) {
    const section = document.querySelector(`.${sectionClass}`);
    if (section) {
        section.style.display = 'none';
    }
}

// Show error
function showError(message) {
    const errorSection = document.querySelector('.error-section');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Hide other sections
    hideSection('loading-section');
    hideSection('results-section');
}

// Clear error
function clearError() {
    hideSection('error-section');
}

// Scroll to element
function scrollToElement(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}