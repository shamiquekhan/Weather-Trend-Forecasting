import pandas as pd
import numpy as np
import pmdarima as pm
from prophet import Prophet
from xgboost import XGBRegressor

class TimeSeriesModel:
    """Base class for models."""
    pass

class ARIMAModel(TimeSeriesModel):
    def __init__(self):
        self.model = None
    
    def fit(self, data):
        self.model = pm.auto_arima(data, seasonal=True, m=12, suppress_warnings=True)
        return self.model
    
    def predict(self, n_periods):
        return self.model.predict(n_periods=n_periods)

class ProphetModel(TimeSeriesModel):
    def __init__(self):
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        
    def fit(self, df):
        self.model.fit(df)
        return self.model

class XGBoostModel(TimeSeriesModel):
    def __init__(self):
        self.model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6)
        
    def fit(self, X, y):
        self.model.fit(X, y)
        return self.model
