from pydantic import BaseModel
from typing import List

class SoilData(BaseModel):
  clay: float
  sand: float
  silt: float
  ph: float
  soc: float
  types: List[str]

class ClimateData(BaseModel):
  temperature: float  # °C
  rainfall: float     # mm/year

class SpeciesMatchResult(BaseModel):
  altitude: float
  climate: ClimateData
  soil: SoilData
  matching_species: List[str]
