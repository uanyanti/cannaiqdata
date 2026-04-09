import streamlit as st
import pandas as pd
import plotly.express as px
import os
from payment import show_payment_page
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="CannaIQ — Cannabis Market Intelligence",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

:root {
  --bg:        #0b0717;
  --bg2:       #110d22;
  --bg3:       #1a1333;
  --border:    rgba(140,110,220,0.18);
  --border2:   rgba(140,110,220,0.32);
  --purple:    #7c3aed;
  --purple2:   #6d28d9;
  --purple-lo: rgba(124,58,237,0.14);
  --gold:      #e8a932;
  --gold-lo:   rgba(232,169,50,0.14);
  --text:      #f0eaff;
  --text2:     #b8a8d8;
  --text3:     #7a6a9a;
  --green:     #4ade80;
  --red:       #f87171;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }
.stApp > header { background-color: var(--bg) !important; }
.main { background-color: var(--bg) !important; }
[data-testid="stAppViewContainer"] { background-color: var(--bg) !important; }
[data-testid="stHeader"] { background-color: var(--bg) !important; }
.main .block-container { max-width: 1100px !important; padding: 2rem 2.5rem !important; margin: 0 auto !important; }

p, label, span, div { color: var(--text2) !important; }
.stMarkdown p { color: var(--text2) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text2) !important; }
input::placeholder { color: var(--text3) !important; }
[data-testid="stTextInput"] label { color: var(--text3) !important; }
[data-testid="stSelectbox"] label { color: var(--text3) !important; }
[data-testid="stSlider"] label { color: var(--text3) !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}

h1, h2, h3 {
  font-family: 'Syne', sans-serif !important;
  color: var(--text) !important;
  font-weight: 700 !important;
  letter-spacing: -0.3px !important;
}

[data-testid="metric-container"] {
  background: var(--bg2) !important;
  border: 0.5px solid var(--border2) !important;
  border-radius: 14px !important;
  padding: 20px !important;
}
[data-testid="metric-container"] label {
  color: var(--text3) !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 32px !important;
  font-weight: 700 !important;
}

[data-testid="stDataFrame"] {
  background: var(--bg2) !important;
  border: 0.5px solid var(--border) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
}

[data-testid="stButton"] button {
  background: var(--purple) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  padding: 10px 24px !important;
  transition: background 0.15s !important;
}
[data-testid="stButton"] button:hover { background: var(--purple2) !important; }

[data-testid="stSelectbox"] > div {
  background: var(--bg2) !important;
  border: 0.5px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
}
[data-testid="stTextInput"] input {
  background: var(--bg2) !important;
  border: 0.5px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  padding: 10px 14px !important;
  font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--purple) !important;
}

[data-testid="stAlert"] {
  background: var(--bg2) !important;
  border: 0.5px solid var(--border) !important;
  border-radius: 10px !important;
}

hr { border-color: var(--border) !important; margin: 28px 0 !important; }

div[data-baseweb="radio"] label { color: var(--text2) !important; }
div[data-baseweb="radio"] [data-checked="true"] { border-color: var(--purple) !important; }

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--purple) !important;
}

@media (max-width: 768px) {
  .main .block-container { padding: 1rem !important; }
}

/* ── Custom Components ────────────────────────── */
.ciq-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0 18px;
  border-bottom: 0.5px solid rgba(140,110,220,0.2);
  margin-bottom: 28px;
}
.ciq-logo {
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #f0eaff;
}
.ciq-logo span { color: #e8a932; }
.ciq-nav-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(74,222,128,0.1);
  border: 0.5px solid rgba(74,222,128,0.3);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  color: #4ade80;
}
.ciq-nav-badge::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4ade80;
  display: inline-block;
}

.ciq-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(232,169,50,0.12);
  border: 0.5px solid rgba(232,169,50,0.3);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 11px;
  color: #e8a932;
  margin-bottom: 10px;
}

