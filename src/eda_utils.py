"""
EDA Utilities for Weather Forecasting Project

This module provides reusable visualization and analysis helpers for exploratory
data analysis on weather datasets.

Usage:
    from src.eda_utils import plot_temperature_trends, plot_correlation_matrix
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional

logger = logging.getLogger(__name__)


def plot_temperature_trends(
    df: pd.DataFrame,
    title: str = "Global Average Daily Temperature Over Time",
    save_path: Optional[str] = None
) -> None:
    """
    Create interactive line plot of temperature trends over time.
    
    Args:
        df (pd.DataFrame): DataFrame with 'last_updated' and 'temperature_celsius'
        title (str): Plot title
        save_path (str): Path to save HTML file (optional)
    """
    daily_avg = df.groupby("last_updated")["temperature_celsius"].mean().reset_index()
    
    fig = px.line(
        daily_avg, x="last_updated", y="temperature_celsius",
        title=title,
        labels={"temperature_celsius": "Avg Temp (°C)", "last_updated": "Date"},
        template="plotly_dark"
    )
    fig.update_traces(line_color="#FF6B35", line_width=1.5)
    
    if save_path:
        fig.write_html(save_path)
        logger.info(f" Saved temperature trends to {save_path}")
    
    fig.show()


def plot_monthly_distribution(
    df: pd.DataFrame,
    save_path: Optional[str] = None
) -> None:
    """
    Create boxplot of temperature by month.
    
    Args:
        df (pd.DataFrame): DataFrame with 'month' and 'temperature_celsius'
        save_path (str): Path to save PNG file (optional)
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.boxplot(data=df, x="month", y="temperature_celsius",
                palette="coolwarm", ax=ax)
    ax.set_title("Monthly Temperature Distribution (Global)", 
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature (°C)")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        logger.info(f" Saved monthly distribution to {save_path}")
    
    plt.show()


def plot_precipitation_cities(
    df: pd.DataFrame,
    top_n: int = 20,
    save_path: Optional[str] = None
) -> None:
    """
    Create horizontal bar chart of top cities by average precipitation.
    
    Args:
        df (pd.DataFrame): DataFrame with 'location_name' and 'precip_mm'
        top_n (int): Number of top cities to display
        save_path (str): Path to save HTML file (optional)
    """
    top_rain = (
        df.groupby("location_name")["precip_mm"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    
    fig = px.bar(
        top_rain, x="precip_mm", y="location_name", orientation="h",
        title=f"Top {top_n} Cities by Average Daily Precipitation",
        color="precip_mm", color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    
    if save_path:
        fig.write_html(save_path)
        logger.info(f" Saved precipitation chart to {save_path}")
    
    fig.show()


def plot_correlation_matrix(
    df: pd.DataFrame,
    features: Optional[List[str]] = None,
    save_path: Optional[str] = None
) -> None:
    """
    Create heatmap of feature correlations.
    
    Args:
        df (pd.DataFrame): DataFrame with numeric features
        features (List[str]): List of columns to include (default: all numeric)
        save_path (str): Path to save PNG file (optional)
    """
    if features is None:
        features = [
            "temperature_celsius", "humidity", "wind_kph", "precip_mm",
            "pressure_mb", "visibility_km", "uv_index", "cloud",
            "air_quality_us-epa-index", "heat_index", "wind_chill"
        ]
    
    features = [c for c in features if c in df.columns]
    corr = df[features].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="RdYlGn", center=0, linewidths=0.5,
        annot_kws={"size": 8}
    )
    plt.title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        logger.info(f" Saved correlation matrix to {save_path}")
    
    plt.show()


def plot_anomalies(
    df: pd.DataFrame,
    anomaly_column: str = "anomaly_iforest",
    save_path: Optional[str] = None
) -> None:
    """
    Create scatter plot showing detected anomalies.
    
    Args:
        df (pd.DataFrame): DataFrame with anomaly labels and temperature
        anomaly_column (str): Name of anomaly indicator column
        save_path (str): Path to save HTML file (optional)
    """
    normal = df[df[anomaly_column] == 0]
    anomalies = df[df[anomaly_column] == 1]
    
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
        title="Temperature Anomalies Detected",
        xaxis_title="Date", yaxis_title="Temperature (°C)",
        template="plotly_dark"
    )
    
    if save_path:
        fig.write_html(save_path)
        logger.info(f" Saved anomaly plot to {save_path}")
    
    fig.show()
    print(f"Total anomalies: {len(anomalies)} ({len(anomalies)/len(df)*100:.1f}%)")


def plot_precipitation_heatmap(
    df: pd.DataFrame,
    save_path: Optional[str] = None
) -> None:
    """
    Create heatmap of precipitation by season and month.
    
    Args:
        df (pd.DataFrame): DataFrame with 'season', 'month', 'precip_mm'
        save_path (str): Path to save PNG file (optional)
    """
    pivot = df.pivot_table(
        values="precip_mm", index="season", columns="month", aggfunc="mean"
    )
    plt.figure(figsize=(12, 4))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5)
    plt.title("Average Precipitation (mm) by Season and Month")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        logger.info(f" Saved precipitation heatmap to {save_path}")
    
    plt.show()


if __name__ == "__main__":
    print("EDA utilities module for weather forecasting project")
