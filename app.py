import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="akka · Growth Overview",
    page_icon="▦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme colours ───────────────────────────────────────────────────────────────
C = dict(
    blue="#509ee3", green="#67c15e", red="#f86f74",
    yellow="#f5c842", purple="#9b59b6", teal="#1abc9c",
    orange="#f39c12", muted="#64748b", label="#94a3b8",
    border="#e2e8f0", text="#2c3e50",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700;800&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', system-ui, sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2d2d3b !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.75) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] .sidebar-brand {
    color: white !important; font-weight: 800;
}

/* Metric cards */
.metric-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 14px 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    height: 100%;
}
.metric-card.accent-blue { border-top: 3px solid #509ee3; }
.metric-card.accent-red  { border-top: 3px solid #f86f74; }
.metric-card.accent-yellow { border-top: 3px solid #f5c842; }
.metric-card.accent-green  { border-top: 3px solid #67c15e; }
.metric-card.accent-purple { border-top: 3px solid #9b59b6; }

.metric-label {
    font-size: 10px; font-weight: 700; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;
}
.metric-value-large {
    font-size: 36px; font-weight: 800; color: #509ee3;
    letter-spacing: -1px; line-height: 1; margin-bottom: 6px;
}
.metric-value-med {
    font-size: 26px; font-weight: 300; color: #2c3e50;
    letter-spacing: -0.5px; margin-bottom: 6px;
}
.metric-sub { font-size: 10px; color: #94a3b8; margin-top: 6px; }

.pill {
    display: inline-block; font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 4px; white-space: nowrap;
}
.pill-green  { background: #dcfce7; color: #16a34a; }
.pill-red    { background: #fee2e2; color: #dc2626; }
.pill-yellow { background: #fefce8; color: #a16207; }
.pill-grey   { background: #f1f5f9; color: #64748b;  }
.pill-orange { background: #fff7ed; color: #c2410c; }

.section-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.8px; color: #94a3b8;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 10px; margin-top: 4px;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block; margin-right: 4px;
}

.alert-banner {
    background: #fffbeb; border: 1px solid #f5c842;
    border-left: 4px solid #f5c842; border-radius: 6px;
    padding: 9px 14px; font-size: 11px; color: #92400e;
    margin-bottom: 16px;
}

.kpi-row {
    padding: 10px 0; border-bottom: 1px solid #e2e8f0;
}
.kpi-row:last-child { border-bottom: none; }
.kpi-label { font-size: 12px; color: #2c3e50; font-weight: 500; }
.kpi-value { font-size: 14px; font-weight: 700; color: #2c3e50; }
.bench-text { font-size: 9px; color: #94a3b8; line-height: 1.4; margin-top: 3px; }

.card-header {
    padding: 10px 16px; border-bottom: 1px solid #e2e8f0;
    background: #f8fafc; font-size: 11px; font-weight: 700;
    color: #64748b; text-transform: uppercase; letter-spacing: 0.6px;
}
.footer-note {
    font-size: 10px; color: #94a3b8; text-align: right;
    line-height: 1.6; padding-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Data ────────────────────────────────────────────────────────────────────────
trend_data = pd.DataFrame({
    "month": ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"],
    "volume": [355, 400, 370, 440, 490, 510, 480, 550, 590, 640, 710, 840],
    "target": [300, 340, 380, 420, 460, 500, 540, 580, 640, 720, 820, 1000],
})

channels = pd.DataFrame([
    {"Channel": "Organic / SEO",   "New Members": 92,  "Share %": 31, "Est. CAC (€)": 80,  "MoM": "+5%",  "LTV/CAC": "30×", "Recommendation": "Invest more",    "rec_color": "green"},
    {"Channel": "Referral",        "New Members": 72,  "Share %": 24, "Est. CAC (€)": 60,  "MoM": "+12%", "LTV/CAC": "40×", "Recommendation": "Scale urgently",  "rec_color": "green"},
    {"Channel": "Influencer/Club", "New Members": 51,  "Share %": 17, "Est. CAC (€)": 220, "MoM": "→",    "LTV/CAC": "11×", "Recommendation": "Monitor ROI",     "rec_color": "orange"},
    {"Channel": "Paid Social",     "New Members": 83,  "Share %": 28, "Est. CAC (€)": 380, "MoM": "+8%",  "LTV/CAC": "6×",  "Recommendation": "Review spend",    "rec_color": "red"},
])

acq_kpis = [
    ("New members / month",       "298",   C["red"],    60, 75, "+12% MoM · +38% YoY",  "Target: 400/month"),
    ("Lead → member conversion",  "4.2%",  C["red"],    42, 50, "+50% MoM",              "✓ Within fintech SaaS benchmark (3–5%)"),
    ("CAC (blended)",             "€273",  C["red"],    55, 60, "directional",           "Derived: €39/mo × 7mo payback. Attribution ~50% — estimate only."),
    ("Payback period",            "7 mo",  C["green"],  70, 80, "✓ 7mo",                 "✓ Well within SaaS benchmark (<12 months)"),
    ("LTV / CAC ratio",           "8.8×",  C["green"],  88, 30, "strong",                "✓ Excellent. Benchmark: >3× good, >5× great"),
]
ret_kpis = [
    ("Renewal rate — year 1",           "61%",  C["yellow"], 61, 70, "+36pp YoY",    "⚠️ At lower end of benchmark (60–70%). Trend is strong."),
    ("Retention rate — year 2",         "82%",  C["green"],  82, 75, "strong",       "✓ Above benchmark (~75%). Year 2 cohorts are loyal."),
    ("Monthly churn",                   "3.2%", C["red"],    64, 40, "↑ watch",      "⚠️ Above SaaS benchmark (<2%). Key area to address."),
    ("NPS",                             "51",   C["yellow"], 51, 35, "→ stable",     "✓ Above fintech avg (30–40). Target: >60."),
    ("Free lifetime members (3yr+)",    "360",  C["purple"], 12, None,"growing",     "12% of base. Track investing rate for this cohort separately."),
]
eng_kpis = [
    ("MAU",                              "1,920", C["green"], 64, 80, "+8% MoM · +42% YoY",  "⚠️ No automated tracking yet. Manual estimate."),
    ("DAU / MAU ratio",                  "22%",   C["green"], 44, 50, "baseline",             "✓ Within consumer app benchmark (20–25%)."),
    ("% members investing (30d)",        "56%",   C["green"], 56, 70, "+4pp MoM",             "Target: 70%"),
    ("Avg sessions / member / month",    "6.4",   C["green"], 55, 60, "+5% MoM",              "Target: 8 sessions/month"),
    ("Portfolio view freq / member",     "3.1×",  C["teal"],  40, 60, "→",                    "Leading indicator of retention. Target: 5×"),
]
deal_kpis = [
    ("Avg ticket size",                  "€862", C["purple"], 58, 70, "+9% MoM · +22% YoY",  "Target: €1,000"),
    ("Avg investments / member / year",  "6.8",  C["purple"], 68, 70, "→ 7 target",           "Thomas's model assumption: 7×/year. Almost there."),
    ("% members at max allocation",      "22%",  C["purple"], 22, 40, "+3pp MoM",             "Proxy for deal conviction. Target: 40%."),
    ("Deal fill rate",                   "94%",  C["green"],  94, 80, "↑ high",               "✓ Strong. Indicates high member trust in curation."),
    ("Deals funded YTD",                 "19",   C["purple"], 40, 42, "on track",             "~1 deal/week target. On track."),
]

# ── Helpers ─────────────────────────────────────────────────────────────────────

def pill(text: str, style: str = "grey") -> str:
    return f'<span class="pill pill-{style}">{text}</span>'


def kpi_block(kpis: list) -> str:
    html = ""
    for label, value, color, pct, target, delta, bench in kpis:
        bar_html = f"""
        <div style="position:relative;height:5px;background:#e2e8f0;border-radius:3px;margin:4px 0;">
          <div style="position:absolute;height:100%;width:{min(pct,100)}%;background:{color};border-radius:3px;"></div>
          {"" if not target else f'<div style="position:absolute;top:-3px;left:{target}%;width:2px;height:11px;background:#1e293b;opacity:0.2;border-radius:1px;"></div>'}
        </div>"""
        # delta pill colour
        d_lower = delta.lower()
        if any(x in d_lower for x in ["✓","strong","high","on track","growing"]):
            d_style = "green"
        elif any(x in d_lower for x in ["watch","above","⚠️","↑ watch"]):
            d_style = "red"
        elif "directional" in d_lower or "→" in d_lower or "baseline" in d_lower:
            d_style = "grey"
        else:
            d_style = "green" if delta.startswith("+") else "grey"

        html += f"""
        <div class="kpi-row">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
            <span class="kpi-label" style="flex:1">{label}</span>
            <span class="kpi-value">{value}</span>
            {pill(delta, d_style)}
          </div>
          {bar_html}
          <div class="bench-text">{bench}</div>
        </div>"""
    return html


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:14px;">
      <div style="width:32px;height:32px;background:#509ee3;border-radius:7px;
                  display:flex;align-items:center;justify-content:center;
                  font-weight:800;font-size:16px;color:white;">A</div>
      <div>
        <div style="color:white;font-weight:700;font-size:15px;line-height:1;">akka</div>
        <div style="color:rgba(255,255,255,0.35);font-size:9px;margin-top:2px;">Data Studio</div>
      </div>
    </div>
    <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;
                color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:8px;">
      Dashboards
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("▦", "Growth Overview"),
        ("↻", "Retention"),
        ("◈", "Attribution"),
        ("◉", "Member Behaviour"),
        ("◇", "Deal Performance"),
    ]
    nav_sel = st.radio(
        label="nav",
        options=[f"{icon}  {label}" for icon, label in nav_items],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("""
    <div style="margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,0.07);
                font-size:9px;color:rgba(255,255,255,0.25);line-height:1.5;">
      Series A Prep · May 2025<br/>Confidential
    </div>
    """, unsafe_allow_html=True)

# ── Top bar filters ─────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([1.2, 1, 1, 1, 0.6])
with col_f1:
    period = st.selectbox("Period", ["May 2025","Apr 2025","Q1 2025","Last 12 months"], label_visibility="collapsed")
with col_f2:
    market = st.selectbox("Market", ["All markets","France","Spain","Italy","Nordics"], label_visibility="collapsed")
with col_f3:
    cohort = st.selectbox("Cohort", ["All cohorts","Year 1 members","Year 2 members","Year 3+ (free lifetime)"], label_visibility="collapsed")
with col_f4:
    tier = st.selectbox("Tier", ["All tiers","Starter","Premium","Free lifetime"], label_visibility="collapsed")
with col_f5:
    cmp = st.radio("Compare", ["MoM","YoY"], horizontal=True, label_visibility="collapsed")

st.divider()

# ── Page header ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:12px;margin-bottom:8px;">
  <span style="font-size:20px;font-weight:700;color:{C['text']};">Growth Overview</span>
  <span style="font-size:11px;color:{C['label']};">Series A prep · {period} · {market}</span>
</div>
""", unsafe_allow_html=True)

# Alert
st.markdown("""
<div class="alert-banner">
  ⚠️ Marketing attribution at <strong>~50%</strong>. CAC figures are directional only.
  Fixing attribution is <strong>priority #1</strong> for the incoming data function.
</div>
""", unsafe_allow_html=True)

# ── North Star section ──────────────────────────────────────────────────────────
st.markdown(f'<div class="section-label"><span class="dot" style="background:{C["blue"]};"></span>North Star</div>', unsafe_allow_html=True)

ns1, ns2, ns3, ns4 = st.columns([2.2, 1, 1, 1])

with ns1:
    st.markdown(f"""
    <div class="metric-card accent-blue">
      <div class="metric-label">Monthly Invested Volume</div>
      <div class="metric-value-large">€840K</div>
      <div style="display:flex;gap:6px;margin-bottom:4px;">
        {pill("▲ +18% MoM","green")} {pill("▲ +112% YoY","green")}
      </div>
      <div class="metric-sub">Target Q3 2025: €1.2M</div>
      <div style="border-top:1px solid #e2e8f0;margin-top:12px;padding-top:12px;
                  display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:4px;align-items:center;">
        <div style="text-align:center;">
          <div style="font-size:15px;font-weight:700;color:{C['text']};">1,680</div>
          <div style="font-size:9px;color:{C['label']};margin-top:2px;line-height:1.3;">Investing Members</div>
        </div>
        <div style="text-align:center;font-size:18px;font-weight:700;color:{C['label']};">×</div>
        <div style="text-align:center;">
          <div style="font-size:15px;font-weight:700;color:{C['text']};">0.58</div>
          <div style="font-size:9px;color:{C['label']};margin-top:2px;line-height:1.3;">Investments / Member</div>
        </div>
        <div style="text-align:center;font-size:18px;font-weight:700;color:{C['label']};">×</div>
        <div style="text-align:center;">
          <div style="font-size:15px;font-weight:700;color:{C['text']};">€862</div>
          <div style="font-size:9px;color:{C['label']};margin-top:2px;line-height:1.3;">Avg Ticket Size</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

for col, title, value, delta, sub, is_up in [
    (ns2, "Total Members", "3,000",  "▲ +298 MoM", "Goal: 1M users (50% paying)", True),
    (ns3, "ARR",           "€4.1M",  "▲ growing",  "Target raise: €10–15M",       True),
    (ns4, "NPS",           "51",     "→ stable",   "✓ Above fintech avg 30–40",   None),
]:
    p_style = "green" if is_up else "grey"
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{title}</div>
          <div class="metric-value-med">{value}</div>
          {pill(delta, p_style)}
          <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Trend chart ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card-header">Monthly Invested Volume — 12 month trend (€K) · dashed line = target trajectory</div>', unsafe_allow_html=True)

bar_colors = [C["blue"] if i == len(trend_data)-1 else "rgba(80,158,227,0.4)" for i in range(len(trend_data))]

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=trend_data["month"], y=trend_data["volume"],
    marker_color=bar_colors, marker_line_width=0,
    name="Invested Volume", hovertemplate="€%{y}K<extra>Invested Volume</extra>",
))
fig_trend.add_trace(go.Scatter(
    x=trend_data["month"], y=trend_data["target"],
    mode="lines", line=dict(color=C["green"], dash="dash", width=2),
    name="Target", hovertemplate="€%{y}K<extra>Target</extra>",
))
fig_trend.update_layout(
    height=180, margin=dict(l=40, r=10, t=10, b=30),
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(size=10, color=C["label"]),
    xaxis=dict(showgrid=False, tickfont=dict(size=10)),
    yaxis=dict(showgrid=True, gridcolor="#e2e8f0", tickprefix="€", ticksuffix="K",
               tickfont=dict(size=10), gridwidth=1),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10)),
    bargap=0.35,
)
st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

# ── 4 KPI cards ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="section-label">
  <span class="dot" style="background:{C['red']};"></span>Acquisition &nbsp;
  <span class="dot" style="background:{C['yellow']};"></span>Retention &nbsp;
  <span class="dot" style="background:{C['green']};"></span>Product &amp; Engagement &nbsp;
  <span class="dot" style="background:{C['purple']};"></span>Deal Quality
</div>
""", unsafe_allow_html=True)

k1, k2 = st.columns(2)
k3, k4 = st.columns(2)

with k1:
    st.markdown(f"""<div class="metric-card accent-red" style="padding:0;">
      <div class="card-header" style="border-top:none;">
        <span class="dot" style="background:{C['red']};margin-right:4px;"></span>Acquisition KPIs
      </div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 16px 8px;">{kpi_block(acq_kpis)}</div>', unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="metric-card accent-yellow" style="padding:0;">
      <div class="card-header" style="border-top:none;">
        <span class="dot" style="background:{C['yellow']};margin-right:4px;"></span>Retention KPIs
      </div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 16px 8px;">{kpi_block(ret_kpis)}</div>', unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="metric-card accent-green" style="padding:0;">
      <div class="card-header" style="border-top:none;">
        <span class="dot" style="background:{C['green']};margin-right:4px;"></span>Product &amp; Engagement
      </div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 16px 8px;">{kpi_block(eng_kpis)}</div>', unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="metric-card accent-purple" style="padding:0;">
      <div class="card-header" style="border-top:none;">
        <span class="dot" style="background:{C['purple']};margin-right:4px;"></span>Deal Quality &amp; Trust
      </div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 16px 8px;">{kpi_block(deal_kpis)}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Attribution table ───────────────────────────────────────────────────────────
st.markdown(f'<div class="section-label"><span class="dot" style="background:{C["teal"]};"></span>Marketing Attribution</div>', unsafe_allow_html=True)
st.markdown('<div class="card-header">CAC &amp; volume by channel · directional only (~50% attributed) · blended CAC = €273</div>', unsafe_allow_html=True)

# Build styled channel table with Plotly
rec_colors = {"green": ("#dcfce7","#16a34a"), "orange": ("#fff7ed","#c2410c"), "red": ("#fee2e2","#dc2626")}
mom_color  = lambda m: C["green"] if m.startswith("+") else C["muted"]

fig_tbl = go.Figure(data=[go.Table(
    columnwidth=[180, 100, 80, 90, 70, 80, 130],
    header=dict(
        values=["<b>Channel</b>","<b>New Members</b>","<b>Share %</b>",
                "<b>Est. CAC</b>","<b>MoM</b>","<b>LTV/CAC</b>","<b>Recommendation</b>"],
        fill_color="#f8fafc", align="left",
        font=dict(size=10, color=C["muted"]),
        height=32, line_color="#e2e8f0",
    ),
    cells=dict(
        values=[
            channels["Channel"].tolist(),
            channels["New Members"].tolist(),
            [f'{s}%' for s in channels["Share %"].tolist()],
            [f'€{c}' for c in channels["Est. CAC (€)"].tolist()],
            channels["MoM"].tolist(),
            channels["LTV/CAC"].tolist(),
            channels["Recommendation"].tolist(),
        ],
        fill_color=[
            ["white"]*4,
            ["white"]*4,
            ["white"]*4,
            ["white"]*4,
            ["white"]*4,
            ["white"]*4,
            [rec_colors[r][0] for r in channels["rec_color"].tolist()],
        ],
        align="left",
        font=dict(
            size=12,
            color=[
                [C["text"]]*4,
                [C["text"]]*4,
                [C["text"]]*4,
                [C["text"]]*4,
                [mom_color(m) for m in channels["MoM"].tolist()],
                [C["text"]]*4,
                [rec_colors[r][1] for r in channels["rec_color"].tolist()],
            ]
        ),
        height=40, line_color="#e2e8f0",
    )
)])
fig_tbl.update_layout(
    height=230, margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="white",
)
st.plotly_chart(fig_tbl, use_container_width=True, config={"displayModeBar": False})

# ── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  All figures are assumptions based on interviews with Benoît &amp; Thomas · May 2025 · Pending data infrastructure build<br/>
  Benchmarks: Fintech SaaS conversion 3–5% · Monthly churn &lt;2% · LTV/CAC &gt;3× · Payback &lt;12mo · DAU/MAU 20–25% · NPS fintech avg 30–40
</div>
""", unsafe_allow_html=True)
