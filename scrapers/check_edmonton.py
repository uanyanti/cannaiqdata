import pandas as pd
df = pd.read_csv("../data/edmonton_geocoded.csv")
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("Lat/lng sample:")
print(df[["Establishment Name", "lat", "lng"]].dropna().head(5))
print(f"Total with coordinates: {df[['lat','lng']].dropna().shape[0]}")