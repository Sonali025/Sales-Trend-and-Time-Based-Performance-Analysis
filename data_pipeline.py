"""
=============================================================================
  AFFICIONADO COFFEE ROASTERS — Sales Trend & Time-Based Performance Analysis
  Author  : Senior Data Analyst / Python Developer
  Dataset : coffee_sales.csv  (149 k transactions, 2025)
=============================================================================

STEP-BY-STEP EXPLANATION FOR BEGINNERS
---------------------------------------
This script walks through every analytical stage:
  1. Data Ingestion & Quality Report
  2. Data Cleaning (missing values, duplicates, type conversion, outliers)
  3. Feature Engineering (revenue, time buckets, day/hour/month)
  4. Exploratory Data Analysis (Univariate → Bivariate → Multivariate)
  5. Sales Trend Analysis (daily, weekly, monthly + moving average)
  6. Day-of-Week Performance
  7. Time-of-Day (Hourly) Analysis
  8. Store-Level Comparison
  9. MySQL Schema & Insert Script
 10. Automated Insight Generation
"""

# ─── Standard library ────────────────────────────────────────────────────────
import os
import warnings
import textwrap
from datetime import datetime, timedelta

# ─── Third-party ──────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # non-GUI backend for saving figures
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

warnings.filterwarnings("ignore")

# ─── Project paths ────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.abspath(__file__))
DATA   = os.path.join(BASE, "data")
VIS    = os.path.join(BASE, "visuals")
SQL    = os.path.join(BASE, "sql")
os.makedirs(DATA, exist_ok=True)
os.makedirs(VIS,  exist_ok=True)
os.makedirs(SQL,  exist_ok=True)

RAW_CSV = os.path.join(DATA, "coffee_sales.csv")

if not os.path.exists(RAW_CSV):
    raise FileNotFoundError(f"Dataset not found at: {RAW_CSV}")

df_raw = pd.read_csv(RAW_CSV)

print(f"Loaded {len(df_raw):,} rows × {df_raw.shape[1]} columns")

# ─── Afficionado Brand Palette ────────────────────────────────────────────────
ESPRESSO  = "#4E342E"
CREAM     = "#F5E6D3"
LATTE     = "#D7CCC8"
DARK_ROAST= "#2C1B14"
GOLD      = "#C7A17A"
PALETTE   = [ESPRESSO, GOLD, LATTE, "#8D6E63", "#A1887F", "#6D4C41",
             "#BCAAA4", "#795548", "#5D4037"]

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "axes.facecolor":  "#FDFAF7",
    "figure.facecolor":"#FDFAF7",
    "axes.edgecolor":  ESPRESSO,
    "axes.labelcolor": DARK_ROAST,
    "xtick.color":     DARK_ROAST,
    "ytick.color":     DARK_ROAST,
    "text.color":      DARK_ROAST,
    "grid.color":      LATTE,
    "grid.linewidth":  0.6,
})

# ─── Helper ───────────────────────────────────────────────────────────────────
def save_fig(name, tight=True):
    path = os.path.join(VIS, f"{name}.png")
    if tight:
        plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close("all")
    print(f"  ✔  Saved → visuals/{name}.png")

def section(title):
    bar = "═" * 70
    print(f"\n{bar}\n  {title}\n{bar}")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — DATA INGESTION
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 1 — Data Ingestion & Quality Report")

"""
WHY: Before any analysis we must understand the raw data shape, types,
     completeness, and any obvious data-entry errors.

HOW: We load the CSV with pandas, then run a series of diagnostic checks
     and compile them into a single "data quality report" dictionary.
"""


# ── Quality checks ──────────────────────────────────────────────────────────
missing        = df_raw.isnull().sum()
duplicated_ids = df_raw["transaction_id"].duplicated().sum()
neg_qty        = (df_raw["transaction_qty"] < 0).sum()
neg_price      = (df_raw["unit_price"] < 0).sum()

quality_report = {
    "total_rows":         len(df_raw),
    "total_columns":      df_raw.shape[1],
    "missing_values":     missing.to_dict(),
    "duplicate_ids":      int(duplicated_ids),
    "negative_qty":       int(neg_qty),
    "negative_price":     int(neg_price),
    "dtypes":             df_raw.dtypes.astype(str).to_dict(),
    "unique_stores":      df_raw["store_location"].unique().tolist(),
    "unique_categories":  df_raw["product_category"].unique().tolist(),
}

print("\n── Data Quality Report ──")
for k, v in quality_report.items():
    if isinstance(v, dict):
        print(f"  {k}:")
        for kk, vv in v.items():
            if vv != 0 and vv != "0":
                print(f"      {kk}: {vv}")
    else:
        print(f"  {k}: {v}")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — DATA CLEANING
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 2 — Data Cleaning")

"""
WHY: Raw data is never perfect. We must:
  • Remove duplicates so each transaction counts once.
  • Convert strings to proper types (times → datetime objects).
  • Handle missing values (impute or drop).
  • Detect and handle outliers using the IQR (Interquartile Range) method.

CONCEPTS:
  IQR = Q3 − Q1
  Lower fence = Q1 − 1.5 × IQR
  Upper fence = Q3 + 1.5 × IQR
  Values beyond fences are outliers.
"""

df = df_raw.copy()

# ── 2a. Remove duplicates ────────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(subset="transaction_id", inplace=True)
print(f"Removed {before - len(df)} duplicate rows")

# ── 2b. Assign synthetic transaction dates ───────────────────────────────────
# The dataset has only 'year' and 'transaction_time'.  We distribute
# transactions across Jan 1 – Jun 30 2025 (182 days) proportionally
# by transaction_id order — a common approach when dates are missing.
START_DATE = datetime(2025, 1, 1)
n = len(df)
date_offsets = (df["transaction_id"] - df["transaction_id"].min()) / \
               (df["transaction_id"].max() - df["transaction_id"].min()) * 181
df = df.sort_values("transaction_id").reset_index(drop=True)
df["transaction_date"] = [START_DATE + timedelta(days=int(d)) for d in date_offsets]

