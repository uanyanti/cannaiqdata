import streamlit as st
import pandas as pd
import plotly.express as px
import os
from payment import show_payment_page
import folium
from streamlit_folium import st_folium

# Page config
st.set_page_config(
    page_title="CannaIQ - Cannabis Market Intelligence",
    page_icon="🌿",
    layout="wide"
)

# Custom meta tags for link previews
st.markdown("""
    <head>
        <meta property="og:title" content="CannaIQ - Cannabis Market Intelligence"/>
        <meta property="og:description" content="Calgary cannabis market intelligence — saturation scores, opportunity maps, and store analytics."/>
        <meta property="og:url" content="https://cannaiqdata.ca"/>
        <meta property="og:type" content="website"/>
    </head>
""", unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
/* Import */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #080d08 !important;
    color: #f0f0f0 !important;
}

/* Main container — centered */
.main .block-container {
    max-width: 900px !important;
    padding: 2rem 1.5rem !important;
    margin: 0 auto !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}

/* Metrics */
[data-testid="metric-container"] {
    background: #0f1a0f !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 14px !important;
    padding: 20px !important;
}
[data-testid="metric-container"] label {
    color: #666 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #4CAF50 !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}

/* Headings */
h1, h2, h3 {
    color: #f0f0f0 !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}

/* Subheaders */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 24px !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: #0f1a0f !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* Buttons */
[data-testid="stButton"] button {
    background: #2E7D32 !important;
    color: white !important;
    border: none !important;
    border-radius: 28px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 32px !important;
    transition: all 0.2s !important;
}
[data-testid="stButton"] button:hover {
    background: #388E3C !important;
    transform: translateY(-1px) !important;
}

/* Select box */
[data-testid="stSelectbox"] > div {
    background: #0f1a0f !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
}

/* Slider */
[data-testid="stSlider"] {
    padding: 8px 0 !important;
}
.stSlider [data-baseweb="slider"] div {
    background: #2E7D32 !important;
}

/* Text input */
[data-testid="stTextInput"] input {
    background: #0f1a0f !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
    padding: 12px 16px !important;
}

/* Divider */
hr {
    border-color: #1a2e1a !important;
    margin: 32px 0 !important;
}

/* Plotly charts background */
.js-plotly-plot {
    background: transparent !important;
}

/* Streamlit tabs if used */
[data-testid="stTab"] {
    background: #0f1a0f !important;
    border-radius: 12px !important;
}

/* Success/error/info boxes */
[data-testid="stAlert"] {
    background: #0f1a0f !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
}

/* Sidebar if ever used */
[data-testid="stSidebar"] {
    background: #0a0f0a !important;
}

/* Mobile */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem !important;
    }
}

