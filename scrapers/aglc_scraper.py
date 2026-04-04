import requests
import pandas as pd
from datetime import datetime

def download_aglc_data():
    print("Downloading AGLC cannabis licensee data...")
    
    url = "https://aglc.ca/cannabis/cannabis-licensee-report/EXCEL"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        # Save raw Excel file
        filename = f"../data/aglc_stores_{datetime.now().strftime('%Y%m%d')}.xlsx"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Excel file saved to {filename}")
        
        # Load into pandas
        df = pd.read_excel(filename)
        print(f"\nTotal stores found: {len(df)}")
        print(f"\nColumns available:")
        print(df.columns.tolist())
        print(f"\nFirst 5 rows:")
        print(df.head())
        # Filter Alberta only
        df_alberta = df[df['Site Province Abbrev'] == 'AB']
        print(f"\nAlberta stores: {len(df_alberta)}")
        
        # Filter Calgary only
        df_calgary = df[df['Site City Name'] == 'CALGARY']
        print(f"Calgary stores: {len(df_calgary)}")
        
        # Save Alberta data
        df_alberta.to_csv("../data/alberta_stores.csv", index=False)
        print("\nAlberta data saved to alberta_stores.csv")
        
        # Show Calgary stores
        print("\nCalgary stores preview:")
        print(df_calgary[['Establishment Name', 'Site Address Line 1', 'Telephone Number']].to_string())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_aglc_data()