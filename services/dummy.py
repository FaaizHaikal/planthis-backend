from models import SpeciesMatchResult
from models import ClimateData
import json

def get_dummy_response() -> SpeciesMatchResult:
  try:
    with open("dummy.json") as file:
      data = json.load(file)
      
      return SpeciesMatchResult(**data)
  except Exception as e:
    raise ValueError(f"Dummy response error: {str(e)}")