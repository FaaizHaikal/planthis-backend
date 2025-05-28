# 🌱 Planthis Backend API
A FastAPI backend for [Planthis](https://github.com/FaaizHaikal/planthis) project. Predicts suitable plant species based on location-derived biophysical data (altitude, climate, soil)

# 🚀 Quick Start
1. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
2. Run the server
   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Test the API
   ```
   GET /species?lat=-3.22&lon=113.81
   ```

# 🙏 Credits
- Plants data: [World Agroforesty](https://www.worldagroforestry.org/)
- Climate data: [Open-meteo](https://open-meteo.com/)
- Soil data: [SoilGrids](https://soilgrids.org/)
- Elevation: [Open-elevation](https://open-elevation.com/)