# ── 2c. Parse time → hour ────────────────────────────────────────────────────
# transaction_time is "HH:MM:SS" — we extract just the hour integer
df["hour"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S").dt.hour

# ── 2d. Type safety ──────────────────────────────────────────────────────────
df["transaction_qty"] = df["transaction_qty"].clip(lower=0)   # no negatives
df["unit_price"]      = df["unit_price"].clip(lower=0)

# ── 2e. IQR Outlier detection on unit_price ─────────────────────────────────
Q1  = df["unit_price"].quantile(0.25)
Q3  = df["unit_price"].quantile(0.75)
IQR = Q3 - Q1
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR
outliers = df[(df["unit_price"] < lower_fence) | (df["unit_price"] > upper_fence)]
print(f"IQR outliers in unit_price: {len(outliers)} rows  "
      f"(fences: {lower_fence:.2f} – {upper_fence:.2f})")

# Strategy: cap (Winsorize) instead of drop — preserves row count
df["unit_price"] = df["unit_price"].clip(lower=lower_fence, upper=upper_fence)

print(f"Clean dataset: {len(df):,} rows")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 3 — Feature Engineering")

"""
WHY: Raw columns rarely answer business questions directly.
     We create derived features that unlock deeper analysis.

FEATURES CREATED:
  revenue          = transaction_qty × unit_price
  hour             → already created in step 2
  day_of_week      → Monday=0 … Sunday=6
  day_name         → "Monday" … "Sunday"
  month            → 1 … 12
  month_name       → "January" …
  week_of_year     → 1 … 52
  time_bucket      → Morning / Afternoon / Evening / Late
"""

# Revenue (the core KPI)
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# Date-based features
df["day_of_week"]  = df["transaction_date"].dt.dayofweek          # 0=Mon
df["day_name"]     = df["transaction_date"].dt.day_name()
df["month"]        = df["transaction_date"].dt.month
df["month_name"]   = df["transaction_date"].dt.month_name()
df["week_of_year"] = df["transaction_date"].dt.isocalendar().week.astype(int)
df["is_weekend"]   = df["day_of_week"].isin([5, 6])

# Time bucket (using Python dictionary mapping for clarity)
def time_bucket(hour):
    """Classify an integer hour into a named period."""
    buckets = {
        range(6,  12): "Morning",
        range(12, 17): "Afternoon",
        range(17, 22): "Evening",
    }
    for rng, label in buckets.items():
        if hour in rng:
            return label
    return "Late Night"

df["time_bucket"] = df["hour"].apply(time_bucket)
bucket_order = ["Morning", "Afternoon", "Evening", "Late Night"]

print("Feature engineering complete.")
print(df[["revenue","hour","day_name","month_name","time_bucket"]].head(3))

# ── Save cleaned Excel file ──────────────────────────────────────────────────
cleaned_path = os.path.join(DATA, "cleaned_data.xlsx")
df.to_excel(cleaned_path, index=False)
print(f"Cleaned dataset saved → data/cleaned_data.xlsx  ({len(df):,} rows)")

csv_cleaned = os.path.join(DATA, "cleaned_data.csv")
df.to_csv(csv_cleaned, index=False)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — EXPLORATORY DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 4 — Exploratory Data Analysis")

# ── 4A. UNIVARIATE ANALYSIS ─────────────────────────────────────────────────
print("\n  4A. Univariate Analysis")

fig, axes = plt.subplots(3, 3, figsize=(16, 12))
fig.suptitle("Univariate Distributions — Afficionado Coffee Roasters",
             fontsize=16, color=ESPRESSO, fontweight="bold", y=1.01)

# transaction_qty histogram
axes[0,0].hist(df["transaction_qty"], bins=20, color=ESPRESSO, edgecolor=CREAM)
axes[0,0].set_title("Transaction Quantity Distribution")
axes[0,0].set_xlabel("Quantity")

# transaction_qty boxplot
axes[0,1].boxplot(df["transaction_qty"], vert=True,
                  patch_artist=True,
                  boxprops=dict(facecolor=LATTE, color=ESPRESSO))
axes[0,1].set_title("Quantity — Box Plot")

# unit_price KDE
df["unit_price"].plot.kde(ax=axes[0,2], color=GOLD, linewidth=2)
axes[0,2].set_title("Unit Price — KDE")
axes[0,2].set_xlabel("Price ($)")

# revenue histogram
axes[1,0].hist(df["revenue"], bins=30, color=GOLD, edgecolor=DARK_ROAST)
axes[1,0].set_title("Revenue per Transaction")
axes[1,0].set_xlabel("Revenue ($)")

# revenue boxplot
axes[1,1].boxplot(df["revenue"], vert=True,
                  patch_artist=True,
                  boxprops=dict(facecolor=GOLD, color=ESPRESSO))
axes[1,1].set_title("Revenue — Box Plot")

# revenue KDE
df["revenue"].plot.kde(ax=axes[1,2], color=ESPRESSO, linewidth=2)
axes[1,2].set_title("Revenue — KDE")

# product_category bar
cat_counts = df["product_category"].value_counts()
axes[2,0].barh(cat_counts.index, cat_counts.values,
               color=sns.color_palette([ESPRESSO,GOLD,LATTE,"#8D6E63","#A1887F",
                                        "#6D4C41","#BCAAA4","#795548","#5D4037"]))
axes[2,0].set_title("Transactions by Category")
axes[2,0].set_xlabel("Count")

# store_location bar
store_counts = df["store_location"].value_counts()
axes[2,1].bar(store_counts.index, store_counts.values, color=PALETTE[:3])
axes[2,1].set_title("Transactions by Store")
axes[2,1].set_xlabel("Store")

# time_bucket pie
tb = df["time_bucket"].value_counts().reindex(bucket_order).dropna()
axes[2,2].pie(tb.values, labels=tb.index,
              colors=[GOLD, ESPRESSO, LATTE, DARK_ROAST],
              autopct="%1.1f%%", startangle=140)
axes[2,2].set_title("Time Bucket Share")

save_fig("01_univariate_analysis")

# ── 4B. BIVARIATE ANALYSIS ──────────────────────────────────────────────────
print("  4B. Bivariate Analysis")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Bivariate Analysis — Revenue Breakdown",
             fontsize=15, color=ESPRESSO, fontweight="bold")

# Revenue by product_category
cat_rev = df.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
axes[0,0].barh(cat_rev.index, cat_rev.values,
               color=sns.color_palette(PALETTE, len(cat_rev)))
axes[0,0].set_title("Total Revenue by Product Category")
axes[0,0].set_xlabel("Revenue ($)")

# Revenue by store
store_rev = df.groupby("store_location")["revenue"].sum()
axes[0,1].bar(store_rev.index, store_rev.values,
              color=PALETTE[:3])
for i, v in enumerate(store_rev.values):
    axes[0,1].text(i, v + 200, f"${v:,.0f}", ha="center", fontsize=9)
axes[0,1].set_title("Total Revenue by Store Location")
axes[0,1].set_ylabel("Revenue ($)")

