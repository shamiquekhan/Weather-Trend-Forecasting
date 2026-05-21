import pandas as pd
import numpy as np
import os
import sys
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from prophet import Prophet
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("NOTEBOOK 05: MODEL BUILDING - ADVANCED")
print("="*60)

try:
    # Load data
    print("\n✅ Loading dataset...")
    df = pd.read_csv("data/weather_cleaned.csv", parse_dates=["last_updated"])
    
    city = "London"
    city_data = df[df["location_name"] == city].copy()
    city_ts = (city_data.set_index("last_updated")["temperature_celsius"]
               .resample("D").mean().interpolate())
    
    # Split
    train_size = int(len(city_ts) * 0.8)
    train_ts = city_ts.iloc[:train_size]
    test_ts = city_ts.iloc[train_size:]
    
    # Prophet
    print(f"\n✅ Prophet Model")
    prophet_df = city_ts.reset_index().rename(columns={"last_updated": "ds", "temperature_celsius": "y"})
    train_prophet = prophet_df.iloc[:train_size]
    
    model_prophet = Prophet(changepoint_prior_scale=0.05, seasonality_prior_scale=10,
                           yearly_seasonality=True, weekly_seasonality=True)
    with open(os.devnull, 'w') as f:
        old = sys.stdout
        sys.stdout = f
        model_prophet.fit(train_prophet)
        sys.stdout = old
    
    future = model_prophet.make_future_dataframe(periods=len(test_ts))
    forecast_prophet = model_prophet.predict(future)
    pred_prophet = forecast_prophet.tail(len(test_ts))["yhat"].values
    
    mae_p = mean_absolute_error(test_ts, pred_prophet)
    rmse_p = np.sqrt(mean_squared_error(test_ts, pred_prophet))
    r2_p = r2_score(test_ts, pred_prophet)
    print(f"   MAE: {mae_p:.3f}°C, RMSE: {rmse_p:.3f}°C, R²: {r2_p:.3f}")
    
    # XGBoost with lags
    print(f"\n✅ XGBoost Model")
    lag_df = pd.DataFrame({"y": city_ts})
    for lag in [1, 2, 3, 7, 14, 30]:
        lag_df[f"lag_{lag}"] = city_ts.shift(lag)
    lag_df["rolling_mean_7"] = city_ts.shift(1).rolling(7).mean()
    lag_df["month"] = lag_df.index.month
    lag_df = lag_df.dropna()
    
    X_lag = lag_df.drop("y", axis=1)
    y_lag = lag_df["y"]
    cut = int(len(lag_df) * 0.8)
    X_train, X_test = X_lag.iloc[:cut], X_lag.iloc[cut:]
    y_train, y_test = y_lag.iloc[:cut], y_lag.iloc[cut:]
    
    xgb_model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6,
                            random_state=42, verbosity=0, early_stopping_rounds=30)
    xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    
    pred_xgb = xgb_model.predict(X_test)
    mae_xgb = mean_absolute_error(y_test, pred_xgb)
    rmse_xgb = np.sqrt(mean_squared_error(y_test, pred_xgb))
    r2_xgb = r2_score(y_test, pred_xgb)
    print(f"   MAE: {mae_xgb:.3f}°C, RMSE: {rmse_xgb:.3f}°C, R²: {r2_xgb:.3f}")
    
    # Ensemble
    print(f"\n✅ Ensemble (Prophet + XGBoost)")
    ensemble_preds = 0.35 * pred_prophet[:len(y_test)] + 0.65 * pred_xgb
    mae_ens = mean_absolute_error(y_test, ensemble_preds)
    rmse_ens = np.sqrt(mean_squared_error(y_test, ensemble_preds))
    r2_ens = r2_score(y_test, ensemble_preds)
    print(f"   MAE: {mae_ens:.3f}°C, RMSE: {rmse_ens:.3f}°C, R²: {r2_ens:.3f}")
    
    # Save results
    results = pd.DataFrame({
        "Model": ["Prophet", "XGBoost", "Ensemble"],
        "MAE": [mae_p, mae_xgb, mae_ens],
        "RMSE": [rmse_p, rmse_xgb, rmse_ens],
        "R2": [r2_p, r2_xgb, r2_ens]
    })
    results.to_csv("reports/advanced_model_results.csv", index=False)
    
    print(f"\n🏆 Best Model: {results.loc[results['MAE'].idxmin(), 'Model']}")
    print(f"✅ Results saved to reports/advanced_model_results.csv")
    
    print(f"\n🎉 Notebook 05 Complete!")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
