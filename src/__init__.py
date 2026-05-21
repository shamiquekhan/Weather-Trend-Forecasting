"""
Weather Trend Forecasting — Source Module

A production-grade machine learning pipeline for global weather forecasting.

Submodules:
    data_loader: Data ingestion and preprocessing utilities
    eda_utils: Exploratory data analysis visualization helpers
    models: Forecasting model implementations
    ensemble: Ensemble stacking utilities
    spatial_utils: Geospatial analysis tools

Example:
    >>> from src.data_loader import load_data, clean_weather_data
    >>> df = load_data("data/GlobalWeatherRepository.csv")
    >>> df_clean = clean_weather_data(df)

Version: 1.0.0
Author: [Your Name]
Created: May 15, 2026
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import key functions for easy access
from src.data_loader import load_data, clean_weather_data, get_city_timeseries
from src.eda_utils import (
    plot_temperature_trends,
    plot_monthly_distribution,
    plot_precipitation_cities,
    plot_correlation_matrix,
    plot_anomalies,
    plot_precipitation_heatmap
)

__all__ = [
    # Data loading
    'load_data',
    'clean_weather_data',
    'get_city_timeseries',
    
    # EDA utilities
    'plot_temperature_trends',
    'plot_monthly_distribution',
    'plot_precipitation_cities',
    'plot_correlation_matrix',
    'plot_anomalies',
    'plot_precipitation_heatmap',
]
