# ☕ Sales Trend and Time-Based Performance Analysis
### Afficionado Coffee Roasters — Interactive BI Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Project Overview
End-to-end sales trend and time-based performance analysis for
Afficionado Coffee Roasters using 149,116 POS transactions
(January – June 2025) across 3 NYC store locations.

## 🎯 Objectives
- Identify peak hours, busiest/slowest days, and monthly trends
- Compare store-level demand patterns
- Build an interactive Streamlit dashboard for decision-makers

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.11 | Data pipeline & EDA |
| Pandas / NumPy | Data manipulation |
| Matplotlib / Seaborn | Static visualisations |
| Plotly | Interactive charts |
| Streamlit | BI Dashboard |
| MySQL | Data storage & queries |
| Excel | Cleaned dataset export |

## 📁 Project Structure
```
Sales_Trend_Analysis/
├── assets/              # Logo images
├── data/                # Dataset folder
├── report/              # Research paper & insights
├── sql/                 # MySQL schema & queries
├── visuals/             # Generated charts
├── app.py               # Streamlit dashboard
├── data_pipeline.py     # Full analysis pipeline
├── requirements.txt     # Dependencies
└── README.md
```

## 🚀 How to Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run the data pipeline**
```bash
python data_pipeline.py
```

**3. Launch the dashboard**
```bash
streamlit run app.py
```

## 📊 Key Findings
- 💰 **Total Revenue:** $653,691 (H1 2025)
- 🕙 **Peak Hour:** 10:00 AM across all stores
- 📅 **Best Day:** Thursday | **Slowest:** Tuesday
- 🏪 **Top Store:** Astoria (by volume)
- ☕ **Top Category:** Coffee (40% of revenue)

## 👩‍💻 Author
**Sonali** — Data Analytics Intern @ Unified Mentor

## 📄 License
MIT License