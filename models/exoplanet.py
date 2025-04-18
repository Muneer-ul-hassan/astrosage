from typing import Dict, Optional, List
from pydantic import BaseModel, Field

class ExoplanetDetail(BaseModel):
    """Model representing detailed information about an exoplanet"""
    name: str
    size_comparison: Dict[str, float]
    discovery_method: str
    orbital_period: str
    distance: Optional[float] = None  # in light years
    habitability_score: float = 0.0
    eq_temperature: Optional[float] = None
    discovery_year: Optional[int] = None
    ml_habitability_prediction: Optional[str] = None

class HabitableExoplanet(BaseModel):
    """Model representing a potentially habitable exoplanet"""
    name: str
    habitability_score: float = Field(..., ge=0.0, le=1.0)
    distance: Optional[float] = None  # in light years
    earth_radius: Optional[float] = None
    eq_temperature: Optional[float] = None

class TimelineExoplanet(BaseModel):
    """Model representing an exoplanet with discovery timeline information"""
    name: str
    discovery_date: str
    discovery_method: str
