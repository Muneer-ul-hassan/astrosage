/**
 * Exoplanet Visualization Functions
 * 
 * This file contains functions for creating and rendering visualizations
 * for exoplanet data using Plotly.js.
 */

// Create a visualization comparing an exoplanet to Earth
function createExoplanetComparison(exoplanetData, containerElement) {
    // Size comparison visualization
    const sizeComparisonDiv = document.createElement('div');
    sizeComparisonDiv.id = 'size-comparison-chart';
    sizeComparisonDiv.className = 'plotly-graph mb-4';
    containerElement.appendChild(sizeComparisonDiv);

    // Create size comparison data
    const sizeData = [{
        x: ['Earth', exoplanetData.name],
        y: [1, exoplanetData.size_comparison.earth_radius],
        type: 'bar',
        marker: {
            color: ['#3366cc', '#dc3912']
        }
    }];

    const sizeLayout = {
        title: 'Size Comparison (Earth Radius)',
        xaxis: {
            title: ''
        },
        yaxis: {
            title: 'Radius (Earth = 1)'
        }
    };

    // Apply dark theme and render
    createExoplanetBarChart('size-comparison-chart', sizeData, sizeLayout);

    // Temperature comparison visualization
    const tempComparisonDiv = document.createElement('div');
    tempComparisonDiv.id = 'temperature-comparison-chart';
    tempComparisonDiv.className = 'plotly-graph mb-4';
    containerElement.appendChild(tempComparisonDiv);

    // Create temperature comparison data
    const tempData = [{
        x: ['Earth', exoplanetData.name],
        y: [288, exoplanetData.eq_temperature || 0],
        type: 'bar',
        marker: {
            color: ['#3366cc', '#dc3912']
        }
    }];

    const tempLayout = {
        title: 'Temperature Comparison (Kelvin)',
        xaxis: {
            title: ''
        },
        yaxis: {
            title: 'Equilibrium Temperature (K)'
        }
    };

    // Apply dark theme and render
    createExoplanetBarChart('temperature-comparison-chart', tempData, tempLayout);

    // Habitability score gauge
    const habitabilityDiv = document.createElement('div');
    habitabilityDiv.id = 'habitability-gauge';
    habitabilityDiv.className = 'plotly-graph mb-4';
    containerElement.appendChild(habitabilityDiv);

    // Create gauge data
    const habitabilityData = [{
        type: 'indicator',
        mode: 'gauge+number',
        value: exoplanetData.habitability_score,
        title: { text: 'Habitability Score', font: { size: 24 } },
        gauge: {
            axis: { range: [null, 1], tickwidth: 1, tickcolor: '#f5f5f5' },
            bar: { color: '#48bb78' },
            bgcolor: 'transparent',
            borderwidth: 2,
            bordercolor: '#f5f5f5',
            steps: [
                { range: [0, 0.3], color: '#f56565' },
                { range: [0.3, 0.7], color: '#ecc94b' },
                { range: [0.7, 1], color: '#48bb78' }
            ]
        }
    }];

    const habitabilityLayout = {
        margin: { t: 40, r: 25, l: 25, b: 25 },
        font: { color: '#f5f5f5', family: 'sans-serif' }
    };

    // Apply dark theme and render
    Plotly.newPlot('habitability-gauge', habitabilityData, 
        applyDarkTheme(habitabilityLayout), defaultPlotlyConfig);
}

// Create a scatter plot of habitable exoplanets
function createHabitabilityScatterPlot(exoplanetsData, containerElement) {
    const scatterDiv = document.createElement('div');
    scatterDiv.id = 'habitability-scatter';
    scatterDiv.className = 'plotly-graph mb-4';
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
            size: 15,
            color: colors,
            opacity: 0.8,
            line: {
                color: '#ffffff',
                width: 1
            }
        },
        hovertemplate: '<b>%{text}</b><br>Radius: %{x} Earth<br>Temp: %{y} K<br>Habitability: %{marker.color}<extra></extra>'
    }];

    const scatterLayout = {
        title: 'Habitability by Planet Size and Temperature',
        xaxis: {
            title: 'Planet Radius (Earth = 1)'
        },
        yaxis: {
            title: 'Equilibrium Temperature (K)'
        },
        hovermode: 'closest'
    };

    // Add Earth reference point
    scatterData.push({
        x: [1],
        y: [288],
        text: ['Earth'],
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 15,
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
    createExoplanetScatter('habitability-scatter', scatterData, scatterLayout);
}

// Create a timeline visualization of exoplanet discoveries
function createDiscoveryTimeline(discoveriesData, containerElement) {
    const timelineDiv = document.createElement('div');
    timelineDiv.id = 'discovery-timeline';
    timelineDiv.className = 'plotly-graph mb-4';
    containerElement.appendChild(timelineDiv);

    // Sort discoveries by date
    const sortedDiscoveries = [...discoveriesData].sort((a, b) => 
        new Date(a.discovery_date) - new Date(b.discovery_date));

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
            size: 16,
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
        title: 'Recent Exoplanet Discoveries',
        xaxis: {
            title: 'Discovery Date'
        },
        yaxis: {
            title: 'Exoplanet Name',
            autorange: "reversed"
        },
        hovermode: 'closest'
    };

    // Create legend for discovery methods
    const uniqueMethods = [...new Set(methods)];

    if (uniqueMethods.length > 0) {
        // Add traces for the legend
        uniqueMethods.forEach(method => {
            timelineData.push({
                x: [null],
                y: [null],
                mode: 'markers',
                type: 'scatter',
                marker: {
                    size: 10,
                    color: methodColors[method] || '#dddddd'
                },
                name: method,
                showlegend: true
            });
        });
    }

    // Apply dark theme and render
    createExoplanetTimeline('discovery-timeline', timelineData, timelineLayout);
}

// Create visualizations
function createVisualizations(exoplanetsData) {
    const visualizationContainer = document.getElementById('visualization-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    if (visualizationContainer && exoplanetsData.length > 0) {
        createHabitabilityScatterPlot(exoplanetsData, visualizationContainer);
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    }
}