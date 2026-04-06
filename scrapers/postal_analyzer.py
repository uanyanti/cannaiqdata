import pandas as pd
import re

def extract_postal_code(address):
    """Extract postal code from address"""
    if pd.isna(address):
        return "Unknown"
    # Canadian postal code pattern
    match = re.search(r'[A-Z]\d[A-Z]\s?\d[A-Z]\d', str(address).upper())
    if match:
        return match.group().replace(" ", "")
    return "Unknown"

def extract_fsa(postal_code):
    """Extract Forward Sortation Area (first 3 chars)"""
    if postal_code == "Unknown":
        return "Unknown"
    return postal_code[:3]

def build_postal_report():
    print("Building postal code analysis...")
    
    enriched = pd.read_csv("../data/calgary_enriched.csv")
    alberta = pd.read_csv("../data/alberta_stores.csv")
    calgary = alberta[alberta["Site City Name"] == "CALGARY"].copy()
    
    # Extract postal codes
    calgary["postal_code"] = calgary["Site Postal Code"].apply(
        lambda x: str(x).strip().replace(" ", "") if pd.notna(x) else "Unknown"
    )
    calgary["fsa"] = calgary["postal_code"].apply(extract_fsa)
    
    # Merge with enriched
    merged = calgary.merge(
        enriched[["Establishment Name", "rating", "review_count", "business_status"]],
        on="Establishment Name",
        how="left"
    ).drop_duplicates(subset=["Establishment Name"])
    
    # Group by FSA
    fsa_stats = merged.groupby("fsa").agg(
        store_count=("Establishment Name", "count"),
        avg_rating=("rating", "mean"),
        total_reviews=("review_count", "sum"),
        avg_reviews=("review_count", "mean")
    ).reset_index()
    
    # Calculate scores
    max_count = fsa_stats["store_count"].max()
    fsa_stats["saturation_score"] = (fsa_stats["store_count"] / max_count * 10).round(1)
    fsa_stats["opportunity_score"] = fsa_stats.apply(
        lambda row: round(min(max((10 - row["saturation_score"]) + (5 - row["avg_rating"]), 1), 10), 1),
        axis=1
    )
    fsa_stats["avg_rating"] = fsa_stats["avg_rating"].round(2)
    fsa_stats = fsa_stats.sort_values("opportunity_score", ascending=False)
    
    # Save
    fsa_stats.to_csv("../data/calgary_postal_analysis.csv", index=False)
    
    print(f"\nTotal FSA areas analyzed: {len(fsa_stats)}")
    print("\nTop 10 Opportunity Postal Areas:")
    print(fsa_stats.head(10)[["fsa", "store_count", "avg_rating", "opportunity_score"]].to_string(index=False))
    print("\nMost Saturated Postal Areas:")
    print(fsa_stats.nlargest(5, "saturation_score")[["fsa", "store_count", "saturation_score"]].to_string(index=False))

if __name__ == "__main__":
    build_postal_report()