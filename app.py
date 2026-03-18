"""
══════════════════════════════════════════════════════════════════════
  AFFICIONADO COFFEE ROASTERS
  Sales Trend & Time-Based Performance — Interactive Dashboard
  Built with Streamlit + Plotly
══════════════════════════════════════════════════════════════════════
HOW TO RUN:  streamlit run streamlit_app.py
"""

import os, base64, warnings
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ─── Logo loader ──────────────────────────────────────────────────────────────
# ── Embedded logo URIs (baked in so logos always show even without assets/) ──
_AFF_LOGO_URI = "data:image/avif;base64,AAAAHGZ0eXBhdmlmAAAAAG1pZjFhdmlmbWlhZgAAA1ptZXRhAAAAAAAAACFoZGxyAAAAAAAAAABwaWN0AAAAAAAAAAAAAAAAAAAAAA5waXRtAAAAAAABAAAARmlsb2MAAAAAREAAAwABAAAAAAN+AAEAAAAAAAADsgACAAAAAAcwAAEAAAAAAAARPwADAAAAABhvAAEAAAAAAAAAvgAAAE1paW5mAAAAAAADAAAAFWluZmUCAAAAAAEAAGF2MDEAAAAAFWluZmUCAAAAAAIAAGF2MDEAAAAAFWluZmUCAAABAAMAAEV4aWYAAAACZGlwcnAAAAI+aXBjbwAAAAxhdjFDgQAMAAAAAbRjb2xycklDQwAAAahsY21zAhAAAG1udHJSR0IgWFlaIAfcAAEAGQADACkAOWFjc3BBUFBMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD21gABAAAAANMtbGNtcwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACWRlc2MAAADwAAAAX2NwcnQAAAFMAAAADHd0cHQAAAFYAAAAFHJYWVoAAAFsAAAAFGdYWVoAAAGAAAAAFGJYWVoAAAGUAAAAFHJUUkMAAAEMAAAAQGdUUkMAAAEMAAAAQGJUUkMAAAEMAAAAQGRlc2MAAAAAAAAABWMyY2kAAAAAAAAAAAAAAABjdXJ2AAAAAAAAABoAAADLAckDYwWSCGsL9hA/FVEbNCHxKZAyGDuSRgVRd13ta3B6BYmxmnysab9908PpMP//dGV4dAAAAABDQzAAWFlaIAAAAAAAAPbWAAEAAAAA0y1YWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts8AAAAUaXNwZQAAAAAAAAGQAAAAyAAAABBwaXhpAAAAAAMICAgAAAAMYXYxQ4EAHAAAAAAOcGl4aQAAAAABCAAAADhhdXhDAAAAAHVybjptcGVnOm1wZWdCOmNpY3A6c3lzdGVtczphdXhpbGlhcnk6YWxwaGEAAAAAHmlwbWEAAAAAAAAAAgABBIECAwQAAgSFAwaHAAAAKGlyZWYAAAAAAAAADmF1eGwAAgABAAEAAAAOY2RzYwADAAEAAQAAFbdtZGF0EgAKChgh8fjskBDQaEAyoQdOEsAgAJIC226MumWVHBSj58cqJUVGWgq57FUgTe8hDowGqr/Pen5//K5ewy8yCejEf8qkCdIq////aigGFu//HkjL84QRLCAIl9+///9LHD///TXACFLN0OvMzzcqR+S/////wAAMLl///9b1H//8qEAAGKwgAN3H///////x/AAAARgz/9rnM8TQ78Ylfhcj20pRkiDv/q4auupD/d/6lO12VgspK/1N1pWP/+fYaJ6BQVszyBm/D0wmk9p8W7jet/////////BoAE9A/nyiEIctJJP///4xTR92t0A///////vOASt7///////3yrf//9zoAAAb/h4LaNX6P//////QZE7gwIj/////////+RqQgAAAB/wP///8Bwf//+o2gHIwfqz0zj24SHRPGh3/////giA2UT5MXS+//////9nU4QyAP9Sv////////wFgAAV1mpPgH06C///g6jv///wpuJf0rdAVm/0Pux///8Ts+cHHQtpmxOGvI//6Oeg22uYgFdMD9P/7i5Zq9f8e15tC0UCgCVfpSDl4pgR2S3lViSrnd2+Dj7LRRXIuGITn6sqlWWF+Z54Y8gNZgD+7HIeA9rVrvjE1mpTbi+oh0cbAM0dMcXyYSY5KIXfs7PiVrEXsZRh/VB0GKwmRgcbvWKvR0DuNld5k45kiB7AeHJ+enZeqBAqKGvXQA01+grCuEAnvOEr7l3yhgyNeE9nkJayJWQaf//vp/KDmU/SVki7hQfvfXC/M6HlHfGnP873F9QIetb+n7THGZc9XMIpif8LT/TZJ3ZZvCLiyFYf/8RYSVfe4/gfujeUEVrYbeqtJGhvRDwOR/DlvT713bmnzWCxBl2vUtrByX44/riwxWPIhO31VoRW+fJUDVAACts9lbfePcVz1Jgr8Pq5LOY3zaQhJe5CRIWnYLwAAAACj+AAAACxfgAHEozPLRaxWm/aY+CDLbvGEB1dpP////3sK7B+zgLc1BbMB//x8jeJdqDc8iVAGvDXUCsG/8CB57AuU1KylHC/Ojy07quUHa93+gpwBGtNDRXR+NA7hb9abTrI8VSvsnsQrPR5IWPMWm5ZFveO9smnCKi/9SxA4/HKf43Rd+AG3Zy9M/iGa1plAGRirHscsnKKnj5bMGJv6EjV9YfyEQZKja8XDwZp2hIvF9FGWTQogbO7B0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"
_UM_LOGO_URI  = "data:image/png;base64,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"

