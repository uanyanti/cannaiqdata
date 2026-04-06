import pandas as pd

def extract_neighbourhood(address):
    if pd.isna(address):
        return "Unknown"
    quadrants = ["NW", "NE", "SW", "SE"]
    for q in quadrants:
        if q in str(address).upper():
            return q
    return "Downtown"

def calculate_saturation_score(count, max_count):
    return round((count / max_count) * 10, 1)

def calculate_opportunity_score(saturation, avg_rating):
    rating_factor = (5 - avg_rating) if avg_rating > 0 else 2.5
    opportunity = (10 - saturation) + rating_factor
    return round(min(max(opportunity, 1), 10), 1)

def build_saturation_report():
    print("Building neighbourhood saturation report...")

    # Load Calgary stores directly from enriched data
    enriched = pd.read_csv("../data/calgary_enriched.csv")
    alberta = pd.read_csv("../data/alberta_stores.csv")
    calgary = alberta[alberta["Site City Name"] == "CALGARY"].copy()

    # Extract neighbourhood from address
    calgary = calgary.copy()
    calgary["neighbourhood"] = calgary["Site Address Line 1"].apply(extract_neighbourhood)

    # Keep only unique stores
    calgary_unique = calgary.drop_duplicates(subset=["Establishment Name"])

    # Merge with enriched data
    merged = calgary_unique.merge(
        enriched[["Establishment Name", "rating", "review_count", "business_status"]],
        on="Establishment Name",
        how="left"
    )

    print(f"Total stores after dedup: {len(merged)}")

    # Group by neighbourhood
    neighbourhood_stats = merged.groupby("neighbourhood").agg(
        store_count=("Establishment Name", "count"),
        avg_rating=("rating", "mean"),
        total_reviews=("review_count", "sum"),
        avg_reviews=("review_count", "mean")
    ).reset_index()

    # Calculate scores
    max_count = neighbourhood_stats["store_count"].max()
    neighbourhood_stats["saturation_score"] = neighbourhood_stats["store_count"].apply(
        lambda x: calculate_saturation_score(x, max_count)
    )
    neighbourhood_stats["opportunity_score"] = neighbourhood_stats.apply(
        lambda row: calculate_opportunity_score(row["saturation_score"], row["avg_rating"]), axis=1
    )

    neighbourhood_stats["avg_rating"] = neighbourhood_stats["avg_rating"].round(2)
    neighbourhood_stats["avg_reviews"] = neighbourhood_stats["avg_reviews"].round(0)
    neighbourhood_stats = neighbourhood_stats.sort_values("opportunity_score", ascending=False)

    # Save
    neighbourhood_stats.to_csv("../data/calgary_saturation_report.csv", index=False)

    print("\n=== CALGARY CANNABIS MARKET INTELLIGENCE REPORT ===")
    print(f"Total stores analyzed: {len(merged)}")
    print("\nNeighbourhood Breakdown:")
    print(neighbourhood_stats.to_string(index=False))

if __name__ == "__main__":
    build_saturation_report()