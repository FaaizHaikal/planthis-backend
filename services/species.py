import pandas as pd
from config import PLANTS_CSV
from typing import Dict, List

class SpeciesMatcher:
    def __init__(self):
        self.df = pd.read_csv(PLANTS_CSV)

    # DIUBAH: Tipe data yang dikembalikan sekarang adalah List[Dict]
    def find_matches(self, conditions: Dict) -> List[Dict]:
        """Find species matching biophysical conditions."""
        
        # Logika untuk menangani tipe data tanah tetap sama
        soil_types = ([conditions["soil_type"]] if isinstance(conditions["soil_type"], str)
                      else conditions["soil_type"])
        
        # Logika untuk membuat filter (mask) tetap sama
        mask = (
            (self.df["altitude_min"] <= conditions["altitude"]) &
            (self.df["altitude_max"] >= conditions["altitude"]) &
            (self.df["temperature_min"] <= conditions["temperature"]) &
            (self.df["temperature_max"] >= conditions["temperature"]) &
            (self.df["rainfall_min"] <= conditions["rainfall"]) &
            (self.df["rainfall_max"] >= conditions["rainfall"]) &
            (self.df["ph_min"] <= conditions["ph"]) &
            (self.df["ph_max"] >= conditions["ph"]) &
            (self.df[soil_types].eq(1).any(axis=1))
        )
        
        # --- PERUBAHAN UTAMA ADA DI SINI ---
        
        # 1. Pilih kolom yang relevan (nama ilmiah, nama umum, nama indonesia)
        matched_df = self.df.loc[mask, ["scientific_name", "local_names.common", "local_names.indonesian"]]
        
        # 2. Ganti nama kolom agar cocok dengan model Pydantic 'Tree' di models.py
        matched_df = matched_df.rename(columns={
            "local_names.common": "common_name",
            "local_names.indonesian": "indonesian_name"
        })
        
        # 3. Konversi DataFrame yang sudah difilter menjadi daftar dictionary
        #    Ini adalah format yang bisa langsung dikirim sebagai JSON oleh FastAPI
        return matched_df.to_dict('records')

species_matcher = SpeciesMatcher() # Singleton instance