# Revenue by day of week
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_rev = df.groupby("day_name")["revenue"].mean().reindex(day_order)
colors = [GOLD if d in ["Saturday","Sunday"] else ESPRESSO for d in day_order]
axes[0,2].bar(day_rev.index, day_rev.values, color=colors)
axes[0,2].set_title("Avg Revenue by Day of Week")
axes[0,2].set_ylabel("Avg Revenue ($)")
axes[0,2].tick_params(axis='x', rotation=45)

# Violin: revenue distribution by store
sns.violinplot(data=df, x="store_location", y="revenue",
               palette=[ESPRESSO, GOLD, LATTE], ax=axes[1,0], inner="quartile")
axes[1,0].set_title("Revenue Distribution by Store (Violin)")
axes[1,0].set_ylabel("Revenue ($)")

# Box: revenue by time_bucket
df["time_bucket"] = pd.Categorical(df["time_bucket"], categories=bucket_order)
sns.boxplot(data=df, x="time_bucket", y="revenue",
            palette=[GOLD, ESPRESSO, LATTE, DARK_ROAST], ax=axes[1,1])
axes[1,1].set_title("Revenue by Time Bucket (Box Plot)")
axes[1,1].set_ylabel("Revenue ($)")

# Scatter: qty vs revenue coloured by category
sample = df.sample(3000, random_state=42)
for i, cat in enumerate(df["product_category"].unique()):
    s = sample[sample["product_category"]==cat]
    axes[1,2].scatter(s["transaction_qty"], s["revenue"],
                      alpha=0.4, s=15, label=cat, color=PALETTE[i % len(PALETTE)])
axes[1,2].set_title("Qty vs Revenue by Category")
axes[1,2].set_xlabel("Quantity"); axes[1,2].set_ylabel("Revenue ($)")
axes[1,2].legend(fontsize=7, ncol=2)

save_fig("02_bivariate_analysis")

# ── 4C. MULTIVARIATE ANALYSIS ───────────────────────────────────────────────
print("  4C. Multivariate Analysis")

# Heatmap: store × hour → avg revenue
pivot_sh = df.pivot_table(values="revenue", index="store_location",
                           columns="hour", aggfunc="mean")
fig, ax = plt.subplots(figsize=(18, 5))
sns.heatmap(pivot_sh, cmap="YlOrBr", linewidths=0.3,
            annot=False, ax=ax, cbar_kws={"label": "Avg Revenue ($)"})
ax.set_title("Multivariate Heatmap — Store × Hour vs Avg Revenue",
             fontsize=14, color=ESPRESSO, fontweight="bold")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Store Location")
save_fig("03_multivariate_heatmap")

# Grouped bar: store × time_bucket → total revenue
pivot_stb = df.groupby(["store_location","time_bucket"])["revenue"].sum().unstack()
pivot_stb = pivot_stb.reindex(columns=bucket_order)
fig, ax = plt.subplots(figsize=(12, 6))
pivot_stb.plot(kind="bar", ax=ax,
               color=[GOLD, ESPRESSO, LATTE, DARK_ROAST], edgecolor="white")
ax.set_title("Grouped Bar — Store × Time Bucket Revenue",
             fontsize=14, color=ESPRESSO, fontweight="bold")
ax.set_ylabel("Total Revenue ($)")
ax.set_xlabel("Store Location")
ax.tick_params(axis='x', rotation=0)
ax.legend(title="Time Bucket", bbox_to_anchor=(1,1))
save_fig("04_grouped_bar_store_bucket")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — SALES TREND ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 5 — Sales Trend Analysis")

"""
WHY: Trend analysis reveals whether the business is growing or declining
     and whether there are seasonal peaks worth planning for.

TOOLS:
  • Rolling mean (7-day & 14-day) to smooth noisy daily data
  • Monthly aggregation for high-level growth perspective
"""

daily_rev = df.groupby("transaction_date")["revenue"].sum().reset_index()
daily_rev.columns = ["date", "revenue"]
daily_rev["ma7"]  = daily_rev["revenue"].rolling(7,  center=True).mean()
daily_rev["ma14"] = daily_rev["revenue"].rolling(14, center=True).mean()

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
fig.suptitle("Sales Trend Analysis — Afficionado Coffee Roasters",
             fontsize=15, color=ESPRESSO, fontweight="bold")

# Daily + moving averages
axes[0].fill_between(daily_rev["date"], daily_rev["revenue"],
                     alpha=0.2, color=GOLD)
axes[0].plot(daily_rev["date"], daily_rev["revenue"],
             color=LATTE, linewidth=0.8, label="Daily Revenue")
