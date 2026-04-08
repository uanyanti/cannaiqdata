import pandas as pd
import re

def extract_neighbourhood(address):
    if pd.isna(address):
        return "Unknown"
    quadrants = ["NW", "NE", "SW", "SE"]
    for q in quadrants:
        if q in str(address).upper():
            return q
    return "Downtown"

def extract_fsa(postal_code):
    if pd.isna(postal_code) or str(postal_code).strip() == "":
        return "Unknown"
    return str(postal_code).strip().replace(" ", "")[:3]

def calculate_saturation_score(count, max_count):
    return round((count / max_count) * 10, 1)

def calculate_opportunity_score(saturation, avg_rating):
    rating_factor = (5 - avg_rating) if avg_rating > 0 else 2.5
    opportunity = (10 - saturation) + rating_factor
    return round(min(max(opportunity, 1), 10), 1)

def build_edmonton_report():
    print("Building Edmonton saturation report...")

    enriched = pd.read_csv("../data/edmonton_enriched.csv")
    edmonton = pd.read_csv("../data/edmonton_stores.csv")

    edmonton["neighbourhood"] = edmonton["Site Address Line 1"].apply(extract_neighbourhood)
    edmonton["fsa"] = edmonton["Site Postal Code"].apply(extract_fsa)

    merged = edmonton.merge(
        enriched[["Establishment Name", "rating", "review_count", "business_status"]],
        on="Establishment Name",
        how="left"
    ).drop_duplicates(subset=["Establishment Name"])

    print(f"Total Edmonton stores: {len(merged)}")

    # Quadrant saturation
    neighbourhood_stats = merged.groupby("neighbourhood").agg(
        store_count=("Establishment Name", "count"),
        avg_rating=("rating", "mean"),
        total_reviews=("review_count", "sum"),
        avg_reviews=("review_count", "mean")
    ).reset_index()

    max_count = neighbourhood_stats["store_count"].max()
    neighbourhood_stats["saturation_score"] = neighbourhood_stats["store_count"].apply(
        lambda x: calculate_saturation_score(x, max_count)
    )
    neighbourhood_stats["opportunity_score"] = neighbourhood_stats.apply(
        lambda row: calculate_opportunity_score(row["saturation_score"], row["avg_rating"]), axis=1
    )
    neighbourhood_stats["avg_rating"] = neighbourhood_stats["avg_rating"].round(2)
    neighbourhood_stats = neighbourhood_stats.sort_values("opportunity_score", ascending=False)
    neighbourhood_stats.to_csv("../data/edmonton_saturation_report.csv", index=False)

    # Postal code analysis
    fsa_stats = merged.groupby("fsa").agg(
        store_count=("Establishment Name", "count"),
        avg_rating=("rating", "mean"),
        total_reviews=("review_count", "sum"),
        avg_reviews=("review_count", "mean")
    ).reset_index()

    max_fsa = fsa_stats["store_count"].max()
    fsa_stats["saturation_score"] = (fsa_stats["store_count"] / max_fsa * 10).round(1)
    fsa_stats["opportunity_score"] = fsa_stats.apply(
        lambda row: round(min(max((10 - row["saturation_score"]) + (5 - row["avg_rating"]), 1), 10), 1),
        axis=1
    )
    fsa_stats["avg_rating"] = fsa_stats["avg_rating"].round(2)
    fsa_stats = fsa_stats.sort_values("opportunity_score", ascending=False)
    fsa_stats.to_csv("../data/edmonton_postal_analysis.csv", index=False)

    print("\n=== EDMONTON CANNABIS MARKET REPORT ===")
    print("\nNeighbourhood Breakdown:")
    print(neighbourhood_stats.to_string(index=False))
    print("\nTop 5 Opportunity Postal Areas:")
    print(fsa_stats.head(5)[["fsa", "store_count", "avg_rating", "opportunity_score"]].to_string(index=False))
    print("\nMost Saturated Postal Areas:")
    print(fsa_stats.nlargest(5, "saturation_score")[["fsa", "store_count", "saturation_score"]].to_string(index=False))

if __name__ == "__main__":
    build_edmonton_report()