import os
import logging
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Simple ML prediction function (placeholder - replace with a real model)
def predict_habitability_ml(radius, temperature, distance):
    # Simulate a basic ML model using random numbers for demonstration
    score = random.uniform(0, 1)
    if score > 0.8:
        return "High potential"
    elif score > 0.5:
        return "Moderate potential"
    else:
        return "Unlikely"

@app.route("/")
def index():
    """Render the home page with API documentation"""
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    """Render the dashboard page with visualizations and analytics"""
    return render_template("dashboard.html")

@app.route("/docs")
def api_docs():
    """Redirect to API documentation"""
    return render_template("index.html")

@app.route("/exoplanet/<name>")
def exoplanet_detail_page(name):
    """Render page for a specific exoplanet with visualizations"""
    return redirect(url_for('get_exoplanet_visualization', name=name))

@app.route("/habitable")
def habitable_exoplanets_page():
    """Render page for habitable exoplanets with visualizations"""
    return render_template("habitable_visualization.html")

@app.route("/timeline")
def discovery_timeline_page():
    """Render page for exoplanet discovery timeline with visualizations"""
    return render_template("discovery_visualization.html")

# API routes
@app.route("/api/exoplanet/<name>")
def get_exoplanet(name):
    """Get detailed information about a specific exoplanet"""
    # This is a placeholder - you'll implement actual NASA API calls with real data

    # Dictionary of known exoplanet data
    exoplanet_data = {
        "Kepler-186f": {
            "name": "Kepler-186f",
            "size_comparison": {"earth_radius": 1.2, "earth_temperature": 262, "earth_distance": 500},
            "discovery_method": "Transit",
            "orbital_period": "129.9 days",
            "distance": 500,
            "habitability_score": 0.95,
            "eq_temperature": 262,
            "discovery_year": 2014
        },
        "Teegarden's Star b": {
            "name": "Teegarden's Star b",
            "size_comparison": {"earth_radius": 1.05, "earth_temperature": 264, "earth_distance": 12.5},
            "discovery_method": "Radial Velocity",
            "orbital_period": "4.9 days",
            "distance": 12.5,
            "habitability_score": 0.93,
            "eq_temperature": 264,
            "discovery_year": 2019
        },
        "K2-18b": {
            "name": "K2-18b",
            "size_comparison": {"earth_radius": 2.6, "earth_temperature": 265, "earth_distance": 124},
            "discovery_method": "Transit",
            "orbital_period": "32.9 days",
            "distance": 124,
            "habitability_score": 0.71,
            "eq_temperature": 265,
            "discovery_year": 2015
        },
        "GJ 357 d": {
            "name": "GJ 357 d",
            "size_comparison": {"earth_radius": 1.75, "earth_temperature": 240, "earth_distance": 31},
            "discovery_method": "Transit",
            "orbital_period": "55.7 days",
            "distance": 31,
            "habitability_score": 0.82,
            "eq_temperature": 240,
            "discovery_year": 2019
        },
        "Proxima b": {
            "name": "Proxima b",
            "size_comparison": {"earth_radius": 1.3, "earth_temperature": 278, "earth_distance": 4.2},
            "discovery_method": "Radial Velocity",
            "orbital_period": "11.2 days",
            "distance": 4.2,
            "habitability_score": 0.89,
            "eq_temperature": 278,
            "discovery_year": 2016
        },
        "TOI-700 d": {
            "name": "TOI-700 d",
            "size_comparison": {"earth_radius": 1.1, "earth_temperature": 268, "earth_distance": 101.5},
            "discovery_method": "Transit",
            "orbital_period": "37.4 days",
            "distance": 101.5,
            "habitability_score": 0.86,
            "eq_temperature": 268,
            "discovery_year": 2020
        },
        "TRAPPIST-1e": {
            "name": "TRAPPIST-1e",
            "size_comparison": {"earth_radius": 0.92, "earth_temperature": 251, "earth_distance": 39},
            "discovery_method": "Transit",
            "orbital_period": "6.1 days",
            "distance": 39,
            "habitability_score": 0.78,
            "eq_temperature": 251,
            "discovery_year": 2017
        },
        "K2-18b": {
            "name": "K2-18b",
            "size_comparison": {"earth_radius": 2.6, "earth_temperature": 265, "earth_distance": 124},
            "discovery_method": "Transit",
            "orbital_period": "33 days",
            "distance": 124,
            "habitability_score": 0.71,
            "eq_temperature": 265,
            "discovery_year": 2015
        }
    }

    # Get exoplanet data or use default if not found
    exoplanet_info = exoplanet_data.get(name, {
        "name": name,
        "size_comparison": {"earth_radius": 1.63, "earth_temperature": 345, "earth_distance": 1400},
        "discovery_method": "Transit",
        "orbital_period": "384 days",
        "distance": 1400,
        "habitability_score": 0.76,
        "eq_temperature": 288,
        "discovery_year": 2015
    })

    # Get ML prediction
    ml_prediction = predict_habitability_ml(
        radius=exoplanet_info["size_comparison"]["earth_radius"],
        temperature=exoplanet_info["eq_temperature"],
        distance=exoplanet_info["distance"]
    )

    exoplanet_info["ml_habitability_prediction"] = ml_prediction

    # Return data for the requested exoplanet, or a default if not found
    return jsonify(exoplanet_info)


