import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="akka · Growth Overview",
    page_icon="▦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colours ────────────────────────────────────────────────────────────────────
C = dict(
    blue="#509ee3", green="#67c15e", red="#f86f74",
    yellow="#e6a817", purple="#9b59b6", teal="#1abc9c",
    orange="#f39c12", muted="#64748b", label="#94a3b8",
    border="#e2e8f0", text="#2c3e50",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', system-ui, sans-serif; }}

[data-testid="stSidebar"] {{ background-color: #2d2d3b !important; }}
[data-testid="stSidebar"] * {{ color: rgba(255,255,255,0.75) !important; }}

/* Section divider headers */
.section-block {{
    margin: 28px 0 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid {C['border']};
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-block .section-dot {{
    width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}}
.section-block .section-title {{
    font-size: 13px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 1px; color: {C['text']};
}}
.section-block .section-sub {{
    font-size: 11px; color: {C['muted']}; margin-left: 4px;
}}

/* KPI card panels */
.kpi-panel {{
    border-radius: 8px;
    border: 1px solid {C['border']};
    border-left-width: 4px;
    background: white;
    padding: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 4px;
}}
.kpi-panel-header {{
    font-size: 11px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.8px; padding: 10px 14px 8px;
    border-bottom: 1px solid {C['border']};
    background: #f8fafc; border-radius: 6px 6px 0 0;
}}
.kpi-panel-body {{ padding: 6px 14px 10px; }}

/* KPI rows */
.kpi-label-row {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 3px; margin-top: 10px;
}}
.kpi-lbl {{ font-size: 12px; color: {C['muted']}; font-weight: 500; }}
.kpi-val {{ font-size: 13px; font-weight: 700; color: {C['text']}; }}

.kpi-delta-green {{ font-size: 10px; font-weight: 700; color: #16a34a;
    background: #dcfce7; padding: 1px 7px; border-radius: 4px; margin-left: 6px; }}
.kpi-delta-red {{ font-size: 10px; font-weight: 700; color: #dc2626;
    background: #fee2e2; padding: 1px 7px; border-radius: 4px; margin-left: 6px; }}
.kpi-delta-yellow {{ font-size: 10px; font-weight: 700; color: #92400e;
    background: #fef9c3; padding: 1px 7px; border-radius: 4px; margin-left: 6px; }}
.kpi-delta-grey {{ font-size: 10px; font-weight: 700; color: #64748b;
    background: #f1f5f9; padding: 1px 7px; border-radius: 4px; margin-left: 6px; }}

/* Progress bar track */
.progress-track {{
    height: 5px; background: {C['border']}; border-radius: 3px;
    margin: 3px 0 10px; overflow: hidden;
}}
.progress-fill {{
    height: 100%; border-radius: 3px;
}}

/* North Star cards */
.ns-card {{
    background: white; border: 1px solid {C['border']}; border-top: 3px solid {C['blue']};
    border-radius: 8px; padding: 14px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); height: 100%;
}}
.ns-value-large {{
    font-size: 36px; font-weight: 800; color: {C['blue']};
    letter-spacing: -1px; line-height: 1; margin: 6px 0;
}}
.ns-value-med {{
    font-size: 26px; font-weight: 300; color: {C['text']};
    letter-spacing: -0.5px; margin: 6px 0;
}}
.ns-label {{ font-size: 10px; font-weight: 700; color: {C['muted']};
    text-transform: uppercase; letter-spacing: 0.6px; }}
.ns-sub {{ font-size: 10px; color: {C['label']}; margin-top: 4px; }}
.pill-green {{ display:inline-block; font-size:10px; font-weight:700;
    color:#16a34a; background:#dcfce7; padding:2px 8px; border-radius:4px; }}
.pill-grey {{ display:inline-block; font-size:10px; font-weight:700;
    color:#64748b; background:#f1f5f9; padding:2px 8px; border-radius:4px; }}
.decomp-grid {{
    display:grid; grid-template-columns:1fr auto 1fr auto 1fr;
    gap:4px; align-items:center; margin-top:12px;
    border-top:1px solid {C['border']}; padding-top:12px;
}}
.decomp-val {{ font-size:15px; font-weight:700; color:{C['text']}; text-align:center; }}
.decomp-lbl {{ font-size:9px; color:{C['label']}; text-align:center; margin-top:2px; line-height:1.3; }}
.decomp-op {{ font-size:18px; font-weight:700; color:{C['label']}; text-align:center; }}

.alert-box {{
    background:#fffbeb; border:1px solid #f5c842; border-left:4px solid #f5c842;
    border-radius:6px; padding:10px 14px; font-size:11px; color:#92400e; margin-bottom:8px;
}}

/* Glossary */
.glossary-grid {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 8px 24px; margin-top: 8px;
}}
.glossary-item {{ padding: 8px 0; border-bottom: 1px solid {C['border']}; }}
.glossary-term {{ font-size: 12px; font-weight: 700; color: {C['text']}; }}
.glossary-def {{ font-size: 11px; color: {C['muted']}; margin-top: 2px; line-height: 1.4; }}

.footer-note {{
    font-size:10px; color:{C['label']}; text-align:right; line-height:1.6; padding:12px 0;
}}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
trend_data = pd.DataFrame({
    "month":  ["Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"],
    "volume": [355, 400, 370, 440, 490, 510, 480, 550, 590, 640, 710, 840],
    "target": [300, 340, 380, 420, 460, 500, 540, 580, 640, 720, 820, 1000],
})

channels = [
    {"Channel": "Organic / SEO",   "New Members": 92,  "Share": 31, "CAC": "€80",  "MoM": "+5%",  "LTV/CAC": "30x", "Rec": "Invest more",    "rec": "green"},
    {"Channel": "Referral",        "New Members": 72,  "Share": 24, "CAC": "€60",  "MoM": "+12%", "LTV/CAC": "40x", "Rec": "Scale urgently", "rec": "green"},
    {"Channel": "Influencer/Club", "New Members": 51,  "Share": 17, "CAC": "€220", "MoM": "stable","LTV/CAC": "11x", "Rec": "Monitor ROI",    "rec": "orange"},
    {"Channel": "Paid Social",     "New Members": 83,  "Share": 28, "CAC": "€380", "MoM": "+8%",  "LTV/CAC": "6x",  "Rec": "Review spend",   "rec": "red"},
]

# (label, value, bar_pct, bar_color, delta, delta_style)
acq_kpis = [
    ("New members / month",       "298",   60, C["red"],    "+12% MoM · +38% YoY", "green"),
    ("Lead to member conversion", "4.2%",  42, C["red"],    "+50% MoM",             "green"),
    ("CAC (blended)",             "€273",  55, C["red"],    "directional",          "grey"),
    ("Payback period",            "7 mo",  70, C["green"],  "7 months",             "green"),
    ("LTV / CAC ratio",           "8.8x",  88, C["green"],  "strong",               "green"),
]
ret_kpis = [
    ("Renewal rate — year 1",         "61%",  61, C["yellow"], "+36pp YoY",  "green"),
    ("Retention rate — year 2",       "82%",  82, C["green"],  "strong",     "green"),
    ("Monthly churn",                 "3.2%", 64, C["red"],    "watch",      "red"),
    ("NPS",                           "51",   51, C["yellow"], "stable",     "yellow"),
    ("Free lifetime members (3yr+)",  "360",  12, C["purple"], "growing",    "green"),
]
eng_kpis = [
    ("MAU",                           "1,920", 64, C["green"], "+8% MoM · +42% YoY", "green"),
    ("DAU / MAU ratio",               "22%",   44, C["green"], "on track",            "green"),
    ("% members investing (30d)",     "56%",   56, C["green"], "+4pp MoM",            "green"),
    ("Avg sessions / member / month", "6.4",   55, C["green"], "+5% MoM",             "green"),
    ("Portfolio view freq / member",  "3.1x",  40, C["teal"],  "stable",              "yellow"),
]
deal_kpis = [
    ("Avg ticket size",                 "€862", 58, C["purple"], "+9% MoM · +22% YoY", "green"),
    ("Avg investments / member / year", "6.8",  68, C["purple"], "near target",         "yellow"),
    ("% members at max allocation",     "22%",  22, C["purple"], "+3pp MoM",            "green"),
    ("Deal fill rate",                  "94%",  94, C["green"],  "strong",              "green"),
    ("Deals funded YTD",                "19",   40, C["purple"], "on track",            "green"),
]

glossary = [
    ("Monthly Invested Volume", "Total euros deployed by members into deals in a given month. The North Star metric."),
    ("Investing Members", "Members who have made at least one investment in the last 30 days."),
    ("ARR", "Annualised Recurring Revenue. Membership fee revenue x 12."),
    ("NPS", "Net Promoter Score. Members rating 9-10 minus those rating 0-6. Scale: -100 to +100."),
    ("CAC", "Customer Acquisition Cost. Total marketing spend divided by new members acquired. ~50% attribution currently."),
    ("LTV", "Lifetime Value. Average revenue per member over their full membership duration."),
    ("LTV / CAC", "Ratio of lifetime value to acquisition cost. >3x = good, >5x = great."),
    ("Payback period", "Months of membership fees required to recover the CAC. Target: <12 months."),
    ("Renewal rate — year 1", "Share of year-1 members who renew for year 2. Benchmark: 60-70%."),
    ("Retention rate — year 2", "Share of year-2 members who remain active. Benchmark: ~75%."),
    ("Monthly churn", "Share of active members who cancel each month. Target: <2%."),
    ("MAU", "Monthly Active Users. Members who logged in at least once in the last 30 days."),
    ("DAU / MAU", "Daily active users divided by monthly active users. Measures engagement stickiness. Benchmark: 20-25%."),
    ("Deal fill rate", "Share of each deal's target that gets funded by members. High fill rate = strong member conviction."),
    ("Free lifetime members", "Members who have been with akka 3+ years and receive free membership. ~12% of base."),
    ("Portfolio view frequency", "Average number of times a member views their portfolio per month. Leading retention indicator."),
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def section_header(title, subtitle, dot_color):
    st.markdown(f"""
    <div class="section-block">
      <div class="section-dot" style="background:{dot_color};"></div>
      <span class="section-title">{title}</span>
      <span class="section-sub">{subtitle}</span>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(kpis):
    for label, value, pct, bar_color, delta, d_style in kpis:
        st.markdown(
            f'<div class="kpi-label-row">'
            f'<span class="kpi-lbl">{label}</span>'
            f'<span class="kpi-val">{value}<span class="kpi-delta-{d_style}">{delta}</span></span>'
            f'</div>'
            f'<div class="progress-track">'
            f'<div class="progress-fill" style="width:{min(pct,100)}%;background:{bar_color};"></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

def kpi_panel(title, header_color, kpis, border_color):
    st.markdown(f"""
    <div class="kpi-panel" style="border-left-color:{border_color};">
      <div class="kpi-panel-header" style="color:{border_color};">{title}</div>
      <div class="kpi-panel-body">
    """, unsafe_allow_html=True)
    render_kpis(kpis)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
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
    st.radio("nav", [
        "Growth Overview", "Retention", "Attribution",
        "Member Behaviour", "Deal Performance",
    ], index=0, label_visibility="collapsed")
    st.markdown("""
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.07);
                font-size:9px;color:rgba(255,255,255,0.25);line-height:1.5;">
      Series A Prep · May 2025<br/>Confidential
    </div>
    """, unsafe_allow_html=True)

# ── Filters ────────────────────────────────────────────────────────────────────
f1, f2, f3, f4, f5 = st.columns([1.2, 1, 1, 1, 0.6])
with f1: period = st.selectbox("Period", ["May 2025","Apr 2025","Q1 2025","Last 12 months"], label_visibility="collapsed")
with f2: market = st.selectbox("Market", ["All markets","France","Spain","Italy","Nordics"], label_visibility="collapsed")
with f3: cohort = st.selectbox("Cohort", ["All cohorts","Year 1","Year 2","Year 3+ (free lifetime)"], label_visibility="collapsed")
with f4: tier   = st.selectbox("Tier",   ["All tiers","Starter","Premium","Free lifetime"], label_visibility="collapsed")
with f5: cmp    = st.radio("Cmp", ["MoM","YoY"], horizontal=True, label_visibility="collapsed")

st.divider()

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:12px;margin-bottom:8px;">
  <span style="font-size:20px;font-weight:800;color:{C['text']};">Growth Overview</span>
  <span style="font-size:11px;color:{C['label']};">Series A prep · {period} · {market}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="alert-box">
  ⚠️ Marketing attribution at <strong>~50%</strong>. CAC figures are directional only.
  Fixing attribution is <strong>priority #1</strong> for the incoming data function.
</div>
""", unsafe_allow_html=True)

# ── North Star ─────────────────────────────────────────────────────────────────
section_header("North Star", "Core business metrics", C["blue"])

ns1, ns2, ns3, ns4 = st.columns([2.2, 1, 1, 1])

with ns1:
    st.markdown(f"""
    <div class="ns-card">
      <div class="ns-label">Monthly Invested Volume</div>
      <div class="ns-value-large">€840K</div>
      <span class="pill-green">+18% MoM</span>&nbsp;<span class="pill-green">+112% YoY</span>
      <div class="ns-sub">Target Q3 2025: €1.2M</div>
      <div class="decomp-grid">
        <div><div class="decomp-val">1,680</div><div class="decomp-lbl">Investing Members</div></div>
        <div class="decomp-op">x</div>
        <div><div class="decomp-val">0.58</div><div class="decomp-lbl">Investments / Member</div></div>
        <div class="decomp-op">x</div>
        <div><div class="decomp-val">€862</div><div class="decomp-lbl">Avg Ticket Size</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

for col, title, value, delta, sub, is_up in [
    (ns2, "Total Members", "3,000", "+298 MoM", "Goal: 1M users (50% paying)", True),
    (ns3, "ARR",           "€4.1M", "growing",  "Target raise: €10-15M",       True),
    (ns4, "NPS",           "51",    "stable",   "Above fintech avg 30-40",     None),
]:
    pill_cls = "pill-green" if is_up else "pill-grey"
    with col:
        st.markdown(f"""
        <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;
                    padding:14px 16px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
          <div class="ns-label">{title}</div>
          <div class="ns-value-med">{value}</div>
          <span class="{pill_cls}">{delta}</span>
          <div class="ns-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Trend chart ────────────────────────────────────────────────────────────────
section_header("Monthly Invested Volume", "12-month trend (€K) · dashed = target trajectory", C["blue"])

bar_colors = [
    "rgba(80,158,227,1)" if i == len(trend_data) - 1 else "rgba(80,158,227,0.4)"
    for i in range(len(trend_data))
]
fig = go.Figure()
fig.add_trace(go.Bar(
    x=trend_data["month"], y=trend_data["volume"],
    marker_color=bar_colors, marker_line_width=0,
    name="Invested Volume",
    hovertemplate="€%{y}K<extra>Invested Volume</extra>",
))
fig.add_trace(go.Scatter(
    x=trend_data["month"], y=trend_data["target"],
    mode="lines", line=dict(color=C["green"], dash="dash", width=2),
    name="Target",
    hovertemplate="€%{y}K<extra>Target</extra>",
))
fig.update_layout(
    height=200, margin=dict(l=40, r=10, t=10, b=30),
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(size=10, color=C["label"]),
    xaxis=dict(showgrid=False, tickfont=dict(size=10)),
    yaxis=dict(showgrid=True, gridcolor="#e2e8f0",
               tickprefix="€", ticksuffix="K", tickfont=dict(size=10)),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, font=dict(size=10)),
    bargap=0.35,
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── KPI panels ─────────────────────────────────────────────────────────────────
section_header("KPI Dashboard", "Acquisition · Retention · Engagement · Deal Quality", C["text"])

k1, k2 = st.columns(2)
k3, k4 = st.columns(2)

with k1:
    kpi_panel("Acquisition KPIs", C["red"], acq_kpis, C["red"])
with k2:
    kpi_panel("Retention KPIs", C["yellow"], ret_kpis, C["yellow"])
with k3:
    kpi_panel("Product & Engagement", C["green"], eng_kpis, C["green"])
with k4:
    kpi_panel("Deal Quality & Trust", C["purple"], deal_kpis, C["purple"])

# ── Attribution table ──────────────────────────────────────────────────────────
section_header("Marketing Attribution", "CAC & volume by channel · directional only (~50% attributed) · blended CAC = €273", C["teal"])

rec_fill = {"green": "#dcfce7", "orange": "#fff7ed", "red": "#fee2e2"}
rec_font = {"green": "#16a34a", "orange": "#c2410c", "red": "#dc2626"}

fig_tbl = go.Figure(data=[go.Table(
    columnwidth=[180, 110, 80, 90, 70, 80, 130],
    header=dict(
        values=["<b>Channel</b>","<b>New Members</b>","<b>Share %</b>",
                "<b>Est. CAC</b>","<b>MoM</b>","<b>LTV/CAC</b>","<b>Recommendation</b>"],
        fill_color="#f8fafc", align="left",
        font=dict(size=10, color=C["muted"]),
        height=32, line_color="#e2e8f0",
    ),
    cells=dict(
        values=[
            [r["Channel"]     for r in channels],
            [r["New Members"] for r in channels],
            [f'{r["Share"]}%' for r in channels],
            [r["CAC"]         for r in channels],
            [r["MoM"]         for r in channels],
            [r["LTV/CAC"]     for r in channels],
            [r["Rec"]         for r in channels],
        ],
        fill_color=[
            ["white"] * 4,
            ["white"] * 4,
            ["white"] * 4,
            ["white"] * 4,
            ["white"] * 4,
            ["white"] * 4,
            [rec_fill[r["rec"]] for r in channels],
        ],
        align="left",
        font=dict(
            size=12,
            color=[
                [C["text"]] * 4,
                [C["text"]] * 4,
                [C["text"]] * 4,
                [C["text"]] * 4,
                [C["green"] if r["MoM"].startswith("+") else C["muted"] for r in channels],
                [C["text"]] * 4,
                [rec_font[r["rec"]] for r in channels],
            ],
        ),
        height=40, line_color="#e2e8f0",
    ),
)])
fig_tbl.update_layout(
    height=230, margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="white",
)
st.plotly_chart(fig_tbl, use_container_width=True, config={"displayModeBar": False})

# ── KPI Glossary ───────────────────────────────────────────────────────────────
section_header("KPI Glossary", "Definitions for all metrics shown in this dashboard", C["muted"])

half = len(glossary) // 2 + len(glossary) % 2
col_a, col_b = st.columns(2)

for col, items in [(col_a, glossary[:half]), (col_b, glossary[half:])]:
    with col:
        for term, definition in items:
            st.markdown(f"""
            <div class="glossary-item">
              <div class="glossary-term">{term}</div>
              <div class="glossary-def">{definition}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
  All figures are assumptions based on interviews with Benoit and Thomas · May 2025 · Pending data infrastructure build<br/>
  Benchmarks: Fintech SaaS conversion 3-5% · Monthly churn &lt;2% · LTV/CAC &gt;3x · Payback &lt;12mo · DAU/MAU 20-25% · NPS fintech avg 30-40
</div>
""", unsafe_allow_html=True)
