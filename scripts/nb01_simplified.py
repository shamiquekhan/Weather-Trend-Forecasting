import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

print("="*60)
print("NOTEBOOK 01: DATA CLEANING")
print("="*60)

try:
    # Load data
    logger.info("✅ Loading raw weather data...")
    df = pd.read_csv("data/weather_raw.csv", parse_dates=["last_updated"])
    logger.info(f"   Shape: {df.shape}")
    logger.info(f"   Date range: {df['last_updated'].min()} to {df['last_updated'].max()}")
    
    # Cleaning pipeline
    logger.info("\n✅ Executing 6-step cleaning pipeline...")
    
    # Step 1: Date handling
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    df = df.sort_values('last_updated')
    logger.info("   1. Date parsing: ✓")
    
    # Step 2: Temporal features
    df['year'] = df['last_updated'].dt.year
    df['month'] = df['last_updated'].dt.month
    df['day'] = df['last_updated'].dt.day
    df['hour'] = df['last_updated'].dt.hour
    df['day_of_week'] = df['last_updated'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                  3: 'Spring', 4: 'Spring', 5: 'Spring',
                  6: 'Summer', 7: 'Summer', 8: 'Summer',
                  9: 'Fall', 10: 'Fall', 11: 'Fall'}
    df['season'] = df['month'].map(season_map)
    logger.info("   2. Temporal features: ✓")
    
    # Step 3: Missing values
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].isna().sum() > 0:
            median_val = df.groupby('location_name')[col].transform('median').fillna(df[col].median())
            df[col].fillna(median_val, inplace=True)
    logger.info("   3. Missing value imputation: ✓")
    
    # Step 4: Outlier clipping
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.01)
        q99 = df[col].quantile(0.99)
        df[col] = df[col].clip(q1, q99)
    logger.info("   4. Outlier clipping: ✓")
    
    # Step 5: Feature engineering
    df['heat_index'] = 0.5 * (df['temperature_celsius'] + 61.0 + ((df['temperature_celsius']-14.)**1.2)+(0.94*df['humidity']/100))
    df['wind_chill'] = 13.12 + 0.6215*df['temperature_celsius'] - 11.37*(df['wind_kph']**0.16) + 0.3965*(df['temperature_celsius'])*((df['wind_kph'])**0.16)
    df['temp_humidity_index'] = df['temperature_celsius'] - 0.55 * (1 - df['humidity']/100) * (df['temperature_celsius'] - 14.5)
    df['log_precip'] = np.log1p(df['precip_mm'])
    logger.info("   5. Feature engineering: ✓")
    
    # Step 6: Normalization
    scaler = MinMaxScaler()
    cols_to_norm = ['temperature_celsius', 'humidity', 'wind_kph', 'precip_mm', 'pressure_mb', 'visibility_km', 'uv_index']
    df[cols_to_norm] = scaler.fit_transform(df[cols_to_norm])
    logger.info("   6. MinMaxScaler normalization: ✓")
    
    # Save cleaned data
    df.to_csv("data/weather_cleaned.csv", index=False)
    logger.info("\n✅ Cleaned data saved to data/weather_cleaned.csv")
    logger.info(f"   Records: {len(df):,}")
    logger.info(f"   Missing values: {df.isna().sum().sum()}")
    logger.info(f"\n🎉 Notebook 01 Complete!")
    
except Exception as e:
    logger.error(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