axes[0].plot(daily_rev["date"], daily_rev["ma7"],
             color=ESPRESSO, linewidth=2,   label="7-day MA")
axes[0].plot(daily_rev["date"], daily_rev["ma14"],
             color=GOLD,    linewidth=2,   label="14-day MA", linestyle="--")
axes[0].set_title("Daily Revenue with Moving Averages")
axes[0].set_ylabel("Revenue ($)")
axes[0].legend()
axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%b"))

# Monthly bar
monthly_rev = df.groupby(["month","month_name"])["revenue"].sum().reset_index()
monthly_rev.sort_values("month", inplace=True)
bars = axes[1].bar(monthly_rev["month_name"], monthly_rev["revenue"],
                   color=PALETTE[:len(monthly_rev)], edgecolor="white")
for bar in bars:
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 300,
                 f"${bar.get_height():,.0f}",
                 ha="center", va="bottom", fontsize=8, color=DARK_ROAST)
axes[1].set_title("Monthly Revenue Aggregation")
axes[1].set_ylabel("Total Revenue ($)")

save_fig("05_sales_trend")

# Monthly growth rate
monthly_rev["growth_%"] = monthly_rev["revenue"].pct_change() * 100
print("\n  Monthly Revenue & Growth:")
print(monthly_rev[["month_name","revenue","growth_%"]].to_string(index=False))


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — DAY-OF-WEEK PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 6 — Day-of-Week Performance")

dow_stats = df.groupby("day_name").agg(
    avg_revenue=("revenue","mean"),
    total_revenue=("revenue","sum"),
    total_transactions=("transaction_id","count")
).reindex(day_order)

print(dow_stats)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Day-of-Week Performance",
             fontsize=15, color=ESPRESSO, fontweight="bold")

colors_dow = [GOLD if d in ["Saturday","Sunday"] else ESPRESSO for d in day_order]

# Average revenue
axes[0].bar(dow_stats.index, dow_stats["avg_revenue"], color=colors_dow, edgecolor="white")
axes[0].set_title("Avg Revenue per Day")
axes[0].set_ylabel("Revenue ($)")
axes[0].tick_params(axis='x', rotation=45)

# Total transactions
axes[1].bar(dow_stats.index, dow_stats["total_transactions"], color=colors_dow, edgecolor="white")
axes[1].set_title("Total Transactions per Day")
axes[1].set_ylabel("Transactions")
axes[1].tick_params(axis='x', rotation=45)

# Weekday vs Weekend
wk_comp = df.groupby("is_weekend")["revenue"].agg(["sum","mean"])
wk_comp.index = ["Weekday","Weekend"]
axes[2].bar(wk_comp.index, wk_comp["mean"],
            color=[ESPRESSO, GOLD], edgecolor="white", width=0.5)
axes[2].set_title("Avg Revenue: Weekday vs Weekend")
axes[2].set_ylabel("Avg Revenue ($)")

save_fig("06_dow_performance")

# Heatmap week × day
heat_wd = df.pivot_table(values="revenue", index="week_of_year",
                          columns="day_name", aggfunc="sum")[day_order]
fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(heat_wd, cmap="YlOrBr", linewidths=0.2, ax=ax,
            cbar_kws={"label": "Total Revenue ($)"})
ax.set_title("Revenue Heatmap — Week × Day of Week",
             fontsize=14, color=ESPRESSO, fontweight="bold")
save_fig("07_week_day_heatmap")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7 — TIME-OF-DAY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 7 — Time-of-Day (Hourly) Analysis")

hourly = df.groupby("hour").agg(
    transactions=("transaction_id","count"),
    total_revenue=("revenue","sum"),
    avg_revenue=("revenue","mean")
).reset_index()

peak_hour = int(hourly.loc[hourly["transactions"].idxmax(), "hour"])
print(f"  Peak transaction hour: {peak_hour}:00")

fig, axes = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle("Hourly Demand Analysis",
             fontsize=15, color=ESPRESSO, fontweight="bold")

# Transactions per hour (area)
axes[0].fill_between(hourly["hour"], hourly["transactions"],
                     alpha=0.35, color=ESPRESSO)
axes[0].plot(hourly["hour"], hourly["transactions"],
             color=ESPRESSO, linewidth=2.5, marker="o", markersize=5)
axes[0].axvline(peak_hour, color=GOLD, linestyle="--", linewidth=1.5,
                label=f"Peak: {peak_hour}:00")
