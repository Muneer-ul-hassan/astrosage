import io
import base64
import logging
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List

from models.exoplanet import ExoplanetDetail, HabitableExoplanet, TimelineExoplanet

# Set matplotlib to use a non-interactive backend
matplotlib.use('Agg')

# Configure logging
logger = logging.getLogger(__name__)

def generate_exoplanet_comparison_plot(exoplanet: ExoplanetDetail) -> str:
    """
    Generate an HTML page with both Matplotlib and Plotly visualizations comparing 
    the exoplanet to Earth.
    
    Args:
        exoplanet: Exoplanet details
    
    Returns:
        HTML content string with embedded visualizations
    """
    logger.debug(f"Generating comparison plot for exoplanet: {exoplanet.name}")
    
    # Create Matplotlib figure comparing to Earth
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart comparing size, temperature, and distance to Earth
    categories = ["Size (Earth Radii)", "Temperature (K)", "Distance (Light Years)"]
    values = [
        exoplanet.size_comparison["earth_radius"],
        exoplanet.size_comparison["earth_temperature"],
        exoplanet.size_comparison["earth_distance"]
    ]
    
    # Normalize values for better visualization
    normalized_values = [
        values[0],  # Earth radius (already a ratio)
        values[1]/288,  # Temperature relative to Earth's average (288K)
        min(1, 10/values[2])  # Distance (inversely related to habitability)
    ]
    
    # Earth comparison values (normalized)
    earth_values = [1.0, 1.0, 1.0]
    
    # Create bar chart
    x = range(len(categories))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], normalized_values, width, label=exoplanet.name)
    ax.bar([i + width/2 for i in x], earth_values, width, label='Earth')
    
    ax.set_ylabel('Normalized Value')
    ax.set_title(f'Comparison of {exoplanet.name} to Earth')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    plt.tight_layout()
    
    # Save the Matplotlib figure to a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    # Create a Plotly radar chart for comparison
    plotly_fig = go.Figure()
    
    # Categories for radar chart
    radar_categories = ["Size", "Temperature", "Distance", "Habitability"]
    
    # Values for the exoplanet
    radar_values_exoplanet = [
        exoplanet.size_comparison["earth_radius"],
        exoplanet.size_comparison["earth_temperature"]/288,  # Normalized to Earth's temp
        min(1, 10/exoplanet.size_comparison["earth_distance"]),  # Inverse of distance (closer is better)
        exoplanet.habitability_score
    ]
    
    # Values for Earth (reference)
    radar_values_earth = [1, 1, 1, 1]
    
    # Add radar chart traces
    plotly_fig.add_trace(go.Scatterpolar(
        r=radar_values_exoplanet,
        theta=radar_categories,
        fill='toself',
        name=exoplanet.name
    ))
    
    plotly_fig.add_trace(go.Scatterpolar(
        r=radar_values_earth,
        theta=radar_categories,
        fill='toself',
        name='Earth'
    ))
    
    # Update layout
    plotly_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(radar_values_exoplanet), 1) * 1.2]
            )
        ),
        title=f"Comparison of {exoplanet.name} to Earth",
        template="plotly_dark"  # Use dark theme
    )
    
    # Create the combined HTML response with both visualizations
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{exoplanet.name} - Exoplanet Comparison</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link href="/static/css/custom.css" rel="stylesheet">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body data-bs-theme="dark">
        <div class="container mt-4">
            <h1>{exoplanet.name} Details</h1>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h3>Overview</h3>
                        </div>
                        <div class="card-body">
                            <p><strong>Distance:</strong> {exoplanet.distance if exoplanet.distance else "Unknown"} light years</p>
                            <p><strong>Habitability Score:</strong> {exoplanet.habitability_score:.2f}</p>
                            <p><strong>Size:</strong> {exoplanet.size_comparison["earth_radius"]:.2f} Earth radii</p>
                            <p><strong>Temperature:</strong> {exoplanet.size_comparison["earth_temperature"]} K</p>
                            <p><strong>Orbital Period:</strong> {exoplanet.orbital_period}</p>
                            <p><strong>Discovery Method:</strong> {exoplanet.discovery_method}</p>
                            <p><strong>Discovery Year:</strong> {exoplanet.discovery_year if exoplanet.discovery_year else "Unknown"}</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h3>Comparison to Earth</h3>
                        </div>
                        <div class="card-body d-flex justify-content-center">
                            <img src="data:image/png;base64,{img_str}" class="img-fluid" alt="Exoplanet Comparison">
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Interactive Comparison</h3>
                        </div>
                        <div class="card-body">
                            <div id="plotly-chart" style="height: 500px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4 mb-4">
                <div class="col-12">
                    <a href="/" class="btn btn-primary">Back to Home</a>
                </div>
            </div>
        </div>
        
        <script>
            // Create interactive Plotly chart
            const plotlyData = {plotly_fig.to_json()};
            Plotly.newPlot('plotly-chart', plotlyData.data, plotlyData.layout);
        </script>
    </body>
    </html>
    """
    
    return html_content

def generate_habitability_scatter_plot(exoplanets: List[HabitableExoplanet]) -> str:
    """
    Generate an HTML page with Plotly visualizations of habitable exoplanets.
    
    Args:
        exoplanets: List of habitable exoplanets
    
    Returns:
        HTML content string with embedded visualizations
    """
    logger.debug(f"Generating habitability scatter plot for {len(exoplanets)} exoplanets")
    
    if not exoplanets:
        return "<h1>No habitable exoplanets found</h1>"
    
    # Create a scatter plot of habitability scores vs. distance
    names = [planet.name for planet in exoplanets]
    habitability_scores = [planet.habitability_score for planet in exoplanets]
    distances = [planet.distance if planet.distance else 1000 for planet in exoplanets]  # Default large distance if unknown
    sizes = [planet.earth_radius * 10 if planet.earth_radius else 5 for planet in exoplanets]  # Scale point size
    
    # Create Plotly figure
    fig = px.scatter(
        x=distances,
        y=habitability_scores,
        size=sizes,
        hover_name=names,
        labels={
            "x": "Distance (Light Years)",
            "y": "Habitability Score",
            "size": "Planet Size (Earth Radii)"
        },
        title="Habitability Score vs. Distance from Earth",
        color=habitability_scores,
        color_continuous_scale=px.colors.sequential.Viridis,
        template="plotly_dark"
    )
    
    fig.update_layout(
        xaxis_title="Distance from Earth (Light Years)",
        yaxis_title="Habitability Score (0-1)",
        coloraxis_colorbar_title="Habitability Score"
    )
    
    # Create another visualization: Bubble chart with size and temperature
    sizes = [planet.earth_radius if planet.earth_radius else 1 for planet in exoplanets]
    temperatures = [planet.eq_temperature if planet.eq_temperature else 300 for planet in exoplanets]
    
    bubble_fig = px.scatter(
        x=temperatures,
        y=sizes,
        size=habitability_scores,
        hover_name=names,
        size_max=25,
        labels={
            "x": "Equilibrium Temperature (K)",
            "y": "Planet Size (Earth Radii)",
            "size": "Habitability Score"
        },
        title="Exoplanet Size vs. Temperature",
        color=habitability_scores,
        color_continuous_scale=px.colors.sequential.Viridis,
        template="plotly_dark"
    )
    
    bubble_fig.update_layout(
        xaxis_title="Equilibrium Temperature (K)",
        yaxis_title="Planet Size (Earth Radii)",
        coloraxis_colorbar_title="Habitability Score"
    )
    
    # Create the HTML response
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Habitable Exoplanets</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link href="/static/css/custom.css" rel="stylesheet">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body data-bs-theme="dark">
        <div class="container mt-4">
            <h1>Potentially Habitable Exoplanets</h1>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Habitability vs. Distance</h3>
                        </div>
                        <div class="card-body">
                            <div id="scatter-plot" style="height: 600px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Size vs. Temperature</h3>
                        </div>
                        <div class="card-body">
                            <div id="bubble-chart" style="height: 600px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Top Habitable Exoplanets</h3>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Habitability Score</th>
                                            <th>Distance (Light Years)</th>
                                            <th>Size (Earth Radii)</th>
                                            <th>Temperature (K)</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {''.join([f"<tr><td>{planet.name}</td><td>{planet.habitability_score:.2f}</td><td>{planet.distance if planet.distance else 'Unknown'}</td><td>{planet.earth_radius if planet.earth_radius else 'Unknown'}</td><td>{planet.eq_temperature if planet.eq_temperature else 'Unknown'}</td><td><a href='/exoplanet/{planet.name}' class='btn btn-sm btn-primary'>Details</a></td></tr>" for planet in exoplanets[:10]])}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4 mb-4">
                <div class="col-12">
                    <a href="/" class="btn btn-primary">Back to Home</a>
                </div>
            </div>
        </div>
        
        <script>
            // Create scatter plot
            const scatterData = {fig.to_json()};
            Plotly.newPlot('scatter-plot', scatterData.data, scatterData.layout);
            
            // Create bubble chart
            const bubbleData = {bubble_fig.to_json()};
            Plotly.newPlot('bubble-chart', bubbleData.data, bubbleData.layout);
        </script>
    </body>
    </html>
    """
    
    return html_content

