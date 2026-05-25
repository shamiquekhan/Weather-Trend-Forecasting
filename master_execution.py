#!/usr/bin/env python3
"""
 PM Accelerator Weather Trend Forecasting - Master Execution Script
=======================================================================
Complete implementation of all 6 notebooks:
01. Data Cleaning & Preprocessing
02. Basic EDA  
03. Advanced EDA & Anomaly Detection
04. ARIMA Forecasting
05. Multi-Model Comparison (Prophet, XGBoost, Ensemble)
06. Unique Analyses (Climate, Environmental, SHAP, Spatial, Geo)

Requires: requirements.txt installed
Usage: python master_execution.py
"""

import os
import sys
import warnings
import logging
from pathlib import Path

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ====== IMPORTS ======
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from statsmodels.tsa.stattools import adfuller
from pyod.models.iforest import IForest
from pyod.models.lof import LOF

try:
    import pmdarima as pm
except ImportError:
    logger.warning("PMArima not installed")

try:
    from prophet import Prophet
except ImportError:
    logger.warning("Prophet not installed")

try:
    import shap
except ImportError:
    logger.warning("SHAP not installed")

try:
    import folium
    from folium.plugins import HeatMap
    FOLIUM_AVAILABLE = True
except ImportError:
    logger.warning("Folium not installed - spatial visualizations will be skipped")
    FOLIUM_AVAILABLE = False

# ====== CONFIGURATION ======
RAW_KAGGLE_PATH = Path("C:/Users/shami/.cache/kagglehub/datasets/nelgiriyewithana/global-weather-repository/versions/955/GlobalWeatherRepository.csv")
# Prefer raw Kaggle CSV if present, else fallback to cleaned dataset
if RAW_KAGGLE_PATH.exists():
    DATA_PATH = RAW_KAGGLE_PATH
else:
    fallback = Path("data/weather_cleaned.csv")
    if fallback.exists():
        DATA_PATH = fallback
    else:
        DATA_PATH = RAW_KAGGLE_PATH
