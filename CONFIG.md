# 🌦️ Weather Prediction Project - Configuration & Data Source

## Data Source

**Dataset:** Global Weather Repository  
**Platform:** Kaggle  
**URL:** https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository  
**Local Cache Path:** `C:\Users\shami\.cache\kagglehub\datasets\nelgiriyewithana\global-weather-repository\versions\955\GlobalWeatherRepository.csv`

### How to Access Data

The project uses **kagglehub** to automatically download and cache the dataset. The data is referenced directly from Kaggle's cache rather than being stored in the repository.

```python
import kagglehub
path = kagglehub.dataset_download("nelgiriyewithana/global-weather-repository")
```

**Dataset Statistics:**
- **Records:** 141,508
- **Columns:** 41 (original) → 52 (after cleaning)
- **File Size:** 35.7 MB (raw)
- **Date Range:** 2024-05-16 to 2026-05-15 (24 months)
- **Geographic Coverage:** 211 countries, 257 cities

---

## Directory Structure

```
weather prediction/
├── notebooks/
│   ├── 01_data_cleaning.ipynb          # Data cleaning & preprocessing
│   ├── 02_eda_basic.ipynb              # Basic exploratory analysis
│   ├── 03_eda_advanced.ipynb           # Anomaly detection & patterns
│   ├── 04_modeling_basic.ipynb         # ARIMA time-series forecasting
│   ├── 05_modeling_advanced.ipynb      # Prophet, XGBoost, Ensemble
│   └── 06_unique_analyses.ipynb        # SHAP, spatial, climate analyses
│
├── scripts/
│   ├── nb01_simplified.py              # Standalone execution script for NB01
│   ├── nb02_simplified.py              # Standalone execution script for NB02
│   ├── nb03_simplified.py              # Standalone execution script for NB03
│   ├── nb04_simplified.py              # Standalone execution script for NB04
│   ├── nb05_simplified.py              # Standalone execution script for NB05
│   └── nb06_simplified.py              # Standalone execution script for NB06
│
├── data/
│   ├── weather_cleaned.csv             # Processed data (141,508 × 52 cols)
│   └── weather_with_anomalies.csv      # Data with anomaly flags
│
├── reports/
│   ├── figures/
│   │   ├── 01_global_temp_trend.html   # Interactive temperature trends
│   │   ├── 02_monthly_temp_boxplot.png # Seasonal distribution
│   │   ├── 04_correlation_matrix.png   # Feature correlations
│   │   └── 06_spatial_heatmap.html     # Geographic distribution
│   ├── model_results.csv               # ARIMA metrics
│   └── advanced_model_results.csv      # Prophet/XGBoost/Ensemble results
│
├── src/
│   ├── data_loader.py                  # Data loading utilities
│   ├── eda_utils.py                    # EDA helper functions
│   └── __init__.py
│
├── docs/
│   ├── BUILD_GUIDE.md                  # Setup & build instructions
│   ├── QUICKSTART.md                   # Quick start guide
│   ├── START_HERE.md                   # Entry point documentation
│   ├── SUBMISSION_CHECKLIST.md         # Pre-submission verification
│   ├── PACKAGE_CONTENTS.md             # Complete file listing
│   └── DEMO_SCRIPT.md                  # Demo video script
│
├── .gitignore                          # Git ignore rules
├── environment.yml                     # Conda environment file
├── requirements.txt                    # Python dependencies (25 packages)
├── README.md                           # Project overview
├── CONFIG.md                           # This file
└── .venv/                              # (Excluded from repo)
```

---

## Data Pipeline

### Processing Steps (Notebook 01)

1. **Load Raw Data** → 141,508 × 41 columns
2. **Parse Dates** → Standardize timestamps
3. **Extract Temporal Features** → Year, month, day, hour, day_of_week, season
4. **Handle Missing Values** → Per-city median imputation
5. **Clip Outliers** → IQR method (1st/99th percentile)
6. **Feature Engineering** → Heat index, wind chill, temp_humidity_index, log_precip
7. **Normalize Features** → MinMaxScaler [0,1]

**Output:** `data/weather_cleaned.csv` (141,508 × 52 columns)

### Analysis Pipeline

| Notebook | Purpose | Outputs |
|----------|---------|---------|
| NB01 | Data Cleaning | weather_cleaned.csv |
| NB02 | Basic EDA | 4 visualizations |
| NB03 | Anomaly Detection | weather_with_anomalies.csv |
| NB04 | ARIMA Forecasting | model_results.csv |
| NB05 | Multi-Model Comparison | advanced_model_results.csv |
| NB06 | Unique Analyses | spatial_heatmap.html |

---

## Key Metrics

**Best Forecasting Model:** Ensemble (Prophet 35% + XGBoost 65%)
- **MAE:** 0.053°C
- **RMSE:** 0.067°C  
- **R²:** 0.219

**Anomalies Detected:** 212 consensus anomalies (2% contamination)

**Top Predictive Feature:** Lag_1 (yesterday's temperature: 75% importance)

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Kaggle Authentication

```bash
# Install kagglehub
pip install kagglehub

# Login to Kaggle (creates ~/.kaggle/kaggle.json)
kagglehub whoami
```

### 3. Run Notebooks

**Option A - Jupyter (Interactive)**
```bash
jupyter notebook notebooks/
```

**Option B - Python Scripts (Batch)**
```bash
cd scripts
python nb01_simplified.py  # Data cleaning
python nb02_simplified.py  # EDA
# ... etc
```

**Option C - All at Once**
```bash
cd scripts
for script in nb0*.py; do python $script; done
```

---

## Notes

- **No Raw Data Stored:** The raw CSV is retrieved from Kaggle's cache on-demand
- **Cleaned Data Only:** Repository contains only processed datasets
- **Reproducible:** All scripts reference the same Kaggle dataset version
- **System Python:** Project uses system Python 3.11.9 (no virtual env needed)

---

**Last Updated:** May 15, 2026  
**Dataset Version:** Global Weather Repository v955  
**Kaggle URL:** https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository
