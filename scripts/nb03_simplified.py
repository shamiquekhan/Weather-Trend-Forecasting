import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("NOTEBOOK 03: ADVANCED EDA & ANOMALY DETECTION")
print("="*60)

try:
    # Load data
    print("\n Loading dataset...")
    df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])
    
    # Anomaly detection features
    features = ["temperature_celsius", "humidity", "wind_kph", "precip_mm", "pressure_mb"]
    X = df[features].dropna()
    
    print(f"\n Isolation Forest Anomaly Detection")
    clf_if = IForest(contamination=0.02, random_state=42, n_jobs=-1)
    clf_if.fit(X)
    df.loc[X.index, "anomaly_iforest"] = clf_if.labels_
    n_anomalies = (df["anomaly_iforest"] == 1).sum()
    print(f"   Anomalies detected: {n_anomalies:,} ({n_anomalies/len(df)*100:.2f}%)")
    
    print(f"\n LOF Anomaly Detection")
    clf_lof = LOF(contamination=0.02, n_neighbors=20)
    clf_lof.fit(X)
    df.loc[X.index, "anomaly_lof"] = clf_lof.labels_
    both = ((df["anomaly_iforest"] == 1) & (df["anomaly_lof"] == 1)).sum()
    print(f"   LOF anomalies: {(df['anomaly_lof']==1).sum():,}")
    print(f"   Consensus: {both:,}")
    
    print(f"\n Anomaly characteristics:")
    for col in features:
        normal_mean = df[df["anomaly_iforest"] == 0][col].mean()
        anomaly_mean = df[df["anomaly_iforest"] == 1][col].mean()
        pct_diff = (anomaly_mean - normal_mean) / normal_mean * 100 if normal_mean != 0 else 0
        print(f"   {col}: {normal_mean:.2f} (normal) vs {anomaly_mean:.2f} (anomaly) ({pct_diff:+.1f}%)")
    
    print(f"\n Seasonal patterns:")
    for season in df['season'].unique():
        if pd.notna(season):
            temp = df[df['season'] == season]['temperature_celsius'].mean()
            precip = df[df['season'] == season]['precip_mm'].sum()
            print(f"   {season}: {temp:.1f}°C, {precip:.1f}mm")
    
    # Save with anomaly flags
    df.to_csv("data/weather_with_anomalies.csv", index=False)
    print(f"\n Dataset with anomalies saved")
    
    print(f"\n Notebook 03 Complete!")
    
except Exception as e:
    print(f" ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
