
import pandas as pd
import pickle
import os

CACHE_FILE = "data/cache.pkl"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        data = pickle.load(f)
        sheets = data.get("sheets", {})
        
        for key in ["prod_ob", "prod_ch"]:
            df = sheets.get(key)
            if df is not None and not df.empty:
                print(f"--- {key} Hour LU distribution ---")
                print(df["Hour LU"].value_counts().sort_index())
else:
    print("Cache file not found")
