import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_address(address, city="Calgary", province="AB"):
    """Convert address to lat/lng coordinates"""
    full_address = f"{address}, {city}, {province}, Canada"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": full_address,
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None

def geocode_calgary_stores():
    print("Geocoding Calgary stores...")
    
    enriched = pd.read_csv("../data/calgary_enriched.csv")
    alberta = pd.read_csv("../data/alberta_stores.csv")
    calgary = alberta[alberta["Site City Name"] == "CALGARY"].copy()
    
    # Merge
    merged = calgary.merge(
        enriched[["Establishment Name", "rating", "review_count", "business_status"]],
        on="Establishment Name",
        how="left"
    ).drop_duplicates(subset=["Establishment Name"])
    
    lats = []
    lngs = []
    
    for idx, row in merged.iterrows():
        address = row["Site Address Line 1"]
        print(f"Geocoding: {row['Establishment Name']}")
        lat, lng = geocode_address(address)
        lats.append(lat)
        lngs.append(lng)
        time.sleep(0.1)
    
    merged["lat"] = lats
    merged["lng"] = lngs
    
    # Save
    merged.to_csv("../data/calgary_geocoded.csv", index=False)
    print(f"\nDone! {len(merged[merged['lat'].notna()])} stores geocoded successfully")

if __name__ == "__main__":
    geocode_calgary_stores()