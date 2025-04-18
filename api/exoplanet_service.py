import os
import json
import logging
import requests
import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse

from models.exoplanet import ExoplanetDetail, HabitableExoplanet, TimelineExoplanet
from api.visualization import (
    generate_exoplanet_comparison_plot,
    generate_habitability_scatter_plot,
    generate_discovery_timeline_plot

from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize a simple Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Training data based on known habitable zone characteristics
# Features: [radius, temperature, distance]
X_train = np.array([
    [1.0, 288, 0],  # Earth-like
    [1.2, 262, 500],  # Kepler-186f
    [1.3, 278, 4.2],  # Proxima b
    [1.1, 268, 101.5],  # TOI-700 d
    [2.6, 265, 124],  # K2-18b
    [0.92, 251, 39],  # TRAPPIST-1e
    [3.0, 350, 200],  # Too hot
    [0.3, 150, 1000],  # Too cold
    [5.0, 280, 50],   # Too large
])

# Labels: 1 for potentially habitable, 0 for unlikely
y_train = np.array([1, 1, 1, 1, 0, 1, 0, 0, 0])

# Train the model
rf_model.fit(X_train, y_train)

def predict_habitability_ml(radius: float, temperature: float, distance: float) -> str:
    """
    Predict habitability using the ML model
    """
    features = np.array([[radius, temperature, distance]])
    prediction = rf_model.predict_proba(features)[0]
    
    confidence = prediction[1]  # Probability of being habitable
    
    if confidence > 0.8:
        return "High potential for habitability"
    elif confidence > 0.5:
        return "Moderate potential for habitability"
    else:
        return "Unlikely to be habitable"

)

# Set up logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(tags=["exoplanets"])

# NASA API endpoints
NASA_EXOPLANET_ARCHIVE_API = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TESS_API_ENDPOINT = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

# Cache to store API responses and avoid repeated calls
cache = {}
CACHE_EXPIRY = 3600  # seconds (1 hour)

