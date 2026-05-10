
import pandas as pd
import pickle
import os

CACHE_FILE = "data/cache.pkl"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        data = pickle.load(f)
        sheets = data.get("sheets", {})
        
        prod_ob = sheets.get("prod_ob")
        if prod_ob is not None and not prod_ob.empty:
            print("--- Sample OB Data ---")
            print(prod_ob[["Date", "Hour LU", "Volume"]].tail(20))
            
        prod_ch = sheets.get("prod_ch")
        if prod_ch is not None and not prod_ch.empty:
            print("\n--- Sample CH Data ---")
            print(prod_ch[["Date", "Hour LU", "Volume"]].tail(20))
else:
    print("Cache file not found")
