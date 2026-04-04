import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Page config
st.set_page_config(
    page_title="CannaIQ - Cannabis Market Intelligence",
    page_icon="🌿",
    layout="wide"
)

# Header
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
    }
    .sub-header {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f7f0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌿 CannaIQ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Cannabis Market Intelligence Platform — Calgary, Alberta</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    enriched = pd.read_csv("data/calgary_enriched.csv")
    saturation = pd.read_csv("data/calgary_saturation_report.csv")
    alberta = pd.read_csv("data/alberta_stores.csv")
    calgary = alberta[alberta["Site City Name"] == "CALGARY"].copy()
    return enriched, saturation, calgary

# Top metrics
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Calgary Stores", "196")
with col2:
    st.metric("Avg Rating", f"{enriched['rating'].mean():.2f} ⭐")
with col3:
    st.metric("Operational", len(enriched[enriched['business_status'] == 'OPERATIONAL']))
with col4:
    st.metric("Permanently Closed", len(enriched[enriched['business_status'] == 'CLOSED_PERMANENTLY']))
with col5:
    st.metric("Rated Above 4.0", len(enriched[enriched['rating'] > 4.0]))

st.markdown("---")

# Two columns layout
left, right = st.columns(2)

with left:
    st.subheader("📊 Neighbourhood Saturation Score")
    fig_sat = px.bar(
        saturation.sort_values("saturation_score", ascending=True),
        x="saturation_score",
        y="neighbourhood",
        orientation="h",
        color="saturation_score",
        color_continuous_scale="RdYlGn_r",
        title="Saturation by Quadrant (Higher = More Saturated)",
        labels={"saturation_score": "Saturation Score", "neighbourhood": "Area"}
    )
    st.plotly_chart(fig_sat, use_container_width=True)

with right:
    st.subheader("🎯 Opportunity Score by Area")
    fig_opp = px.bar(
        saturation.sort_values("opportunity_score", ascending=True),
        x="opportunity_score",
        y="neighbourhood",
        orientation="h",
        color="opportunity_score",
        color_continuous_scale="RdYlGn",
        title="Opportunity Score (Higher = Better Opportunity)",
        labels={"opportunity_score": "Opportunity Score", "neighbourhood": "Area"}
    )
    st.plotly_chart(fig_opp, use_container_width=True)

st.markdown("---")

# Store performance
st.subheader("🏆 Top Performing Stores in Calgary")
top_stores = enriched[enriched['review_count'] > 50].sort_values("rating", ascending=False).head(20)
fig_stores = px.scatter(
    top_stores,
    x="review_count",
    y="rating",
    hover_name="Establishment Name",
    size="review_count",
    color="rating",
    color_continuous_scale="RdYlGn",
    title="Store Performance — Rating vs Review Volume",
    labels={"review_count": "Number of Reviews", "rating": "Google Rating"}
)
st.plotly_chart(fig_stores, use_container_width=True)

st.markdown("---")

# Raw data table
st.subheader("📋 Full Calgary Store Intelligence")
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
with col_filter2:
    status_filter = st.selectbox("Business Status", ["All", "OPERATIONAL", "CLOSED_PERMANENTLY"])

filtered = enriched[enriched['rating'] >= min_rating]
if status_filter != "All":
    filtered = filtered[filtered['business_status'] == status_filter]

st.dataframe(
    filtered[["Establishment Name", "Address", "rating", "review_count", "business_status"]].sort_values("rating", ascending=False),
    use_container_width=True
)

st.markdown("---")
st.markdown("**CannaIQ** — Cannabis Market Intelligence for Canada | Calgary Beta v0.1")