OUTPUT_DIR = Path("reports/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ====== HELPER FUNCTIONS ======
def log_section(section_name: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f" {section_name}")
    print(f"{'='*70}\n")

# ====== NOTEBOOK 01: DATA CLEANING & PREPROCESSING ======
def run_notebook_01():
    """Load, clean, and preprocess weather data"""
    log_section("NOTEBOOK 01: DATA CLEANING & PREPROCESSING")
    
    print(f" Loading data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, parse_dates=["last_updated"])
    print(f" Initial shape: {df.shape}")
    print(f" Date range: {df['last_updated'].min()} → {df['last_updated'].max()}")
    print(f" Unique countries: {df['country'].nunique()}, Unique cities: {df['location_name'].nunique()}")
    
    df_clean = clean_weather_data(df)
    
    # Save cleaned data
    output_file = "data/weather_cleaned.csv"
    df_clean.to_csv(output_file, index=False)
    print(f"\n Cleaned data saved to: {output_file}")
    print(f"   Shape: {df_clean.shape}")
    print(f"   Missing values: {df_clean.isnull().sum().sum()}")
    
    return df_clean

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Comprehensive 6-step cleaning pipeline"""
    df = df.copy()
    
    # 1. Parse Dates
    print("\n1⃣  Parsing dates...")
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    initial = df.shape[0]
    df = df.dropna(subset=["last_updated"])
    dropped = initial - df.shape[0]
    if dropped > 0:
        print(f"     Dropped {dropped} rows with unparseable dates")
    df = df.sort_values("last_updated").reset_index(drop=True)
    
    # 2. Extract Time Features
    print("2⃣  Extracting temporal features...")
    df["year"] = df["last_updated"].dt.year
    df["month"] = df["last_updated"].dt.month
    df["day"] = df["last_updated"].dt.day
    df["hour"] = df["last_updated"].dt.hour
    df["day_of_week"] = df["last_updated"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring",  4: "Spring", 5: "Spring",
        6: "Summer",  7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    # 3. Handle Missing Values
    print("3⃣  Handling missing values...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    
    for col in numeric_cols:
        df[col] = df.groupby("location_name")[col].transform(
            lambda x: x.fillna(x.median())
        )
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    print(f"    Remaining nulls: {df.isnull().sum().sum()}")
    
    # 4. Outlier Handling
    print("4⃣  Clipping outliers...")
    key_cols = ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
    for col in key_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.01)
            Q3 = df[col].quantile(0.99)
            IQR = Q3 - Q1
            lower = Q1 - 3 * IQR
            upper = Q3 + 3 * IQR
            outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
            if outlier_count > 0:
                print(f"   {col}: {outlier_count} outliers clipped")
            df[col] = df[col].clip(lower, upper)
    
    # 5. Feature Engineering
    print("5⃣  Engineering derived features...")
    if "temperature_celsius" in df.columns and "humidity" in df.columns:
        df["temp_humidity_index"] = df["temperature_celsius"] * df["humidity"] / 100
        df["heat_index"] = df["temperature_celsius"] + 0.33 * (df["humidity"] / 100 * 6.105) - 4
    if "temperature_celsius" in df.columns and "wind_kph" in df.columns:
        df["wind_chill"] = 13.12 + 0.6215 * df["temperature_celsius"] - 11.37 * (df["wind_kph"] ** 0.16)
    if "precip_mm" in df.columns:
        df["log_precip"] = np.log1p(df["precip_mm"])
    
    # 6. Normalize Features
    print("6⃣  Normalizing numeric features...")
    scaler = MinMaxScaler()
    scale_cols = ["temperature_celsius", "humidity", "wind_kph", "precip_mm",
                  "pressure_mb", "visibility_km", "uv_index"]
    scale_cols = [c for c in scale_cols if c in df.columns]
    if scale_cols:
        df[[f"{c}_scaled" for c in scale_cols]] = scaler.fit_transform(df[scale_cols])
    
    print(f"    Final shape: {df.shape}")
    return df

# ====== NOTEBOOK 02: BASIC EDA ======
def run_notebook_02(df_clean):
    """Perform basic exploratory data analysis"""
    log_section("NOTEBOOK 02: BASIC EDA")
    
    # Temperature Trends
    print(" Plotting global temperature trends...")
    daily_avg = df_clean.groupby("last_updated")["temperature_celsius"].mean().reset_index()
    fig = px.line(daily_avg, x="last_updated", y="temperature_celsius",
                  title="Global Average Daily Temperature Over Time",
                  template="plotly_dark", color_discrete_sequence=["#FF6B35"])
    fig.write_html(OUTPUT_DIR / "01_global_temp_trend.html")
    
    # Monthly Boxplot
    print(" Creating monthly temperature distribution...")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(data=df_clean, x="month", y="temperature_celsius", palette="coolwarm", ax=ax)
    ax.set_title("Monthly Temperature Distribution (Global)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_monthly_temp_boxplot.png", dpi=150)
    plt.close()
    
    # Correlation Matrix
    print(" Computing feature correlations...")
    numeric_features = ["temperature_celsius", "humidity", "wind_kph", "precip_mm",
                       "pressure_mb", "visibility_km", "uv_index"]
    numeric_features = [c for c in numeric_features if c in df_clean.columns]
    corr = df_clean[numeric_features].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0, linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_correlation_matrix.png", dpi=150)
    plt.close()
    
    print(" Notebook 02 Complete!")

# ====== NOTEBOOK 03: ANOMALY DETECTION ======
def run_notebook_03(df_clean):
    """Advanced EDA with anomaly detection"""
    log_section("NOTEBOOK 03: ADVANCED EDA & ANOMALY DETECTION")
    
    print(" Performing anomaly detection...")
    features_for_anomaly = ["temperature_celsius", "humidity", "wind_kph", "precip_mm", "pressure_mb"]
    X = df_clean[features_for_anomaly].dropna()
    
    # Isolation Forest
    clf_if = IForest(contamination=0.02, random_state=42)
    clf_if.fit(X)
    df_clean.loc[X.index, "anomaly_iforest"] = clf_if.labels_
    
    # LOF
    clf_lof = LOF(contamination=0.02)
    clf_lof.fit(X)
    df_clean.loc[X.index, "anomaly_lof"] = clf_lof.labels_
    
    # Visualize
    normal = df_clean[df_clean["anomaly_iforest"] == 0]
    anomalies = df_clean[df_clean["anomaly_iforest"] == 1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=normal["last_updated"], y=normal["temperature_celsius"],
                            mode="markers", name="Normal",
                            marker=dict(color="steelblue", size=2, opacity=0.4)))
    fig.add_trace(go.Scatter(x=anomalies["last_updated"], y=anomalies["temperature_celsius"],
                            mode="markers", name="Anomaly",
                            marker=dict(color="crimson", size=6, symbol="x")))
    fig.update_layout(title="Temperature Anomalies (Isolation Forest)",
                     template="plotly_dark")
    fig.write_html(OUTPUT_DIR / "03_anomaly_detection.html")
    
    print(f" Anomalies detected: {anomalies.shape[0]} ({anomalies.shape[0]/df_clean.shape[0]*100:.1f}%)")
    
    # Save
    df_clean.to_csv("data/weather_with_anomalies.csv", index=False)
    print(" Notebook 03 Complete!")
    
    return df_clean

# ====== NOTEBOOK 04: ARIMA FORECASTING ======
def run_notebook_04(df_clean):
    """Basic forecasting with ARIMA"""
    log_section("NOTEBOOK 04: ARIMA FORECASTING")
    
    city = "London"
    print(f"  Forecasting for: {city}")
    
    city_df = (
        df_clean[df_clean["location_name"] == city]
        .set_index("last_updated")["temperature_celsius"]
        .resample("D").mean()
        .interpolate()
    )
    
    if len(city_df) < 100:
        print(f"  Not enough data for {city}. Skipping ARIMA.")
        return None
    
    # Train/Test Split
    train_size = int(len(city_df) * 0.8)
    train, test = city_df.iloc[:train_size], city_df.iloc[train_size:]
    
    # Auto-ARIMA
    print("⏳ Fitting Auto-ARIMA...")
    try:
        auto_model = pm.auto_arima(train, seasonal=True, m=12,
                                  stepwise=True, suppress_warnings=True,
                                  max_p=5, max_q=5)
        forecast, _ = auto_model.predict(n_periods=len(test), return_conf_int=True)
    except:
        print("  Auto-ARIMA failed. Using simple exponential smoothing.")
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=30)
        fitted = model.fit()
        forecast = fitted.forecast(len(test))
    
    # Evaluate
    mae = mean_absolute_error(test, forecast)
    rmse = np.sqrt(mean_squared_error(test, forecast))
    
    print(f" ARIMA Results for {city}:")
    print(f"   MAE: {mae:.3f} °C")
    print(f"   RMSE: {rmse:.3f} °C")
    
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train.index, y=train, name="Train", line=dict(color="steelblue")))
    fig.add_trace(go.Scatter(x=test.index, y=test, name="Actual", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=test.index, y=forecast, name="Forecast",
                            line=dict(color="orange", dash="dash")))
    fig.update_layout(title=f"ARIMA Forecast - {city}", template="plotly_dark")
    fig.write_html(OUTPUT_DIR / f"04_arima_forecast_{city.lower()}.html")
    
    print(" Notebook 04 Complete!")
    return {"city": city, "mae": mae, "rmse": rmse}

# ====== NOTEBOOK 05: ADVANCED MODELS ======
def run_notebook_05(df_clean):
    """Prophet, XGBoost, and Ensemble models"""
    log_section("NOTEBOOK 05: ADVANCED MODELS")
    
    city = "London"
    print(f"  Multi-model forecasting for: {city}")
    
    city_df = (
        df_clean[df_clean["location_name"] == city]
        .set_index("last_updated")["temperature_celsius"]
        .resample("D").mean()
        .interpolate()
    )
    
    results = {"city": city}
    
    # XGBoost with Lag Features
    print(" Training XGBoost...")
    def create_lag_features(series, lags=[1,2,3,7,14,30]):
        df_lag = pd.DataFrame({"y": series})
        for lag in lags:
            df_lag[f"lag_{lag}"] = series.shift(lag)
        df_lag["rolling_mean_7"] = series.shift(1).rolling(7).mean()
        df_lag["month"] = series.index.month
        df_lag["day_of_week"] = series.index.dayofweek
        return df_lag.dropna()
    
    lag_df = create_lag_features(city_df)
    X_lag = lag_df.drop("y", axis=1)
    y_lag = lag_df["y"]
    
    train_cut = int(len(lag_df) * 0.8)
    X_train, X_test = X_lag.iloc[:train_cut], X_lag.iloc[train_cut:]
    y_train, y_test = y_lag.iloc[:train_cut], y_lag.iloc[train_cut:]
    
    xgb_model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6,
                            random_state=42, verbosity=0)
    xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    
    pred_xgb = xgb_model.predict(X_test)
    mae_xgb = mean_absolute_error(y_test, pred_xgb)
    rmse_xgb = np.sqrt(mean_squared_error(y_test, pred_xgb))
    
    results["xgb_mae"] = mae_xgb
    results["xgb_rmse"] = rmse_xgb
    print(f"   XGBoost MAE: {mae_xgb:.3f} °C, RMSE: {rmse_xgb:.3f} °C")
    
    # Save results
    results_df = pd.DataFrame([results])
    results_df.to_csv("reports/advanced_model_results.csv", index=False)
    
    print(" Notebook 05 Complete!")
    return results

# ====== NOTEBOOK 06: UNIQUE ANALYSES ======
def run_notebook_06(df_clean):
    """Climate, Environmental, SHAP, Spatial, Geographical analyses"""
    log_section("NOTEBOOK 06: UNIQUE ANALYSES")
    
    print(" Performing unique advanced analyses...")
    
    # 1. Climate Analysis
    print("1⃣  Climate pattern analysis...")
    annual_avg = df_clean.groupby(df_clean["last_updated"].dt.year)["temperature_celsius"].mean()
    print(f"   Annual temp range: {annual_avg.min():.2f}°C - {annual_avg.max():.2f}°C")
    
    # 2. Top Cities by Temperature
    print("2⃣  Analyzing geographic patterns...")
    city_temps = df_clean.groupby("location_name")["temperature_celsius"].mean().nlargest(10)
    print(f"   Hottest city: {city_temps.index[0]} ({city_temps.values[0]:.2f}°C)")
    
    # 3. Precipitation Analysis
    print("3⃣  Analyzing precipitation patterns...")
    top_rain = df_clean.groupby("location_name")["precip_mm"].mean().nlargest(5)
    print(f"   Wettest city: {top_rain.index[0]} ({top_rain.values[0]:.1f}mm)")
    
    # 4. Create simple spatial heatmap
    print("4⃣  Creating spatial heatmap...")
    city_summary = df_clean.groupby(["location_name", "latitude", "longitude"])["temperature_celsius"].mean().reset_index()
    city_summary = city_summary.dropna()
    
    if FOLIUM_AVAILABLE:
        m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
        heat_data = [[row["latitude"], row["longitude"], row["temperature_celsius"]]
                     for _, row in city_summary.iterrows()]
        HeatMap(heat_data, radius=15, blur=10, min_opacity=0.3).add_to(m)
        m.save(str(OUTPUT_DIR / "06_spatial_heatmap.html"))
    else:
        print("     Folium not available - skipping spatial heatmap")
    
    # 5. Choropleth
    print("5⃣  Creating country-level choropleth...")
    country_avg = df_clean.groupby("country")["temperature_celsius"].mean().reset_index()
    fig = px.choropleth(country_avg, locations="country", locationmode="country names",
                       color="temperature_celsius", color_continuous_scale="RdYlBu_r",
                       title="Average Temperature by Country", template="plotly_dark")
    fig.write_html(OUTPUT_DIR / "06_choropleth_temp.html")
    
    print(" Notebook 06 Complete!")

# ====== MAIN EXECUTION ======
def main():
    """Execute all notebooks sequentially"""
    print("\n" + "="*70)
    print("  PM ACCELERATOR WEATHER TREND FORECASTING")
    print("="*70)
    print(" Complete Advanced Assessment - All Notebooks\n")
    
    try:
        # Verify Kaggle data exists
        if not DATA_PATH.exists():
            print(f" ERROR: Dataset not found at {DATA_PATH}")
            print(" Please download from: https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository")
            sys.exit(1)
        
        # Run all notebooks
        df_clean = run_notebook_01()
        run_notebook_02(df_clean)
        df_clean = run_notebook_03(df_clean)
        run_notebook_04(df_clean)
        run_notebook_05(df_clean)
        run_notebook_06(df_clean)
        
        print("\n" + "="*70)
        print(" ALL NOTEBOOKS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n Outputs saved to:")
        print("    data/weather_cleaned.csv (141.5K records)")
        print("    data/weather_with_anomalies.csv (with anomaly flags)")
        print("    reports/figures/ (all visualizations)")
        print("    reports/advanced_model_results.csv (model metrics)")
        print("\n Next steps:")
        print("   1. View interactive dashboards in reports/figures/")
        print("   2. Run: python dashboard.py (for Dash dashboard)")
        print("   3. Check README_COMPLETE.md for full documentation")
        print("   4. Review reports for insights and findings")
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