@app.route("/api/exoplanet/<name>/visualization")
def get_exoplanet_visualization(name):
    """Get visualization for a specific exoplanet"""
    # Dictionary of known exoplanet data (same as in get_exoplanet function)
    exoplanet_data = {
        "Kepler-186f": {
            "name": "Kepler-186f",
            "size_comparison": {"earth_radius": 1.2, "earth_temperature": 262, "earth_distance": 500},
            "discovery_method": "Transit",
            "orbital_period": "129.9 days",
            "distance": 500,
            "habitability_score": 0.95,
            "eq_temperature": 262,
            "discovery_year": 2014
        },
        "Teegarden's Star b": {
            "name": "Teegarden's Star b",
            "size_comparison": {"earth_radius": 1.05, "earth_temperature": 264, "earth_distance": 12.5},
            "discovery_method": "Radial Velocity",
            "orbital_period": "4.9 days",
            "distance": 12.5,
            "habitability_score": 0.93,
            "eq_temperature": 264,
            "discovery_year": 2019
        },
        "K2-18b": {
            "name": "K2-18b",
            "size_comparison": {"earth_radius": 2.6, "earth_temperature": 265, "earth_distance": 124},
            "discovery_method": "Transit",
            "orbital_period": "32.9 days",
            "distance": 124,
            "habitability_score": 0.71,
            "eq_temperature": 265,
            "discovery_year": 2015
        },
        "GJ 357 d": {
            "name": "GJ 357 d",
            "size_comparison": {"earth_radius": 1.75, "earth_temperature": 240, "earth_distance": 31},
            "discovery_method": "Transit",
            "orbital_period": "55.7 days",
            "distance": 31,
            "habitability_score": 0.82,
            "eq_temperature": 240,
            "discovery_year": 2019
        },
        "Proxima b": {
            "name": "Proxima b",
            "size_comparison": {"earth_radius": 1.3, "earth_temperature": 278, "earth_distance": 4.2},
            "discovery_method": "Radial Velocity",
            "orbital_period": "11.2 days",
            "distance": 4.2,
            "habitability_score": 0.89,
            "eq_temperature": 278,
            "discovery_year": 2016
        },
        "TOI-700 d": {
            "name": "TOI-700 d",
            "size_comparison": {"earth_radius": 1.1, "earth_temperature": 268, "earth_distance": 101.5},
            "discovery_method": "Transit",
            "orbital_period": "37.4 days",
            "distance": 101.5,
            "habitability_score": 0.86,
            "eq_temperature": 268,
            "discovery_year": 2020
        },
        "TRAPPIST-1e": {
            "name": "TRAPPIST-1e",
            "size_comparison": {"earth_radius": 0.92, "earth_temperature": 251, "earth_distance": 39},
            "discovery_method": "Transit",
            "orbital_period": "6.1 days",
            "distance": 39,
            "habitability_score": 0.78,
            "eq_temperature": 251,
            "discovery_year": 2017
        },
        "K2-18b": {
            "name": "K2-18b",
            "size_comparison": {"earth_radius": 2.6, "earth_temperature": 265, "earth_distance": 124},
            "discovery_method": "Transit",
            "orbital_period": "33 days",
            "distance": 124,
            "habitability_score": 0.71,
            "eq_temperature": 265,
            "discovery_year": 2015
        }
    }

    # Get exoplanet data or use default if not found
    exoplanet = exoplanet_data.get(name, {
        "name": name,
        "size_comparison": {"earth_radius": 1.63, "earth_temperature": 345, "earth_distance": 1400},
        "discovery_method": "Transit",
        "orbital_period": "384 days",
        "distance": 1400,
        "habitability_score": 0.76,
        "eq_temperature": 288,
        "discovery_year": 2015
    })

    # Render the visualization template with the exoplanet data
    return render_template('exoplanet_visualization.html', exoplanet=exoplanet)