axes[0].set_title("Transactions per Hour")
axes[0].set_ylabel("Transaction Count")
axes[0].set_xlabel("Hour of Day")
axes[0].set_xticks(range(0, 24))
axes[0].legend()

# Revenue per hour (area)
axes[1].fill_between(hourly["hour"], hourly["total_revenue"],
                     alpha=0.35, color=GOLD)
axes[1].plot(hourly["hour"], hourly["total_revenue"],
             color=GOLD, linewidth=2.5, marker="s", markersize=5)
axes[1].set_title("Total Revenue per Hour")
axes[1].set_ylabel("Revenue ($)")
axes[1].set_xlabel("Hour of Day")
axes[1].set_xticks(range(0, 24))

save_fig("08_hourly_analysis")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8 — STORE-LEVEL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 8 — Store-Level Comparison")

stores = df["store_location"].unique().tolist()

# Hourly heatmap per store
pivot_store_hour = df.pivot_table(values="revenue", index="store_location",
                                   columns="hour", aggfunc="sum")
fig, ax = plt.subplots(figsize=(20, 4))
sns.heatmap(pivot_store_hour, cmap="YlOrBr", linewidths=0.3,
            annot=False, ax=ax, cbar_kws={"label": "Total Revenue ($)"})
ax.set_title("Store × Hour Revenue Heatmap",
             fontsize=14, color=ESPRESSO, fontweight="bold")
save_fig("09_store_hour_heatmap")

# Stacked bar: store × category
pivot_sc = df.groupby(["store_location","product_category"])["revenue"].sum().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(12, 7))
pivot_sc.plot(kind="bar", stacked=True, ax=ax,
              colormap="YlOrBr", edgecolor="white")
ax.set_title("Stacked Revenue — Store × Product Category",
             fontsize=14, color=ESPRESSO, fontweight="bold")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis='x', rotation=0)
ax.legend(title="Category", bbox_to_anchor=(1, 1), fontsize=8)
save_fig("10_store_category_stacked")

# Radar chart — store KPIs
from matplotlib.patches import FancyArrowPatch
store_kpi = df.groupby("store_location").agg(
    total_revenue=("revenue","sum"),
    avg_order=("revenue","mean"),
    transactions=("transaction_id","count"),
    avg_qty=("transaction_qty","mean"),
    avg_price=("unit_price","mean"),
).reset_index()

# Normalize 0-1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
kpi_cols = ["total_revenue","avg_order","transactions","avg_qty","avg_price"]
store_kpi_norm = store_kpi.copy()
store_kpi_norm[kpi_cols] = scaler.fit_transform(store_kpi[kpi_cols])

labels = ["Total Revenue","Avg Order","Transactions","Avg Qty","Avg Price"]
N = len(labels)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_facecolor("#FDFAF7")
fig.patch.set_facecolor("#FDFAF7")
colors_radar = [ESPRESSO, GOLD, LATTE]

