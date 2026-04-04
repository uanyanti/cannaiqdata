import pandas as pd
import re

def extract_neighbourhood(address):
    """Extract neighbourhood from Calgary address using postal code and quadrant"""
    if pd.isna(address):
        return "Unknown"
    
    # Extract quadrant (NW, NE, SW, SE) from address
    quadrants = ["NW", "NE", "SW", "SE"]
    for q in quadrants:
        if q in str(address).upper():
            return q
    return "Downtown"

def calculate_saturation_score(count, max_count):
    """Score from 1-10. Higher = more saturated"""
    return round((count / max_count) * 10, 1)

def calculate_opportunity_score(saturation, avg_rating):
    """Score from 1-10. Higher = better opportunity"""
    # Low saturation + low average rating = high opportunity
    rating_factor = (5 - avg_rating) if avg_rating > 0 else 2.5
    opportunity = (10 - saturation) + rating_factor
    return round(min(max(opportunity, 1), 10), 1)

def build_saturation_report():
    print("Building neighbourhood saturation report...")
    
    # Load enriched data
    df = pd.read_csv("../data/calgary_enriched.csv")
    aglc = pd.read_csv("../data/alberta_stores.csv")
    calgary = aglc[aglc["Site City Name"] == "CALGARY"].copy()
    
    # Extract quadrant from address
    calgary["neighbourhood"] = calgary["Site Address Line 1"].apply(extract_neighbourhood)
    
    # Merge with enriched data
    merged = calgary.merge(df[["Establishment Name", "rating", "review_count", "business_status"]], 
                          on="Establishment Name", how="left")
    
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
    
    # Round ratings
    neighbourhood_stats["avg_rating"] = neighbourhood_stats["avg_rating"].round(2)
    neighbourhood_stats["avg_reviews"] = neighbourhood_stats["avg_reviews"].round(0)
    
    # Sort by opportunity score
    neighbourhood_stats = neighbourhood_stats.sort_values("opportunity_score", ascending=False)
    
    # Save report
    neighbourhood_stats.to_csv("../data/calgary_saturation_report.csv", index=False)
    
    print("\n=== CALGARY CANNABIS MARKET INTELLIGENCE REPORT ===")
    print(f"Total stores analyzed: {len(merged)}")
    print("\nNeighbourhood Breakdown:")
    print(neighbourhood_stats.to_string(index=False))
    print("\nHighest Opportunity Areas:")
    print(neighbourhood_stats.head(3)[["neighbourhood", "store_count", "avg_rating", "opportunity_score"]].to_string(index=False))
    print("\nMost Saturated Areas:")
    print(neighbourhood_stats.tail(3)[["neighbourhood", "store_count", "saturation_score"]].to_string(index=False))
    print("\nReport saved to calgary_saturation_report.csv")

if __name__ == "__main__":
    build_saturation_report()