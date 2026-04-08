import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_place_details(store_name, address, city):
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
        "google_name": "", "rating": 0, "review_count": 0,
        "business_status": "", "google_address": "", "place_id": ""
    }

def enrich_edmonton_stores():
    print("Loading Edmonton stores...")
    df = pd.read_csv("../data/edmonton_stores.csv")
    print(f"Enriching {len(df)} Edmonton stores with Google Maps data...")

    results = []
    for idx, row in df.iterrows():
        store_name = row["Establishment Name"]
        address = row["Site Address Line 1"]
        print(f"Processing: {store_name}")
        details = get_place_details(store_name, address, "Edmonton")
        details["Establishment Name"] = store_name
        details["Address"] = address
        results.append(details)
        time.sleep(0.2)

    df_enriched = pd.DataFrame(results)
    df_enriched.to_csv("../data/edmonton_enriched.csv", index=False)

    print(f"\nDone! Enriched data saved to edmonton_enriched.csv")
    print(f"\nTop rated stores:")
    print(df_enriched.sort_values("rating", ascending=False).head(5)[
        ["Establishment Name", "rating", "review_count"]
    ])

if __name__ == "__main__":
    enrich_edmonton_stores()