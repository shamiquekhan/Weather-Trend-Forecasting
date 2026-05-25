"""
Data Loading and Cleaning Utilities for Weather Forecasting Project

This module provides robust utilities for loading, cleaning, and preprocessing
weather data for time-series forecasting models.

Usage:
    from src.data_loader import load_data, clean_weather_data
    df = load_data("data/GlobalWeatherRepository.csv")
    df_clean = clean_weather_data(df)
"""

import logging
import pandas as pd
import numpy as np
from typing import Tuple, List
from sklearn.preprocessing import MinMaxScaler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(path: str = "data/GlobalWeatherRepository.csv") -> pd.DataFrame:
    """
    Load and perform initial inspection of weather data.
    
    Args:
        path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset with parsed datetime column
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the CSV is malformed
    """
    # Try the provided path first, then fall back to commonly available candidates
    candidates = [path,
                  "data/weather_cleaned.csv",
                  "data/GlobalWeatherRepository.csv",
                  "../data/weather_cleaned.csv",
                  "notebooks/../data/weather_cleaned.csv"]
    last_exc = None
    for p in candidates:
        try:
            logger.info(f"Loading data from {p}")
            df = pd.read_csv(p, parse_dates=["last_updated"])
            logger.info(f" Loaded {df.shape[0]} rows, {df.shape[1]} columns")
            logger.info(f"   Date range: {df['last_updated'].min()} → {df['last_updated'].max()}")
            logger.info(f"   Unique countries: {df['country'].nunique()}")
            logger.info(f"   Unique cities: {df['location_name'].nunique()}")
            return df
        except FileNotFoundError as e:
            logger.debug(f"Not found: {p}")
            last_exc = e
            continue
        except Exception as e:
            logger.error(f"Error loading data from {p}: {e}")
            raise
    # If none of the candidates worked, raise the last FileNotFoundError
    logger.error(f"None of the candidate data files were found. Checked: {candidates}")
    if last_exc:
        raise last_exc
    raise FileNotFoundError(path)


def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive data cleaning and feature engineering pipeline.
    
    This function:
    1. Parses dates and removes unparseable entries
    2. Extracts temporal features (year, month, season, day_of_week)
    3. Handles missing values (per-city median imputation)
    4. Removes/clips outliers (IQR method with 3-sigma bounds)
    5. Engineers derived features (heat index, wind chill, etc.)
    6. Normalizes numeric features
    
    Args:
        df (pd.DataFrame): Raw weather DataFrame
        
    Returns:
        pd.DataFrame: Cleaned and feature-engineered DataFrame
    """
    df = df.copy()
    
    # ── 1. Parse Dates ────────────────────────────────────────────────────────
    logger.info("Step 1: Parsing dates...")
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    initial_rows = df.shape[0]
    df = df.dropna(subset=["last_updated"])
    dropped = initial_rows - df.shape[0]
    if dropped > 0:
        logger.warning(f"   Dropped {dropped} rows with unparseable dates")
    
    df = df.sort_values("last_updated").reset_index(drop=True)
    logger.info(f" Date range: {df['last_updated'].min()} → {df['last_updated'].max()}")
    
    # ── 2. Extract Time Features ──────────────────────────────────────────────
    logger.info("Step 2: Extracting temporal features...")
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
    logger.info(" Temporal features extracted")
    
    # ── 3. Handle Missing Values ──────────────────────────────────────────────
    logger.info("Step 3: Handling missing values...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    
    # Fill numeric with median per city
    for col in numeric_cols:
        df[col] = df.groupby("location_name")[col].transform(
            lambda x: x.fillna(x.median())
        )
    
    # Global median for remaining NaNs
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Fill categorical with mode
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    
    logger.info(f" Missing values handled (remaining: {df.isnull().sum().sum()})")
    
    # ── 4. Outlier Handling (IQR method) ──────────────────────────────────────
    logger.info("Step 4: Clipping outliers...")
    key_cols = ["temperature_celsius", "precip_mm", "wind_kph", "humidity"]
    key_cols = [c for c in key_cols if c in df.columns]
    
    for col in key_cols:
        Q1 = df[col].quantile(0.01)
        Q3 = df[col].quantile(0.99)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
        if outlier_count > 0:
            logger.info(f"   {col}: {outlier_count} outliers clipped")
        df[col] = df[col].clip(lower, upper)
    
    # ── 5. Feature Engineering ─────────────────────────────────────────────────
    logger.info("Step 5: Engineering derived features...")
    if "temperature_celsius" in df.columns and "humidity" in df.columns:
        df["temp_humidity_index"] = df["temperature_celsius"] * df["humidity"] / 100
        df["heat_index"] = df["temperature_celsius"] + 0.33 * (df["humidity"] / 100 * 6.105) - 4
    
    if "temperature_celsius" in df.columns and "wind_kph" in df.columns:
        df["wind_chill"] = 13.12 + 0.6215 * df["temperature_celsius"] - 11.37 * (df["wind_kph"] ** 0.16)
    
    if "temperature_celsius" in df.columns and "feelslike_celsius" in df.columns:
        df["temp_feels_like_diff"] = df["temperature_celsius"] - df["feelslike_celsius"]
    
    if "precip_mm" in df.columns:
        df["log_precip"] = np.log1p(df["precip_mm"])
    
    logger.info(" Derived features created")
    
    # ── 6. Normalize Numeric Features ─────────────────────────────────────────
    logger.info("Step 6: Normalizing numeric features...")
    scaler = MinMaxScaler()
    scale_cols = ["temperature_celsius", "humidity", "wind_kph", "precip_mm",
                  "pressure_mb", "visibility_km", "uv_index"]
    scale_cols = [c for c in scale_cols if c in df.columns]
    
    if scale_cols:
        df[[f"{c}_scaled" for c in scale_cols]] = scaler.fit_transform(df[scale_cols])
        logger.info(f" Normalized {len(scale_cols)} features")
    
    logger.info(f"\n Cleaning complete!")
    logger.info(f"   Final shape: {df.shape}")
    logger.info(f"   Remaining nulls: {df.isnull().sum().sum()}")
    
    return df


def get_city_timeseries(
    df: pd.DataFrame,
    city: str,
    column: str = "temperature_celsius",
    freq: str = "D"
) -> pd.Series:
    """
    Extract time-series for a specific city and resample to given frequency.
    
    Args:
        df (pd.DataFrame): Cleaned weather DataFrame
        city (str): City name to extract
        column (str): Column to extract (default: temperature_celsius)
        freq (str): Resampling frequency (D=daily, H=hourly, etc.)
        
    Returns:
        pd.Series: Time-indexed series for the city
    """
    city_data = df[df["location_name"] == city].set_index("last_updated")[column]
    city_data = city_data.resample(freq).mean().interpolate()
    logger.info(f"Extracted {len(city_data)} {freq}-frequency records for {city}")
    return city_data


if __name__ == "__main__":
    # Example usage (ensure data directory exists)
    from pathlib import Path
    Path("data").mkdir(parents=True, exist_ok=True)
    df = load_data("data/GlobalWeatherRepository.csv")
    df_clean = clean_weather_data(df)
    df_clean.to_csv("data/weather_cleaned.csv", index=False)
    print(" Data processing complete. Saved to data/weather_cleaned.csv")
