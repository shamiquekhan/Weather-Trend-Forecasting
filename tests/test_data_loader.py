import pytest
import pandas as pd
import os
from src.data_loader import load_data, clean_weather_data

def test_load_data_error():
    """Test that loading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")

def test_clean_weather_data_dummy():
    """Test the cleaning pipeline with a dummy dataset."""
    dummy_data = pd.DataFrame({
        "last_updated": ["2023-01-01 12:00:00", "2023-01-02 12:00:00", "invalid_date"],
        "location_name": ["London", "London", "London"],
        "country": ["UK", "UK", "UK"],
        "temperature_celsius": [15.5, 16.0, 15.8],
        "humidity": [60, 65, 62],
        "precip_mm": [0.0, 0.5, 0.2]
    })
    
    # This might print warnings for the invalid date
    df_clean = clean_weather_data(dummy_data)
    
    assert isinstance(df_clean, pd.DataFrame)
    assert not df_clean.empty
    # The invalid date row should have been dropped
    assert len(df_clean) == 2
    assert "year" in df_clean.columns
    assert "season" in df_clean.columns
