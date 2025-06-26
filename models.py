from pydantic import BaseModel
from typing import List, Optional

class Tree(BaseModel):
    scientific_name: str
    common_name: Optional[str] = None
    indonesian_name: Optional[str] = None

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
  matching_species: List[Tree]
  
class TreeDetail(BaseModel):
    scientific_name: str
    common_name: Optional[str]
    indonesian_name: Optional[str]
