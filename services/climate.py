import requests
from datetime import datetime
from config import OPEN_ELEVATION_URL, OPEN_METEO_URL
from models import ClimateData

def get_elevation(lat: float, lon: float) -> float:
  """Fetch altitude in meters from Open-Elevation."""
  try:
    params = {"locations": f"{lat},{lon}"}
    response = requests.get(OPEN_ELEVATION_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["results"][0]["elevation"]
  except Exception as e:
    raise ValueError(f"Elevation API error: {str(e)}")

def get_climate(lat: float, lon: float) -> ClimateData:
  """Fetch average temperature and rainfall from Open-Meteo."""
  try:
    last_year = (datetime.now().year) - 1
    params = {
      "latitude": lat,
      "longitude": lon,
      "start_date": f"{last_year}-01-01",
      "end_date": f"{last_year}-12-31",
      "daily": "temperature_2m_mean,precipitation_sum",
      "timezone": "auto"
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["daily"]
    return ClimateData(
      temperature=sum(data["temperature_2m_mean"]) / len(data["temperature_2m_mean"]),
      rainfall=sum(data["precipitation_sum"])
    )
  except Exception as e:
    raise ValueError(f"Climate API error: {str(e)}")
