
import pandas as pd
import pickle
import os

CACHE_FILE = "data/cache.pkl"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        data = pickle.load(f)
        sheets = data.get("sheets", {})
        cp = sheets.get("cumm_plan")
        if cp is not None and not cp.empty:
            print("--- cumm_plan Columns ---")
            print(cp.columns.tolist())
            print("\n--- cumm_plan Sample (first 5) ---")
            print(cp.head(5))
else:
    print("Cache file not found")
