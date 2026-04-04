import pandas as pd

df = pd.read_csv("../data/calgary_enriched.csv")

print("Total stores:", len(df))
print("Stores rated above 4.0:", len(df[df["rating"] > 4.0]))
print("Permanently closed:", len(df[df["business_status"] == "CLOSED_PERMANENTLY"]))
print("Operational:", len(df[df["business_status"] == "OPERATIONAL"]))
print("Average rating:", round(df["rating"].mean(), 2))
print("\nMost reviewed store:")
print(df.loc[df["review_count"].idxmax()][["Establishment Name", "rating", "review_count"]])
print("\nTop 5 rated stores:")
print(df.sort_values("rating", ascending=False).head(5)[["Establishment Name", "rating", "review_count"]])