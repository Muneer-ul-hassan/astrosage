/**
 * Plotly Configuration Utilities
 * 
 * This file contains utility functions for configuring Plotly charts
 * with consistent styling and behavior.
 */

// Default Plotly configuration options
const defaultPlotlyConfig = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: [
        'sendDataToCloud',
        'autoScale2d',
        'resetScale2d',
        'hoverClosestCartesian',
        'hoverCompareCartesian',
        'select2d',
        'lasso2d'
    ],
    toImageButtonOptions: {
        format: 'png',
        filename: 'exoplanet_chart',
        height: 500,
        width: 700,
        scale: 2
    }
};

// Apply dark theme to Plotly layout
function applyDarkTheme(layout) {
    const darkTheme = {
        font: {
            color: '#f5f5f5',
            family: 'sans-serif'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)',
            linecolor: 'rgba(255,255,255,0.2)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)',
            linecolor: 'rgba(255,255,255,0.2)'
        },
        legend: {
            bgcolor: 'rgba(0,0,0,0.2)',
            font: {
                color: '#f5f5f5'
            }
        }
    };
    
    // Merge the dark theme with the provided layout
    return {...darkTheme, ...layout};
}

// Create a scatter plot with consistent styling
function createExoplanetScatter(divId, data, layout) {
    Plotly.newPlot(
        divId, 
        data, 
        applyDarkTheme(layout), 
        defaultPlotlyConfig
    );
}

// Create a bar chart with consistent styling
function createExoplanetBarChart(divId, data, layout) {
    Plotly.newPlot(
        divId, 
        data, 
        applyDarkTheme(layout), 
        defaultPlotlyConfig
    );
}

// Create a timeline chart with consistent styling
function createExoplanetTimeline(divId, data, layout) {
    Plotly.newPlot(
        divId, 
        data, 
        applyDarkTheme(layout), 
        defaultPlotlyConfig
    );
}

// Format habitability score with color coding
function formatHabitabilityScore(score) {
    const formattedScore = score.toFixed(2);
    
    if (score >= 0.7) {
        return `<span class="habitability-high">${formattedScore}</span>`;
    } else if (score >= 0.4) {
        return `<span class="habitability-medium">${formattedScore}</span>`;
    } else {
        return `<span class="habitability-low">${formattedScore}</span>`;
    }
}