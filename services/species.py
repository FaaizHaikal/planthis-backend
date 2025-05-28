import pandas as pd
from config import PLANTS_CSV
from typing import Dict, List

class SpeciesMatcher:
  def __init__(self):
    self.df = pd.read_csv(PLANTS_CSV)
  
  def find_matches(self, conditions: Dict) -> List[str]:
    """Find species matching biophysical conditions."""
    matches = []
    for _, row in self.df.iterrows():
      if all([
        conditions["altitude"] >= row["altitude_min"],
        conditions["altitude"] <= row["altitude_max"],
        conditions["temperature"] >= row["temperature_min"],
        conditions["temperature"] <= row["temperature_max"],
        conditions["rainfall"] >= row["rainfall_min"],
        conditions["rainfall"] <= row["rainfall_max"],
        conditions["ph"] >= row["ph_min"],
        conditions["ph"] <= row["ph_max"],
        any(soil in row["soil_types"].split(",") for soil in conditions["soil_type"])
      ]):
        matches.append(row["scientific_name"])
    return matches

species_matcher = SpeciesMatcher()  # Singleton instance
