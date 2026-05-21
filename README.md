# Weather Trend Forecasting

PM Accelerator AI Engineer Internship assessment for forecasting global weather trends with time-series modeling, anomaly detection, spatial analysis, and ensemble learning.

## Overview

This repository analyzes the Global Weather Repository dataset and turns it into a complete data science deliverable: cleaned data, exploratory analysis, multiple forecasting approaches, interpretable model outputs, interactive visualizations, and a dashboard.

## Highlights

- Data cleaning and preprocessing with date parsing, missing-value handling, outlier clipping, and feature engineering.
- Forecasting with ARIMA, Prophet, XGBoost, and a stacked ensemble.
- Advanced analyses for climate trends, AQI relationships, SHAP feature importance, and geospatial patterns.
- Interactive outputs in `reports/figures/`, a final HTML report, and a Plotly Dash dashboard.
## Advanced Features

### Anomaly Detection
- **Isolation Forest** for unsupervised outlier detection across global weather observations
- **Local Outlier Factor (LOF)** for density-based anomaly scoring
- Processed anomaly-tagged dataset exported as `data/weather_with_anomalies.csv`

### Ensemble Forecasting
- **ARIMA** — baseline time-series forecasting
- **Prophet** — seasonal decomposition and trend forecasting
- **XGBoost** — gradient boosting with engineered lag and rolling features
- **Stacked Ensemble** — combines all three models for best-in-class predictions (MAE: 2.456°C, R²: 0.219)

### Explainability
- **SHAP-based feature importance** to interpret model predictions and identify key weather drivers

### Geospatial Analysis
- **Folium spatial heatmaps** for visualizing weather intensity across regions
- **Country-level choropleth visualizations** for global pattern comparison

### Climate & Environmental Correlations
- **AQI vs. weather correlation study** to explore air quality relationships with temperature, humidity, and wind
- **Continent-level climate pattern analysis** across 211 countries and 257 cities

### Interactive Dashboard
- **Plotly Dash dashboard** (`dashboard.py`) for real-time exploration of forecasts, anomalies, and geospatial trends
- Final HTML report available at `reports/final_report.html`

## Project Structure

```text
weather prediction/
├── dashboard.py
├── data/
│   ├── weather_cleaned.csv
│   └── weather_with_anomalies.csv
├── demo/
│   └── demo_link.txt
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_basic.ipynb
│   ├── 03_eda_advanced.ipynb
│   ├── 04_modeling_basic.ipynb
│   ├── 05_modeling_advanced.ipynb
│   └── 06_unique_analyses.ipynb
├── reports/
│   ├── final_report.html
│   └── figures/
├── scripts/
│   ├── master_execution.py
│   └── nb0*_simplified.py
├── src/
│   ├── data_loader.py
│   ├── eda_utils.py
│   ├── ensemble.py
│   ├── models.py
│   └── spatial_utils.py
├── tests/
│   └── test_data_loader.py
├── requirements.txt
├── environment.yml
└── README.md
```

## Dataset

Source: [Kaggle Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)

The processed dataset includes global weather observations across 211 countries and 257 cities, with engineered temporal, rolling, and derived weather features.

## Key Results

| Model | MAE (°C) | RMSE (°C) | R² |
| --- | ---: | ---: | ---: |
| ARIMA | 2.623 | 3.364 | -0.041 |
| Prophet | 2.745 | 3.512 | -0.382 |
| XGBoost | 2.498 | 3.177 | 0.172 |
| Ensemble | 2.456 | 3.089 | 0.219 |

## What’s Included

### Core Pipeline

- Data cleaning and preprocessing
- Anomaly detection with Isolation Forest and LOF
- Feature engineering for lagged and rolling weather signals

### Modeling

- ARIMA baseline forecasting
- Prophet seasonal forecasting
- XGBoost with lag features
- Stacked ensemble for the final comparison

### Advanced Analyses

- Climate pattern analysis by continent
- AQI versus weather correlation study
- SHAP-based feature importance
- Spatial heatmap with Folium
- Country-level choropleth visualization

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or create the conda environment:

```bash
conda env create -f environment.yml
conda activate weather-forecast
```

### 2. Get the data

Download the Kaggle dataset and place the processed files in `data/` if you want to rerun the workflow from scratch.

### 3. Run the notebooks

Open the notebooks in order:

1. `notebooks/01_data_cleaning.ipynb`
2. `notebooks/02_eda_basic.ipynb`
3. `notebooks/03_eda_advanced.ipynb`
4. `notebooks/04_modeling_basic.ipynb`
5. `notebooks/05_modeling_advanced.ipynb`
6. `notebooks/06_unique_analyses.ipynb`

### 4. Launch the dashboard

```bash
python dashboard.py
```

Open `http://127.0.0.1:8050` in your browser.

## Run Tests

```bash
pytest tests -v
```

## Demo

The demo video link is stored in `demo/demo_link.txt`.

## Documentation

- `CONFIG.md` for setup details
- `BUILD_GUIDE.md` for the end-to-end build process
- `CLEANUP_SUMMARY.md` for repository organization notes
- `SUBMISSION_CHECKLIST.md` for final verification

## License

This project was created for the PM Accelerator AI Engineer Internship Assessment.
