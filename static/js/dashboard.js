/**
 * Dashboard.js - Functions for the Exoplanet Discovery Dashboard
 * 
 * This file contains specialized functions for the dashboard interface,
 * including data processing, chart creation, and UI interactions.
 */

// Dashboard-specific visualization functions

/**
 * Create a compact version of the habitability scatter plot for the dashboard
 * @param {Array} exoplanetsData - Array of exoplanet data objects
 * @param {HTMLElement} containerElement - Container element to render the visualization
 */
function createDashboardHabitabilityPlot(exoplanetsData, containerElement) {
    const scatterDiv = document.createElement('div');
    scatterDiv.id = 'dashboard-habitability-scatter';
    scatterDiv.className = 'plotly-graph';
    containerElement.innerHTML = '';
    containerElement.appendChild(scatterDiv);

    // Extract data for plotting
    const names = exoplanetsData.map(planet => planet.name);
    const habitabilityScores = exoplanetsData.map(planet => planet.habitability_score);
    const earthRadii = exoplanetsData.map(planet => planet.earth_radius || 0);
    const temperatures = exoplanetsData.map(planet => planet.eq_temperature || 0);

    // Colors based on habitability score
    const colors = habitabilityScores.map(score => {
        if (score >= 0.7) return '#48bb78';
        else if (score >= 0.4) return '#ecc94b';
        else return '#f56565';
    });

    // Create scatter plot data
    const scatterData = [{
        x: earthRadii,
        y: temperatures,
        text: names,
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 12,
            color: colors,
            opacity: 0.8,
            line: {
                color: '#ffffff',
                width: 1
            }
        },
        hovertemplate: '<b>%{text}</b><br>Radius: %{x} Earth<br>Temp: %{y} K<extra></extra>'
    }];

    const scatterLayout = {
        height: 300,
        xaxis: {
            title: 'Planet Radius (Earth = 1)'
        },
        yaxis: {
            title: 'Temperature (K)'
        },
        hovermode: 'closest',
        margin: { t: 10, r: 10, b: 50, l: 50 }
    };

    // Add Earth reference point
    scatterData.push({
        x: [1],
        y: [288],
        text: ['Earth'],
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 12,
            color: '#3366cc',
            symbol: 'star',
            opacity: 1,
            line: {
                color: '#ffffff',
                width: 2
            }
        },
        hovertemplate: '<b>Earth</b><br>Our home planet<extra></extra>'
    });

    // Apply dark theme and render
    Plotly.newPlot('dashboard-habitability-scatter', scatterData, 
                 applyDarkTheme(scatterLayout), defaultPlotlyConfig);
}

/**
 * Create a compact version of the discovery timeline for the dashboard
 * @param {Array} discoveriesData - Array of exoplanet discovery data objects
 * @param {HTMLElement} containerElement - Container element to render the visualization
 */
function createDashboardTimeline(discoveriesData, containerElement) {
    const timelineDiv = document.createElement('div');
    timelineDiv.id = 'dashboard-timeline';
    timelineDiv.className = 'plotly-graph';
    containerElement.innerHTML = '';
    containerElement.appendChild(timelineDiv);

    // Sort discoveries by date and limit to 5 most recent
    const sortedDiscoveries = [...discoveriesData]
        .sort((a, b) => new Date(b.discovery_date) - new Date(a.discovery_date))
        .slice(0, 5);

    // Extract data for plotting
    const dates = sortedDiscoveries.map(planet => planet.discovery_date);
    const names = sortedDiscoveries.map(planet => planet.name);
    const methods = sortedDiscoveries.map(planet => planet.discovery_method);

    // Create color mapping for discovery methods
    const methodColors = {
        'Transit': '#3366cc',
        'Radial Velocity': '#dc3912',
        'Direct Imaging': '#ff9900',
        'Gravitational Microlensing': '#109618',
        'Timing Variations': '#990099',
        'Astrometry': '#0099c6'
    };

    // Create colors array based on discovery method
    const colors = methods.map(method => methodColors[method] || '#dddddd');

    // Create timeline data
    const timelineData = [{
        x: dates,
        y: names,
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 14,
            color: colors,
            symbol: 'circle',
            opacity: 0.8,
            line: {
                color: '#ffffff',
                width: 1
            }
        },
        text: methods,
        hovertemplate: '<b>%{y}</b><br>Discovered: %{x}<br>Method: %{text}<extra></extra>'
    }];

    const timelineLayout = {
        height: 250,
        xaxis: {
            title: 'Discovery Date'
        },
        yaxis: {
            title: 'Exoplanet',
            autorange: "reversed"
        },
        hovermode: 'closest',
        margin: { t: 10, r: 10, b: 50, l: 100 }
    };

    // Apply dark theme and render
    Plotly.newPlot('dashboard-timeline', timelineData, 
                 applyDarkTheme(timelineLayout), defaultPlotlyConfig);
}

