import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_place_details(store_name, address, city):
    """Get Google Maps data for a cannabis store"""
    
    query = f"{store_name} cannabis {city} Alberta"
    
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": query,
        "inputtype": "textquery",
        "fields": "name,rating,user_ratings_total,business_status,formatted_address,place_id",
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["status"] == "OK" and data["candidates"]:
            place = data["candidates"][0]
            return {
                "google_name": place.get("name", ""),
                "rating": place.get("rating", 0),
                "review_count": place.get("user_ratings_total", 0),
                "business_status": place.get("business_status", ""),
                "google_address": place.get("formatted_address", ""),
                "place_id": place.get("place_id", "")
            }
    except Exception as e:
        print(f"Error for {store_name}: {e}")
    
    return {
        "google_name": "",
        "rating": 0,
        "review_count": 0,
        "business_status": "",
        "google_address": "",
        "place_id": ""
    }

def enrich_calgary_stores():
    print("Loading Calgary stores...")
    df = pd.read_csv("../data/alberta_stores.csv")
    df_calgary = df[df["Site City Name"] == "CALGARY"].copy()
    print(f"Enriching {len(df_calgary)} Calgary stores with Google Maps data...")
    
    results = []
    for idx, row in df_calgary.iterrows():
        store_name = row["Establishment Name"]
        address = row["Site Address Line 1"]
        
        print(f"Processing: {store_name}")
        details = get_place_details(store_name, address, "Calgary")
        details["Establishment Name"] = store_name
        details["Address"] = address
        results.append(details)
        
        # Be respectful to the API
        time.sleep(0.2)
    
    df_enriched = pd.DataFrame(results)
    df_enriched.to_csv("../data/calgary_enriched.csv", index=False)
    
    print(f"\nDone! Enriched data saved to calgary_enriched.csv")
    print(f"\nTop rated stores:")
    print(df_enriched.sort_values("rating", ascending=False).head(10)[
        ["Establishment Name", "rating", "review_count"]
    ])

if __name__ == "__main__":
    enrich_calgary_stores()