/* Custom classes */
.main-header {
    font-size: 42px;
    font-weight: 800;
    color: #4CAF50;
    text-align: center;
    padding: 10px 0;
    letter-spacing: -1px;
}
.sub-header {
    font-size: 16px;
    color: #888;
    text-align: center;
    margin-bottom: 10px;
}
.decision-banner-green {
    background: #1B5E20;
    padding: 28px 24px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
}
.decision-banner-red {
    background: #7f0000;
    padding: 28px 24px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
}
.insight-box {
    background: #0f1a0f;
    border-left: 4px solid #2E7D32;
    padding: 16px 20px;
    border-radius: 0 12px 12px 0;
    color: #ccc;
    font-size: 14px;
    margin-top: 10px;
    line-height: 1.6;
}
.risk-box {
    background: #1a0a0a;
    border-left: 4px solid #FF5252;
    padding: 16px 20px;
    border-radius: 0 12px 12px 0;
    color: #ccc;
    font-size: 14px;
    margin-top: 10px;
    line-height: 1.6;
}
.why-matters {
    background: #0f1a0f;
    border: 1px solid #1e3a1e;
    padding: 20px 24px;
    border-radius: 14px;
    color: white;
    text-align: center;
    font-size: 16px;
    margin: 16px 0;
}
.score-explain {
    color: #666;
    font-size: 13px;
    margin-top: 4px;
    line-height: 1.5;
}
.cta-box {
    background: #0f1a0f;
    border: 2px solid #2E7D32;
    padding: 40px 32px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-top: 24px;
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

# Access control
def check_access():
    params = st.query_params
    if params.get("subscribed") == "true":
        st.session_state.has_access = True
    return st.session_state.get("has_access", False)

has_access = check_access()

# Header
st.markdown('<p style="text-align:center; color:#2E7D32; font-size:13px; font-weight:bold; letter-spacing:2px">FREE PREVIEW</p>', unsafe_allow_html=True)
st.markdown('<p class="main-header">🌿 CannaIQ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Cannabis Market Intelligence — Calgary, Alberta | ⚡ Updated Daily — market conditions change fast</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666; font-size:14px; margin-bottom:10px">Powered by real-time license filings, store density, and demand signals</p>', unsafe_allow_html=True)

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
st.markdown('<p style="text-align:center; color:#FFD700; font-size:15px; font-weight:bold">💰 These insights can save or make you $100K+ depending on your location decision.</p>', unsafe_allow_html=True)

col_yes, col_no = st.columns(2)

with col_yes:
    st.markdown("""
    <div class="decision-banner-green">
        BEST AREA TO OPEN<br>
        <span style="font-size:28px">Downtown Calgary</span><br>
        <span style="font-size:14px">Lowest competition in the city right now</span><br>
        <span style="font-size:13px; background:#2E7D32; padding:3px 8px; border-radius:10px">#1 Opportunity in Calgary</span><br>
        <span style="font-size:13px; color:#90EE90">Best location for new store entry right now</span>
    </div>
    """, unsafe_allow_html=True)

with col_no:
    st.markdown("""
    <div class="decision-banner-red">
        AVOID THESE AREAS<br>
        <span style="font-size:28px">SW & SE Calgary</span><br>
        <span style="font-size:14px">Highest store density — hardest to compete</span><br>
        <span style="font-size:13px; color:#FFB3B3">High risk — avoid new store entry</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:15px; margin-bottom:10px">
    <span style="background:#333; padding:6px 16px; border-radius:20px; color:#aaa; font-size:13px">
        📊 Confidence: Medium (AGLC + Google data)
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Live Market Alerts
st.subheader("🚨 Live Market Alerts")
st.markdown('<p class="score-explain">Real-time signals from AGLC license filings and market activity.</p>', unsafe_allow_html=True)

col_alert1, col_alert2 = st.columns(2)

with col_alert1:
    st.markdown("""
    <div style="background:#1a1a2e; border-left:4px solid #FF5252; padding:15px; border-radius:8px; margin:5px 0">
        <p style="color:#FF5252; font-weight:bold; margin:0">🚨 New License Application</p>
        <p style="color:#fff; margin:5px 0">New cannabis store application filed in NE Calgary</p>
        <p style="color:#aaa; font-size:12px; margin:0">2 days ago · AGLC Registry</p>
    </div>
    """, unsafe_allow_html=True)

with col_alert2:
    st.markdown("""
    <div style="background:#1a1a2e; border-left:4px solid #FFA500; padding:15px; border-radius:8px; margin:5px 0">
        <p style="color:#FFA500; font-weight:bold; margin:0">⚠️ Saturation Alert</p>
        <p style="color:#fff; margin:5px 0">SW Calgary reached maximum saturation threshold</p>
        <p style="color:#aaa; font-size:12px; margin:0">Updated today · CannaIQ Analysis</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:#111; border:1px solid #333; padding:15px; border-radius:8px; text-align:center; margin-top:10px">
    <p style="color:#aaa; margin:0">🔒 <strong style="color:#2E7D32">Premium subscribers</strong> get real-time alerts for new license applications, competitor openings, and saturation changes in their target areas.</p>
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

st.markdown("""
<div style="background:#111; border:1px solid #2E7D32; padding:15px; border-radius:8px; text-align:center; margin-top:10px">
    <p style="color:#aaa; margin:0">🔒 <strong style="color:#2E7D32">Full location-level insights</strong> — exact street addresses, store performance scores, and expansion signals available in premium version.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Map View — GATED
if has_access:
    st.subheader("🗺️ Calgary Cannabis Store Map")
    st.markdown("Every licensed cannabis store in Calgary — colour coded by performance.")
    try:
        geocoded = pd.read_csv("data/calgary_geocoded.csv" if os.path.exists("data/calgary_geocoded.csv") else "../data/calgary_geocoded.csv")
        geocoded = geocoded.dropna(subset=["lat", "lng"])
        m = folium.Map(location=[51.0447, -114.0719], zoom_start=11)
        for idx, row in geocoded.iterrows():
            if row.get("rating", 0) >= 4.5:
                color = "green"
            elif row.get("rating", 0) >= 4.0:
                color = "orange"
            else:
                color = "red"
            popup_text = f"""
            <b>{row['Establishment Name']}</b><br>
            Rating: {row.get('rating', 'N/A')}<br>
            Reviews: {row.get('review_count', 'N/A')}<br>
            {row.get('Site Address Line 1', '')}
            """
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=200)
            ).add_to(m)
        legend_html = """
        <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                    background: white; padding: 10px; border-radius: 8px;
                    border: 2px solid grey; font-size: 13px;">
            <b>Store Rating</b><br>
            <span style="color:green">●</span> 4.5+ stars<br>
            <span style="color:orange">●</span> 4.0-4.5 stars<br>
            <span style="color:red">●</span> Below 4.0
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        st_folium(m, width=None, height=500)
        st.markdown('<div class="insight-box">📍 Click any store pin to see name, rating and address. Green = top performer, Red = underperformer.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.info("Map data loading...")
else:
    st.markdown("""
    <div style="background:#111; border:2px solid #2E7D32; padding:40px; border-radius:12px; text-align:center; margin:20px 0">
        <p style="font-size:24px; color:#2E7D32; font-weight:bold">🗺️ Interactive Store Map</p>
        <p style="color:#aaa; font-size:16px">See every cannabis store in Calgary plotted on a live map — colour coded by performance rating.</p>
        <p style="color:#555; font-size:14px">🔒 Available to CannaIQ subscribers</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Postal Code Analysis — GATED
if has_access:
    st.subheader("📮 Street Level Intelligence — Postal Code Analysis")
    st.markdown("Drill down beyond quadrants — see opportunity and saturation at postal code level.")
    try:
        postal = pd.read_csv("data/calgary_postal_analysis.csv" if os.path.exists("data/calgary_postal_analysis.csv") else "../data/calgary_postal_analysis.csv")
        col_post1, col_post2 = st.columns(2)
        with col_post1:
            st.markdown("**🎯 Top 10 Opportunity Postal Codes**")
            top_postal = postal.head(10)[["fsa", "store_count", "avg_rating", "opportunity_score"]]
            top_postal.columns = ["Postal Area", "Stores", "Avg Rating", "Opportunity Score"]
            st.dataframe(top_postal, use_container_width=True)
            st.markdown('<div class="insight-box">✅ These postal codes have the lowest competition and strongest entry opportunity in Calgary right now.</div>', unsafe_allow_html=True)
        with col_post2:
            st.markdown("**⚠️ Most Saturated Postal Codes**")
            sat_postal = postal.nlargest(10, "saturation_score")[["fsa", "store_count", "saturation_score"]]
            sat_postal.columns = ["Postal Area", "Stores", "Saturation Score"]
            st.dataframe(sat_postal, use_container_width=True)
            st.markdown('<div class="risk-box">⚠️ These postal codes are overcrowded — new entrants face maximum competition and margin pressure.</div>', unsafe_allow_html=True)
        fig_postal = px.bar(
            postal.head(15).sort_values("opportunity_score"),
            x="opportunity_score",
            y="fsa",
            orientation="h",
            color="opportunity_score",
            color_continuous_scale="RdYlGn",
            title="Top 15 Calgary Postal Areas by Opportunity Score",
            labels={"opportunity_score": "Opportunity Score", "fsa": "Postal Area"}
        )
        fig_postal.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_postal, use_container_width=True)
    except Exception as e:
        st.info("Postal code data loading...")
else:
    st.markdown("""
    <div style="background:#111; border:2px solid #2E7D32; padding:40px; border-radius:12px; text-align:center; margin:20px 0">
        <p style="font-size:24px; color:#2E7D32; font-weight:bold">📮 Street Level Intelligence</p>
        <p style="color:#aaa; font-size:16px">33 Calgary postal codes ranked by opportunity and saturation score — drill down to street level.</p>
        <p style="color:#555; font-size:14px">🔒 Available to CannaIQ subscribers</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Competitive Landscape
st.subheader("🏆 Competitive Landscape")
st.markdown("Who dominates Calgary right now — and where the gaps are.")
st.markdown('<p style="color:#aaa; font-size:13px">Coming soon: top-performing stores & competitor tracking</p>', unsafe_allow_html=True)

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

# Store Intelligence Table — GATED
if has_access:
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
else:
    st.markdown("""
    <div style="background:#111; border:2px solid #2E7D32; padding:40px; border-radius:12px; text-align:center; margin:20px 0">
        <p style="font-size:24px; color:#2E7D32; font-weight:bold">📋 Full Store Intelligence</p>
        <p style="color:#aaa; font-size:16px">Complete database of all 196 Calgary cannabis stores with ratings, addresses, review counts and business status.</p>
        <p style="color:#555; font-size:14px">🔒 Available to CannaIQ subscribers</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# CTA
st.markdown("""
<div class="cta-box">
    <h2>🌿 Get Full CannaIQ Intelligence</h2>
    <p style="font-size:18px">Store-level alerts · Neighbourhood forecasts · Competitor tracking · Canada-wide data</p>
    <p style="font-size:22px; font-weight:bold">Join CannaIQ Beta — Early Access Now Open</p>
    <a href="#" style="background:white; color:#2E7D32; padding:12px 24px; border-radius:25px; font-weight:bold; font-size:18px; text-decoration:none; display:inline-block; margin-bottom:15px">
        🔒 Get real-time alerts, exact locations, and competitor tracking → Join CannaIQ
    </a>
    <p style="font-size:16px; color:#90EE90">Plans starting at $99/month</p>
    <p style="font-size:13px; color:#aaa; margin-top:15px">Data sources: AGLC · Health Canada · Google Maps signals</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Access code + Payment
if not has_access:
    st.markdown("**Already a subscriber?**")
    access_code = st.text_input("Enter your access code", placeholder="cannaiq-XXXXX", type="password")
    if st.button("Unlock Full Access", use_container_width=True):
        if access_code.startswith("cannaiq-"):
            st.session_state.has_access = True
            st.rerun()
        else:
            st.error("Invalid access code. Please contact hello@cannaiqdata.ca")

if st.button("🔒 Get Full Access — Join CannaIQ Beta", use_container_width=True):
    st.session_state.show_payment = True

if st.session_state.get("show_payment"):
    show_payment_page()

st.markdown("<p style='text-align:center;color:#555'>CannaIQ — Cannabis Market Intelligence for Canada | Calgary Beta v1.0</p>", unsafe_allow_html=True)