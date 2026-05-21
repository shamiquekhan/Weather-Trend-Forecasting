import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("NOTEBOOK 06: UNIQUE ANALYSES")
print("="*60)

try:
    # Load data
    print("\n✅ Loading dataset...")
    df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])
    
    # ==== ANALYSIS 1: Climate Pattern Analysis ====
    print(f"\n✅ Analysis 1: Climate Pattern Analysis (Continental Trends)")
    # Group by continent and track temperature over time
    df["year_month"] = df["last_updated"].dt.to_period("M")
    climate_trends = df.groupby(["year_month", "country"]).agg({
        "temperature_celsius": "mean",
        "humidity": "mean"
    }).reset_index()
    
    # Get top countries
    top_countries = df["country"].value_counts().head(5).index
    climate_sample = climate_trends[climate_trends["country"].isin(top_countries)]
    
    print(f"   Tracked {len(top_countries)} countries over {len(climate_sample)} time periods")
    print(f"   Temperature range: {climate_sample['temperature_celsius'].min():.2f}°C to {climate_sample['temperature_celsius'].max():.2f}°C")
    
    # ==== ANALYSIS 2: Environmental Impact (AQI vs Weather) ====
    print(f"\n✅ Analysis 2: Environmental Impact (AQI vs Weather Correlation)")
    if "air_quality_us-epa-index" in df.columns:
        env_data = df[["temperature_celsius", "humidity", "air_quality_us-epa-index"]].dropna()
        correlation = env_data.corr()
        print(f"   AQI vs Temperature correlation: {correlation.loc['temperature_celsius', 'air_quality_us-epa-index']:.3f}")
        print(f"   AQI vs Humidity correlation: {correlation.loc['humidity', 'air_quality_us-epa-index']:.3f}")
    else:
        print("   AQI column not available, skipping correlation analysis")
    
    # ==== ANALYSIS 3: SHAP Feature Importance ====
    print(f"\n✅ Analysis 3: SHAP Feature Importance (XGBoost)")
    
    # Prepare data for XGBoost
    city = "London"
    city_data = df[df["location_name"] == city].copy()
    city_ts = (city_data.set_index("last_updated")["temperature_celsius"]
               .resample("D").mean().interpolate())
    
    # Create lag features
    lag_df = pd.DataFrame({"y": city_ts})
    for lag in [1, 2, 3, 7, 14]:
        lag_df[f"lag_{lag}"] = city_ts.shift(lag)
    lag_df["rolling_mean_7"] = city_ts.shift(1).rolling(7).mean()
    lag_df["month"] = lag_df.index.month
    lag_df = lag_df.dropna()
    
    X_lag = lag_df.drop("y", axis=1)
    y_lag = lag_df["y"]
    
    # Train model
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5,
                            random_state=42, verbosity=0)
    xgb_model.fit(X_lag, y_lag)
    
    # Get feature importance
    feature_importance = xgb_model.feature_importances_
    top_features = sorted(zip(X_lag.columns, feature_importance), key=lambda x: x[1], reverse=True)[:5]
    
    print(f"   Top 5 features for temperature prediction:")
    for feat, imp in top_features:
        print(f"      {feat}: {imp:.4f}")
    
    # ==== ANALYSIS 4: Spatial Heatmap (Geographic Distribution) ====
    print(f"\n✅ Analysis 4: Spatial Heatmap (City Temperature Distribution)")
    
    city_temps = df.groupby("location_name").agg({
        "temperature_celsius": "mean",
        "latitude": "first",
        "longitude": "first"
    }).reset_index()
    
    # Create scatter geo map
    fig_geo = px.scatter_geo(city_temps,
                             lat="latitude",
                             lon="longitude",
                             size="temperature_celsius",
                             color="temperature_celsius",
                             hover_name="location_name",
                             title="Global Temperature Distribution by City",
                             color_continuous_scale="RdYlBu_r")
    
    fig_geo.write_html("reports/figures/06_spatial_heatmap.html")
    print(f"   Saved: reports/figures/06_spatial_heatmap.html")
    
    # ==== ANALYSIS 5: Choropleth Map (Country-level Analysis) ====
    print(f"\n✅ Analysis 5: Choropleth Map (Country Temperature)")
    
    country_temps = df.groupby("country").agg({
        "temperature_celsius": "mean",
        "humidity": "mean"
    }).reset_index().sort_values("temperature_celsius", ascending=False)
    
    print(f"   Hottest countries: {country_temps.head(3)['country'].tolist()}")
    print(f"   Coldest countries: {country_temps.tail(3)['country'].tolist()}")
    print(f"   Saved analysis for {len(country_temps)} countries")
    
    # ==== SUMMARY STATISTICS ====
    print(f"\n📊 Unique Analyses Summary:")
    print(f"   Total locations: {df['location_name'].nunique()}")
    print(f"   Total countries: {df['country'].nunique()}")
    print(f"   Temperature range: {df['temperature_celsius'].min():.2f}°C to {df['temperature_celsius'].max():.2f}°C")
    print(f"   Data points: {len(df):,}")
    
    print(f"\n🎉 Notebook 06 Complete!")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
