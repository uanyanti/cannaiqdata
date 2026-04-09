from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os
import math

app = FastAPI(title="CannaIQ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dashboard.cannaiqdata.ca", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

CITIES = {
    "calgary": {
        "enriched":   "calgary_enriched.csv",
        "saturation": "calgary_saturation_report.csv",
        "postal":     "calgary_postal_analysis.csv",
        "geocoded":   "calgary_geocoded.csv",
        "label":      "Calgary, Alberta",
        "center":     [51.0447, -114.0719],
        "best_area":  "Downtown Calgary",
        "avoid_area": "SW & SE Calgary",
        "new_stores": 15,
    },
    "edmonton": {
        "enriched":   "edmonton_enriched.csv",
        "saturation": "edmonton_saturation_report.csv",
        "postal":     "edmonton_postal_analysis.csv",
        "geocoded":   "edmonton_geocoded.csv",
        "label":      "Edmonton, Alberta",
        "center":     [53.5461, -113.4938],
        "best_area":  "Downtown Edmonton",
        "avoid_area": "NW Edmonton",
        "new_stores": 12,
    },
}

ACCESS_CODES_PREFIX = "cannaiq-"

def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Data file not found: {filename}")
    return pd.read_csv(path)

def clean(val):
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

def clean_row(row: dict) -> dict:
    return {k: clean(v) for k, v in row.items()}

def get_city_config(city: str) -> dict:
    city = city.lower()
    if city not in CITIES:
        raise HTTPException(status_code=400, detail=f"City must be 'calgary' or 'edmonton'")
    return CITIES[city], city


# ── Health check ──────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


# ── Access code validation ────────────────────────────────────
@app.get("/api/validate")
def validate(code: str = Query(...)):
    valid = code.startswith(ACCESS_CODES_PREFIX) and len(code) > len(ACCESS_CODES_PREFIX) + 3
    return {"valid": valid}


# ── Summary KPIs ──────────────────────────────────────────────
@app.get("/api/summary")
def summary(city: str = Query("calgary")):
    cfg, city_key = get_city_config(city)
    enriched = load_csv(cfg["enriched"])
    operational = int(len(enriched[enriched["business_status"] == "OPERATIONAL"]))
    high_comp = int(len(enriched[enriched["review_count"] > 200]))
    total = len(enriched)
    return {
        "city": city_key,
        "city_label": cfg["label"],
        "center": cfg["center"],
        "best_area": cfg["best_area"],
        "avoid_area": cfg["avoid_area"],
        "new_stores": cfg["new_stores"],
        "total_stores": total,
        "operational_stores": operational,
        "high_competition_stores": high_comp,
    }


# ── Saturation + Opportunity scores ───────────────────────────
@app.get("/api/saturation")
def saturation(city: str = Query("calgary")):
    cfg, _ = get_city_config(city)
    df = load_csv(cfg["saturation"])
    df = df.sort_values("saturation_score", ascending=False)
    return {
        "city": city,
        "data": [clean_row(r) for r in df.to_dict(orient="records")]
    }


# ── Postal code analysis ──────────────────────────────────────
@app.get("/api/postal")
def postal(city: str = Query("calgary")):
    cfg, _ = get_city_config(city)
    df = load_csv(cfg["postal"])
    top_opportunity = df.sort_values("opportunity_score", ascending=False).head(10)
    top_saturated   = df.sort_values("saturation_score",  ascending=False).head(10)
    all_sorted      = df.sort_values("opportunity_score", ascending=False).head(15)
    return {
        "city": city,
        "top_opportunity": [clean_row(r) for r in top_opportunity.to_dict(orient="records")],
        "top_saturated":   [clean_row(r) for r in top_saturated.to_dict(orient="records")],
        "chart_data":      [clean_row(r) for r in all_sorted.to_dict(orient="records")],
    }


# ── Store intelligence ────────────────────────────────────────
@app.get("/api/stores")
def stores(
    city: str = Query("calgary"),
    min_rating: float = Query(0.0),
    status: str = Query("ALL"),
):
    cfg, _ = get_city_config(city)
    df = load_csv(cfg["enriched"])
    if min_rating > 0:
        df = df[df["rating"] >= min_rating]
    if status != "ALL":
        df = df[df["business_status"] == status]
    df = df.sort_values("rating", ascending=False)
    cols = ["Establishment Name", "Address", "rating", "review_count", "business_status"]
    df = df[cols]
    return {
        "city": city,
        "count": len(df),
        "data": [clean_row(r) for r in df.to_dict(orient="records")]
    }


# ── Geocoded map data ─────────────────────────────────────────
@app.get("/api/geocoded")
def geocoded(city: str = Query("calgary")):
    cfg, _ = get_city_config(city)
    df = load_csv(cfg["geocoded"])
    df = df.dropna(subset=["lat", "lng"])
    cols = ["Establishment Name", "Site Address Line 1", "rating", "review_count", "business_status", "lat", "lng"]
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols]
    return {
        "city": city,
        "count": len(df),
        "data": [clean_row(r) for r in df.to_dict(orient="records")]
    }


# ── Competitive landscape ─────────────────────────────────────
@app.get("/api/competitive")
def competitive(city: str = Query("calgary")):
    cfg, _ = get_city_config(city)
    df = load_csv(cfg["enriched"])
    top = df[df["review_count"] > 50].sort_values("rating", ascending=False).head(20)
    cols = ["Establishment Name", "rating", "review_count", "business_status"]
    top = top[cols]
    top_store = df.sort_values("review_count", ascending=False).iloc[0]
    return {
        "city": city,
        "top_stores": [clean_row(r) for r in top.to_dict(orient="records")],
        "market_leader": {
            "name": top_store["Establishment Name"],
            "reviews": int(top_store["review_count"]),
            "rating": float(top_store["rating"]),
        }
    }


# ── Serve static dashboard HTML ───────────────────────────────
dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard")
if os.path.exists(dashboard_path):
    app.mount("/static", StaticFiles(directory=dashboard_path), name="static")

@app.get("/")
def root():
    index = os.path.join(dashboard_path, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return JSONResponse({"message": "CannaIQ API running. Dashboard coming soon."})