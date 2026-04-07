import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_store_website(place_id):
    """Get website and phone from Google Maps place details"""
    if not place_id or pd.isna(place_id):
        return None, None
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "website,formatted_phone_number,name",
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "OK":
            result = data.get("result", {})
            website = result.get("website", None)
            phone = result.get("formatted_phone_number", None)
            return website, phone
    except Exception as e:
        print(f"Error: {e}")
    
    return None, None

def build_contact_list():
    print("Building Calgary store contact list...")
    
    # Load enriched data with place IDs
    enriched = pd.read_csv("../data/calgary_enriched.csv")
    
    print(f"Total stores: {len(enriched)}")
    print(f"Stores with place IDs: {enriched['place_id'].notna().sum()}")
    
    websites = []
    phones = []
    
    for idx, row in enriched.iterrows():
        store_name = row['Establishment Name']
        place_id = row.get('place_id', None)
        
        print(f"Getting contact for: {store_name}")
        website, phone = get_store_website(place_id)
        websites.append(website)
        phones.append(phone)
        
        time.sleep(0.1)
    
    enriched['website'] = websites
    enriched['phone'] = phones
    
    # Save contact list
    contact_list = enriched[enriched['website'].notna()][
        ['Establishment Name', 'Address', 'website', 'phone', 'rating', 'review_count']
    ]
    
    contact_list.to_csv("../data/calgary_contact_list.csv", index=False)
    
    print(f"\nStores with websites found: {len(contact_list)}")
    print("\nSample contacts:")
    print(contact_list.head(10)[['Establishment Name', 'website']].to_string(index=False))

if __name__ == "__main__":
    build_contact_list()