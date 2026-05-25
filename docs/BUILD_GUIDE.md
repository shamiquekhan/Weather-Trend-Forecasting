#  Weather Trend Forecasting — Complete Build Guide
### PM Accelerator · AI Engineer Internship · Tech Assessment

> **Mission of PM Accelerator:** Empower the next generation of AI professionals through hands-on experience, mentorship, and real-world projects — bridging the gap between academic learning and industry-ready skills.

---

##  Table of Contents

1. [Project Overview & Strategy](#1-project-overview--strategy)
2. [Repository Structure](#2-repository-structure)
3. [Environment Setup](#3-environment-setup)
4. [Dataset Acquisition & First Look](#4-dataset-acquisition--first-look)
5. [Data Cleaning & Preprocessing](#5-data-cleaning--preprocessing)
6. [Exploratory Data Analysis (EDA)](#6-exploratory-data-analysis-eda)
7. [Advanced EDA & Anomaly Detection](#7-advanced-eda--anomaly-detection)
8. [Model Building — Basic Track](#8-model-building--basic-track)
9. [Model Building — Advanced Track](#9-model-building--advanced-track)
10. [Unique Advanced Analyses](#10-unique-advanced-analyses)
11. [Deliverables: Report / Dashboard](#11-deliverables-report--dashboard)
12. [Demo Video Guide](#12-demo-video-guide)
13. [Submission Checklist](#13-submission-checklist)
14. [Tips to Stand Out](#14-tips-to-stand-out)

---

## 1. Project Overview & Strategy

### What the Assessors are Looking For

| Dimension | Basic Track | Advanced Track |
|-----------|------------|----------------|
| Data Handling | Clean & preprocess | Anomaly detection + robust pipeline |
| EDA | Trends & correlations | Spatial, environmental, multi-dimensional |
| Modeling | Single model + metrics | Ensemble + multi-model comparison |
| Communication | Clear report | Interactive dashboard or polished notebook |
| Code Quality | Functional | Modular, commented, reproducible |

### Recommended Approach (To Maximize Selection Chance)

Complete the **Advanced Track** with clean, well-documented code. Even partially completing advanced analyses signals ambition and capability to a hiring panel. At minimum, deliver:

- Solid data pipeline
- At least 3 forecasting models (ARIMA, Prophet, XGBoost)
- At least 2 unique analyses (Spatial + Environmental Impact recommended)
- A visual dashboard or polished HTML report
- A 2-minute screen-share demo video

---

## 2. Repository Structure

Organize your GitHub repository exactly like this:

```
weather-trend-forecasting/
│
├── data/
│   └── README.md                  # Instructions to download dataset from Kaggle
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_basic.ipynb
│   ├── 03_eda_advanced.ipynb
│   ├── 04_modeling_basic.ipynb
│   ├── 05_modeling_advanced.ipynb
│   └── 06_unique_analyses.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # Data ingestion + cleaning utilities
│   ├── eda_utils.py               # Reusable EDA visualization helpers
│   ├── models.py                  # Model classes & training logic
│   ├── ensemble.py                # Ensemble stacking logic
│   └── spatial_utils.py          # Geo-visualization helpers
│
├── reports/
│   ├── final_report.html          # Or .pdf — polished final deliverable
│   └── figures/                   # All saved plots (PNG/SVG)
│
├── demo/
│   └── demo_link.txt              # URL to your screen-share demo video
│
├── requirements.txt
├── environment.yml                # Optional: conda env
└── README.md                      # ← This is your main project README
```

---

## 3. Environment Setup

### Option A — pip (requirements.txt)

```txt
# requirements.txt
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
plotly==5.22.0
scikit-learn==1.5.0
statsmodels==0.14.2
prophet==1.1.5
xgboost==2.0.3
lightgbm==4.3.0
pmdarima==2.0.4
geopandas==0.14.4
folium==0.16.0
pyod==2.0.0
shap==0.45.1
yellowbrick==1.5
scipy==1.13.0
jupyter==1.0.0
nbformat==5.10.4
```

Install with:
```bash
pip install -r requirements.txt
```

### Option B — conda (environment.yml)

```yaml
name: weather-forecast
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - plotly
  - scikit-learn
  - statsmodels
  - xgboost
  - lightgbm
  - geopandas
  - folium
  - scipy
  - jupyter
  - pip:
    - prophet
    - pmdarima
    - pyod
    - shap
    - yellowbrick
```

```bash
conda env create -f environment.yml
conda activate weather-forecast
```

---

## 4. Dataset Acquisition & First Look

### Download

```python
# Option 1: Kaggle CLI
# pip install kaggle
# Place your kaggle.json API key in ~/.kaggle/
import os
os.system("kaggle datasets download -d nelgiriyewithana/global-weather-repository --unzip -p ./data/")
```

Or manually download from:
**https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository**

### Initial Exploration

```python
# src/data_loader.py
import pandas as pd
import numpy as np

def load_data(path: str = "data/GlobalWeatherRepository.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["last_updated"])
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['last_updated'].min()} → {df['last_updated'].max()}")
    print(f"Unique countries: {df['country'].nunique()}")
    print(f"Unique cities: {df['location_name'].nunique()}")
    return df

# Quick sanity check
df = load_data()
df.info()
df.describe()
df.isnull().sum().sort_values(ascending=False).head(20)
```

### Key Columns to Know

| Column | Type | Notes |
|--------|------|-------|
| `last_updated` | datetime | Primary time axis for all time-series work |
| `location_name` | string | City name |
| `country` | string | Country name |
| `latitude`, `longitude` | float | For spatial analysis |
| `temperature_celsius` | float | Target variable (most models) |
| `precip_mm` | float | Precipitation |
| `humidity` | float | % humidity |
| `wind_kph` | float | Wind speed |
| `air_quality_us-epa-index` | float | Air quality index |
| `condition_text` | string | Weather condition category |

---

## 5. Data Cleaning & Preprocessing

```python
# notebooks/01_data_cleaning.ipynb

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive data cleaning and feature engineering pipeline.
    
    Args:
        df: Raw weather DataFrame
        
    Returns:
        Cleaned and feature-engineered DataFrame
    """
    df = df.copy()

    # ── 1. Parse Dates ────────────────────────────────────────────────────────
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    df = df.dropna(subset=["last_updated"])  # Drop rows with unparseable dates
    df = df.sort_values("last_updated").reset_index(drop=True)

    # ── 2. Extract Time Features ──────────────────────────────────────────────
    df["year"]        = df["last_updated"].dt.year
    df["month"]       = df["last_updated"].dt.month
    df["day"]         = df["last_updated"].dt.day
    df["hour"]        = df["last_updated"].dt.hour
    df["day_of_week"] = df["last_updated"].dt.dayofweek
    df["is_weekend"]  = df["day_of_week"].isin([5, 6]).astype(int)
    df["season"]      = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring",  4: "Spring", 5: "Spring",
        6: "Summer",  7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })

    # ── 3. Handle Missing Values ──────────────────────────────────────────────
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Fill numeric with median per city (preserves local climate context)
    for col in numeric_cols:
        df[col] = df.groupby("location_name")[col].transform(
            lambda x: x.fillna(x.median())
        )
    # Remaining NaNs (cities with all-NaN for a column): fill with global median
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill categorical with mode
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # ── 4. Outlier Handling (IQR method) ──────────────────────────────────────
    key_cols = ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
    for col in key_cols:
        Q1 = df[col].quantile(0.01)
        Q3 = df[col].quantile(0.99)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
        print(f"{col}: {outlier_count} outliers clipped")
        df[col] = df[col].clip(lower, upper)

    # ── 5. Feature Engineering ─────────────────────────────────────────────────
    df["temp_humidity_index"]    = df["temperature_celsius"] * df["humidity"] / 100
    df["heat_index"]             = df["temperature_celsius"] + 0.33 * (df["humidity"] / 100 * 6.105) - 4
        # Note: heat_index formula is approximate; most reliable for temp >= 26C and humidity >= 40%
    df["wind_chill"]             = 13.12 + 0.6215 * df["temperature_celsius"] - 11.37 * (df["wind_kph"] ** 0.16)
        # Note: wind_chill formula valid for temp <= 10C and wind speed >= 4.8 kph; use actual temp otherwise
    df["temp_feels_like_diff"]   = df["temperature_celsius"] - df.get("feelslike_celsius", df["temperature_celsius"])
    df["log_precip"]             = np.log1p(df["precip_mm"])

    # ── 6. Normalize Numeric Features ─────────────────────────────────────────
    scaler = MinMaxScaler()
    scale_cols = ["temperature_celsius", "humidity", "wind_kph", "precip_mm",
                  "pressure_mb", "visibility_km", "uv_index"]
    scale_cols = [c for c in scale_cols if c in df.columns]
    df[[f"{c}_scaled" for c in scale_cols]] = scaler.fit_transform(df[scale_cols])

    print(f"\n Cleaned dataset shape: {df.shape}")
    print(f"   Remaining nulls: {df.isnull().sum().sum()}")
    return df

df_clean = clean_weather_data(df)
df_clean.to_csv("data/weather_cleaned.csv", index=False)
```

---

## 6. Exploratory Data Analysis (EDA)

### 6.1 Temperature Trends

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ── Global Average Temperature Over Time ─────────────────────────────────────
daily_avg = df_clean.groupby("last_updated")["temperature_celsius"].mean().reset_index()

fig = px.line(
    daily_avg, x="last_updated", y="temperature_celsius",
    title="Global Average Daily Temperature Over Time",
    labels={"temperature_celsius": "Avg Temp (°C)", "last_updated": "Date"},
    template="plotly_dark"
)
fig.update_traces(line_color="#FF6B35", line_width=1.5)
fig.write_html("reports/figures/global_temp_trend.html")
fig.show()

# ── Monthly Seasonal Boxplot ──────────────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(14, 6))
sns.boxplot(data=df_clean, x="month", y="temperature_celsius",
            palette="coolwarm", ax=ax)
ax.set_title("Monthly Temperature Distribution (Global)", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig("reports/figures/monthly_temp_boxplot.png", dpi=150)
plt.show()
```

### 6.2 Precipitation Patterns

```python
# ── Top 20 Wettest Cities ────────────────────────────────────────────────────
top_rain = (
    df_clean.groupby("location_name")["precip_mm"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

fig = px.bar(
    top_rain, x="precip_mm", y="location_name", orientation="h",
    title="Top 20 Cities by Average Daily Precipitation",
    color="precip_mm", color_continuous_scale="Blues",
    template="plotly_white"
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
fig.write_html("reports/figures/top_rain_cities.html")
fig.show()

# ── Precipitation Heatmap (by month x season) ─────────────────────────────────
pivot = df_clean.pivot_table(
    values="precip_mm", index="season", columns="month", aggfunc="mean"
)
plt.figure(figsize=(12, 4))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5)
plt.title("Average Precipitation (mm) by Season and Month")
plt.tight_layout()
plt.savefig("reports/figures/precip_heatmap.png", dpi=150)
```

### 6.3 Correlation Matrix

```python
numeric_features = [
    "temperature_celsius", "humidity", "wind_kph", "precip_mm",
    "pressure_mb", "visibility_km", "uv_index", "cloud",
    "air_quality_us-epa-index", "heat_index", "wind_chill"
]
numeric_features = [c for c in numeric_features if c in df_clean.columns]

corr = df_clean[numeric_features].corr()

mask = np.triu(np.ones_like(corr, dtype=bool))
plt.figure(figsize=(12, 10))
sns.heatmap(
    corr, mask=mask, annot=True, fmt=".2f",
    cmap="RdYlGn", center=0, linewidths=0.5,
    annot_kws={"size": 8}
)
plt.title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("reports/figures/correlation_matrix.png", dpi=150)
```

---

## 7. Advanced EDA & Anomaly Detection

### 7.1 Anomaly Detection with PyOD

```python
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.knn import KNN

features_for_anomaly = [
    "temperature_celsius", "humidity", "wind_kph",
    "precip_mm", "pressure_mb"
]
X = df_clean[features_for_anomaly].dropna()

# ── Isolation Forest ──────────────────────────────────────────────────────────
clf_if = IForest(contamination=0.02, random_state=42, n_jobs=-1)
clf_if.fit(X)
df_clean.loc[X.index, "anomaly_iforest"] = clf_if.labels_
df_clean.loc[X.index, "anomaly_score"]   = clf_if.decision_scores_

# ── LOF ──────────────────────────────────────────────────────────────────────
clf_lof = LOF(contamination=0.02)
clf_lof.fit(X)
df_clean.loc[X.index, "anomaly_lof"] = clf_lof.labels_

# ── Visualize Anomalies on Temperature Timeline ────────────────────────────────
normal    = df_clean[df_clean["anomaly_iforest"] == 0]
anomalies = df_clean[df_clean["anomaly_iforest"] == 1]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=normal["last_updated"], y=normal["temperature_celsius"],
    mode="markers", marker=dict(color="steelblue", size=2, opacity=0.4),
    name="Normal"
))
fig.add_trace(go.Scatter(
    x=anomalies["last_updated"], y=anomalies["temperature_celsius"],
    mode="markers", marker=dict(color="crimson", size=6, symbol="x"),
    name="Anomaly"
))
fig.update_layout(
    title="Temperature Anomalies Detected by Isolation Forest",
    xaxis_title="Date", yaxis_title="Temperature (°C)",
    template="plotly_dark"
)
fig.write_html("reports/figures/anomaly_detection.html")
fig.show()

print(f"Total anomalies detected: {anomalies.shape[0]} ({anomalies.shape[0]/df_clean.shape[0]*100:.1f}%)")
```

---

## 8. Model Building — Basic Track

### Time-Series Forecasting with ARIMA

```python
# notebooks/04_modeling_basic.ipynb
import warnings
warnings.filterwarnings("ignore")

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pmdarima as pm

# ── Prepare City-Level Daily Series (e.g., London) ──────────────────────────
city = "London"
city_df = (
    df_clean[df_clean["location_name"] == city]
    .set_index("last_updated")["temperature_celsius"]
    .resample("D").mean()
    .interpolate()
)

# ── Stationarity Test ─────────────────────────────────────────────────────────
result = adfuller(city_df.dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print("→ Series is", "stationary " if result[1] < 0.05 else "non-stationary ")

# ── Auto-ARIMA ────────────────────────────────────────────────────────────────
train_size = int(len(city_df) * 0.8)
train, test = city_df.iloc[:train_size], city_df.iloc[train_size:]

auto_model = pm.auto_arima(
    train,
    seasonal=True, m=12,        # Monthly seasonality
    stepwise=True,
    suppress_warnings=True,
    error_action="ignore",
    max_p=5, max_q=5, max_P=2, max_Q=2
)
print(auto_model.summary())

# ── Forecast & Evaluate ───────────────────────────────────────────────────────
forecast, conf_int = auto_model.predict(n_periods=len(test), return_conf_int=True)
forecast_series = pd.Series(forecast, index=test.index)

mae  = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))
r2   = r2_score(test, forecast)
mape = np.mean(np.abs((test - forecast) / test)) * 100

print(f"\n ARIMA Evaluation ({city}):")
print(f"   MAE:  {mae:.3f} °C")
print(f"   RMSE: {rmse:.3f} °C")
print(f"   R²:   {r2:.3f}")
print(f"   MAPE: {mape:.2f}%")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig = go.Figure([
    go.Scatter(x=train.index, y=train.values, name="Train", line=dict(color="steelblue")),
    go.Scatter(x=test.index,  y=test.values,  name="Actual", line=dict(color="green")),
    go.Scatter(x=test.index,  y=forecast,     name="Forecast", line=dict(color="orange", dash="dash")),
    go.Scatter(
        x=list(test.index) + list(test.index[::-1]),
        y=list(conf_int[:, 1]) + list(conf_int[::-1, 0]),
        fill="toself", fillcolor="rgba(255,165,0,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% CI"
    )
])
fig.update_layout(
    title=f"ARIMA Temperature Forecast — {city}",
    xaxis_title="Date", yaxis_title="Temperature (°C)",
    template="plotly_dark"
)
fig.write_html(f"reports/figures/arima_forecast_{city.lower()}.html")
```

---

## 9. Model Building — Advanced Track

### 9.1 Prophet Model

```python
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# ── Prepare Prophet DataFrame ─────────────────────────────────────────────────
prophet_df = city_df.reset_index().rename(
    columns={"last_updated": "ds", "temperature_celsius": "y"}
)
train_p = prophet_df.iloc[:train_size]
test_p  = prophet_df.iloc[train_size:]

model_prophet = Prophet(
    changepoint_prior_scale=0.05,
    seasonality_prior_scale=10,
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model_prophet.fit(train_p)

future   = model_prophet.make_future_dataframe(periods=len(test_p))
forecast = model_prophet.predict(future)

# Evaluate on test portion
pred_prophet = forecast.tail(len(test_p))["yhat"].values
mae_p  = mean_absolute_error(test_p["y"], pred_prophet)
rmse_p = np.sqrt(mean_squared_error(test_p["y"], pred_prophet))
r2_p   = r2_score(test_p["y"], pred_prophet)

print(f"\n Prophet Evaluation ({city}):")
print(f"   MAE:  {mae_p:.3f} °C")
print(f"   RMSE: {rmse_p:.3f} °C")
print(f"   R²:   {r2_p:.3f}")

fig = plot_plotly(model_prophet, forecast)
fig.update_layout(template="plotly_dark", title=f"Prophet Forecast — {city}")
fig.write_html(f"reports/figures/prophet_forecast_{city.lower()}.html")
```

### 9.2 XGBoost with Lag Features

```python
from xgboost import XGBRegressor

def create_lag_features(series: pd.Series, lags: list = [1,2,3,7,14,30]) -> pd.DataFrame:
    """Create lag and rolling features for time-series modeling."""
    df_lag = pd.DataFrame({"y": series})
    for lag in lags:
        df_lag[f"lag_{lag}"] = series.shift(lag)
    df_lag["rolling_mean_7"]  = series.shift(1).rolling(7).mean()
    df_lag["rolling_std_7"]   = series.shift(1).rolling(7).std()
    df_lag["rolling_mean_30"] = series.shift(1).rolling(30).mean()
    df_lag["month"]           = series.index.month
    df_lag["day_of_week"]     = series.index.dayofweek
    df_lag["day_of_year"]     = series.index.dayofyear
    return df_lag.dropna()

lag_df = create_lag_features(city_df)
X_lag = lag_df.drop("y", axis=1)
y_lag = lag_df["y"]

train_cutoff = int(len(lag_df) * 0.8)
X_train, X_test = X_lag.iloc[:train_cutoff], X_lag.iloc[train_cutoff:]
y_train, y_test = y_lag.iloc[:train_cutoff], y_lag.iloc[train_cutoff:]

xgb_model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    early_stopping_rounds=30,
    eval_metric="rmse",
    verbosity=0
)
xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

pred_xgb = xgb_model.predict(X_test)
mae_xgb  = mean_absolute_error(y_test, pred_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test, pred_xgb))
r2_xgb   = r2_score(y_test, pred_xgb)

print(f"\n XGBoost Evaluation ({city}):")
print(f"   MAE:  {mae_xgb:.3f} °C")
print(f"   RMSE: {rmse_xgb:.3f} °C")
print(f"   R²:   {r2_xgb:.3f}")
```

### 9.3 Ensemble Model (Stacking)

```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict

# Stack ARIMA + Prophet + XGBoost predictions using a Ridge meta-learner
# (Build predictions from all three models on a validation set)

meta_X = np.column_stack([
    # Replace with actual held-out OOF predictions from each model
    pred_arima_oof,
    pred_prophet_oof,
        arima_test,
        prophet_test,
        xgb_test
])
meta_y = y_test_common   # aligned ground truth

meta_learner = Ridge(alpha=1.0)
meta_learner.fit(meta_X[:train_meta], meta_y[:train_meta])
ensemble_preds = meta_learner.predict(meta_X[train_meta:])

mae_ens  = mean_absolute_error(meta_y[train_meta:], ensemble_preds)
rmse_ens = np.sqrt(mean_squared_error(meta_y[train_meta:], ensemble_preds))

print(f"\n Ensemble Evaluation:")
print(f"   MAE:  {mae_ens:.3f} °C")
print(f"   RMSE: {rmse_ens:.3f} °C")
```

### 9.4 Model Comparison Table

```python
results = {
    "Model":   ["ARIMA",  "Prophet", "XGBoost", "Ensemble"],
    "MAE":     [mae,      mae_p,     mae_xgb,   mae_ens],
    "RMSE":    [rmse,     rmse_p,    rmse_xgb,  rmse_ens],
    "R²":      [r2,       r2_p,      r2_xgb,    "—"]
}
results_df = pd.DataFrame(results).set_index("Model")
print(results_df.round(3).to_markdown())

# Plotly bar comparison
fig = px.bar(
    results_df.reset_index().melt(id_vars="Model"),
    x="Model", y="value", color="variable",
    barmode="group",
    title="Model Performance Comparison — Temperature Forecasting",
    template="plotly_dark"
)
fig.write_html("reports/figures/model_comparison.html")
```

---

## 10. Unique Advanced Analyses

### 10.1 Climate Pattern Analysis (Long-Term)

```python
# notebooks/06_unique_analyses.ipynb — Part A: Climate

# Annual temperature trend per continent (map latitude to continent)
import pycountry_convert as pc

def get_continent(country_name):
    """Map country name to continent."""
    try:
        code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        cont_code = pc.country_alpha2_to_continent_code(code)
        return pc.convert_continent_code_to_continent_name(cont_code)
    except:
        return "Unknown"

df_clean["continent"] = df_clean["country"].apply(get_continent)

annual_continent = (
    df_clean.groupby(["year", "continent"])["temperature_celsius"]
    .mean()
    .reset_index()
)

fig = px.line(
    annual_continent[annual_continent["continent"] != "Unknown"],
    x="year", y="temperature_celsius", color="continent",
    title="Annual Average Temperature by Continent (Climate Trend)",
    template="plotly_dark",
    labels={"temperature_celsius": "Avg Temp (°C)"}
)
fig.write_html("reports/figures/climate_continent_trend.html")
```

### 10.2 Environmental Impact — Air Quality vs Weather

```python
# ── Correlation: AQI vs Temperature / Humidity ────────────────────────────────
aqi_col = "air_quality_us-epa-index"
if aqi_col in df_clean.columns:
    fig = px.scatter(
        df_clean.sample(5000, random_state=42),
        x="temperature_celsius", y=aqi_col,
        color="humidity",
        color_continuous_scale="Viridis",
        opacity=0.5,
        title="Air Quality Index vs Temperature (colored by Humidity)",
        template="plotly_dark",
        trendline="ols"
    )
    fig.write_html("reports/figures/aqi_vs_temp.html")
    fig.show()

    # Correlation breakdown by season
    aqi_season = df_clean.groupby("season")[[aqi_col, "temperature_celsius", "humidity"]].corr()
    print("AQI Correlations by Season:\n", aqi_season)
```

### 10.3 Feature Importance with SHAP

```python
import shap

explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test)

# Summary plot
plt.figure(figsize=(10, 7))
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.title("XGBoost Feature Importance (SHAP Values)", fontweight="bold")
plt.tight_layout()
plt.savefig("reports/figures/shap_feature_importance.png", dpi=150, bbox_inches="tight")
plt.show()

# Beeswarm plot
shap.summary_plot(shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig("reports/figures/shap_beeswarm.png", dpi=150, bbox_inches="tight")
```

### 10.4 Spatial Analysis with Folium

```python
import folium
from folium.plugins import HeatMap

# ── Temperature Heatmap of the World ─────────────────────────────────────────
city_summary = (
    df_clean.groupby(["location_name", "latitude", "longitude"])
    ["temperature_celsius"].mean()
    .reset_index()
    .dropna()
)

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

heat_data = [
    [row["latitude"], row["longitude"], row["temperature_celsius"]]
    for _, row in city_summary.iterrows()
]
HeatMap(heat_data, radius=15, blur=10, min_opacity=0.3).add_to(m)

m.save("reports/figures/global_temp_heatmap.html")
print(" Spatial heatmap saved.")
```

### 10.5 Geographical Patterns (Choropleth)

```python
import plotly.express as px

country_avg = (
    df_clean.groupby("country")["temperature_celsius"]
    .mean()
    .reset_index()
)

fig = px.choropleth(
    country_avg,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    color_continuous_scale="RdYlBu_r",
    title="Average Temperature by Country",
    template="plotly_dark"
)
fig.update_geos(showcoastlines=True, coastlinecolor="white", showland=True)
fig.write_html("reports/figures/choropleth_temp.html")
```

---

## 11. Deliverables: Report / Dashboard

### Recommended: Plotly Dash Interactive Dashboard

```python
# dashboard.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])

app = dash.Dash(__name__, title=" Weather Forecasting Dashboard")

app.layout = html.Div([
    html.H1(" Global Weather Trend Forecasting",
            style={"textAlign": "center", "color": "#FF6B35", "fontFamily": "Arial"}),

    html.P("PM Accelerator Mission: Empower the next generation of AI professionals.",
           style={"textAlign": "center", "color": "#aaa", "fontSize": "12px"}),

    html.Div([
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label": c, "value": c} for c in sorted(df["location_name"].unique())],
            value="London",
            style={"width": "300px"}
        ),
    ], style={"padding": "20px"}),

    dcc.Graph(id="temp-chart"),
    dcc.Graph(id="precip-chart"),
    dcc.Graph(id="model-compare-chart"),
], style={"backgroundColor": "#1a1a2e", "minHeight": "100vh", "padding": "20px"})

@app.callback(
    Output("temp-chart", "figure"),
    Input("city-dropdown", "value")
)
def update_temp(city):
    city_data = df[df["location_name"] == city].sort_values("last_updated")
    fig = px.line(city_data, x="last_updated", y="temperature_celsius",
                  title=f"Temperature Trend — {city}", template="plotly_dark",
                  color_discrete_sequence=["#FF6B35"])
    return fig

if __name__ == "__main__":
    app.run(debug=True)
```

Run with:
```bash
pip install dash
python dashboard.py
# Open: http://127.0.0.1:8050
```

---

## 12. Demo Video Guide

**Tools:** Loom (free), OBS Studio, or Google Meet screen recording

### 2-Minute Script Outline

| Time | Section |
|------|---------|
| 0:00–0:15 | Brief intro: "Hi, I'm [name]. This is my PM Accelerator weather forecasting assessment." |
| 0:15–0:40 | Show the GitHub repo structure and README |
| 0:40–1:10 | Walk through 2–3 key visualizations (choropleth, anomaly chart, correlation matrix) |
| 1:10–1:40 | Show the model comparison table and highlight the best result |
| 1:40–2:00 | Close: "The ensemble model achieved the best performance. The code is modular and extensible." |

**Hosting options:** Google Drive (share link → "Anyone with link can view"), YouTube (unlisted), Loom (free public link)

---

## 13. Submission Checklist

Before submitting your Google Form, verify every item:

- [ ] GitHub repo is **public** (or private with `community@pmaccelerator.io` + `hr@pmaccelerator.io` as collaborators)
- [ ] `requirements.txt` or `environment.yml` is present and accurate
- [ ] `README.md` explains: project overview, setup steps, how to run, key findings
- [ ] PM Accelerator mission statement is displayed in your report/dashboard
- [ ] At least one forecasting model is trained and evaluated with metrics (MAE, RMSE, R²)
- [ ] Visualizations for temperature and precipitation are included
- [ ] Clone/Download is enabled on the repo
- [ ] Demo video is recorded and a **viewable** link is included
- [ ] Google Form is submitted before the 7-day deadline

---

## 14. Tips to Stand Out

### Code Quality
- Use **type hints** in Python functions
- Add **docstrings** to all functions
- Write at least a few **unit tests** (`pytest`) for your cleaning pipeline
- Use `logging` instead of raw `print()` for pipeline steps

### Analysis Depth
- Don't just forecast one city — show results for **3–5 diverse cities** (different climates/continents)
- Include a **residual analysis plot** for each model (shows you understand model diagnostics)
- Mention **confidence intervals** in your forecast plots

### Presentation
- Include the **PM Accelerator mission** prominently in your report header
- Add a **Key Insights** section (3–5 bullet points summarizing what you discovered)
- Make at least one visualization **interactive** (Plotly or Folium)

### README Essentials

Your README should include:
1. **Project Title & Description** (2–3 sentences)
2. **PM Accelerator Mission** (copy from their website)
3. **Tech Stack** (Python, libraries)
4. **Setup Instructions** (clone → install → run)
5. **Project Structure** (folder tree)
6. **Key Results** (table with model metrics)
7. **Demo Video Link**
8. **Author** (your name + LinkedIn)

---

> **Built for PM Accelerator AI Engineer Internship Assessment**
> Dataset: [Global Weather Repository — Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
> PM Accelerator: [pmaccelerator.io](https://www.pmaccelerator.io)
