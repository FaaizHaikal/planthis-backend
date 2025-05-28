from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import SpeciesMatchResult
from services.climate import get_elevation, get_climate
from services.soil import get_soil_data
from services.species import species_matcher

app = FastAPI()

# CORS Setup
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["GET"],
  allow_headers=["*"],
)

@app.get("/species", response_model=SpeciesMatchResult)
async def get_biophysical(lat: float, lon: float):
  try:
    soil = get_soil_data(lat, lon)
    elevation = get_elevation(lat, lon)
    climate = get_climate(lat, lon)
      
    matches = species_matcher.find_matches({
      "altitude": elevation,
      "temperature": climate.temperature,
      "rainfall": climate.rainfall,
      "ph": soil.ph,
      "soil_type": soil.types
    })
    return SpeciesMatchResult(
      altitude=elevation,
      climate=climate,
      soil=soil,
      matching_species=matches
    )

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def health_check():
  return {"status": "healthy"}
