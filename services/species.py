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
      soil_types = ([conditions["soil_type"]] if isinstance(conditions["soil_type"], str)
                     else conditions["soil_type"])
        
      mask = (
            (self.df["altitude_min"] <= conditions["altitude"]) &
            (self.df["altitude_max"] >= conditions["altitude"]) &
            (self.df["temperature_min"] <= conditions["temperature"]) &
            (self.df["temperature_max"] >= conditions["temperature"]) &
            (self.df["rainfall_min"] <= conditions["rainfall"]) &
            (self.df["rainfall_max"] >= conditions["rainfall"]) &
            (self.df["ph_min"] <= conditions["ph"]) &
            (self.df["ph_max"] >= conditions["ph"]) &
            (self.df[soil_types].eq(1).any(axis=1))  # Check any soil match
      )
      
      return self.df.loc[mask, "scientific_name"].tolist()
      
    return matches

species_matcher = SpeciesMatcher()  # Singleton instance
