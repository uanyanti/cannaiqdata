import requests
import pandas as pd
import os

def download_health_canada_data():
    print("Downloading Health Canada cannabis market data...")
    
    # Direct CSV from Health Canada Open Government Portal
    url = "https://open.canada.ca/data/dataset/1f8d838e-f738-4549-8019-edfc0d931cd7/resource/2f960711-2447-472d-81b0-731fdfbf59a1/download/hc-sc_cannabis_market_data_-_donnees_sur_le_marche_du_cannabis_-_inventory_and_sales_en.csv"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        filename = "../data/health_canada_market_data.csv"
        with open(filename, "wb") as f:
            f.write(response.content)
        
        df = pd.read_csv(filename, encoding='latin-1')
        print(f"\nTotal records: {len(df)}")
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        
        # Filter Alberta data
        if any('province' in col.lower() for col in df.columns):
            province_col = [col for col in df.columns if 'province' in col.lower()][0]
            alberta = df[df[province_col].str.contains('Alberta|AB', na=False)]
            print(f"\nAlberta records: {len(alberta)}")
            alberta.to_csv("../data/health_canada_alberta.csv", index=False)
            print("Alberta data saved to health_canada_alberta.csv")
        # Process trend data
        df['year_month'] = pd.to_datetime(df['year_month'])
        df = df.sort_values('year_month')
        
        # Latest 12 months
        latest_12 = df.tail(12)
        
        # Sales trend by product
        sales_trend = latest_12.groupby('product_type').agg(
    total_medical_sales=('sales_medical_kg', lambda x: pd.to_numeric(x, errors='coerce').sum()),
    total_non_medical_sales=('sales_non_medical_kg', lambda x: pd.to_numeric(x, errors='coerce').sum()),
    avg_inventory=('packaged_inventory_kg_prov_distributors_retailers', lambda x: pd.to_numeric(x, errors='coerce').mean())
).reset_index()
       
        
        sales_trend['total_sales'] = sales_trend['total_medical_sales'] + sales_trend['total_non_medical_sales']
        sales_trend = sales_trend.sort_values('total_sales', ascending=False)
        
        sales_trend.to_csv("../data/health_canada_trends.csv", index=False)
        
        print("\n=== CANADA CANNABIS MARKET TRENDS (Last 12 Months) ===")
        print(sales_trend[['product_type', 'total_sales', 'avg_inventory']].to_string(index=False))


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_health_canada_data()