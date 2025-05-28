import requests
from config import SOILGRIDS_URL, PEAT_SOC_THRESHOLD, CHALKY_PH_THRESHOLD
from models import SoilData

def get_soil_data(lat: float, lon: float) -> SoilData:
  """Fetch soil properties from SoilGrids."""
  try:
    params = {
      "lon": lon,
      "lat": lat,
      "property": ["clay", "sand", "silt", "phh2o", "soc"],
      "depth": "0-5cm"
    }
    response = requests.get(SOILGRIDS_URL, params=params, timeout=10)
    response.raise_for_status()
    props = response.json()["properties"]
    
    return SoilData(
      clay=props["clay"]["mean"] / 10,
      sand=props["sand"]["mean"] / 10,
      silt=props["silt"]["mean"] / 10,
      ph=props["phh2o"]["mean"] / 10,
      soc=props["soc"]["mean"] * 0.1,
      types=classify_soil(
        clay=props["clay"]["mean"] / 10,
        sand=props["sand"]["mean"] / 10,
        silt=props["silt"]["mean"] / 10,
        ph=props["phh2o"]["mean"] / 10,
        soc=props["soc"]["mean"] * 0.1
      )
    )
  except Exception as e:
    raise ValueError(f"Soil API error: {str(e)}")

def classify_soil(clay: float, sand: float, silt: float, ph: float, soc: float) -> List[str]:
  """Classify soil into types using USDA texture triangle and special cases."""
  soil_types = []
  
  # Calculate intermediate values
  silt_plus_1_5_clay = silt + 1.5 * clay
  silt_plus_2_clay = silt + 2 * clay
  
  # USDA Texture Classification
  if sand >= 85 and silt_plus_1_5_clay < 15:
    usda_texture = "sand"
  elif 70 <= sand <= 91 and silt_plus_1_5_clay >= 15 and silt_plus_2_clay < 30:
    usda_texture = "loamy_sand"
  elif 7 <= clay <= 20 and sand > 52 and silt_plus_2_clay >= 30:
    usda_texture = "sandy_loam"
  elif 7 <= clay <= 27 and 28 <= silt <= 50 and sand <= 52:
    usda_texture = "loam"
  elif 50 <= silt <= 80 and clay < 12:
    usda_texture = "silt_loam"
  elif silt >= 80 and clay < 12:
    usda_texture = "silt"
  elif 20 <= clay <= 35 and silt < 28 and sand > 45:
    usda_texture = "sandy_clay_loam"
  elif 27 <= clay <= 40 and 20 <= sand <= 46:
    usda_texture = "clay_loam"
  elif 27 <= clay <= 40 and sand <= 20:
    usda_texture = "silty_clay_loam"
  elif clay >= 35 and sand >= 45:
    usda_texture = "sandy_clay"
  elif clay >= 40 and silt >= 40:
    usda_texture = "silty_clay"
  elif clay >= 40 and sand <= 45 and silt < 40:
    usda_texture = "clay"
  else:
    usda_texture = "unknown"

  # Map USDA textures
  if usda_texture == "sand":
    soil_types.append("sandy")
  elif usda_texture == "loamy_sand":
    soil_types.extend(["loamy", "sandy"])
  elif usda_texture == "sandy_loam":
    soil_types.extend(["sandy", "loamy"])
  elif usda_texture == "loam":
    soil_types.append("loamy")
  elif usda_texture == "silt_loam":
    soil_types.extend(["silt", "loamy"])
  elif usda_texture == "silt":
    soil_types.append("silt")
  elif usda_texture == "sandy_clay_loam":
    soil_types.extend(["sandy", "clay", "loamy"])
  elif usda_texture == "clay_loam":
    soil_types.extend(["clay", "loamy"])
  elif usda_texture == "silty_clay_loam":
    soil_types.extend(["silt", "clay", "loamy"])
  elif usda_texture == "sandy_clay":
    soil_types.extend(["sandy", "clay"])
  elif usda_texture == "silty_clay":
    soil_types.extend(["silt", "clay"])
  elif usda_texture == "clay":
    soil_types.append("clay")
  # Special cases
  if soc > PEAT_SOC_THRESHOLD:
    soil_types.append("peat")
  if ph > CHALKY_PH_THRESHOLD and "sandy" in soil_types:
    soil_types.append("chalky")
  
  return sorted(list(set(soil_types)))  # Remove duplicates
