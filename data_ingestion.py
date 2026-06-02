import os
import glob
import pandas as pd

def load_and_profile_datasets(csv_files):
    """
    Loads CSV datasets, prints comprehensive profiling metadata, and checks for anomalies.
    """
    datasets = {}
    print("="*70)
    print(" PHASE 1: LOADING & PROFILING LOCAL DATASETS ")
    print("="*70)
    
    if not csv_files:
        print("\n⚠️ No CSV files found in data/raw/")
        return datasets
    
    for file_path in csv_files:
        if not os.path.exists(file_path):
            print(f"\n⚠️ Warning: File not found at {file_path}. Skipping.")
            continue
            
        name = os.path.basename(file_path).split('.')[0]
        try:
            df = pd.read_csv(file_path)
            datasets[name] = df
            
            print(f"\n📊 Dataset: {name.upper()}")
            print("-" * 70)
            print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
            print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            print("\n📋 Data Types:")
            print(df.dtypes)
            
            print("\n📝 First 3 Rows:")
            print(df.head(3))
            
            print("\n❓ Null Count by Column:")
            null_counts = df.isnull().sum()
            if null_counts.sum() > 0:
                null_df = pd.DataFrame({
                    'Column': null_counts.index,
                    'Null_Count': null_counts.values,
                    'Null_Percentage': (null_counts.values / len(df) * 100).round(2)
                })
                null_df = null_df[null_df['Null_Count'] > 0].sort_values('Null_Count', ascending=False)
                print(null_df.to_string(index=False))
            else:
                print("✅ No null values detected")
            
            # Basic Anomalies check
            missing_vals = df.isnull().sum().sum()
            dup_rows = df.duplicated().sum()
            
            print("\n🔍 Data Quality Checks:")
            if missing_vals > 0:
                print(f"  ⚠️ Total missing values: {missing_vals:,} ({missing_vals/(df.shape[0]*df.shape[1])*100:.2f}%)")
            else:
                print(f"  ✅ No missing values detected")
            
            if dup_rows > 0:
                print(f"  ⚠️ Duplicate rows found: {dup_rows:,} ({dup_rows/len(df)*100:.2f}%)")
            else:
                print(f"  ✅ No duplicate rows detected")
            
            print("." * 70)
        except Exception as e:
            print(f"\n💥 Error reading {file_path}: {e}")
            
    return datasets

def validate_amfi_data(datasets):
    """
    Explores Fund Master and validates referential integrity against NAV History.
    Assumes keys 'fund_master' and 'nav_history' exist in the datasets dict.
    """
    print("\n" + "="*70)
    print(" PHASE 2: MUTUAL FUND METADATA EXPLORATION & DQ VALIDATION ")
    print("="*70)
    
    if 'fund_master' not in datasets or 'nav_history' not in datasets:
        print("\n❌ Critical: Validation skipped.")
        print("   Ensure 'fund_master.csv' and 'nav_history.csv' are in data/raw/")
        return

    fm = datasets['fund_master']
    nh = datasets['nav_history']
    
    # 1. Exploration
    print("\n🔍 Fund Master Metadata Highlights:")
    print("-" * 70)
    for col in ['fund_house', 'category', 'sub_category', 'risk_grade']:
        if col in fm.columns:
            unique_count = fm[col].nunique()
            print(f"\n  {col.replace('_', ' ').title()}:")
            print(f"    Unique values: {unique_count}")
            if unique_count <= 15:
                print(f"    Values: {sorted(fm[col].unique())}")
            else:
                print(f"    Sample values: {list(fm[col].unique())[:10]}")
                
    # 2. Scheme Code Structure Explanation
    print("\n\nℹ️ AMFI Scheme Code Structure:")
    print("-" * 70)
    print("  AMFI codes are unique 6-digit numeric identifiers assigned by the")
    print("  Association of Mutual Funds in India.")
    print("\n  Structure in this project:")
    print("    • fund_master.csv: Maps scheme codes → structural metadata")
    print("                       (fund house, category, risk grade)")
    print("    • nav_history.csv: Maps scheme codes → time-series NAV data")
    print("                       (historical price movements)")

    # 3. Data Quality Validation (Referential Integrity Check)
    fm_code_col = 'scheme_code' if 'scheme_code' in fm.columns else 'amfi_code'
    nh_code_col = 'scheme_code' if 'scheme_code' in nh.columns else 'amfi_code'
    
    print("\n\n⚖️ Referential Integrity Validation:")
    print("-" * 70)
    
    if fm_code_col in fm.columns and nh_code_col in nh.columns:
        master_codes = set(fm[fm_code_col].dropna().unique())
        history_codes = set(nh[nh_code_col].dropna().unique())
        
        missing_in_history = master_codes - history_codes
        extra_in_history = history_codes - master_codes
        
        print(f"\n  Fund Master Statistics:")
        print(f"    Unique schemes: {len(master_codes):,}")
        print(f"    Total records:  {len(fm):,}")
        
        print(f"\n  NAV History Statistics:")
        print(f"    Unique schemes: {len(history_codes):,}")
        print(f"    Total records:  {len(nh):,}")
        
        print(f"\n  Integrity Check Results:")
        
        if len(missing_in_history) == 0 and len(extra_in_history) == 0:
            print(f"    ✅ SUCCESS: Perfect referential integrity!")
            print(f"       Every scheme code in fund_master exists in nav_history")
            print(f"       No orphaned codes in nav_history")
        else:
            if len(missing_in_history) > 0:
                print(f"    ⚠️ WARNING: Missing in History!")
                print(f"       {len(missing_in_history)} schemes in Master have NO records in NAV History")
                print(f"       Sample codes: {list(sorted(missing_in_history))[:5]}")
            
            if len(extra_in_history) > 0:
                print(f"    ⚠️ WARNING: Orphaned codes in History!")
                print(f"       {len(extra_in_history)} schemes in NAV History NOT in Master")
                print(f"       Sample codes: {list(sorted(extra_in_history))[:5]}")
    else:
        print(f"    ❌ Validation Failed: Could not match key columns")
        print(f"       Master key column '{fm_code_col}': {'✅ Found' if fm_code_col in fm.columns else '❌ Missing'}")
        print(f"       History key column '{nh_code_col}': {'✅ Found' if nh_code_col in nh.columns else '❌ Missing'}")