/**
 * Format a habitability score with color coding
 * @param {number} score - Habitability score (0-1)
 * @returns {string} HTML string with formatted score
 */
function formatHabitabilityScoreWithIcon(score) {
    let colorClass = '';
    let icon = '';

    if (score >= 0.8) {
        colorClass = 'text-success';
        icon = 'check-circle';
    } else if (score >= 0.6) {
        colorClass = 'text-info';
        icon = 'check';
    } else if (score >= 0.4) {
        colorClass = 'text-warning';
        icon = 'alert-circle';
    } else {
        colorClass = 'text-danger';
        icon = 'x-circle';
    }

    return `<span class="${colorClass}">
              <i data-feather="${icon}" class="feather-sm me-1"></i>
              ${score.toFixed(2)}
            </span>`;
}

/**
 * Create a small stats card for the dashboard
 * @param {string} title - Card title
 * @param {string|number} value - Value to display
 * @param {string} icon - Feather icon name
 * @param {string} colorClass - Bootstrap color class
 * @returns {HTMLElement} The created card element
 */
function createStatsCard(title, value, icon, colorClass) {
    const card = document.createElement('div');
    card.className = 'card mb-3';

    card.innerHTML = `
        <div class="card-body p-3">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="small text-muted">${title}</div>
                    <div class="fs-4 fw-bold ${colorClass}">${value}</div>
                </div>
                <div class="${colorClass} bg-opacity-10 p-3 rounded">
                    <i data-feather="${icon}"></i>
                </div>
            </div>
        </div>
    `;

    return card;
}

/**
 * Update dashboard metrics with the latest data
 * This function will be called periodically to refresh dashboard data
 */
function updateDashboardMetrics() {
    // This would normally fetch fresh data from the API
    // For the prototype, we'll simulate with static data

    document.getElementById('total-exoplanets').textContent = '5,000+';
    document.getElementById('habitable-exoplanets').textContent = '7';
    document.getElementById('recent-discoveries').textContent = '10';

    // Update last refresh time
    document.getElementById('last-refresh').textContent = 
        new Date().toLocaleTimeString();
}

// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const discoveryFilter = document.getElementById('discovery-method-filter');
    const habitabilityFilter = document.getElementById('habitability-filter');

    function filterExoplanets() {
        const searchTerm = searchInput.value.toLowerCase();
        const discoveryMethod = discoveryFilter.value;
        const habitabilityScore = habitabilityFilter.value;

        fetch('/api/exoplanets/habitable')
            .then(response => response.json())
            .then(exoplanets => {
                const filtered = exoplanets.filter(planet => {
                    const matchesSearch = planet.name.toLowerCase().includes(searchTerm);
                    const matchesMethod = !discoveryMethod || planet.discovery_method === discoveryMethod;

                    let matchesHabitability = true;
                    if (habitabilityScore === 'high') {
                        matchesHabitability = planet.habitability_score > 0.8;
                    } else if (habitabilityScore === 'medium') {
                        matchesHabitability = planet.habitability_score >= 0.5 && planet.habitability_score <= 0.8;
                    } else if (habitabilityScore === 'low') {
                        matchesHabitability = planet.habitability_score < 0.5;
                    }

                    return matchesSearch && matchesMethod && matchesHabitability;
                });

                updateResults(filtered);
            });
    }

    function updateResults(planets) {
        const container = document.getElementById('exoplanet-results');
        if (!container) return;

        container.innerHTML = planets.map(planet => `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${planet.name}</h5>
                        <p class="card-text">
                            Habitability Score: ${planet.habitability_score.toFixed(2)}
                        </p>
                        <a href="/exoplanet/${planet.name}" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Add event listeners
    searchInput.addEventListener('input', filterExoplanets);
    discoveryFilter.addEventListener('change', filterExoplanets);
    habitabilityFilter.addEventListener('change', filterExoplanets);

    // Initial load
    filterExoplanets();
    
    // Load exoplanet options for comparison tool
    fetch('/api/exoplanets/habitable')
        .then(response => response.json())
        .then(exoplanets => {
            const select1 = document.getElementById('exoplanet1-select');
            const select2 = document.getElementById('exoplanet2-select');
            
            // Clear existing options except the first default one
            select1.innerHTML = '<option value="">Select first exoplanet...</option>';
            select2.innerHTML = '<option value="">Select second exoplanet...</option>';
            
            // Add hardcoded planets for now (since API might not return all)
            const planets = [
                "Kepler-186f",
                "Teegarden's Star b",
                "K2-18b",
                "GJ 357 d",
                "Proxima b",
                "TRAPPIST-1e",
                "TOI-700 d"
            ];
            
            planets.forEach(planetName => {
                const option = document.createElement('option');
                option.value = planetName;
                option.textContent = planetName;
                select1.appendChild(option.cloneNode(true));
                select2.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading exoplanets:', error);
        });

    // Handle comparison
    const compareButton = document.getElementById('compare-button');
    if (compareButton) {
        compareButton.addEventListener('click', async () => {
            const planet1Name = document.getElementById('exoplanet1-select').value;
            const planet2Name = document.getElementById('exoplanet2-select').value;
            
            if (!planet1Name || !planet2Name) {
                alert('Please select two exoplanets to compare');
                return;
            }

            const resultsDiv = document.getElementById('comparison-results');
            resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-info"></div></div>';

            try {
                const [planet1Data, planet2Data] = await Promise.all([
                    fetch(`/api/exoplanet/${encodeURIComponent(planet1Name)}`).then(r => r.json()),
                    fetch(`/api/exoplanet/${encodeURIComponent(planet2Name)}`).then(r => r.json())
                ]);

                const comparisonHtml = `
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Characteristic</th>
                                    <th>${planet1Data.name}</th>
                                    <th>${planet2Data.name}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Size (Earth Radii)</td>
                                    <td>${planet1Data.size_comparison.earth_radius}</td>
                                    <td>${planet2Data.size_comparison.earth_radius}</td>
                                </tr>
                                <tr>
                                    <td>Temperature (K)</td>
                                    <td>${planet1Data.size_comparison.earth_temperature}</td>
                                    <td>${planet2Data.size_comparison.earth_temperature}</td>
                                </tr>
                                <tr>
                                    <td>Distance (Light Years)</td>
                                    <td>${planet1Data.distance || 'Unknown'}</td>
                                    <td>${planet2Data.distance || 'Unknown'}</td>
                                </tr>
                                <tr>
                                    <td>Habitability Score</td>
                                    <td>${planet1Data.habitability_score.toFixed(2)}</td>
                                    <td>${planet2Data.habitability_score.toFixed(2)}</td>
                                </tr>
                                <tr>
                                    <td>Discovery Method</td>
                                    <td>${planet1Data.discovery_method}</td>
                                    <td>${planet2Data.discovery_method}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                `;
                
                resultsDiv.innerHTML = comparisonHtml;
            } catch (error) {
                resultsDiv.innerHTML = '<div class="alert alert-danger">Error loading comparison data</div>';
                console.error('Error comparing exoplanets:', error);
            }
        });
    }
});