.ciq-section-label {
  font-size: 11px;
  font-weight: 500;
  color: #a78bfa;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.decision-banner-green {
  background: var(--bg2);
  border: 0.5px solid rgba(74,222,128,0.3);
  border-top: 3px solid #4ade80;
  padding: 24px 20px;
  border-radius: 14px;
  text-align: center;
  color: #f0eaff;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}
.decision-banner-red {
  background: var(--bg2);
  border: 0.5px solid rgba(248,113,113,0.3);
  border-top: 3px solid #f87171;
  padding: 24px 20px;
  border-radius: 14px;
  text-align: center;
  color: #f0eaff;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}

.insight-box {
  background: var(--bg2);
  border-left: 3px solid #7c3aed;
  padding: 14px 18px;
  border-radius: 0 10px 10px 0;
  color: var(--text2);
  font-size: 13.5px;
  margin-top: 10px;
  line-height: 1.6;
}
.risk-box {
  background: var(--bg2);
  border-left: 3px solid #f87171;
  padding: 14px 18px;
  border-radius: 0 10px 10px 0;
  color: var(--text2);
  font-size: 13.5px;
  margin-top: 10px;
  line-height: 1.6;
}

.alert-card {
  background: var(--bg2);
  border: 0.5px solid var(--border);
  border-radius: 12px;
  padding: 16px 18px;
  margin: 6px 0;
}
.alert-card.danger { border-left: 3px solid #f87171; }
.alert-card.warning { border-left: 3px solid #e8a932; }

.gate-card {
  background: var(--bg2);
  border: 0.5px solid var(--border2);
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
  margin: 16px 0;
}

.cta-box {
  background: var(--bg3);
  border: 0.5px solid var(--border2);
  border-radius: 20px;
  padding: 44px 36px;
  text-align: center;
  margin-top: 24px;
}

.score-explain {
  color: var(--text3);
  font-size: 13px;
  margin-top: 2px;
  line-height: 1.5;
}

.why-matters {
  background: var(--bg2);
  border: 0.5px solid var(--border2);
  padding: 18px 24px;
  border-radius: 12px;
  color: var(--text);
  text-align: center;
  font-size: 15px;
  margin: 12px 0;
}

.confidence-badge {
  display: inline-block;
  background: var(--bg2);
  border: 0.5px solid var(--border);
  padding: 5px 16px;
  border-radius: 20px;
  color: var(--text3);
  font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_calgary():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    enriched = pd.read_csv(os.path.join(base, "data", "calgary_enriched.csv"))
    saturation = pd.read_csv(os.path.join(base, "data", "calgary_saturation_report.csv"))
    postal = pd.read_csv(os.path.join(base, "data", "calgary_postal_analysis.csv"))
    geocoded = pd.read_csv(os.path.join(base, "data", "calgary_geocoded.csv"))
    return enriched, saturation, postal, geocoded

@st.cache_data
def load_edmonton():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    enriched = pd.read_csv(os.path.join(base, "data", "edmonton_enriched.csv"))
    saturation = pd.read_csv(os.path.join(base, "data", "edmonton_saturation_report.csv"))
    postal = pd.read_csv(os.path.join(base, "data", "edmonton_postal_analysis.csv"))
    geocoded = pd.read_csv(os.path.join(base, "data", "edmonton_geocoded.csv"))
    return enriched, saturation, postal, geocoded

# ── Navbar ────────────────────────────────────────────────────
st.markdown("""
<div class="ciq-navbar">
  <div class="ciq-logo">Canna<span>IQ</span></div>
  <div class="ciq-nav-badge">Live data</div>
</div>
""", unsafe_allow_html=True)

# ── City Switcher ─────────────────────────────────────────────
city = st.radio("Select city", ["Calgary", "Edmonton"], horizontal=True)

if city == "Calgary":
    enriched, saturation, postal_data, geocoded_data = load_calgary()
    city_stores = 196
    city_label = "Calgary, Alberta"
    best_area = "Downtown Calgary"
    avoid_area = "SW & SE Calgary"
    map_center = [51.0447, -114.0719]
else:
    enriched, saturation, postal_data, geocoded_data = load_edmonton()
    city_stores = 183
    city_label = "Edmonton, Alberta"
    best_area = "Downtown Edmonton"
    avoid_area = "NW Edmonton"
    map_center = [53.5461, -113.4938]

def check_access():
    params = st.query_params
    if params.get("subscribed") == "true":
        st.session_state.has_access = True
    return st.session_state.get("has_access", False)

has_access = check_access()

# ── Header ────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding: 8px 0 24px">
  <div class="ciq-badge">Alberta cannabis market intelligence · {city_label}</div>
  <h1 style="font-size:38px; font-weight:700; color:#f0eaff; margin:10px 0 8px; line-height:1.15">
    Know where to open<br><span style="color:#e8a932">before your competitors do.</span>
  </h1>
  <p style="font-size:15px; color:#7a6a9a; max-width:520px; margin:0 auto; line-height:1.7">
    Powered by AGLC license filings, Google Maps signals, and real-time store density data.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="why-matters">
  ⚡ <strong style="color:#f0eaff">Avoid costly mistakes</strong>
  <span style="color:#7a6a9a"> — CannaIQ tells you exactly where to open and where to stay away.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Decision Banners ──────────────────────────────────────────
st.markdown('<div class="ciq-section-label">What you should do right now</div>', unsafe_allow_html=True)
st.markdown(f'<p class="score-explain" style="font-size:14px; margin-bottom:14px">Based on competition density and demand gaps in {city} — updated daily.</p>', unsafe_allow_html=True)

col_yes, col_no = st.columns(2)
with col_yes:
    st.markdown(f"""
    <div class="decision-banner-green">
      <div style="font-size:11px; font-weight:500; color:#4ade80; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px">Best area to open</div>
      <div style="font-family:'Syne',sans-serif; font-size:26px; font-weight:700; color:#f0eaff; margin-bottom:6px">{best_area}</div>
      <div style="font-size:13px; color:#b8a8d8">Lowest competition in {city} right now</div>
      <div style="margin-top:10px; display:inline-block; background:rgba(74,222,128,0.12); border:0.5px solid rgba(74,222,128,0.3); border-radius:20px; padding:3px 12px; font-size:12px; color:#4ade80">#1 Opportunity zone</div>
    </div>
    """, unsafe_allow_html=True)

with col_no:
    st.markdown(f"""
    <div class="decision-banner-red">
      <div style="font-size:11px; font-weight:500; color:#f87171; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px">Avoid these areas</div>
      <div style="font-family:'Syne',sans-serif; font-size:26px; font-weight:700; color:#f0eaff; margin-bottom:6px">{avoid_area}</div>
      <div style="font-size:13px; color:#b8a8d8">Highest store density — hardest to compete</div>
      <div style="margin-top:10px; display:inline-block; background:rgba(248,113,113,0.12); border:0.5px solid rgba(248,113,113,0.3); border-radius:20px; padding:3px 12px; font-size:12px; color:#f87171">High risk · avoid entry</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:12px; margin-bottom:4px">
  <span class="confidence-badge">📊 Confidence: Medium — AGLC + Google data</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Live Alerts ───────────────────────────────────────────────
st.markdown('<div class="ciq-section-label">Live market alerts</div>', unsafe_allow_html=True)
st.markdown('<p class="score-explain" style="margin-bottom:12px">Real-time signals from AGLC license filings and market activity.</p>', unsafe_allow_html=True)

col_alert1, col_alert2 = st.columns(2)
with col_alert1:
    st.markdown(f"""
    <div class="alert-card danger">
      <div style="font-size:12px; font-weight:500; color:#f87171; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.06em">New license application</div>
      <div style="font-size:14px; color:#f0eaff; margin-bottom:4px">New cannabis store application filed in {city}</div>
      <div style="font-size:11px; color:#7a6a9a">2 days ago · AGLC Registry</div>
    </div>
    """, unsafe_allow_html=True)

with col_alert2:
    st.markdown(f"""
    <div class="alert-card warning">
      <div style="font-size:12px; font-weight:500; color:#e8a932; margin-bottom:5px; text-transform:uppercase; letter-spacing:0.06em">Saturation alert</div>
      <div style="font-size:14px; color:#f0eaff; margin-bottom:4px">{avoid_area} reached maximum saturation threshold</div>
      <div style="font-size:11px; color:#7a6a9a">Updated today · CannaIQ Analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(124,58,237,0.08); border:0.5px solid rgba(124,58,237,0.25); padding:14px 18px; border-radius:10px; text-align:center; margin-top:10px">
  <span style="color:#7a6a9a; font-size:13px">🔒 <strong style="color:#a78bfa">Premium subscribers</strong> get real-time alerts for new license applications, competitor openings, and saturation changes.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPI Metrics ───────────────────────────────────────────────
st.markdown('<div class="ciq-section-label">Market risk overview</div>', unsafe_allow_html=True)
st.markdown('<p class="score-explain" style="margin-bottom:14px">Rising store count increases competition and reduces margins.</p>', unsafe_allow_html=True)

operational = len(enriched[enriched['business_status'] == 'OPERATIONAL'])
high_comp = len(enriched[enriched['review_count'] > 200])
new_stores = 15 if city == "Calgary" else 12

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total active stores", operational)
with col2:
    st.metric("High competition stores", high_comp)
with col3:
    st.metric("New stores (last 6 months)", new_stores)

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────
st.markdown("""
<div class="insight-box" style="text-align:center; font-size:15px; margin-bottom:16px">
  💰 <strong style="color:#f0eaff">These scores show where you're most likely to win or lose money.</strong>
</div>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans, sans-serif', color='#b8a8d8'),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor='rgba(140,110,220,0.1)', zerolinecolor='rgba(140,110,220,0.15)'),
    yaxis=dict(gridcolor='rgba(140,110,220,0.1)')
)

left, right = st.columns(2)

with left:
    st.markdown('<div class="ciq-section-label">Where not to open</div>', unsafe_allow_html=True)
    st.markdown('<p class="score-explain">Higher score = more saturated = higher risk.</p>', unsafe_allow_html=True)
    fig_sat = px.bar(
        saturation.sort_values("saturation_score", ascending=True),
        x="saturation_score", y="neighbourhood", orientation="h",
        color="saturation_score", color_continuous_scale=["#4ade80", "#e8a932", "#f87171"],
        labels={"saturation_score": "Saturation score", "neighbourhood": "Area"}
    )
    fig_sat.update_layout(**PLOT_LAYOUT)
    fig_sat.update_coloraxes(showscale=False)
    st.plotly_chart(fig_sat, use_container_width=True)
    st.markdown(f'<div class="risk-box">⚠️ {avoid_area} has the highest competition density — expect lower margins and harder customer acquisition.</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="ciq-section-label">Best areas to open</div>', unsafe_allow_html=True)
    st.markdown('<p class="score-explain">Higher score = lower competition + stronger demand signals.</p>', unsafe_allow_html=True)
    fig_opp = px.bar(
        saturation.sort_values("opportunity_score", ascending=True),
        x="opportunity_score", y="neighbourhood", orientation="h",
        color="opportunity_score", color_continuous_scale=["#f87171", "#e8a932", "#4ade80"],
        labels={"opportunity_score": "Opportunity score", "neighbourhood": "Area"}
    )
    fig_opp.update_layout(**PLOT_LAYOUT)
    fig_opp.update_coloraxes(showscale=False)
    st.plotly_chart(fig_opp, use_container_width=True)
    st.markdown(f'<div class="insight-box">✅ {best_area} = highest opportunity score in the city. Low saturation, strong foot traffic, underserved market.</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(124,58,237,0.08); border:0.5px solid rgba(124,58,237,0.25); padding:14px 18px; border-radius:10px; text-align:center; margin-top:10px">
  <span style="color:#7a6a9a; font-size:13px">🔒 <strong style="color:#a78bfa">Full location-level insights</strong> — exact addresses, store performance scores, and expansion signals in premium.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Map (Gated) ───────────────────────────────────────────────
if has_access:
    st.markdown('<div class="ciq-section-label">Interactive store map</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="score-explain" style="margin-bottom:12px">Every licensed cannabis store in {city} — colour coded by performance rating.</p>', unsafe_allow_html=True)
    try:
        geocoded = geocoded_data.dropna(subset=["lat", "lng"])
        m = folium.Map(location=map_center, zoom_start=11, tiles="CartoDB dark_matter")
        for idx, row in geocoded.iterrows():
            rating = row.get("rating", 0)
            if rating >= 4.5:
                color = "#4ade80"
            elif rating >= 4.0:
                color = "#e8a932"
            else:
                color = "#f87171"
            popup_text = f"""
            <b style="color:#1a1333">{row['Establishment Name']}</b><br>
            Rating: {row.get('rating', 'N/A')}<br>
            Reviews: {row.get('review_count', 'N/A')}<br>
            {row.get('Site Address Line 1', '')}
            """
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=8, color=color, fill=True,
                fill_color=color, fill_opacity=0.8,
                popup=folium.Popup(popup_text, max_width=200)
            ).add_to(m)
        legend_html = """
        <div style="position:fixed; bottom:30px; left:30px; z-index:1000;
                    background:#1a1333; border:1px solid rgba(140,110,220,0.3);
                    padding:12px 16px; border-radius:10px; font-size:12px; color:#b8a8d8;">
          <b style="color:#f0eaff">Store rating</b><br>
          <span style="color:#4ade80">●</span> 4.5+ stars<br>
          <span style="color:#e8a932">●</span> 4.0–4.5 stars<br>
          <span style="color:#f87171">●</span> Below 4.0
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        st_folium(m, width=None, height=500)
        st.markdown('<div class="insight-box">📍 Click any store pin to see name, rating, and address. Green = top performer · Red = underperformer.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.info(f"Map data loading... {e}")
else:
    st.markdown(f"""
    <div class="gate-card">
      <div style="font-size:28px; margin-bottom:10px">🗺️</div>
      <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#f0eaff; margin-bottom:8px">Interactive store map</div>
      <div style="color:#7a6a9a; font-size:14px; margin-bottom:12px">See every cannabis store in {city} plotted on a live map — colour coded by performance rating.</div>
      <div style="display:inline-block; background:rgba(124,58,237,0.12); border:0.5px solid rgba(124,58,237,0.3); border-radius:20px; padding:4px 14px; font-size:12px; color:#a78bfa">🔒 Available to subscribers</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Postal Code Analysis (Gated) ──────────────────────────────
if has_access:
    st.markdown('<div class="ciq-section-label">Street level intelligence</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="score-explain" style="margin-bottom:12px">Postal code breakdown — opportunity and saturation at street level in {city}.</p>', unsafe_allow_html=True)
    try:
        postal = postal_data
        col_post1, col_post2 = st.columns(2)
        with col_post1:
            st.markdown("**Top 10 opportunity postal codes**")
            top_postal = postal.head(10)[["fsa", "store_count", "avg_rating", "opportunity_score"]]
            top_postal.columns = ["Postal area", "Stores", "Avg rating", "Opportunity score"]
            st.dataframe(top_postal, use_container_width=True)
            st.markdown(f'<div class="insight-box">✅ These postal codes have the lowest competition and strongest entry opportunity in {city} right now.</div>', unsafe_allow_html=True)
        with col_post2:
            st.markdown("**Most saturated postal codes**")
            sat_postal = postal.nlargest(10, "saturation_score")[["fsa", "store_count", "saturation_score"]]
            sat_postal.columns = ["Postal area", "Stores", "Saturation score"]
            st.dataframe(sat_postal, use_container_width=True)
            st.markdown(f'<div class="risk-box">⚠️ These postal codes are overcrowded — new entrants face maximum competition and margin pressure.</div>', unsafe_allow_html=True)
        fig_postal = px.bar(
            postal.head(15).sort_values("opportunity_score"),
            x="opportunity_score", y="fsa", orientation="h",
            color="opportunity_score",
            color_continuous_scale=["#f87171", "#e8a932", "#4ade80"],
            title=f"Top 15 {city} postal areas by opportunity score",
            labels={"opportunity_score": "Opportunity score", "fsa": "Postal area"}
        )
        fig_postal.update_layout(**PLOT_LAYOUT)
        fig_postal.update_coloraxes(showscale=False)
        st.plotly_chart(fig_postal, use_container_width=True)
    except Exception as e:
        st.info("Postal code data loading...")
else:
    st.markdown(f"""
    <div class="gate-card">
      <div style="font-size:28px; margin-bottom:10px">📮</div>
      <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#f0eaff; margin-bottom:8px">Street level intelligence</div>
      <div style="color:#7a6a9a; font-size:14px; margin-bottom:12px">{city} postal codes ranked by opportunity and saturation — drill down to street level.</div>
      <div style="display:inline-block; background:rgba(124,58,237,0.12); border:0.5px solid rgba(124,58,237,0.3); border-radius:20px; padding:4px 14px; font-size:12px; color:#a78bfa">🔒 Available to subscribers</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Competitive Landscape ─────────────────────────────────────
st.markdown('<div class="ciq-section-label">Competitive landscape</div>', unsafe_allow_html=True)
st.markdown(f'<p class="score-explain" style="margin-bottom:12px">Who dominates {city} right now — and where the gaps are.</p>', unsafe_allow_html=True)

top_stores = enriched[enriched['review_count'] > 50].sort_values("rating", ascending=False).head(20)
fig_stores = px.scatter(
    top_stores, x="review_count", y="rating",
    hover_name="Establishment Name", size="review_count", color="rating",
    color_continuous_scale=["#f87171", "#e8a932", "#4ade80"],
    labels={"review_count": "Number of reviews", "rating": "Google rating"}
)
fig_stores.update_layout(**PLOT_LAYOUT)
fig_stores.update_coloraxes(showscale=False)
st.plotly_chart(fig_stores, use_container_width=True)
top_store = enriched.sort_values("review_count", ascending=False).iloc[0]
st.markdown(f'<div class="insight-box">{top_store["Establishment Name"]} leads with {int(top_store["review_count"])} reviews and a {top_store["rating"]} rating — the benchmark every {city} operator is competing against.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Store Intelligence Table (Gated) ──────────────────────────
if has_access:
    st.markdown('<div class="ciq-section-label">Full store intelligence</div>', unsafe_allow_html=True)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        min_rating = st.slider("Minimum rating", 0.0, 5.0, 4.0, 0.1)
    with col_filter2:
        status_filter = st.selectbox("Business status", ["All", "OPERATIONAL", "CLOSED_PERMANENTLY"])
    filtered = enriched[enriched['rating'] >= min_rating]
    if status_filter != "All":
        filtered = filtered[filtered['business_status'] == status_filter]
    st.dataframe(
        filtered[["Establishment Name", "Address", "rating", "review_count", "business_status"]].sort_values("rating", ascending=False),
        use_container_width=True
    )
else:
    st.markdown(f"""
    <div class="gate-card">
      <div style="font-size:28px; margin-bottom:10px">📋</div>
      <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#f0eaff; margin-bottom:8px">Full store intelligence</div>
      <div style="color:#7a6a9a; font-size:14px; margin-bottom:12px">Complete database of all {city_stores} {city} cannabis stores with ratings, addresses, review counts and business status.</div>
      <div style="display:inline-block; background:rgba(124,58,237,0.12); border:0.5px solid rgba(124,58,237,0.3); border-radius:20px; padding:4px 14px; font-size:12px; color:#a78bfa">🔒 Available to subscribers</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── CTA Box ───────────────────────────────────────────────────
st.markdown(f"""
<div class="cta-box">
  <div class="ciq-badge" style="margin:0 auto 14px; display:inline-flex">Early access now open</div>
  <div style="font-family:'Syne',sans-serif; font-size:30px; font-weight:700; color:#f0eaff; margin-bottom:10px; line-height:1.2">
    Get full CannaIQ intelligence
  </div>
  <p style="font-size:15px; color:#b8a8d8; max-width:460px; margin:0 auto 20px; line-height:1.7">
    Store-level alerts · Neighbourhood forecasts · Competitor tracking · Canada-wide data
  </p>
  <a href="https://buy.stripe.com/4gM28kf5K8Tn3duf4dcEw00" target="_blank"
     style="display:inline-block; background:#7c3aed; color:white; padding:13px 28px;
            border-radius:10px; font-weight:500; font-size:15px; text-decoration:none; margin-bottom:14px">
    Start free trial — CA$199/month
  </a>
  <p style="font-size:13px; color:#7a6a9a">Data sources: AGLC · Health Canada · Google Maps</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Access Code ───────────────────────────────────────────────
if not has_access:
    st.markdown('<div class="ciq-section-label">Already a subscriber?</div>', unsafe_allow_html=True)
    access_code = st.text_input("Enter your access code", placeholder="cannaiq-XXXXX", type="password")
    if st.button("Unlock full access", use_container_width=True):
        if access_code.startswith("cannaiq-"):
            st.session_state.has_access = True
            st.rerun()
        else:
            st.error("Invalid access code. Please contact hello@cannaiqdata.ca")

if st.button("🔒 Get full access — join CannaIQ", use_container_width=True):
    st.session_state.show_payment = True

if st.session_state.get("show_payment"):
    show_payment_page()

st.markdown(f"<p style='text-align:center; color:#3d3060; font-size:12px; margin-top:24px'>CannaIQ — Cannabis Market Intelligence for Canada · {city} · v1.0</p>", unsafe_allow_html=True)