async def fetch_from_nasa_exoplanet_archive(query: str) -> Dict[str, Any]:
    """Fetch data from NASA Exoplanet Archive"""
    cache_key = f"nasa_archive_{hash(query)}"
    
    # Check if we have a cached response
    if cache_key in cache and cache[cache_key]["timestamp"] > datetime.datetime.now() - datetime.timedelta(seconds=CACHE_EXPIRY):
        logger.debug("Using cached NASA Exoplanet Archive response")
        return cache[cache_key]["data"]
    
    logger.debug(f"Fetching data from NASA Exoplanet Archive: {query}")
    params = {
        "query": query,
        "format": "json"
    }
    
    try:
        response = requests.get(NASA_EXOPLANET_ARCHIVE_API, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Cache the response
        cache[cache_key] = {
            "timestamp": datetime.datetime.now(),
            "data": data
        }
        
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching data from NASA Exoplanet Archive: {str(e)}")
        raise HTTPException(status_code=503, detail=f"NASA Exoplanet Archive unavailable: {str(e)}")

async def fetch_from_tess_api(params: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch data from TESS API"""
    cache_key = f"tess_api_{hash(json.dumps(params, sort_keys=True))}"
    
    # Check if we have a cached response
    if cache_key in cache and cache[cache_key]["timestamp"] > datetime.datetime.now() - datetime.timedelta(seconds=CACHE_EXPIRY):
        logger.debug("Using cached TESS API response")
        return cache[cache_key]["data"]
    
    logger.debug(f"Fetching data from TESS API with params: {params}")
    params["table"] = "exoplanets"
    params["format"] = "json"
    
    try:
        response = requests.get(TESS_API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Cache the response
        cache[cache_key] = {
            "timestamp": datetime.datetime.now(),
            "data": data
        }
        
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching data from TESS API: {str(e)}")
        raise HTTPException(status_code=503, detail=f"TESS API unavailable: {str(e)}")

def calculate_habitability_score(planet_data: Dict[str, Any]) -> float:
    """
    Calculate a habitability score based on available planet characteristics.
    
    This is a simplified model that considers:
    - Distance from host star relative to habitable zone
    - Planet mass/radius (Earth-like is better)
    - Host star type (K and G stars are most favorable)
    - Equilibrium temperature (closer to Earth's average is better)
    
    Returns a score between 0 and 1, where 1 is most Earth-like/habitable.
    """
    score = 0.5  # Default score
    
    # Size/mass factor (Earth-like mass/radius is best)
    earth_radii = planet_data.get("pl_rade", None)
    if earth_radii:
        # Closer to Earth's radius increases score
        if 0.8 <= earth_radii <= 1.5:
            score += 0.15
        elif 0.5 <= earth_radii <= 2.0:
            score += 0.05
        else:
            score -= 0.1
    
    # Temperature factor
    eq_temp = planet_data.get("pl_eqt", None)
    if eq_temp:
        # Earth's equilibrium temp is around 255K
        temp_diff = abs(eq_temp - 255)
        if temp_diff < 30:
            score += 0.15
        elif temp_diff < 50:
            score += 0.05
        elif temp_diff > 100:
            score -= 0.1
    
    # Orbit factor (Earth-like orbit is best)
    orbit_period = planet_data.get("pl_orbper", None)
    if orbit_period:
        # Closer to Earth's orbital period (365 days)
        period_ratio = abs(orbit_period - 365) / 365
        if period_ratio < 0.2:
            score += 0.1
        elif period_ratio < 0.5:
            score += 0.05
    
    # Insolation factor (Earth = 1)
    insol = planet_data.get("pl_insol", None)
    if insol:
        insol_diff = abs(insol - 1)
        if insol_diff < 0.2:
            score += 0.1
        elif insol_diff < 0.5:
            score += 0.05
        elif insol_diff > 2:
            score -= 0.05
    
    # Limit to range 0-1
    return max(0, min(1, score))

@router.get("/exoplanet/{name}", response_model=ExoplanetDetail)
async def get_exoplanet(name: str = Path(..., description="Name of the exoplanet")):
    """
    Get detailed information about a specific exoplanet.
    """
    logger.info(f"Getting information for exoplanet: {name}")
    
    # Query NASA Exoplanet Archive for planet details
    query = f"select * from ps where pl_name='{name}'"
    planet_data = await fetch_from_nasa_exoplanet_archive(query)
    
    if not planet_data or len(planet_data) == 0:
        raise HTTPException(status_code=404, detail=f"Exoplanet '{name}' not found")
    
    planet_info = planet_data[0]
    
    # Extract relevant data for our model
    earth_radius = planet_info.get("pl_rade", None)
    orbital_period = planet_info.get("pl_orbper", None)
    eq_temperature = planet_info.get("pl_eqt", None)
    distance = planet_info.get("st_dist", None) * 3.26 if planet_info.get("st_dist") else None  # Convert to light years
    discovery_method = planet_info.get("pl_discmethod", "Unknown")
    discovery_year = planet_info.get("pl_disc", None)
    
    habitability_score = calculate_habitability_score(planet_info)
    
    # Create size comparison data for visualization
    size_comparison = {
        "earth_radius": earth_radius if earth_radius else 1.0,
        "earth_temperature": eq_temperature if eq_temperature else 300,
        "earth_distance": distance if distance else 100
    }
    
    # Create the response model
    exoplanet = ExoplanetDetail(
        name=name,
        size_comparison=size_comparison,
        discovery_method=discovery_method,
        orbital_period=f"{orbital_period} days" if orbital_period else "Unknown",
        distance=distance,
        habitability_score=habitability_score,
        eq_temperature=eq_temperature,
        discovery_year=discovery_year
    )
    
    return exoplanet

@router.get("/exoplanet/{name}/visualization")
async def get_exoplanet_visualization(name: str = Path(..., description="Name of the exoplanet")):
    """
    Get visualization for a specific exoplanet comparing to Earth.
    """
    exoplanet = await get_exoplanet(name)
    
    # Generate visualization
    visualization_data = generate_exoplanet_comparison_plot(exoplanet)
    
    return HTMLResponse(content=visualization_data)

@router.get("/exoplanets/habitable", response_model=List[HabitableExoplanet])
async def get_habitable_exoplanets():
    """
    Get a list of potentially habitable exoplanets with habitability scores.
    """
    logger.info("Getting potentially habitable exoplanets")
    
    # Query for exoplanets that might be habitable
    # This is a simplified query focusing on planets with Earth-like sizes and temperatures
    query = """
    select pl_name, pl_rade, pl_orbper, pl_eqt, pl_discmethod, pl_disc, st_dist 
    from ps 
    where pl_rade between 0.5 and 2.0 
    and pl_eqt between 200 and 320
    order by pl_eqt
    """
    planets_data = await fetch_from_nasa_exoplanet_archive(query)
    
    if not planets_data:
        return []
    
    habitable_exoplanets = []
    
    for planet in planets_data:
        # Calculate distance in light years
        distance = planet.get("st_dist", None)
        if distance:
            distance = distance * 3.26  # Convert parsecs to light years
        
        # Calculate habitability score
        habitability_score = calculate_habitability_score(planet)
        
        if habitability_score >= 0.5:  # Only include planets with decent habitability
            exoplanet = HabitableExoplanet(
                name=planet.get("pl_name", "Unknown"),
                habitability_score=habitability_score,
                distance=distance,
                earth_radius=planet.get("pl_rade", None),
                eq_temperature=planet.get("pl_eqt", None)
            )
            habitable_exoplanets.append(exoplanet)
    
    # Sort by habitability score (descending)
    habitable_exoplanets.sort(key=lambda x: x.habitability_score, reverse=True)
    
    return habitable_exoplanets

@router.get("/exoplanets/habitable/visualization")
async def get_habitable_exoplanets_visualization():
    """
    Get visualization of habitable exoplanets (scatter plot).
    """
    habitable_planets = await get_habitable_exoplanets()
    
    # Generate visualization
    visualization_data = generate_habitability_scatter_plot(habitable_planets)
    
    return HTMLResponse(content=visualization_data)

@router.get("/exoplanets/discovered/last-year", response_model=List[TimelineExoplanet])
async def get_recent_discoveries():
    """
    Get exoplanets discovered in the last year.
    """
    logger.info("Getting exoplanets discovered in the last year")
    
    # Get current year
    current_year = datetime.datetime.now().year
    
    # Query for recent discoveries
    query = f"""
    select pl_name, pl_disc, pl_discmethod
    from ps 
    where pl_disc >= {current_year - 1}
    order by pl_disc desc
    """
    planets_data = await fetch_from_nasa_exoplanet_archive(query)
    
    if not planets_data:
        return []
    
    # Create discovery date based on available information
    recent_discoveries = []
    for planet in planets_data:
        discovery_year = planet.get("pl_disc", None)
        
        # Create a discovery date (this is approximated since we only have year)
        # In a real system, we'd look for more precise dates
        discovery_date = f"{discovery_year}-01-01"
        
        exoplanet = TimelineExoplanet(
            name=planet.get("pl_name", "Unknown"),
            discovery_date=discovery_date,
            discovery_method=planet.get("pl_discmethod", "Unknown")
        )
        recent_discoveries.append(exoplanet)
    
    return recent_discoveries

@router.get("/exoplanets/discovered/last-year/visualization")
async def get_recent_discoveries_visualization():
    """
    Get visualization of recent exoplanet discoveries (timeline).
    """
    recent_discoveries = await get_recent_discoveries()
    
    # Generate visualization
    visualization_data = generate_discovery_timeline_plot(recent_discoveries)
    
    return HTMLResponse(content=visualization_data)