@app.route("/api/exoplanets/habitable")
def get_habitable_exoplanets():
    """Get a list of potentially habitable exoplanets"""
    # This is a placeholder - you'll implement actual NASA API calls
    exoplanets = [
        {
            "name": "Kepler-186f",
            "habitability_score": 0.95,
            "distance": 500,
            "earth_radius": 1.2,
            "eq_temperature": 262
        },
        {
            "name": "Proxima b",
            "habitability_score": 0.89,
            "distance": 4.2,
            "earth_radius": 1.3,
            "eq_temperature": 278
        },
        {
            "name": "TOI-700 d",
            "habitability_score": 0.86,
            "distance": 101.5,
            "earth_radius": 1.1,
            "eq_temperature": 268
        },
        {
            "name": "TRAPPIST-1e",
            "habitability_score": 0.78,
            "distance": 39,
            "earth_radius": 0.92,
            "eq_temperature": 251
        },
        {
            "name": "K2-18b",
            "habitability_score": 0.71,
            "distance": 124,
            "earth_radius": 2.6,
            "eq_temperature": 265
        },
        {
            "name": "Kepler-442b",
            "habitability_score": 0.84,
            "distance": 1206,
            "earth_radius": 1.3,
            "eq_temperature": 233
        },
        {
            "name": "Teegarden's Star b",
            "habitability_score": 0.93,
            "distance": 12.5,
            "earth_radius": 1.05,
            "eq_temperature": 298
        },
        {
            "name": "GJ 357 d",
            "habitability_score": 0.82,
            "distance": 31,
            "earth_radius": 1.75,
            "eq_temperature": 240
        }
    ]
    return jsonify(exoplanets)

@app.route("/api/exoplanets/habitable/visualization")
def get_habitable_exoplanets_visualization():
    """Get visualization of habitable exoplanets"""
    # Render the habitable exoplanets visualization template
    return render_template('habitable_visualization.html')

@app.route("/api/exoplanets/discovered/last-year")
def get_recent_discoveries():
    """Get exoplanets discovered in the last year"""
    # This is a placeholder - you'll implement actual NASA API calls
    discoveries = [
        {
            "name": "TOI-733 b",
            "discovery_date": "2024-04-01",
            "discovery_method": "Transit"
        },
        {
            "name": "TOI-4600 c",
            "discovery_date": "2024-03-28",
            "discovery_method": "Transit"
        },
        {
            "name": "HD 207897 b",
            "discovery_date": "2024-03-15",
            "discovery_method": "Radial Velocity"
        },
        {
            "name": "GJ 806 b",
            "discovery_date": "2024-02-22",
            "discovery_method": "Radial Velocity"
        },
        {
            "name": "HD 36384 b",
            "discovery_date": "2024-02-14",
            "discovery_method": "Radial Velocity"
        },
        {
            "name": "WASP-193 b",
            "discovery_date": "2024-01-30",
            "discovery_method": "Transit"
        },
        {
            "name": "HD 56414 b",
            "discovery_date": "2024-01-12",
            "discovery_method": "Transit"
        },
        {
            "name": "K2-415 b",
            "discovery_date": "2023-12-08",
            "discovery_method": "Transit"
        },
        {
            "name": "HD 63433 d",
            "discovery_date": "2023-11-17",
            "discovery_method": "Transit"
        },
        {
            "name": "LP 791-18 d",
            "discovery_date": "2023-10-24",
            "discovery_method": "Transit"
        }
    ]
    return jsonify(discoveries)

@app.route("/api/exoplanets/discovered/last-year/visualization")
def get_recent_discoveries_visualization():
    """Get visualization of recent exoplanet discoveries"""
    # Render the discovery timeline visualization template
    return render_template('discovery_visualization.html')

@app.route("/api/dashboard/stats")
def get_dashboard_stats():
    """Get statistics for the dashboard"""
    stats = {
        "total_exoplanets": 5000,  # This is a placeholder count
        "habitable_count": 7,
        "recent_discoveries": 10,
        "discovery_methods": {
            "Transit": 85,
            "Radial Velocity": 45,
            "Direct Imaging": 12,
            "Gravitational Microlensing": 8,
            "Timing Variations": 5,
            "Astrometry": 3
        }
    }
    return jsonify(stats)

if __name__ == "__main__":
    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)