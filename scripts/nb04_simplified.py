import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("NOTEBOOK 04: MODEL BUILDING - BASIC (ARIMA)")
print("="*60)

try:
    # Load data
    print("\n Loading dataset...")
    df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])
    
    # Select city
    city = "London"
    city_data = df[df["location_name"] == city].copy()
    city_ts = (city_data.set_index("last_updated")["temperature_celsius"]
               .resample("D").mean().interpolate())
    
    print(f"\n City selected: {city}")
    print(f"   Length: {len(city_ts):,} days")
    
    # Stationarity test
    print(f"\n Augmented Dickey-Fuller Test:")
    result = adfuller(city_ts.dropna())
    print(f"   Test Statistic: {result[0]:.6f}")
    print(f"   p-value: {result[1]:.6f}")
    if result[1] < 0.05:
        print(f"   → STATIONARY")
    else:
        print(f"   → NON-STATIONARY")
    
    # Train/test split
    train_size = int(len(city_ts) * 0.8)
    train_ts = city_ts.iloc[:train_size]
    test_ts = city_ts.iloc[train_size:]
    
    print(f"\n Train/Test Split:")
    print(f"   Train: {len(train_ts):,} ({len(train_ts)/len(city_ts)*100:.1f}%)")
    print(f"   Test: {len(test_ts):,} ({len(test_ts)/len(city_ts)*100:.1f}%)")
    
    # Auto-ARIMA
    print(f"\n Fitting Auto-ARIMA...")
    auto_model = pm.auto_arima(train_ts, seasonal=True, m=12, stepwise=True,
                               suppress_warnings=True, error_action="ignore",
                               max_p=5, max_q=5, max_P=2, max_Q=2, trace=False)
    
    forecast_vals, conf_int = auto_model.predict(n_periods=len(test_ts), return_conf_int=True)
    
    # Metrics
    mae = mean_absolute_error(test_ts, forecast_vals)
    rmse = np.sqrt(mean_squared_error(test_ts, forecast_vals))
    r2 = r2_score(test_ts, forecast_vals)
    mape = np.mean(np.abs((test_ts - forecast_vals) / test_ts)) * 100
    
    print(f"\n ARIMA Evaluation Metrics:")
    print(f"   MAE: {mae:.3f}°C")
    print(f"   RMSE: {rmse:.3f}°C")
    print(f"   R²: {r2:.3f}")
    print(f"   MAPE: {mape:.2f}%")
    
    # Save results
    results = pd.DataFrame({
        "Model": ["ARIMA"],
        "City": [city],
        "MAE": [mae],
        "RMSE": [rmse],
        "R2": [r2],
        "MAPE": [mape]
    })
    results.to_csv("reports/model_results.csv", index=False)
    
    print(f"\n Results saved to reports/model_results.csv")
    
    print(f"\n Notebook 04 Complete!")
    
except Exception as e:
    print(f" ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
