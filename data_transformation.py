import pandas as pd
import numpy as np
from datetime import datetime
import os

def standardize_data_types(df, schema_config=None):
    """
    Standardizes data types across a DataFrame based on column characteristics.
    Converts columns to optimal types: datetime, float, int, category.
    """
    print("\n" + "="*70)
    print(" PHASE 1: DATA TYPE STANDARDIZATION ")
    print("="*70)
    
    df_transformed = df.copy()
    
    print(f"\n📋 Original Data Types:")
    print(df_transformed.dtypes)
    
    # Default schema configuration
    if schema_config is None:
        schema_config = {
            'date': ['date', 'nav_date', 'transaction_date'],
            'float': ['nav', 'price', 'value', 'return', 'aum', 'expense_ratio'],
            'int': ['scheme_code', 'holding_count', 'units', 'isin'],
            'category': ['fund_house', 'category', 'sub_category', 'risk_grade', 'scheme_name', 'status', 'plan']
        }
    
    conversions = {'datetime': 0, 'float': 0, 'int': 0, 'category': 0, 'failed': 0}
    
    # Convert datetime columns
    for col in df_transformed.columns:
        # Datetime conversion
        if any(date_keyword in col.lower() for date_keyword in schema_config.get('date', [])):
            try:
                df_transformed[col] = pd.to_datetime(df_transformed[col], errors='coerce')
                print(f"✅ {col:30} → datetime64[ns]")
                conversions['datetime'] += 1
            except Exception as e:
                print(f"⚠️  {col:30} → datetime conversion failed: {str(e)[:40]}")
                conversions['failed'] += 1
        
        # Numeric columns (float)
        elif any(float_keyword in col.lower() for float_keyword in schema_config.get('float', [])):
            try:
                df_transformed[col] = pd.to_numeric(df_transformed[col], errors='coerce')
                print(f"✅ {col:30} → float64")
                conversions['float'] += 1
            except Exception as e:
                print(f"⚠️  {col:30} → float conversion failed: {str(e)[:40]}")
                conversions['failed'] += 1
        
        # Integer columns
        elif any(int_keyword in col.lower() for int_keyword in schema_config.get('int', [])):
            try:
                df_transformed[col] = pd.to_numeric(df_transformed[col], errors='coerce').astype('Int64')
                print(f"✅ {col:30} → Int64")
                conversions['int'] += 1
            except Exception as e:
                print(f"⚠️  {col:30} → int conversion failed: {str(e)[:40]}")
                conversions['failed'] += 1
        
        # Categorical columns
        elif any(cat_keyword in col.lower() for cat_keyword in schema_config.get('category', [])):
            try:
                df_transformed[col] = df_transformed[col].astype('category')
                print(f"✅ {col:30} → category")
                conversions['category'] += 1
            except Exception as e:
                print(f"⚠️  {col:30} → category conversion failed: {str(e)[:40]}")
                conversions['failed'] += 1
    
    print(f"\n📊 Transformation Summary:")
    print(f"  Datetime columns:     {conversions['datetime']}")
    print(f"  Float columns:        {conversions['float']}")
    print(f"  Integer columns:      {conversions['int']}")
    print(f"  Category columns:     {conversions['category']}")
    print(f"  Failed conversions:   {conversions['failed']}")
    
    print(f"\n📋 Transformed Data Types:")
    print(df_transformed.dtypes)
    
    return df_transformed

def normalize_date_formats(df, date_columns=None):
    """
    Ensures all date columns follow consistent ISO 8601 format (YYYY-MM-DD).
    """
    print("\n" + "="*70)
    print(" PHASE 2: DATE FORMAT NORMALIZATION ")
    print("="*70)
    
    if date_columns is None:
        date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    df_normalized = df.copy()
    
    if not date_columns:
        print("\n⚠️  No datetime columns found for normalization")
        return df_normalized
    
    print(f"\n📅 Normalizing {len(date_columns)} date column(s) to ISO 8601 format...")
    
    for col in date_columns:
        if col in df_normalized.columns:
            try:
                # Convert to datetime if not already
                if not pd.api.types.is_datetime64_any_dtype(df_normalized[col]):
                    df_normalized[col] = pd.to_datetime(df_normalized[col], errors='coerce')
                
                print(f"✅ {col:30} normalized to YYYY-MM-DD")
                print(f"   Min date: {df_normalized[col].min()}")
                print(f"   Max date: {df_normalized[col].max()}")
            except Exception as e:
                print(f"⚠️  {col:30} normalization failed: {str(e)[:40]}")
    
    return df_normalized

