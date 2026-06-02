import os
import pandas as pd

def load_and_profile_datasets(csv_files):
    """
    Loads 10 CSV datasets, prints profiling metadata, and checks for anomalies.
    """
    datasets = {}
    print("="*60)
    print(" PHASE 1: LOADING & PROFILING LOCAL DATASETS ")
    print("="*60)
    
    for file_path in csv_files:
        if not os.path.exists(file_path):
            print(f"⚠️ Warning: File not found at {file_path}. Skipping.")
            continue
            
        name = os.path.basename(file_path).split('.')[0]
        try:
            df = pd.read_csv(file_path)
            datasets[name] = df
            
            print(f"\n📊 Dataset: {name.upper()}")
            print("-" * 40)
            print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print("\nData Types:")
            print(df.dtypes)
            print("\nFirst 3 Rows:")
            print(df.head(3))
            
            # Basic Anomalies check
            missing_vals = df.isnull().sum().sum()
            dup_rows = df.duplicated().sum()
            if missing_vals > 0 or dup_rows > 0:
                print(f"❌ Anomalies Detected in {name}:")
                if missing_vals > 0:
                    print(f"   - Total missing values: {missing_vals}")
                if dup_rows > 0:
                    print(f"   - Duplicate rows found: {dup_rows}")
            else:
                print("✅ No immediate missing values or duplicate rows detected.")
                
            print("." * 60)
        except Exception as e:
            print(f"💥 Error reading {file_path}: {e}")
            
    return datasets

def validate_amfi_data(datasets):
    """
    Explores Fund Master and validates referential integrity against NAV History.
    Assumes keys 'fund_master' and 'nav_history' exist in the datasets dict.
    """
    print("\n" + "="*60)
    print(" PHASE 2: MUTUAL FUND METADATA EXPLORATION & DQ VALIDATION ")
    print("="*60)
    
    if 'fund_master' not in datasets or 'nav_history' not in datasets:
        print("❌ Critical: Validation skipped. Ensure 'fund_master' and 'nav_history' dataframes are loaded.")
        return

    fm = datasets['fund_master']
    nh = datasets['nav_history']
    
    # 1. Exploration
    print("\n🔍 Fund Master Metadata Highlights:")
    for col in ['fund_house', 'category', 'sub_category', 'risk_grade']:
        if col in fm.columns:
            print(f" Unique {col.replace('_', ' ').title()} count: {fm[col].nunique()}")
            if fm[col].nunique() < 10:
                print(f"   Values: {fm[col].unique()}")
                
    # 2. Scheme Code Structure Explanation
    print("\nℹ️ AMFI Scheme Code Structure Note:")
    print("> AMFI codes are unique 6-digit numeric identifiers assigned by the Association of Mutual Funds in India.")
    print("> Master data maps these codes to structural metadata (house, category), while historical tables map them to time-series NAV paths.")

    # 3. Data Quality Validation (Referential Integrity Check)
    # Assumes code columns are named 'scheme_code' or 'amfi_code' -> Adjust string if your headers differ
    fm_code_col = 'scheme_code' if 'scheme_code' in fm.columns else 'amfi_code'
    nh_code_col = 'scheme_code' if 'scheme_code' in nh.columns else 'amfi_code'
    
    if fm_code_col in fm.columns and nh_code_col in nh.columns:
        master_codes = set(fm[fm_code_col].dropna().unique())
        history_codes = set(nh[nh_code_col].dropna().unique())
        
        missing_in_history = master_codes - history_codes
        
        print("\n⚖️ Data Quality Summary:")
        print(f" - Unique schemes in Master: {len(master_codes)}")
        print(f" - Unique schemes in History: {len(history_codes)}")
        
        if len(missing_in_history) == 0:
            print(" ✅ SUCCESS: Referential integrity confirmed. Every scheme code in fund_master exists in nav_history.")
        else:
            print(f" ⚠️ WARNING: Referential Integrity Breach!")
            print(f"   - {len(missing_in_history)} schemes found in Master but have NO records in NAV History.")
            print(f"   - Sample missing codes: {list(missing_in_history)[:5]}")
    else:
        print("❌ Validation Fail: Could not match key 'scheme_code' or 'amfi_code' columns across dataframes.")

if __name__ == "__main__":
    # Define paths to your 10 actual CSV datasets
    # (Update names dynamically to match what you actually have in your local environment)
    target_csvs = [
        "data/raw/fund_master.csv",
        "data/raw/nav_history.csv",
        # "data/raw/dataset3.csv", ... add remaining paths up to 10 files
    ]
    
    # Fallback simulation if you haven't placed all files yet
    existing_csvs = [f for f in target_csvs if os.path.exists(f)]
    if not existing_csvs:
        print("ℹ️ Please drop your 10 CSV data files inside 'data/raw/' to see automated execution.")
    else:
        loaded_data = load_and_profile_datasets(existing_csvs)
        validate_amfi_data(loaded_data)
