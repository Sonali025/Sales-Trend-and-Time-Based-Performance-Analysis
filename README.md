# ☕ Sales Trend and Time-Based Performance Analysis
### Afficionado Coffee Roasters — Interactive BI Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)
![Internship](https://img.shields.io/badge/Unified%20Mentor-Internship-orange)

---

## 🌐 Live Dashboard
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sales-trend-and-time-based-performance-analysis.streamlit.app/)

🔗 **[Launch Dashboard →](https://sales-trend-and-time-based-performance-analysis.streamlit.app/)**

---

## 📄 Research Paper
This project is accompanied by a published research paper following IEEE/Elsevier academic standards.

📖 **[Read the Research Paper →](https://doi.org/10.6084/m9.figshare.31760977)**

> *"Sales Trend and Time-Based Performance Analysis for Afficionado Coffee Roasters"*
> Published on Figshare | DOI: [10.6084/m9.figshare.31760977](https://doi.org/10.6084/m9.figshare.31760977)

---

## 📌 Project Overview
End-to-end sales trend and time-based performance analysis for **Afficionado Coffee Roasters**
using **149,116 POS transactions** (January – June 2025) across **3 NYC store locations**
(Astoria, Hell's Kitchen, Lower Manhattan).

The project uncovers temporal demand patterns to help decision-makers optimise
staff scheduling, inventory planning, and marketing initiatives.

---

## 🎯 Objectives

### Primary
- Identify overall sales trends across H1 2025
- Determine the busiest and slowest days of the week
- Pinpoint peak transaction hours across all stores

### Secondary
- Compare demand patterns across 3 store locations
- Generate evidence-based staff scheduling recommendations
- Build an interactive self-service BI dashboard

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Data pipeline, feature engineering & EDA |
| Pandas / NumPy | Data manipulation & statistical computations |
| Matplotlib / Seaborn | Static visualisations (11 publication-quality charts) |
| Plotly | Interactive charts in the dashboard |
| Streamlit | 4-page interactive BI dashboard |
| MySQL | Data storage, analytical views & SQL queries |
| Excel (.xlsx) | Cleaned dataset export for stakeholders |

---

## 📁 Project Structure
```
Sales_Trend_Analysis/
├── assets/                    # Logo images (Afficionado + Unified Mentor)
├── data/
│   ├── raw_data.csv           # Original POS dataset
│   └── cleaned_data.csv       # IQR-cleaned, feature-engineered dataset
├── report/
│   ├── research_paper.docx    # Full IEEE-style research paper
│   └── executive_summary.docx # 1-page stakeholder summary
├── sql/
│   ├── schema.sql             # MySQL database schema & analytical views
│   └── inserts_sample.sql     # Sample INSERT statements (500 rows)
├── visuals/                   # 11 generated EDA & analysis charts
├── app.py                     # Streamlit interactive dashboard
├── data_pipeline.py           # 10-stage end-to-end analysis pipeline
├── requirements.txt           # Python dependencies
└── README.md
```

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Sonali025/Sales-Trend-and-Time-Based-Performance-Analysis.git
cd Sales-Trend-and-Time-Based-Performance-Analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the data pipeline** *(generates cleaned data & all visualisations)*
```bash
python data_pipeline.py
```

**4. Launch the dashboard**
```bash
streamlit run app.py
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 📈 Sales Trend | Daily & monthly revenue with 7/14-day moving averages |
| 📅 Day-of-Week Performance | Busiest vs slowest days, weekday vs weekend comparison |
| 🕐 Hourly Demand | Peak hour detection, time-bucket analysis, store × hour heatmap |
| 🏪 Store Comparison | Cross-store revenue, KPI radar chart, category breakdown |

**Sidebar Controls:** Store filter · Day-of-week selector · Hour range slider · Revenue vs Quantity toggle

---

## 📊 Key Findings

| KPI | Result |
|-----|--------|
| 💰 Total Revenue (H1 2025) | $653,691 |
| 🔢 Total Transactions | 149,116 |
| 🛒 Avg Order Value | $4.38 |
| 🕙 Peak Hour | 10:00 AM (all stores) |
| 📅 Best Day | Thursday |
| 📅 Slowest Day | Tuesday |
| 🏪 Top Store by Volume | Astoria |
| ☕ Top Category | Coffee (40% of revenue) |
| 📆 Weekend vs Weekday | Parity — no weekend drop |

---

## 🔍 Methodology
```
Data Ingestion → Quality Validation → IQR Outlier Treatment
      ↓
Feature Engineering (revenue, hour, day_name, time_bucket)
      ↓
Univariate → Bivariate → Multivariate EDA
      ↓
Sales Trend + Day-of-Week + Hourly + Store Analysis
      ↓
MySQL Schema + Streamlit Dashboard + Research Paper
```

---

## 💡 Business Recommendations

1. **Staff up by 8:30 AM daily** — 10 AM is peak across all 3 stores, every day
2. **Add PM shift at Hell's Kitchen** (1:30–3:30 PM) — secondary demand peak at 2 PM
3. **Tuesday loyalty campaign** — consistent weekly revenue gap vs Thursday
4. **Mobile pre-order at Lower Manhattan** — throughput bottleneck at 8–9 AM
5. **Upsell training at Astoria** — highest volume but lowest avg order value

---

## 📄 Research Publication

The findings of this project are documented in a full academic research paper
following IEEE/Elsevier format, covering EDA methodology, temporal analysis,
business insights, limitations, and future work.

| Item | Link |
|------|------|
| 📖 Full Research Paper | [DOI: 10.6084/m9.figshare.31760977](https://doi.org/10.6084/m9.figshare.31760977) |
| 🌐 Live Dashboard | [sales-trend-and-time-based-performance-analysis.streamlit.app](https://sales-trend-and-time-based-performance-analysis.streamlit.app/) |

---

## 👩‍💻 Author

**Sonali Sagar**
Data Analytics Intern @ [Unified Mentor](https://unifiedmentor.com)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/sagar-sonali)
[![GitHub](https://img.shields.io/badge/GitHub-Sonali025-black?logo=github)](https://github.com/Sonali025)

---

## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ☕ and Python | Afficionado Coffee Roasters | 2025</sub>
</div>