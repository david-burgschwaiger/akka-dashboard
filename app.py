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
    accent="#64748b",  # monochrome panel accent
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', system-ui, sans-serif; }}

[data-testid="stSidebar"] {{ background-color: #2d2d3b !important; }}
[data-testid="stSidebar"] * {{ color: rgba(255,255,255,0.75) !important; }}

.section-block {{
    margin: 28px 0 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid {C['border']};
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.section-title {{
    font-size: 13px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 1px; color: {C['text']};
}}
.section-sub {{ font-size: 11px; color: {C['muted']}; margin-left: 4px; }}

/* North Star cards */
.ns-card {{
    background: white; border: 1px solid {C['border']}; border-top: 3px solid {C['blue']};
    border-radius: 8px; padding: 14px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}
.ns-label {{
    font-size: 10px; font-weight: 700; color: {C['muted']};
    text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px;
}}
.ns-value-large {{
    font-size: 34px; font-weight: 800; color: {C['blue']};
    letter-spacing: -1px; line-height: 1; margin: 4px 0 6px;
}}
.ns-value-med {{
    font-size: 28px; font-weight: 300; color: {C['text']};
    letter-spacing: -0.5px; margin: 4px 0 6px;
}}
.ns-pills {{ display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 4px; }}
.ns-sub {{ font-size: 10px; color: {C['label']}; margin-top: 5px; }}
.ns-divider {{ border-top: 1px solid {C['border']}; margin: 10px 0; }}

.pill-green {{ display:inline-block; font-size:10px; font-weight:700;
    color:#16a34a; background:#dcfce7; padding:2px 8px; border-radius:4px; }}
.pill-grey {{ display:inline-block; font-size:10px; font-weight:700;
    color:#64748b; background:#f1f5f9; padding:2px 8px; border-radius:4px; }}
.pill-yellow {{ display:inline-block; font-size:10px; font-weight:700;
    color:#92400e; background:#fef9c3; padding:2px 8px; border-radius:4px; }}

.decomp-grid {{
    display:grid; grid-template-columns:1fr auto 1fr auto 1fr;
    gap:4px; align-items:center; padding-top:10px;
}}
.decomp-val {{ font-size:14px; font-weight:700; color:{C['text']}; text-align:center; }}
.decomp-lbl {{ font-size:9px; color:{C['label']}; text-align:center; margin-top:2px; line-height:1.3; }}
.decomp-op {{ font-size:16px; font-weight:700; color:{C['label']}; text-align:center; }}

/* KPI panels — monochrome */
.kpi-panel {{
    border-radius: 8px;
    border: 1px solid {C['border']};
    border-left: 4px solid {C['accent']};
    background: white;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 4px;
    overflow: hidden;
}}
.kpi-panel-header {{
    font-size: 11px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.8px; padding: 10px 14px 8px;
    border-bottom: 1px solid {C['border']};
    background: #f8fafc; color: {C['muted']};
}}
.kpi-panel-body {{ padding: 2px 14px 10px; }}

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

.progress-track {{
    height: 5px; background: {C['border']}; border-radius: 3px;
    margin: 3px 0 8px; overflow: hidden;
}}
.progress-fill {{ height: 100%; border-radius: 3px; background: {C['accent']}; }}

/* Glossary */
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
    {"Channel": "Organic / SEO",   "New Members": 92,  "Share": 31, "CAC": "€80",  "MoM": "+5%",   "LTV/CAC": "30x", "Rec": "Invest more",    "rec": "green"},
    {"Channel": "Referral",        "New Members": 72,  "Share": 24, "CAC": "€60",  "MoM": "+12%",  "LTV/CAC": "40x", "Rec": "Scale urgently", "rec": "green"},
    {"Channel": "Influencer/Club", "New Members": 51,  "Share": 17, "CAC": "€220", "MoM": "+2%",   "LTV/CAC": "11x", "Rec": "Monitor ROI",    "rec": "orange"},
    {"Channel": "Paid Social",     "New Members": 83,  "Share": 28, "CAC": "€380", "MoM": "+8%",   "LTV/CAC": "6x",  "Rec": "Review spend",   "rec": "red"},
]

# (label, value, bar_pct, delta, delta_style)
acq_kpis = [
    ("New members / month",       "298",  60, "+12% MoM · +38% YoY", "green"),
    ("Lead to member conversion", "4.2%", 42, "+50% MoM",             "green"),
    ("CAC (blended)",             "€273", 55, "directional",          "grey"),
    ("LTV / CAC ratio",           "8.8x", 88, "strong",               "green"),
]
ret_kpis = [
    ("Renewal rate — year 1",   "61%",  61, "+36pp YoY", "green"),
    ("Retention rate — year 2", "82%",  82, "strong",    "green"),
    ("Monthly churn",           "3.2%", 64, "watch",     "red"),
    ("NPS",                     "51",   51, "+4pts MoM", "green"),
]
eng_kpis = [
    ("MAU",                           "1,920", 64, "+8% MoM · +42% YoY", "green"),
    ("DAU / MAU ratio",               "22%",   44, "on track",            "green"),
    ("% members investing (30d)",     "56%",   56, "+4pp MoM",            "green"),
    ("Avg sessions / member / month", "6.4",   55, "+5% MoM",             "green"),
]
deal_kpis = [
    ("Avg ticket size",                 "€862", 58, "+9% MoM · +22% YoY", "green"),
    ("Avg investments / member / year", "6.8",  68, "near target",         "yellow"),
    ("% members at max allocation",     "22%",  22, "+3pp MoM",            "green"),
    ("Deal fill rate",                  "94%",  94, "strong",              "green"),
]

glossary = [
    ("Monthly Invested Volume", "Total euros deployed by members into deals in a given month. The North Star metric."),
    ("Investing Members",       "Members who have made at least one investment in the last 30 days."),
    ("ARR",                     "Annualised Recurring Revenue. Membership fee revenue x 12."),
    ("NPS",                     "Net Promoter Score. Members rating 9-10 minus those rating 0-6. Scale: -100 to +100."),
    ("CAC",                     "Customer Acquisition Cost. Total marketing spend divided by new members acquired. ~50% attribution currently."),
    ("LTV",                     "Lifetime Value. Average revenue per member over their full membership duration."),
    ("LTV / CAC",               "Ratio of lifetime value to acquisition cost. >3x = good, >5x = great."),
    ("Renewal rate — year 1",   "Share of year-1 members who renew for year 2. Benchmark: 60-70%."),
    ("Retention rate — year 2", "Share of year-2 members who remain active. Benchmark: ~75%."),
    ("Monthly churn",           "Share of active members who cancel each month. Target: <2%."),
    ("MAU",                     "Monthly Active Users. Members who logged in at least once in the last 30 days."),
    ("DAU / MAU",               "Daily active users divided by monthly active users. Measures engagement stickiness. Benchmark: 20-25%."),
    ("Deal fill rate",          "Share of each deal's target that gets funded by members. High fill rate = strong member conviction."),
    ("Avg ticket size",         "Average euros invested per individual investment transaction. Target: €1,000."),
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def section_header(title, subtitle, dot_color):
    sub_html = f'<span class="section-sub">{subtitle}</span>' if subtitle else ""
    st.markdown(f"""
    <div class="section-block">
      <div class="section-dot" style="background:{dot_color};"></div>
      <span class="section-title">{title}</span>
      {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_kpis(kpis):
    for label, value, pct, delta, d_style in kpis:
        st.markdown(
            f'<div class="kpi-label-row">'
            f'<span class="kpi-lbl">{label}</span>'
            f'<span class="kpi-val">{value}'
            f'<span class="kpi-delta-{d_style}">{delta}</span></span>'
            f'</div>'
            f'<div class="progress-track">'
            f'<div class="progress-fill" style="width:{min(pct,100)}%;"></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

def kpi_panel(title, kpis):
    st.markdown(f"""
    <div class="kpi-panel">
      <div class="kpi-panel-header">{title}</div>
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
with f2: market = st.selectbox("Market", ["All markets","France","Spain","Italy","Nordics"],  label_visibility="collapsed")
with f3: cohort = st.selectbox("Cohort", ["All cohorts","Year 1","Year 2","Year 3+ (free lifetime)"], label_visibility="collapsed")
with f4: tier   = st.selectbox("Tier",   ["All tiers","Starter","Premium","Free lifetime"],   label_visibility="collapsed")
with f5: cmp    = st.radio("Cmp", ["MoM","YoY"], horizontal=True, label_visibility="collapsed")

st.divider()

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="font-size:22px;font-weight:800;color:{C['text']};margin-bottom:16px;">
  Growth Overview
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
      <div class="ns-pills">
        <span class="pill-green">+18% MoM</span>
        <span class="pill-green">+112% YoY</span>
      </div>
      <div class="ns-sub">Target Q3 2025: €1.2M &nbsp;·&nbsp; 70% to target</div>
      <div class="ns-divider"></div>
      <div class="decomp-grid">
        <div><div class="decomp-val">1,680</div><div class="decomp-lbl">Investing Members</div></div>
        <div class="decomp-op">×</div>
        <div><div class="decomp-val">0.58</div><div class="decomp-lbl">Investments / Member</div></div>
        <div class="decomp-op">×</div>
        <div><div class="decomp-val">€862</div><div class="decomp-lbl">Avg Ticket Size</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

ns_cards = [
    (ns2, "Total Members", "3,000",
     [("pill-green", "+298 MoM"), ("pill-green", "+11% YoY")],
     "Goal: 1M users (50% paying)"),
    (ns3, "ARR", "€4.1M",
     [("pill-green", "+22% MoM"), ("pill-green", "+65% YoY")],
     "Target raise: €10-15M"),
    (ns4, "NPS", "51",
     [("pill-green", "+4pts MoM"), ("pill-grey", "-2pts YoY")],
     "Fintech avg: 30-40"),
]
for col, title, value, pills, sub in ns_cards:
    with col:
        pills_html = "".join(f'<span class="{cls}">{txt}</span>' for cls, txt in pills)
        st.markdown(f"""
        <div class="ns-card">
          <div class="ns-label">{title}</div>
          <div class="ns-value-med">{value}</div>
          <div class="ns-pills">{pills_html}</div>
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

# ── Performance Metrics ────────────────────────────────────────────────────────
section_header("Performance Metrics", "Acquisition · Retention · Engagement · Deal Quality", C["accent"])

k1, k2 = st.columns(2)
k3, k4 = st.columns(2)

with k1: kpi_panel("Acquisition",          acq_kpis)
with k2: kpi_panel("Retention",            ret_kpis)
with k3: kpi_panel("Product & Engagement", eng_kpis)
with k4: kpi_panel("Deal Quality & Trust", deal_kpis)

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
            ["white"] * 4, ["white"] * 4, ["white"] * 4, ["white"] * 4,
            ["white"] * 4, ["white"] * 4,
            [rec_fill[r["rec"]] for r in channels],
        ],
        align="left",
        font=dict(
            size=12,
            color=[
                [C["text"]] * 4, [C["text"]] * 4, [C["text"]] * 4, [C["text"]] * 4,
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
