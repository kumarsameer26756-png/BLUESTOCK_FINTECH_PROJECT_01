import pandas as pd
import numpy as np
from datetime import datetime
import os

def generate_data_profiling_report(df, dataset_name='Dataset'):
    """
    Generates comprehensive data profiling report.
    """
    print("\n" + "="*60)
    print(f" DATA PROFILING REPORT: {dataset_name.upper()} ")
    print("="*60)
    
    report = {}
    
    # Basic Metadata
    print(f"\n📊 BASIC METADATA")
    print(f"-" * 40)
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    report['shape'] = df.shape
    report['memory_mb'] = df.memory_usage(deep=True).sum() / 1024**2
    
    # Data Types
    print(f"\n📋 DATA TYPES")
    print(f"-" * 40)
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"{str(dtype):30} {count:3} columns")
    
    report['dtypes'] = dtype_counts.to_dict()
    
    # Missing Values
    print(f"\n❓ MISSING VALUES")
    print(f"-" * 40)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    cols_with_missing = missing[missing > 0].sort_values(ascending=False)
    if len(cols_with_missing) == 0:
        print(f"✅ No missing values detected")
    else:
        print(f"⚠️  {len(cols_with_missing)} columns with missing values:")
        for col, count in cols_with_missing.items():
            pct = (count / len(df)) * 100
            print(f"   {col:30} {count:7,} ({pct:6.2f}%)")
    
    report['missing_values'] = missing.to_dict()
    report['missing_pct'] = missing_pct.to_dict()
    
    # Duplicates
    print(f"\n🔄 DUPLICATE RECORDS")
    print(f"-" * 40)
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100
    print(f"Total duplicates: {dup_count:,} ({dup_pct:.2f}%)")
    if dup_count > 0:
        print(f"⚠️  {dup_count} duplicate rows found")
    else:
        print(f"✅ No duplicate rows detected")
    
    report['duplicates'] = dup_count
    
    # Numeric Columns Summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n📈 NUMERIC COLUMNS SUMMARY")
        print(f"-" * 40)
        for col in numeric_cols:
            print(f"\n{col}:")
            stats = df[col].describe()
            print(f"  Count: {stats['count']:.0f}")
            print(f"  Mean: {stats['mean']:.4f}")
            print(f"  Std Dev: {stats['std']:.4f}")
            print(f"  Min: {stats['min']:.4f} | Max: {stats['max']:.4f}")
            print(f"  Median (50%): {stats['50%']:.4f}")
            
            # Skewness and Kurtosis
            skewness = df[col].skew()
            kurtosis = df[col].kurtosis()
            print(f"  Skewness: {skewness:.4f} | Kurtosis: {kurtosis:.4f}")
    
    # Categorical Columns Summary
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        print(f"\n📂 CATEGORICAL COLUMNS SUMMARY")
        print(f"-" * 40)
        for col in categorical_cols:
            unique_count = df[col].nunique()
            print(f"\n{col}:")
            print(f"  Unique values: {unique_count}")
            if unique_count <= 10:
                value_counts = df[col].value_counts()
                for val, count in value_counts.items():
                    pct = (count / len(df)) * 100
                    print(f"    {str(val):25} {count:7,} ({pct:6.2f}%)")
            else:
                print(f"  Top 5 values:")
                value_counts = df[col].value_counts().head(5)
                for val, count in value_counts.items():
                    pct = (count / len(df)) * 100
                    print(f"    {str(val):25} {count:7,} ({pct:6.2f}%)")
    
    # DateTime Columns Summary
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    if len(datetime_cols) > 0:
        print(f"\n📅 DATE/TIME COLUMNS SUMMARY")
        print(f"-" * 40)
        for col in datetime_cols:
            print(f"\n{col}:")
            print(f"  Min date: {df[col].min()}")
            print(f"  Max date: {df[col].max()}")
            date_range = (df[col].max() - df[col].min()).days
            print(f"  Date range: {date_range} days")
    
    return report

def generate_before_after_report(df_original, df_processed, dataset_name='Dataset'):
    """
    Generates before/after comparison report.
    """
    print("\n" + "="*60)
    print(f" BEFORE/AFTER COMPARISON: {dataset_name.upper()} ")
    print("="*60)
    
    print(f"\n📊 SHAPE CHANGES")
    print(f"-" * 40)
    print(f"Original:  {df_original.shape[0]:,} rows × {df_original.shape[1]} columns")
    print(f"Processed: {df_processed.shape[0]:,} rows × {df_processed.shape[1]} columns")
    print(f"Rows removed: {df_original.shape[0] - df_processed.shape[0]:,}")
    print(f"Columns removed: {df_original.shape[1] - df_processed.shape[1]}")
    
    print(f"\n❓ MISSING VALUES")
    print(f"-" * 40)
    missing_before = df_original.isnull().sum().sum()
    missing_after = df_processed.isnull().sum().sum()
    print(f"Before: {missing_before:,} missing values")
    print(f"After:  {missing_after:,} missing values")
    print(f"Improvement: {missing_before - missing_after:,} values fixed")
    
    print(f"\n🔄 DUPLICATES")
    print(f"-" * 40)
    dups_before = df_original.duplicated().sum()
    dups_after = df_processed.duplicated().sum()
    print(f"Before: {dups_before:,} duplicate rows")
    print(f"After:  {dups_after:,} duplicate rows")
    print(f"Improvement: {dups_before - dups_after:,} duplicates removed")
    
    print(f"\n📋 DATA QUALITY SCORE")
    print(f"-" * 40)
    quality_before = ((df_original.shape[0] - missing_before - dups_before) / (df_original.shape[0] * df_original.shape[1])) * 100
    quality_after = ((df_processed.shape[0] - missing_after - dups_after) / (df_processed.shape[0] * df_processed.shape[1])) * 100
    print(f"Before: {quality_before:.2f}%")
    print(f"After:  {quality_after:.2f}%")
    print(f"Improvement: {quality_after - quality_before:.2f} percentage points")

def save_quality_report(report, output_path='reports/data_quality_report.txt'):
    """
    Saves quality report to file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("="*60 + "\n")
        f.write("DATA QUALITY REPORT - BLUESTOCK FINTECH\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(str(report))
    
    print(f"\n✅ Report saved to {output_path}")

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# DATA QUALITY REPORTING - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Example usage
    sample_data = pd.DataFrame({
        'scheme_code': [119551, 120503, 118632, 119551] * 25,
        'fund_house': ['SBI', 'ICICI', 'Nippon', 'SBI'] * 25,
        'category': ['Equity-Large Cap'] * 100,
        'date': pd.date_range('2024-01-01', periods=100, freq='D').repeat(1),
        'nav': np.random.randn(100).cumsum() + 100
    })
    
    # Add some intentional data quality issues
    sample_data.loc[5, 'nav'] = np.nan
    sample_data = pd.concat([sample_data, sample_data.iloc[:5]], ignore_index=True)
    
    print(f"\n📥 Sample Data Loaded: {len(sample_data)} records")
    
    # Generate profiling report
    report = generate_data_profiling_report(sample_data, 'NAV History')
    
    # Simulate cleaned data
    sample_cleaned = sample_data.dropna().drop_duplicates()
    
    # Generate comparison
    generate_before_after_report(sample_data, sample_cleaned, 'NAV History')
    
    print("\n" + "="*60)
    print(" REPORTING COMPLETE ")
    print("="*60)