def generate_discovery_timeline_plot(exoplanets: List[TimelineExoplanet]) -> str:
    """
    Generate an HTML page with Plotly visualizations of exoplanet discovery timeline.
    
    Args:
        exoplanets: List of exoplanets with discovery dates
    
    Returns:
        HTML content string with embedded visualizations
    """
    logger.debug(f"Generating discovery timeline for {len(exoplanets)} exoplanets")
    
    if not exoplanets:
        return "<h1>No recent exoplanet discoveries found</h1>"
    
    # Extract data for timeline
    names = [planet.name for planet in exoplanets]
    dates = [planet.discovery_date for planet in exoplanets]
    methods = [planet.discovery_method for planet in exoplanets]
    
    # Create a timeline visualization using Plotly
    fig = px.timeline(
        x_start=dates,
        y=names,
        color=methods,
        labels={
            "x_start": "Discovery Date",
            "y": "Exoplanet",
            "color": "Discovery Method"
        },
        title="Recent Exoplanet Discoveries Timeline",
        template="plotly_dark"
    )
    
    fig.update_layout(
        xaxis_title="Discovery Date",
        yaxis_title="Exoplanet",
        height=max(500, len(exoplanets) * 25)  # Adjust height based on number of planets
    )
    
    # Create a bar chart of discovery methods
    method_counts = {}
    for method in methods:
        if method in method_counts:
            method_counts[method] += 1
        else:
            method_counts[method] = 1
    
    methods_bar = px.bar(
        x=list(method_counts.keys()),
        y=list(method_counts.values()),
        labels={
            "x": "Discovery Method",
            "y": "Number of Exoplanets"
        },
        title="Exoplanet Discovery Methods",
        template="plotly_dark"
    )
    
    methods_bar.update_layout(
        xaxis_title="Discovery Method",
        yaxis_title="Number of Exoplanets"
    )
    
    # Create the HTML response
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Exoplanet Discovery Timeline</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link href="/static/css/custom.css" rel="stylesheet">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body data-bs-theme="dark">
        <div class="container mt-4">
            <h1>Recent Exoplanet Discoveries</h1>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Discovery Timeline</h3>
                        </div>
                        <div class="card-body">
                            <div id="timeline-chart" style="height: 600px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Discovery Methods</h3>
                        </div>
                        <div class="card-body">
                            <div id="methods-chart" style="height: 400px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h3>Recent Discoveries</h3>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Discovery Date</th>
                                            <th>Discovery Method</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {''.join([f"<tr><td>{planet.name}</td><td>{planet.discovery_date}</td><td>{planet.discovery_method}</td><td><a href='/exoplanet/{planet.name}' class='btn btn-sm btn-primary'>Details</a></td></tr>" for planet in exoplanets])}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4 mb-4">
                <div class="col-12">
                    <a href="/" class="btn btn-primary">Back to Home</a>
                </div>
            </div>
        </div>
        
        <script>
            // Create timeline chart
            const timelineData = {fig.to_json()};
            Plotly.newPlot('timeline-chart', timelineData.data, timelineData.layout);
            
            // Create methods bar chart
            const methodsData = {methods_bar.to_json()};
            Plotly.newPlot('methods-chart', methodsData.data, methodsData.layout);
        </script>
    </body>
    </html>
    """
    
    return html_content
