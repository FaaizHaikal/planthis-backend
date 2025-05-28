from pathlib import Path

# Local path
DATA_DIR = Path(__file__).parent
PLANTS_CSV = DATA_DIR / "plants.csv"

# API Endpoints
OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"
SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"

# Soil Classification Thresholds
PEAT_SOC_THRESHOLD = 120  # g/kg
CHALKY_PH_THRESHOLD = 7.5