def print_dq_summary(datasets):
    """
    Prints overall data quality summary across all loaded datasets.
    """
    print("\n" + "="*70)
    print(" OVERALL DATA QUALITY SUMMARY ")
    print("="*70)
    
    if not datasets:
        print("\n⚠️ No datasets loaded")
        return
    
    total_rows = sum(len(df) for df in datasets.values())
    total_cols = sum(len(df.columns) for df in datasets.values())
    total_missing = sum(df.isnull().sum().sum() for df in datasets.values())
    total_dups = sum(df.duplicated().sum() for df in datasets.values())
    
    completeness = (1 - total_missing / (total_rows * total_cols)) * 100 if (total_rows * total_cols) > 0 else 0
    
    print(f"\n📊 Aggregate Statistics:")
    print(f"  Datasets Loaded:         {len(datasets)}")
    print(f"  Total Rows:              {total_rows:,}")
    print(f"  Total Columns:           {total_cols}")
    print(f"  Total Missing Values:    {total_missing:,}")
    print(f"  Total Duplicate Rows:    {total_dups:,}")
    
    print(f"\n📈 Quality Metrics:")
    print(f"  Data Completeness:       {completeness:.2f}%")
    print(f"  Missing Value Rate:      {(total_missing/(total_rows*total_cols)*100):.4f}%")
    print(f"  Duplication Rate:        {(total_dups/total_rows*100):.4f}%")
    
    print(f"\n✅ Status:")
    if completeness > 95 and total_dups < total_rows * 0.01:
        print(f"  Data quality is EXCELLENT for analysis")
    elif completeness > 90 and total_dups < total_rows * 0.02:
        print(f"  Data quality is GOOD - minor cleaning recommended")
    else:
        print(f"  Data quality needs ATTENTION - review anomalies above")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# DAY 1: DATA INGESTION PIPELINE - BLUESTOCK FINTECH PROJECT")
    print("#"*70)
    
    # Auto-discover CSV files in data/raw/
    target_csvs = sorted(glob.glob("data/raw/*.csv"))
    
    if not target_csvs:
        print("\n⚠️ No CSV files found in data/raw/")
        print("\n📌 To proceed with Day 1 data ingestion:")
        print("   1. Place your 10 CSV datasets in the data/raw/ directory")
        print("   2. Ensure 'fund_master.csv' and 'nav_history.csv' are included")
        print("   3. Run this script again")
        print("\n📁 Current directory structure:")
        print("   BLUESTOCK_FINTECH_PROJECT_01/")
        print("   ├── data/")
        print("   │   ├── raw/           (← Place CSV files here)")
        print("   │   └── processed/")
        print("   ├── data_ingestion.py")
        print("   ├── live_nav_fetch.py")
        print("   └── requirements.txt")
    else:
        print(f"\n✅ Found {len(target_csvs)} CSV file(s) in data/raw/")
        print(f"   Files: {[os.path.basename(f) for f in target_csvs]}\n")
        
        # Run ingestion pipeline
        loaded_data = load_and_profile_datasets(target_csvs)
        
        # Run AMFI validation
        validate_amfi_data(loaded_data)
        
        # Print data quality summary
        print_dq_summary(loaded_data)
        
        print("\n✅ Data ingestion pipeline execution complete!")
