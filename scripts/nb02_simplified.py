import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("NOTEBOOK 02: EXPLORATORY DATA ANALYSIS (BASIC)")
print("="*60)

try:
    # Load data
    print("\n Loading cleaned dataset...")
    df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])
    print(f"   Shape: {df.shape}")
    
    # Analysis 1: Temperature trends
    print("\n Analysis 1: Global Temperature Trends")
    daily_avg = df.groupby("last_updated")["temperature_celsius"].mean().reset_index()
    fig = px.line(daily_avg, x="last_updated", y="temperature_celsius",
                  title="Global Average Daily Temperature", template="plotly_dark", height=400)
    fig.write_html("reports/figures/01_global_temp_trend.html")
    print(f"   Mean: {daily_avg['temperature_celsius'].mean():.2f}°C")
    print(f"   Range: {daily_avg['temperature_celsius'].min():.2f}°C - {daily_avg['temperature_celsius'].max():.2f}°C")
    
    # Analysis 2: Monthly distribution
    print("\n Analysis 2: Monthly Temperature Distribution")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(data=df, x="month", y="temperature_celsius", palette="coolwarm", ax=ax)
    ax.set_title("Monthly Temperature Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("reports/figures/02_monthly_temp_boxplot.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   Saved: 02_monthly_temp_boxplot.png")
    
    # Analysis 3: Top cities by precipitation
    print("\n Analysis 3: Top Cities by Precipitation")
    top_rain = df.groupby("location_name")["precip_mm"].mean().sort_values(ascending=False).head(10)
    print(f"   Wettest: {top_rain.index[0]} ({top_rain.iloc[0]:.1f}mm)")
    
    # Analysis 4: Correlations
    print("\n Analysis 4: Feature Correlations")
    numeric_features = ["temperature_celsius", "humidity", "wind_kph", "precip_mm", 
                       "pressure_mb", "visibility_km", "uv_index"]
    corr_matrix = df[numeric_features].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn", 
                center=0, ax=ax, cbar_kws={"label": "Correlation"})
    ax.set_title("Feature Correlation Matrix", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig("reports/figures/04_correlation_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   Saved: 04_correlation_matrix.png")
    
    # Analysis 5: Precipitation by season
    print("\n Analysis 5: Precipitation by Season")
    season_precip = df.groupby("season")["precip_mm"].mean()
    print(f"   Wettest season: {season_precip.idxmax()} ({season_precip.max():.1f}mm)")
    
    print(f"\n Summary Statistics:")
    print(f"   Average temperature: {df['temperature_celsius'].mean():.1f}°C")
    print(f"   Average humidity: {df['humidity'].mean():.1f}%")
    print(f"   Total precipitation: {df['precip_mm'].sum():.1f}mm")
    
    print(f"\n Notebook 02 Complete!")
    
except Exception as e:
    print(f" ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
