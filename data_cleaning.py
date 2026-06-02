import pandas as pd
import numpy as np
from scipy import stats
import os

def handle_missing_values(df, strategy='auto', threshold=0.5):
    """
    Handles missing values based on column type and strategy.
    - threshold: Drop columns with >50% missing values
    - strategy: 'auto', 'drop', 'forward_fill', 'mean', 'median', 'category'
    """
    print("\n" + "="*60)
    print(" PHASE 1: MISSING VALUE HANDLING ")
    print("="*60)
    
    df_cleaned = df.copy()
    missing_summary = df_cleaned.isnull().sum()
    
    print(f"\n📊 Missing Value Summary:")
    print(f"Total missing values: {missing_summary.sum()}")
    
    # Drop columns with excessive missing values
    cols_to_drop = []
    for col in df_cleaned.columns:
        null_pct = df_cleaned[col].isnull().sum() / len(df_cleaned)
        if null_pct > threshold:
            cols_to_drop.append(col)
            print(f"❌ {col:30} -> {null_pct*100:.2f}% missing (DROPPED)")
    
    df_cleaned = df_cleaned.drop(columns=cols_to_drop)
    
    # Fill remaining missing values by column type
    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() > 0:
            null_count = df_cleaned[col].isnull().sum()
            
            if pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
                # Forward fill for datetime
                df_cleaned[col] = df_cleaned[col].fillna(method='ffill')
                print(f"✅ {col:30} -> Forward fill ({null_count} values)")
            elif pd.api.types.is_numeric_dtype(df_cleaned[col]):
                # Median fill for numeric
                median_val = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_val)
                print(f"✅ {col:30} -> Median fill: {median_val:.4f} ({null_count} values)")
            elif df_cleaned[col].dtype == 'category' or df_cleaned[col].dtype == 'object':
                # Mode fill for categorical
                mode_val = df_cleaned[col].mode()[0] if len(df_cleaned[col].mode()) > 0 else 'Unknown'
                df_cleaned[col] = df_cleaned[col].fillna(mode_val)
                print(f"✅ {col:30} -> Mode fill: {mode_val} ({null_count} values)")
    
    print(f"\n✅ Remaining missing values: {df_cleaned.isnull().sum().sum()}")
    return df_cleaned

def detect_outliers(df, numeric_columns=None, method='iqr', threshold=1.5):
    """
    Detects outliers using IQR or Z-score method.
    - method: 'iqr' (default) or 'zscore'
    - threshold: IQR multiplier (1.5) or Z-score limit (3.0)
    """
    print("\n" + "="*60)
    print(" PHASE 2: OUTLIER DETECTION ")
    print("="*60)
    
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outlier_summary = {}
    
    for col in numeric_columns:
        if col in df.columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
                outlier_count = outliers.sum()
            else:  # zscore
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                outliers = z_scores > threshold
                outlier_count = outliers.sum()
            
            outlier_summary[col] = {
                'method': method,
                'outlier_count': outlier_count,
                'outlier_pct': (outlier_count / len(df)) * 100 if len(df) > 0 else 0
            }
            
            if outlier_count > 0:
                print(f"⚠️  {col:30} -> {outlier_count} outliers detected ({outlier_summary[col]['outlier_pct']:.2f}%)")
                if method == 'iqr':
                    print(f"    Bounds: [{lower_bound:.4f}, {upper_bound:.4f}]")
            else:
                print(f"✅ {col:30} -> No outliers detected")
    
    return outlier_summary

def remove_duplicate_records(df, subset=None, keep='first'):
    """
    Identifies and removes duplicate records.
    """
    print("\n" + "="*60)
    print(" PHASE 3: DUPLICATE RECORD REMOVAL ")
    print("="*60)
    
    initial_rows = len(df)
    df_deduplicated = df.drop_duplicates(subset=subset, keep=keep)
    removed_rows = initial_rows - len(df_deduplicated)
    
    print(f"\n📊 Deduplication Summary:")
    print(f"Initial rows: {initial_rows}")
    print(f"Duplicate rows removed: {removed_rows}")
    print(f"Final rows: {len(df_deduplicated)}")
    
    if removed_rows > 0:
        print(f"✅ Removed {removed_rows} duplicate records")
    else:
        print(f"✅ No duplicate records found")
    
    return df_deduplicated

def flag_anomalies(df, numeric_columns=None):
    """
    Flags data anomalies for manual review:
    - Negative NAV values
    - Future dates
    - Sudden jumps in values
    """
    print("\n" + "="*60)
    print(" PHASE 4: ANOMALY FLAGGING ")
    print("="*60)
    
    df_flagged = df.copy()
    df_flagged['anomaly_flag'] = 0
    anomaly_records = 0
    
    # Check for negative NAV
    if 'nav' in df_flagged.columns:
        negative_nav = df_flagged['nav'] < 0
        if negative_nav.sum() > 0:
            df_flagged.loc[negative_nav, 'anomaly_flag'] = 1
            anomaly_records += negative_nav.sum()
            print(f"⚠️  Negative NAV detected: {negative_nav.sum()} records")
    
    # Check for future dates
    date_cols = df_flagged.select_dtypes(include=['datetime64']).columns
    for col in date_cols:
        future_dates = df_flagged[col] > pd.Timestamp.now()
        if future_dates.sum() > 0:
            df_flagged.loc[future_dates, 'anomaly_flag'] = 1
            anomaly_records += future_dates.sum()
            print(f"⚠️  Future dates in {col}: {future_dates.sum()} records")
    
    # Check for unusual jumps in NAV (>20% change)
    if 'nav' in df_flagged.columns:
        nav_pct_change = df_flagged['nav'].pct_change().abs()
        large_jumps = nav_pct_change > 0.20
        if large_jumps.sum() > 0:
            print(f"⚠️  Large NAV jumps (>20%): {large_jumps.sum()} records")
    
    if anomaly_records > 0:
        print(f"\n🚩 Total anomaly flags set: {anomaly_records}")
    else:
        print(f"\n✅ No major anomalies detected")
    
    return df_flagged

def generate_cleaning_report(df_original, df_cleaned):
    """
    Generates a comprehensive data cleaning report.
    """
    print("\n" + "="*60)
    print(" DATA CLEANING REPORT ")
    print("="*60)
    
    print(f"\n📊 Dataset Comparison:")
    print(f"Original shape: {df_original.shape}")
    print(f"Cleaned shape: {df_cleaned.shape}")
    print(f"Rows removed: {len(df_original) - len(df_cleaned)}")
    print(f"Columns removed: {len(df_original.columns) - len(df_cleaned.columns)}")
    
    print(f"\n✅ Cleaning complete. Dataset ready for analysis.")

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# DATA CLEANING PIPELINE - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Example usage
    sample_data = {
        'scheme_code': [119551, 120503, 118632, 119551, None],
        'fund_house': ['SBI', 'ICICI', 'Nippon', 'SBI', 'Unknown'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01', '2024-01-05'],
        'nav': [125.50, 145.30, 98.75, 125.50, -5.00]  # Last one is anomaly
    }
    
    df = pd.DataFrame(sample_data)
    print(f"\n📥 Sample Data Loaded:")
    print(df)
    
    # Run cleaning pipeline
    df_cleaned = handle_missing_values(df)
    outlier_summary = detect_outliers(df_cleaned)
    df_deduplicated = remove_duplicate_records(df_cleaned)
    df_flagged = flag_anomalies(df_deduplicated)
    generate_cleaning_report(df, df_flagged)
    
    print("\n" + "="*60)
    print(" CLEANING PIPELINE COMPLETE ")
    print("="*60)
