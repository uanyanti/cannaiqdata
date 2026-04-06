import pandas as pd
df = pd.read_csv('../data/health_canada_market_data.csv', encoding='latin-1')
print(df[['product_type', 'sales_medical_kg', 'sales_non_medical_kg']].head(10))
print("\nData types:")
print(df.dtypes)