def load_logo(filename: str) -> str:
    """
    Returns a base64 data-URI for a logo image.

    Priority:
      1. Reads from  assets/<filename>  next to this script (your local folder).
      2. Falls back to the URI embedded at build-time — logos always show.

    YOUR ASSETS FOLDER (optional — logos work without it too):
        Sales_Trend_Analysis/
        ├── streamlit_app.py
        ├── assets/
        │   ├── Afficiando_coffee_.avif
        │   └── Unified_Mentor.png
        └── data/
    """
    import base64 as _b64
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "assets", filename)
    if os.path.exists(path):
        ext  = filename.rsplit(".", 1)[-1].lower()
        mime = {"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg",
                "avif":"image/avif","webp":"image/webp",
                "svg":"image/svg+xml","ico":"image/x-icon"}.get(ext,"image/png")
        with open(path,"rb") as f:
            return f"data:{mime};base64,{_b64.b64encode(f.read()).decode()}"
    # Embedded fallback
    return {"Afficiando_coffee_.avif": _AFF_LOGO_URI,
             "Unified_Mentor.png":      _UM_LOGO_URI}.get(filename, "")


# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters — Analytics",
    page_icon="☕", layout="wide", initial_sidebar_state="expanded",
)

# ─── Brand Palette ────────────────────────────────────────────────────────────
ESPRESSO   = "#4E342E"
CREAM      = "#F5E6D3"
LATTE      = "#D7CCC8"
DARK_ROAST = "#2C1B14"
GOLD       = "#C7A17A"
# Quantity-mode accent — warm amber/cinnamon, stays 100% in coffee palette
AMBER      = "#D4813A"
AMBER_DARK = "#7A3B1E"
AMBER_FILL = "rgba(212,129,58,0.18)"
PALETTE    = [ESPRESSO, GOLD, LATTE, "#8D6E63", "#A1887F",
              "#6D4C41", "#BCAAA4", "#795548", "#5D4037"]

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  .stApp {{ background-color:{CREAM}; }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{ background-color:{DARK_ROAST} !important; }}
  section[data-testid="stSidebar"] * {{ color:{CREAM} !important; }}
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stMultiSelect label,
  section[data-testid="stSidebar"] .stSlider label,
  section[data-testid="stSidebar"] .stRadio label
    {{ color:{GOLD} !important; font-weight:600; }}

  /* ── Dashboard title banner ── */
  .dash-title-bar {{
      background: linear-gradient(135deg,{DARK_ROAST} 0%,{ESPRESSO} 60%,#6D4C41 100%);
      border-radius:16px;
      padding:18px 28px;
      margin-bottom:18px;
      display:flex;
      align-items:center;
      gap:18px;
  }}
  .dash-title-bar .logos {{
      display:flex;
      align-items:center;
      gap:12px;
      flex-shrink:0;
  }}
  .dash-title-bar .logos img {{
      height:44px;
      border-radius:6px;
      background:#fff;
      padding:4px 6px;
      object-fit:contain;
  }}
  .dash-title-bar .logo-text {{
      font-size:0.75rem;
      font-weight:700;
      color:{GOLD};
      text-align:center;
      line-height:1.2;
  }}
  .dash-title-bar .title-block {{
      flex:1;
      text-align:center;
  }}
  .dash-title-bar .title-main {{
      font-size:1.25rem;
      font-weight:800;
      color:{GOLD};
      line-height:1.3;
      letter-spacing:0.01em;
  }}
  .dash-title-bar .title-sub {{
      font-size:0.8rem;
      color:{LATTE};
      margin-top:3px;
  }}
  .dash-title-bar .logo-right {{
      display:flex;
      align-items:center;
      gap:12px;
      flex-shrink:0;
  }}

  /* ── KPI cards ── */
  .kpi-card {{
      background:{ESPRESSO};
      border-radius:12px;
      padding:18px 22px;
      text-align:center;
      box-shadow:0 4px 12px rgba(0,0,0,0.25);
  }}
  .kpi-value {{ font-size:2rem; font-weight:800; color:{GOLD}; margin:4px 0; }}
  .kpi-label {{ font-size:0.8rem; color:{LATTE}; letter-spacing:0.05em; text-transform:uppercase; }}

  /* Quantity mode — warm amber, never blue */
  .kpi-card.qty-mode {{ background:{AMBER_DARK}; }}
  .kpi-card.qty-mode .kpi-value {{ color:{GOLD}; }}
  .kpi-card.qty-mode .kpi-label {{ color:{LATTE}; }}

  /* ── Page header ── */
  .page-header {{
      background:linear-gradient(135deg,{DARK_ROAST} 0%,{ESPRESSO} 100%);
      padding:22px 30px; border-radius:14px; margin-bottom:22px;
  }}
  .page-header h1 {{ color:{GOLD}; margin:0; font-size:1.7rem; }}
  .page-header p  {{ color:{LATTE}; margin:4px 0 0; font-size:0.92rem; }}

  /* ── Section title ── */
  .section-title {{
      color:{ESPRESSO}; font-size:1.05rem; font-weight:700;
      border-left:4px solid {GOLD}; padding-left:10px; margin:20px 0 8px;
  }}
  /* Quantity mode section title — warm amber border, never teal */
  .section-title.qty {{
      border-left-color:{AMBER}; color:{AMBER_DARK};
  }}
</style>
""", unsafe_allow_html=True)


# ─── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Brewing your data... ☕")
def load_data():
    here    = os.path.dirname(os.path.abspath(__file__))
    cleaned = os.path.join(here, "data", "cleaned_data.csv")
    raw     = os.path.join(here, "data", "raw_data.csv")

    if os.path.exists(cleaned):
        df = pd.read_csv(cleaned, parse_dates=["transaction_date"])
    elif os.path.exists(raw):
        df = pd.read_csv(raw)
        START = datetime(2025,1,1)
        df    = df.sort_values("transaction_id").reset_index(drop=True)
        offs  = (df["transaction_id"]-df["transaction_id"].min()) / \
                (df["transaction_id"].max()-df["transaction_id"].min())*181
        df["transaction_date"] = [START+timedelta(days=int(d)) for d in offs]
        df["hour"]         = pd.to_datetime(df["transaction_time"],format="%H:%M:%S").dt.hour
        df["revenue"]      = df["transaction_qty"]*df["unit_price"]
        df["day_of_week"]  = df["transaction_date"].dt.dayofweek
        df["day_name"]     = df["transaction_date"].dt.day_name()
        df["month"]        = df["transaction_date"].dt.month
        df["month_name"]   = df["transaction_date"].dt.month_name()
        df["week_of_year"] = df["transaction_date"].dt.isocalendar().week.astype(int)
        df["is_weekend"]   = df["day_of_week"].isin([5,6])
        def tb(h):
            if 6<=h<=11:  return "Morning"
            if 12<=h<=16: return "Afternoon"
            if 17<=h<=21: return "Evening"
            return "Late Night"
        df["time_bucket"] = df["hour"].apply(tb)
    else:
        st.error("❌ Data file not found. Please add cleaned_data.csv to the data/ folder.")
        st.stop()
    return df

df_full      = load_data()
DAY_ORDER    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
BUCKET_ORDER = ["Morning","Afternoon","Evening","Late Night"]
ALL_STORES   = sorted(df_full["store_location"].unique().tolist())


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Afficionado Coffee logo at the very top of the sidebar ───────────────
    aff_src = load_logo("Afficiando_coffee_.avif")
    if aff_src:
        # Logo loaded from assets/ — show it centred with a white background pill
        st.markdown(f"""
        <div style='text-align:center;padding:14px 10px 8px;'>
          <img src="{aff_src}"
               style='max-height:80px;max-width:88%;border-radius:12px;
                      background:{DARK_ROAST};padding:10px 14px;
                      object-fit:contain;
                      border:1.5px solid {GOLD};
                      box-shadow:0 3px 12px rgba(0,0,0,0.5);'
               alt='Afficionado Coffee Roasters' />
          <div style='font-size:0.68rem;color:{LATTE};margin-top:5px;
                      letter-spacing:0.05em;'>Afficionado Coffee Roasters</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Fallback when logo file hasn't been placed in assets/ yet
        st.markdown(f"""
        <div style='text-align:center;padding:14px 0 8px;'>
          <div style='display:inline-block;background:{ESPRESSO};color:{GOLD};
               font-size:1.05rem;font-weight:800;padding:10px 18px;
               border-radius:10px;border:2px solid {GOLD};'>☕ Afficionado</div>
          <div style='font-size:0.68rem;color:{LATTE};margin-top:5px;'>
            Place Afficiando_coffee_.avif in assets/ folder</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.selectbox("📂  Navigate",
        ["📈 Sales Trend","📅 Day-of-Week Performance",
         "🕐 Hourly Demand","🏪 Store Comparison"])
    st.markdown("---")
    st.markdown(f"<span style='color:{GOLD};font-weight:600;'>🔽 FILTERS</span>",
                unsafe_allow_html=True)
    store_sel  = st.multiselect("Store Location", ALL_STORES, default=ALL_STORES)
    day_sel    = st.multiselect("Day of Week",    DAY_ORDER,  default=DAY_ORDER)
    hour_range = st.slider("Hour Range", 0, 23, (0,23))
    st.markdown("---")
    st.markdown(f"<span style='color:{GOLD};font-weight:600;'>📊 PRIMARY METRIC</span>",
                unsafe_allow_html=True)
    metric = st.radio("View charts by", ["Revenue ($)", "Quantity"],
        help="Revenue ($): transaction_qty × unit_price\n\nQuantity: total units sold")
    st.markdown("---")
    st.markdown(f"<span style='font-size:0.72rem;color:{LATTE};'>"
                f"Data: 2025  |  {len(df_full):,} transactions</span>",
                unsafe_allow_html=True)


# ─── Metric resolution ────────────────────────────────────────────────────────
# All metric-dependent variables are set here once.
# Quantity mode uses warm amber/cinnamon palette — zero blue/teal.
is_qty  = (metric == "Quantity")
M_COL   = "transaction_qty"  if is_qty else "revenue"
M_LABEL = "Quantity (Units)" if is_qty else "Revenue ($)"
M_SHORT = "Quantity"         if is_qty else "Revenue"
M_FMT   = (lambda v: f"{int(v):,} units") if is_qty else (lambda v: f"${v:,.0f}")
M_FMT_S = (lambda v: f"{v:.2f}")          if is_qty else (lambda v: f"${v:.2f}")
# Accent colour: warm amber for qty, gold for revenue
M_COLOR = AMBER if is_qty else GOLD
M_FILL  = AMBER_FILL if is_qty else "rgba(199,161,122,0.18)"
KPI_CLS = "kpi-card qty-mode" if is_qty else "kpi-card"
ST_CLS  = "section-title qty" if is_qty else "section-title"
# Heatmap colour scale: warm amber→terracotta for qty, cream→espresso for revenue
CS      = ["#FFF8E1","#FFD08A","#D4813A","#7A3B1E"] if is_qty \
     else ["#F5E6D3","#C7A17A","#4E342E","#2C1B14"]
# Monthly bar scale: amber for qty, brown for revenue
BAR_CS  = ["#FFF3E0","#D4813A"] if is_qty else ["#D7CCC8","#4E342E"]

# ─── Apply filters ────────────────────────────────────────────────────────────
df = df_full[
    df_full["store_location"].isin(store_sel) &
    df_full["day_name"].isin(day_sel) &
    df_full["hour"].between(hour_range[0], hour_range[1])
].copy()


# ════════════════════════════════════════════════════════════════════════════════
# DASHBOARD TITLE BANNER  (logos + project title — always visible above KPIs)
# ════════════════════════════════════════════════════════════════════════════════
# Logos are loaded from the local assets/ folder as base64 data-URIs.
# The Afficionado logo lives in the sidebar; only Unified Mentor appears here.

um_src = load_logo("Unified_Mentor.png")

if um_src:
    um_img_html = f"""<img src="{um_src}"
           style='height:58px;border-radius:10px;
                  object-fit:contain;
                  box-shadow:0 3px 10px rgba(0,0,0,0.5);'
           alt='Unified Mentor' />"""
else:
    um_img_html = f"""<div style='background:{ESPRESSO};color:{GOLD};
         font-size:0.78rem;font-weight:700;padding:8px 14px;border-radius:8px;
         border:2px solid {GOLD};text-align:center;line-height:1.3;'>
         Unified<br>Mentor</div>
         <div style='font-size:0.65rem;color:{LATTE};margin-top:3px;'>
         Place Unified_Mentor.png in assets/</div>"""

st.markdown(f"""
<div style='background:linear-gradient(135deg,{DARK_ROAST} 0%,{ESPRESSO} 60%,#6D4C41 100%);
     border-radius:16px; padding:16px 28px; margin-bottom:18px;
     display:flex; align-items:center; gap:20px;'>

  <!-- Left: Unified Mentor logo -->
  <div style='display:flex;flex-direction:column;align-items:center;
              gap:4px;flex-shrink:0;min-width:90px;'>
    {um_img_html}
    <span style='font-size:0.65rem;color:{LATTE};font-weight:600;
                 letter-spacing:0.03em;'>Unified Mentor</span>
  </div>

  <!-- Divider -->
  <div style='width:1px;height:60px;background:rgba(215,204,200,0.25);
              flex-shrink:0;'></div>

  <!-- Centre: project title -->
  <div style='flex:1;text-align:center;padding:0 10px;'>
    <div style='font-size:1.22rem;font-weight:800;color:{GOLD};
                line-height:1.35;letter-spacing:0.01em;'>
      ☕&nbsp; Sales Trend and Time-Based Performance Analysis
    </div>
    <div style='font-size:1.0rem;font-weight:600;color:{LATTE};margin-top:2px;'>
      for Afficionado Coffee Roasters
    </div>
  </div>

</div>
""", unsafe_allow_html=True)
# ─── KPI Cards ────────────────────────────────────────────────────────────────
if is_qty:
    k_vals = [
        ("Total Quantity Sold",  f"{df['transaction_qty'].sum():,.0f} units"),
        ("Total Transactions",   f"{len(df):,}"),
        ("Avg Qty per Order",    f"{df['transaction_qty'].mean():.2f} units"),
        ("Peak Hour (by Qty)",
         f"{int(df.groupby('hour')['transaction_qty'].sum().idxmax()):02d}:00"
         if not df.empty else "—"),
    ]
else:
    peak_h = int(df.groupby("hour")["transaction_id"].count().idxmax()) if not df.empty else 0
    k_vals = [
        ("Total Revenue",      f"${df['revenue'].sum():,.0f}"),
        ("Total Transactions", f"{len(df):,}"),
        ("Avg Order Value",    f"${df['revenue'].mean():.2f}"),
        ("Peak Hour",          f"{peak_h:02d}:00"),
    ]

def kpi_card(lbl, val):
    return (f'<div class="{KPI_CLS}">'
            f'<div class="kpi-label">{lbl}</div>'
            f'<div class="kpi-value">{val}</div></div>')

for c, (lbl, val) in zip(st.columns(4), k_vals):
    with c: st.markdown(kpi_card(lbl, val), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 1 — SALES TREND
# ════════════════════════════════════════════════════════════════════════════════
if "Sales Trend" in page:
    sub = ("Daily units sold & monthly quantity patterns with moving-average smoothing"
           if is_qty else "Daily & monthly revenue patterns with moving-average smoothing")
    st.markdown(f'<div class="page-header"><h1>📈 Sales Trend Dashboard</h1><p>{sub}</p></div>',
                unsafe_allow_html=True)

    # Daily trend + moving averages
    # ── FIX: name output column to match M_COL so daily[M_COL] always resolves ──
    daily = df.groupby("transaction_date").agg(
        revenue=("revenue","sum"),
        transaction_qty=("transaction_qty","sum"),
    ).reset_index()
    daily["active"] = daily[M_COL]
    daily["ma7"]    = daily["active"].rolling(7,  center=True, min_periods=1).mean()
    daily["ma14"]   = daily["active"].rolling(14, center=True, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["transaction_date"], y=daily["active"],
        name=f"Daily {M_SHORT}", mode="lines",
        line=dict(color=LATTE, width=1), fill="tozeroy", fillcolor=M_FILL))
    fig.add_trace(go.Scatter(x=daily["transaction_date"], y=daily["ma7"],
        name="7-day MA", mode="lines", line=dict(color=ESPRESSO, width=2.5)))
    fig.add_trace(go.Scatter(x=daily["transaction_date"], y=daily["ma14"],
        name="14-day MA", mode="lines", line=dict(color=M_COLOR, width=2.5, dash="dash")))
    fig.update_layout(title=f"Daily {M_SHORT} Trend with Moving Averages",
        xaxis_title="Date", yaxis_title=M_LABEL,
        plot_bgcolor=CREAM, paper_bgcolor=CREAM, font_color=DARK_ROAST,
        legend=dict(bgcolor=CREAM, bordercolor=ESPRESSO, borderwidth=1),
        hovermode="x unified", height=400)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="{ST_CLS}">Monthly {M_SHORT}</div>', unsafe_allow_html=True)
        monthly = df.groupby(["month","month_name"])[M_COL].sum().reset_index()
        monthly.columns = ["month","month_name","value"]
        monthly.sort_values("month", inplace=True)
        monthly["growth"] = monthly["value"].pct_change() * 100
        fig_m = px.bar(monthly, x="month_name", y="value",
            color="value", color_continuous_scale=BAR_CS,
            text=monthly["value"].apply(M_FMT),
            labels={"value":M_LABEL,"month_name":"Month"})
        fig_m.update_traces(textposition="outside", textfont_size=10)
        fig_m.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM, font_color=DARK_ROAST,
            coloraxis_showscale=False, showlegend=False, height=340)
        st.plotly_chart(fig_m, use_container_width=True)

    with col2:
        gr_lbl = f"{'Quantity' if is_qty else 'Revenue'} Growth Rate (%)"
        st.markdown(f'<div class="{ST_CLS}">{gr_lbl}</div>', unsafe_allow_html=True)
        mn = monthly.dropna(subset=["growth"])
        fig_g = go.Figure(go.Bar(
            x=mn["month_name"], y=mn["growth"],
            marker_color=[M_COLOR if g >= 0 else "#C62828" for g in mn["growth"]],
            text=mn["growth"].apply(lambda x: f"{x:+.1f}%"), textposition="outside"))
        fig_g.update_layout(yaxis_title="Growth (%)", plot_bgcolor=CREAM,
            paper_bgcolor=CREAM, font_color=DARK_ROAST, height=340)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown(f'<div class="{ST_CLS}">{M_SHORT} by Product Category Over Time</div>',
                unsafe_allow_html=True)
    cm = df.groupby(["month_name","month","product_category"])[M_COL].sum()\
           .reset_index().sort_values("month").rename(columns={M_COL:"value"})
    fig_c = px.line(cm, x="month_name", y="value", color="product_category",
        color_discrete_sequence=PALETTE, markers=True,
        labels={"value":M_LABEL,"month_name":"Month","product_category":"Category"})
    fig_c.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM, font_color=DARK_ROAST,
        height=380, legend=dict(bgcolor=CREAM, bordercolor=ESPRESSO, borderwidth=1))
    st.plotly_chart(fig_c, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DAY-OF-WEEK PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════════
elif "Day-of-Week" in page:
    sub = ("Units sold by day — busiest vs slowest, weekday–weekend comparison"
           if is_qty else "Busiest vs slowest days, weekday–weekend comparison & weekly heatmap")
    st.markdown(f'<div class="page-header"><h1>📅 Day-of-Week Performance</h1><p>{sub}</p></div>',
                unsafe_allow_html=True)

    dow = df.groupby("day_name").agg(
        avg_m=(M_COL,"mean"), total_m=(M_COL,"sum"), txns=("transaction_id","count")
    ).reindex(DAY_ORDER).reset_index()
    wknd_c = [M_COLOR if d in ["Saturday","Sunday"] else ESPRESSO for d in DAY_ORDER]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="{ST_CLS}">Avg {M_SHORT} per Day</div>', unsafe_allow_html=True)
        fig1 = go.Figure(go.Bar(x=dow["day_name"], y=dow["avg_m"],
            marker_color=wknd_c, text=dow["avg_m"].apply(M_FMT_S), textposition="outside"))
        fig1.update_layout(yaxis_title=M_LABEL, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=360,
            annotations=[dict(text="🟠 Weekend" if is_qty else "🟡 Weekend",
                showarrow=False, xref="paper", yref="paper", x=0.98, y=0.95)])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f'<div class="{ST_CLS}">Total {M_SHORT} per Day</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(x=dow["day_name"], y=dow["total_m"],
            marker_color=wknd_c, text=dow["total_m"].apply(M_FMT), textposition="outside"))
        fig2.update_layout(yaxis_title=M_LABEL, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=360)
        st.plotly_chart(fig2, use_container_width=True)

    wk = df.groupby("is_weekend")[M_COL].agg(["sum","mean"]).reset_index()
    wk["label"] = wk["is_weekend"].map({False:"Weekday", True:"Weekend"})
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f'<div class="{ST_CLS}">{M_SHORT} Share: Weekday vs Weekend</div>',
                    unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(labels=wk["label"], values=wk["sum"], hole=0.55,
            marker_colors=[ESPRESSO, M_COLOR], textinfo="label+percent"))
        fig3.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=320, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        avg_ttl = "Avg Qty/Order: Weekday vs Weekend" if is_qty else "Avg Order Value: Weekday vs Weekend"
        y_ttl   = "Avg Qty (Units)" if is_qty else "Avg Order ($)"
        st.markdown(f'<div class="{ST_CLS}">{avg_ttl}</div>', unsafe_allow_html=True)
        fig4 = go.Figure(go.Bar(x=wk["label"], y=wk["mean"],
            marker_color=[ESPRESSO, M_COLOR], text=wk["mean"].apply(M_FMT_S),
            textposition="outside", width=0.4))
        fig4.update_layout(yaxis_title=y_ttl, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=320)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f'<div class="{ST_CLS}">{M_SHORT} Heatmap — Week × Day of Week</div>',
                unsafe_allow_html=True)
    heat = df.pivot_table(values=M_COL, index="week_of_year",
                          columns="day_name", aggfunc="sum")
    heat = heat[[d for d in DAY_ORDER if d in heat.columns]]
    fig5 = px.imshow(heat, color_continuous_scale=CS, aspect="auto",
        labels=dict(x="Day of Week", y="Week of Year", color=M_LABEL))
    fig5.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM,
        font_color=DARK_ROAST, height=400)
    st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 3 — HOURLY DEMAND ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
elif "Hourly" in page:
    sub = ("Units sold per hour — morning rush, midday slowdown, evening peaks"
           if is_qty else "Revenue per hour — morning rush, midday slowdown, evening peaks")
    st.markdown(f'<div class="page-header"><h1>🕐 Hourly Demand Analysis</h1><p>{sub}</p></div>',
                unsafe_allow_html=True)

    # ── FIX: name output column to match M_COL so hourly[M_COL] always resolves ──
    hourly = df.groupby("hour").agg(
        transactions=("transaction_id","count"),
        revenue=("revenue","sum"),
        transaction_qty=("transaction_qty","sum"),
        avg_revenue=("revenue","mean"),
        avg_qty=("transaction_qty","mean"),
    ).reset_index()
    hourly["active"]     = hourly[M_COL]
    hourly["avg_active"] = hourly["avg_qty"] if is_qty else hourly["avg_revenue"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="{ST_CLS}">Transactions per Hour</div>', unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=hourly["hour"], y=hourly["transactions"],
            mode="lines+markers", fill="tozeroy", fillcolor="rgba(78,52,46,0.15)",
            line=dict(color=ESPRESSO, width=3), marker=dict(color=ESPRESSO, size=7)))
        fig1.update_layout(
            xaxis=dict(tickmode="linear", tick0=0, dtick=1, title="Hour of Day"),
            yaxis_title="Transactions", plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=340)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f'<div class="{ST_CLS}">{M_SHORT} per Hour</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=hourly["hour"], y=hourly["active"],
            mode="lines+markers", fill="tozeroy", fillcolor=M_FILL,
            line=dict(color=M_COLOR, width=3), marker=dict(color=M_COLOR, size=7)))
        fig2.update_layout(
            xaxis=dict(tickmode="linear", tick0=0, dtick=1, title="Hour of Day"),
            yaxis_title=M_LABEL, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=340)
        st.plotly_chart(fig2, use_container_width=True)

    # Time bucket bars
    st.markdown(f'<div class="{ST_CLS}">Performance by Time Bucket — {M_SHORT}</div>',
                unsafe_allow_html=True)
    bucket = df.groupby("time_bucket").agg(
        total_m=(M_COL,"sum"), txns=("transaction_id","count"), avg_m=(M_COL,"mean")
    ).reindex([b for b in BUCKET_ORDER if b in df["time_bucket"].unique()]).reset_index()

    avg_lbl = "Avg Qty / Order" if is_qty else "Avg Order ($)"
    col3, col4, col5 = st.columns(3)
    for c, (ck, lbl, fmt) in zip([col3,col4,col5], [
        ("total_m", f"Total {M_SHORT}", M_FMT),
        ("txns",    "Transactions",     lambda v: f"{v:,}"),
        ("avg_m",   avg_lbl,            M_FMT_S),
    ]):
        with c:
            cmap = {"Morning": M_COLOR, "Afternoon": ESPRESSO,
                    "Evening": LATTE, "Late Night": DARK_ROAST}
            fig_b = px.bar(bucket, x="time_bucket", y=ck, color="time_bucket",
                color_discrete_map=cmap, text=bucket[ck].apply(fmt),
                labels={"time_bucket":"Period", ck:lbl})
            fig_b.update_traces(textposition="outside")
            fig_b.update_layout(showlegend=False, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
                font_color=DARK_ROAST, height=320, title=lbl)
            c.plotly_chart(fig_b, use_container_width=True)

    # Hour × Store heatmap
    st.markdown(f'<div class="{ST_CLS}">Hour × Store Heatmap ({M_SHORT})</div>',
                unsafe_allow_html=True)
    phs = df.pivot_table(values=M_COL, index="store_location", columns="hour", aggfunc="sum")
    fig_hs = px.imshow(phs, color_continuous_scale=CS, aspect="auto",
        labels=dict(x="Hour of Day", y="Store", color=M_LABEL))
    fig_hs.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM,
        font_color=DARK_ROAST, height=280)
    st.plotly_chart(fig_hs, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 4 — STORE COMPARISON
# ════════════════════════════════════════════════════════════════════════════════
elif "Store" in page:
    sub = ("Cross-store comparison on units sold, volume, peak hours & categories"
           if is_qty else "Cross-store performance on revenue, volume, peak hours & categories")
    st.markdown(f'<div class="page-header"><h1>🏪 Store Location Comparison</h1><p>{sub}</p></div>',
                unsafe_allow_html=True)

    ss = df.groupby("store_location").agg(
        total_m=(M_COL,"sum"), txns=("transaction_id","count"),
        avg_m=(M_COL,"mean"), avg_qty=("transaction_qty","mean")
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="{ST_CLS}">Total {M_SHORT} by Store</div>', unsafe_allow_html=True)
        fig1 = px.bar(ss, x="store_location", y="total_m", color="store_location",
            color_discrete_sequence=PALETTE, text=ss["total_m"].apply(M_FMT),
            labels={"store_location":"Store","total_m":M_LABEL})
        fig1.update_traces(textposition="outside")
        fig1.update_layout(showlegend=False, plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=350)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f'<div class="{ST_CLS}">{M_SHORT} Share by Store</div>', unsafe_allow_html=True)
        fig2 = px.pie(ss, names="store_location", values="total_m", color="store_location",
            color_discrete_sequence=PALETTE, hole=0.5)
        fig2.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM,
            font_color=DARK_ROAST, height=350)
        st.plotly_chart(fig2, use_container_width=True)

    # Hourly heatmap per store
    st.markdown(f'<div class="{ST_CLS}">Hourly {M_SHORT} Heatmap by Store</div>',
                unsafe_allow_html=True)
    pshr = df.pivot_table(values=M_COL, index="store_location", columns="hour", aggfunc="sum")
    fig3 = px.imshow(pshr, color_continuous_scale=CS, aspect="auto",
        labels=dict(x="Hour", y="Store", color=M_LABEL))
    fig3.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM,
        font_color=DARK_ROAST, height=300)
    st.plotly_chart(fig3, use_container_width=True)

    # Stacked category bar
    st.markdown(f'<div class="{ST_CLS}">{M_SHORT} by Store & Product Category</div>',
                unsafe_allow_html=True)
    sc = df.groupby(["store_location","product_category"])[M_COL].sum().reset_index()
    sc.rename(columns={M_COL:"value"}, inplace=True)
    fig4 = px.bar(sc, x="store_location", y="value", color="product_category",
        color_discrete_sequence=PALETTE, barmode="stack",
        labels={"store_location":"Store","value":M_LABEL,"product_category":"Category"})
    fig4.update_layout(plot_bgcolor=CREAM, paper_bgcolor=CREAM, font_color=DARK_ROAST, height=400,
        legend=dict(bgcolor=CREAM, bordercolor=ESPRESSO, borderwidth=1))
    st.plotly_chart(fig4, use_container_width=True)

    # KPI Radar
    st.markdown(f'<div class="{ST_CLS}">KPI Radar — Store Comparison ({M_SHORT})</div>',
                unsafe_allow_html=True)
    from sklearn.preprocessing import MinMaxScaler
    kc = ["total_m","txns","avg_m","avg_qty"]
    sn = ss.copy()
    sn[kc] = MinMaxScaler().fit_transform(ss[kc])
    rl = [f"Total {M_SHORT}", "Transactions", f"Avg {M_SHORT}/Order", "Avg Qty"]
    fig5 = go.Figure()
    for i, row in sn.iterrows():
        v = row[kc].tolist()
        hx = PALETTE[i].lstrip("#")
        r, g, b = int(hx[:2],16), int(hx[2:4],16), int(hx[4:],16)
        fig5.add_trace(go.Scatterpolar(r=v+[v[0]], theta=rl+[rl[0]], fill="toself",
            name=row["store_location"], line_color=PALETTE[i],
            fillcolor=f"rgba({r},{g},{b},0.15)"))
    fig5.update_layout(
        polar=dict(bgcolor=CREAM,
            radialaxis=dict(visible=True, range=[0,1], gridcolor=LATTE, linecolor=LATTE),
            angularaxis=dict(gridcolor=LATTE, linecolor=LATTE)),
        paper_bgcolor=CREAM, font_color=DARK_ROAST,
        legend=dict(bgcolor=CREAM, bordercolor=ESPRESSO, borderwidth=1), height=420)
    st.plotly_chart(fig5, use_container_width=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
badge = (
    f"<span style='background:{AMBER_DARK};color:{GOLD};padding:3px 12px;"
    f"border-radius:20px;font-size:0.75rem;'>📦 Quantity</span>"
    if is_qty else
    f"<span style='background:{ESPRESSO};color:{GOLD};padding:3px 12px;"
    f"border-radius:20px;font-size:0.75rem;'>💰 Revenue</span>"
)
st.markdown(f"""
<div style='text-align:center;color:{ESPRESSO};font-size:0.85rem;padding:10px;'>
  🚀 Developed by 
  <a href="https://www.linkedin.com/in/sagar-sonali" target="_blank"
  style="color:{ESPRESSO};font-weight:600;text-decoration:none;">
  Sonali Sagar
  </a>
</div>
""", unsafe_allow_html=True)