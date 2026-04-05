import streamlit as st
import pandas as pd
import plotly.express as px
import os
from payment import show_payment_page

# Page config
st.set_page_config(
    page_title="CannaIQ - Cannabis Market Intelligence",
    page_icon="🌿",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.main-header {
    font-size: 48px;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
    padding: 10px;
}
.sub-header {
    font-size: 18px;
    color: #888;
    text-align: center;
    margin-bottom: 10px;
}
.decision-banner-green {
    background-color: #1B5E20;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
}
.decision-banner-red {
    background-color: #B71C1C;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
}
.insight-box {
    background-color: #1E1E1E;
    border-left: 4px solid #2E7D32;
    padding: 15px;
    border-radius: 8px;
    color: #eee;
    font-size: 15px;
    margin-top: 10px;
}
.risk-box {
    background-color: #3E1C1C;
    border-left: 4px solid #FF5252;
    padding: 15px;
    border-radius: 8px;
    color: #eee;
    font-size: 15px;
    margin-top: 10px;
}
.why-matters {
    background-color: #1A237E;
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 18px;
    margin: 20px 0;
}
.score-explain {
    color: #aaa;
    font-size: 13px;
    margin-top: 5px;
}
.cta-box {
    background: linear-gradient(135deg, #2E7D32, #1B5E20);
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    color: white;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    enriched = pd.read_csv(os.path.join(base, "data", "calgary_enriched.csv"))
    saturation = pd.read_csv(os.path.join(base, "data", "calgary_saturation_report.csv"))
    alberta = pd.read_csv(os.path.join(base, "data", "alberta_stores.csv"))
    calgary = alberta[alberta["Site City Name"] == "CALGARY"].copy()
    return enriched, saturation, calgary

enriched, saturation, calgary = load_data()

# Header
st.markdown('<p class="main-header">🌿 CannaIQ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Cannabis Market Intelligence — Calgary, Alberta | Updated Daily — market conditions change fast</p>', unsafe_allow_html=True)

# Why This Matters
st.markdown("""
<div class="why-matters">
    🚨 <strong>Avoid costly mistakes</strong> — CannaIQ tells you exactly where to open and where to stay away.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Decision Banners
st.subheader("🎯 What You Should Do Right Now")
st.markdown('<p class="score-explain" style="font-size:15px">These recommendations are based on competition density and demand gaps.</p>', unsafe_allow_html=True)

col_yes, col_no = st.columns(2)

with col_yes:
    st.markdown("""
    <div class="decision-banner-green">
        BEST AREA TO OPEN<br>
        <span style="font-size:28px">Downtown Calgary</span><br>
        <span style="font-size:14px">Lowest competition in the city right now</span><br>
        <span style="font-size:13px; background:#2E7D32; padding:3px 8px; border-radius:10px">#1 Opportunity in Calgary</span><br>
        <span style="font-size:13px; color:#90EE90">Recommended for new store entry</span>
    </div>
    """, unsafe_allow_html=True)

with col_no:
    st.markdown("""
    <div class="decision-banner-red">
        AVOID THESE AREAS<br>
        <span style="font-size:28px">SW & SE Calgary</span><br>
        <span style="font-size:14px">Highest store density — hardest to compete</span><br>
        <span style="font-size:13px; color:#FFB3B3">High risk for new entrants</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Market Risk Overview
st.subheader("📊 Market Risk Overview")
st.markdown('<p class="score-explain" style="font-size:14px">Rising store count increases competition and reduces margins.</p>', unsafe_allow_html=True)

operational = len(enriched[enriched['business_status'] == 'OPERATIONAL'])
high_comp = len(enriched[enriched['review_count'] > 200])
calgary['Initial Effective Date'] = pd.to_datetime(calgary['Initial Effective Date'], errors='coerce')
six_months_ago = pd.Timestamp.now() - pd.DateOffset(months=6)
new_stores = len(calgary[calgary['Initial Effective Date'] >= six_months_ago])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Active Stores", operational)
with col2:
    st.metric("High Competition Stores", high_comp)
with col3:
    st.metric("New Stores (Last 6 Months)", new_stores)

st.markdown("---")

# Killer line above charts
st.markdown("""
<div class="insight-box" style="text-align:center; font-size:17px; margin-bottom:15px">
    💰 <strong>These scores show where you're most likely to win or lose money.</strong>
</div>
""", unsafe_allow_html=True)

# Charts
left, right = st.columns(2)

with left:
    st.subheader("🚫 Where NOT to Open")
    st.markdown('<p class="score-explain">Score based on store density + competition signals. Higher = more saturated = higher risk.</p>', unsafe_allow_html=True)
    fig_sat = px.bar(
        saturation.sort_values("saturation_score", ascending=True),
        x="saturation_score",
        y="neighbourhood",
        orientation="h",
        color="saturation_score",
        color_continuous_scale="RdYlGn_r",
        labels={"saturation_score": "Saturation Score", "neighbourhood": "Area"}
    )
    fig_sat.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sat, use_container_width=True)
    st.markdown('<div class="risk-box">⚠️ SW Calgary has the highest competition density — expect lower margins and harder customer acquisition</div>', unsafe_allow_html=True)

with right:
    st.subheader("✅ Best Areas to Open")
    st.markdown('<p class="score-explain">Score based on opportunity gap — low competition + strong demand signals. Higher = better opportunity.</p>', unsafe_allow_html=True)
    fig_opp = px.bar(
        saturation.sort_values("opportunity_score", ascending=True),
        x="opportunity_score",
        y="neighbourhood",
        orientation="h",
        color="opportunity_score",
        color_continuous_scale="RdYlGn",
        labels={"opportunity_score": "Opportunity Score", "neighbourhood": "Area"}
    )
    fig_opp.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_opp, use_container_width=True)
    st.markdown('<div class="insight-box">✅ Downtown Calgary = highest opportunity score in the city. Low saturation, strong foot traffic, underserved market.</div>', unsafe_allow_html=True)

# Confidence level
st.markdown("""
<div style="text-align:center; margin-top:10px">
    <span style="background:#333; padding:6px 16px; border-radius:20px; color:#aaa; font-size:13px">
        Confidence: Medium — based on AGLC public registry + Google Maps signals
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Competitive Landscape
st.subheader("🏆 Competitive Landscape")
st.markdown("Who dominates Calgary right now — and where the gaps are.")

top_stores = enriched[enriched['review_count'] > 50].sort_values("rating", ascending=False).head(20)
fig_stores = px.scatter(
    top_stores,
    x="review_count",
    y="rating",
    hover_name="Establishment Name",
    size="review_count",
    color="rating",
    color_continuous_scale="RdYlGn",
    labels={"review_count": "Number of Reviews", "rating": "Google Rating"}
)
fig_stores.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_stores, use_container_width=True)
st.markdown('<div class="insight-box">Bud Bar Stampede leads with 815 reviews and a 5.0 rating — the benchmark every Calgary operator is competing against.</div>', unsafe_allow_html=True)

st.markdown("---")

# Store Intelligence Table
st.subheader("📋 Full Store Intelligence")
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

# CTA
st.markdown("""
<div class="cta-box">
    <h2>🌿 Get Full CannaIQ Intelligence</h2>
    <p style="font-size:18px">Store-level alerts · Neighbourhood forecasts · Competitor tracking · Canada-wide data</p>
    <p style="font-size:22px; font-weight:bold">Join CannaIQ Beta — Early Access Now Open</p>
    <a href="mailto:hello@cannaiqdata.ca" style="background:white; color:#2E7D32; padding:12px 30px; border-radius:25px; font-weight:bold; font-size:18px; text-decoration:none">
        🔒 Get exact store locations, competitor alerts & real-time updates → Join CannaIQ Beta
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Payment Section
if st.button("🔒 Get Full Access — Join CannaIQ Beta", use_container_width=True):
    st.session_state.show_payment = True

if st.session_state.get("show_payment"):
    show_payment_page()

st.markdown("<p style='text-align:center;color:#555'>CannaIQ — Cannabis Market Intelligence for Canada | Calgary Beta v1.0</p>", unsafe_allow_html=True)