def validate_numeric_ranges(df, numeric_columns=None):
    """
    Validates numeric columns are within reasonable ranges.
    Flags potential data quality issues.
    """
    print("\n" + "="*70)
    print(" PHASE 3: NUMERIC RANGE VALIDATION ")
    print("="*70)
    
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        print("\n⚠️  No numeric columns found for validation")
        return {}
    
    validation_results = {}
    
    print(f"\n📊 Validating {len(numeric_columns)} numeric column(s)...")
    
    for col in numeric_columns:
        if col in df.columns:
            stats = {
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'std': df[col].std(),
                'null_count': df[col].isnull().sum(),
                'negative_count': (df[col] < 0).sum()
            }
            validation_results[col] = stats
            
            print(f"\n📈 Column: {col}")
            print(f"   Range:   [{stats['min']:.6f}, {stats['max']:.6f}]")
            print(f"   Stats:   Mean={stats['mean']:.6f}, Std={stats['std']:.6f}")
            print(f"   Quality: {stats['null_count']} nulls, {stats['negative_count']} negatives")
            
            # Flag potential issues
            if stats['negative_count'] > 0 and 'nav' in col.lower():
                print(f"   ⚠️  WARNING: Negative NAV values detected!")
            if stats['null_count'] / len(df) > 0.5:
                print(f"   ⚠️  WARNING: >50% null values!")
    
    return validation_results

def encode_categorical_variables(df, categorical_columns=None):
    """
    Encodes categorical variables for analysis.
    Creates label encoding mappings.
    """
    print("\n" + "="*70)
    print(" PHASE 4: CATEGORICAL VARIABLE ENCODING ")
    print("="*70)
    
    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include=['category', 'object']).columns.tolist()
    
    if not categorical_columns:
        print("\n⚠️  No categorical columns found for encoding")
        return df, {}
    
    df_encoded = df.copy()
    encoding_mappings = {}
    
    print(f"\n🏷️  Encoding {len(categorical_columns)} categorical column(s)...")
    
    for col in categorical_columns:
        if col in df_encoded.columns:
            unique_vals = df_encoded[col].nunique()
            print(f"\n📂 Column: {col}")
            print(f"   Unique values: {unique_vals}")
            
            if unique_vals > 0 and unique_vals <= 20:
                print(f"   Values: {list(df_encoded[col].unique()[:10])}")
                
                # Create label encoding
                if df_encoded[col].dtype == 'object' or df_encoded[col].dtype.name == 'category':
                    label_encoder = pd.factorize(df_encoded[col])
                    encoding_mappings[col] = dict(enumerate(label_encoder[1]))
                    print(f"   ✅ Label encoding created")
            else:
                print(f"   (Too many unique values to list)")
    
    return df_encoded, encoding_mappings

def consolidate_transformed_data(processed_dfs, output_dir='data/processed'):
    """
    Consolidates all transformed datasets and saves to processed directory.
    """
    print("\n" + "="*70)
    print(" PHASE 5: CONSOLIDATION & EXPORT ")
    print("="*70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n💾 Exporting {len(processed_dfs)} transformed dataset(s)...")
    
    for name, df in processed_dfs.items():
        try:
            output_path = f"{output_dir}/{name}_transformed.csv"
            df.to_csv(output_path, index=False)
            print(f"✅ {name:30} → {output_path}")
            print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        except Exception as e:
            print(f"❌ {name:30} export failed: {str(e)[:50]}")
    
    print(f"\n✅ All transformed datasets exported to {output_dir}/")

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# DAY 2: DATA TRANSFORMATION PIPELINE - BLUESTOCK FINTECH")
    print("#"*70)
    
    # Example usage - Load sample data
    sample_data = pd.DataFrame({
        'scheme_code': [119551, 120503, 118632, 119551, 120841],
        'fund_house': ['SBI', 'ICICI', 'Nippon', 'SBI', 'Kotak'],
        'category': ['Equity-Large Cap', 'Equity-Large Cap', 'Equity-Large Cap', 'Equity-Large Cap', 'Equity-Large Cap'],
        'date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
        'nav': [125.50, 145.30, 98.75, 126.20, 147.10],
        'expense_ratio': [0.25, 0.30, 0.35, 0.25, 0.28]
    })
    
    print(f"\n📊 Sample Data Loaded:")
    print(sample_data)
    
    # Run transformation pipeline
    df_transformed = standardize_data_types(sample_data)
    df_normalized = normalize_date_formats(df_transformed)
    validation_results = validate_numeric_ranges(df_normalized)
    df_encoded, encodings = encode_categorical_variables(df_normalized)
    
    print("\n" + "="*70)
    print(" TRANSFORMATION PIPELINE COMPLETE ")
    print("="*70)
    print(f"\n✅ All {len(df_encoded)} records transformed successfully")