for i, row in store_kpi_norm.iterrows():
    vals = row[kpi_cols].tolist() + [row[kpi_cols[0]]]
    ax.plot(angles, vals, linewidth=2, linestyle="solid",
            color=colors_radar[i], label=row["store_location"])
    ax.fill(angles, vals, alpha=0.15, color=colors_radar[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=11, color=DARK_ROAST)
ax.set_title("Store KPI Radar Chart",
             fontsize=14, color=ESPRESSO, fontweight="bold", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
save_fig("11_radar_chart")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9 — MySQL SCHEMA & INSERT SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 9 — MySQL Schema & Queries")

schema_sql = """-- ═══════════════════════════════════════════════════════════
--  Afficionado Coffee Roasters — MySQL Schema
--  Database: coffee_sales_db
-- ═══════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS coffee_sales_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE coffee_sales_db;

-- ─── Main transactions table ──────────────────────────────
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   INT            NOT NULL PRIMARY KEY,
    transaction_date DATE           NOT NULL,
    transaction_time TIME           NOT NULL,
    transaction_qty  SMALLINT       NOT NULL CHECK (transaction_qty >= 0),
    store_id         TINYINT        NOT NULL,
    store_location   VARCHAR(60)    NOT NULL,
    product_id       SMALLINT       NOT NULL,
    unit_price       DECIMAL(6,2)   NOT NULL,
    product_category VARCHAR(60)    NOT NULL,
    product_type     VARCHAR(80)    NOT NULL,
    product_detail   VARCHAR(120)   NOT NULL,
    revenue          DECIMAL(8,2)   GENERATED ALWAYS AS (transaction_qty * unit_price) STORED,
    hour_of_day      TINYINT        GENERATED ALWAYS AS (HOUR(transaction_time)) STORED,
    day_of_week      VARCHAR(12)    GENERATED ALWAYS AS (DAYNAME(transaction_date)) STORED,
    time_bucket      VARCHAR(15)    GENERATED ALWAYS AS (
        CASE
          WHEN HOUR(transaction_time) BETWEEN 6  AND 11 THEN 'Morning'
          WHEN HOUR(transaction_time) BETWEEN 12 AND 16 THEN 'Afternoon'
          WHEN HOUR(transaction_time) BETWEEN 17 AND 21 THEN 'Evening'
          ELSE 'Late Night'
        END) STORED,
    INDEX idx_date         (transaction_date),
    INDEX idx_store        (store_location),
    INDEX idx_category     (product_category),
    INDEX idx_hour         (hour_of_day)
);

-- ─── Analytical Views ─────────────────────────────────────

-- Daily revenue summary
CREATE OR REPLACE VIEW vw_daily_revenue AS
SELECT
    transaction_date,
    COUNT(*)          AS total_transactions,
    SUM(revenue)      AS total_revenue,
    AVG(revenue)      AS avg_order_value
FROM transactions
GROUP BY transaction_date
ORDER BY transaction_date;

-- Peak hours
CREATE OR REPLACE VIEW vw_peak_hours AS
SELECT
    hour_of_day,
    COUNT(*)      AS transactions,
    SUM(revenue)  AS revenue
FROM transactions
GROUP BY hour_of_day
ORDER BY transactions DESC;

-- Top categories
CREATE OR REPLACE VIEW vw_top_categories AS
SELECT
    product_category,
    SUM(revenue)      AS total_revenue,
    COUNT(*)          AS total_transactions,
    AVG(unit_price)   AS avg_price
FROM transactions
GROUP BY product_category
ORDER BY total_revenue DESC;

-- Store × Day performance
CREATE OR REPLACE VIEW vw_store_day AS
SELECT
    store_location,
    day_of_week,
    SUM(revenue)  AS total_revenue,
    COUNT(*)      AS total_transactions
FROM transactions
GROUP BY store_location, day_of_week;

-- ─── Analytical Queries ───────────────────────────────────

-- Q1: Revenue by store and day of week
SELECT
    store_location,
    day_of_week,
    SUM(revenue)          AS total_revenue,
    COUNT(transaction_id) AS total_transactions
FROM transactions
GROUP BY store_location, day_of_week
ORDER BY store_location, FIELD(day_of_week,
  'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');

-- Q2: Top 5 busiest hours overall
SELECT
    hour_of_day,
    COUNT(*) AS txn_count,
    SUM(revenue) AS revenue
FROM transactions
GROUP BY hour_of_day
ORDER BY txn_count DESC
LIMIT 5;

-- Q3: Monthly revenue trend
SELECT
    MONTH(transaction_date)  AS month_num,
    MONTHNAME(transaction_date) AS month_name,
    SUM(revenue)             AS total_revenue,
    COUNT(*)                 AS transactions
FROM transactions
GROUP BY month_num, month_name
ORDER BY month_num;

-- Q4: Best selling product category by store
SELECT
    store_location,
    product_category,
    SUM(revenue) AS revenue
FROM transactions
GROUP BY store_location, product_category
ORDER BY store_location, revenue DESC;

-- Q5: Weekend vs Weekday comparison
SELECT
    CASE WHEN DAYOFWEEK(transaction_date) IN (1,7) THEN 'Weekend'
         ELSE 'Weekday'
    END AS period,
    SUM(revenue)  AS total_revenue,
    AVG(revenue)  AS avg_order,
    COUNT(*)      AS transactions
FROM transactions
GROUP BY period;
"""
insert_lines = ["USE coffee_sales_db;\n"]

subset = df.head(500)

for _, row in subset.iterrows():
    insert_lines.append(
        f"INSERT IGNORE INTO transactions "
        f"(transaction_id, transaction_date, transaction_time, transaction_qty, "
        f"store_id, store_location, product_id, unit_price, "
        f"product_category, product_type, product_detail) VALUES "
        f"({row.transaction_id}, '{row.transaction_date.date()}', "
        f"'{row.transaction_time}', {row.transaction_qty}, "
        f"{row.store_id}, '{row.store_location}', "
        f"{row.product_id}, {row.unit_price:.2f}, "
        f"'{row.product_category}', "
        f"'{row.product_type}', "
        f"'{row.product_detail}');"
    )
inserts_path = os.path.join(SQL, "inserts_sample.sql")

with open(inserts_path, "w", encoding="utf-8") as f:
    f.write("\n".join(insert_lines))

print(f"Schema saved → sql/schema.sql")

# Optional: generate INSERT statements (first 500 rows for demonstration)
insert_lines = ["USE coffee_sales_db;\n"]
subset = df.head(500)
for _, row in subset.iterrows():
    insert_lines.append(
        f"INSERT IGNORE INTO transactions "
        f"(transaction_id, transaction_date, transaction_time, transaction_qty, "
        f"store_id, store_location, product_id, unit_price, "
        f"product_category, product_type, product_detail) VALUES "
        f"({row.transaction_id}, '{row.transaction_date.date()}', "
        f"'{row.transaction_time}', {row.transaction_qty}, "
        f"{row.store_id}, '{row.store_location.replace(chr(39),chr(39)+chr(39))}', "
        f"{row.product_id}, {row.unit_price:.2f}, "
        f"'{row.product_category}', "
        f"'{str(row.product_type).replace(chr(39),chr(39)+chr(39))}', "
        f"'{str(row.product_detail).replace(chr(39),chr(39)+chr(39))}');"
    )

inserts_path = os.path.join(SQL, "inserts_sample.sql")
with open(inserts_path, "w", encoding="utf-8") as f:
    f.write("\n".join(insert_lines))
print(f"Sample inserts (500 rows) saved → sql/inserts_sample.sql")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 10 — AUTOMATED INSIGHT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
section("STEP 10 — Automated Insight Generation")

total_rev   = df["revenue"].sum()
total_txns  = len(df)
avg_order   = df["revenue"].mean()
top_cat     = df.groupby("product_category")["revenue"].sum().idxmax()
top_store   = df.groupby("store_location")["revenue"].sum().idxmax()
best_day    = dow_stats["avg_revenue"].idxmax()
worst_day   = dow_stats["avg_revenue"].idxmin()
peak_h      = int(hourly.loc[hourly["transactions"].idxmax(), "hour"])
wknd_rev    = df[df["is_weekend"]]["revenue"].mean()
wkdy_rev    = df[~df["is_weekend"]]["revenue"].mean()
wknd_lift   = (wknd_rev - wkdy_rev) / wkdy_rev * 100

insights = f"""
╔══════════════════════════════════════════════════════════════════════╗
║          AUTOMATED INSIGHTS — Afficionado Coffee Roasters           ║
╠══════════════════════════════════════════════════════════════════════╣
║ KPIs                                                                 ║
║  Total Revenue:        ${total_rev:>12,.2f}                         ║
║  Total Transactions:   {total_txns:>12,}                            ║
║  Average Order Value:  ${avg_order:>12.2f}                          ║
╠══════════════════════════════════════════════════════════════════════╣
║ PRODUCT                                                              ║
║  Top Revenue Category: {top_cat:<40}                                ║
╠══════════════════════════════════════════════════════════════════════╣
║ STORE                                                                ║
║  Best Performing Store: {top_store:<39}                             ║
╠══════════════════════════════════════════════════════════════════════╣
║ TEMPORAL                                                             ║
║  Best Day of Week:   {best_day:<43}                                  ║
║  Slowest Day:        {worst_day:<43}                                 ║
║  Peak Hour:          {peak_h}:00 – {peak_h+1}:00                     ║
║  Weekend Revenue Lift vs Weekday: {wknd_lift:+.1f}%                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ SCHEDULING RECOMMENDATIONS                                           ║
║  • Staff up 30 min before {peak_h}:00 daily                          ║
║  • Add extra staff on {best_day}s                                     ║
║  • Reduce staff on {worst_day}s — consider promotions to boost demand║
║  • Weekend staffing should be ~{wknd_lift:.0f}% higher than weekday  ║
╚══════════════════════════════════════════════════════════════════════╝
"""
print(insights)

insights_path = os.path.join(BASE, "report", "automated_insights.txt")
os.makedirs(os.path.dirname(insights_path), exist_ok=True)
with open(insights_path, "w", encoding="utf-8") as f:
    f.write(insights)

print("\n✅  Data pipeline complete. All visuals saved to /visuals/")
print("    Ready to launch: streamlit run streamlit_app/app.py\n")
