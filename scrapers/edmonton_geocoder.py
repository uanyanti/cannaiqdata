import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_address(address, city="Edmonton", province="AB"):
    full_address = f"{address}, {city}, {province}, Canada"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": full_address, "key": API_KEY}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None

def geocode_edmonton_stores():
    print("Geocoding Edmonton stores...")
    enriched = pd.read_csv("../data/edmonton_enriched.csv")
    edmonton = pd.read_csv("../data/edmonton_stores.csv")
    merged = edmonton.merge(
        enriched[["Establishment Name", "rating", "review_count", "business_status"]],
        on="Establishment Name", how="left"
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
    merged.to_csv("../data/edmonton_geocoded.csv", index=False)
    print(f"\nDone! {len(merged[merged['lat'].notna()])} stores geocoded")

if __name__ == "__main__":
    geocode_edmonton_stores()