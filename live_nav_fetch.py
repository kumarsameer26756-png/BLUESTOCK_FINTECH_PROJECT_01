import os
import json
import requests
import pandas as pd

def fetch_live_nav(scheme_code, filename_suffix):
    """
    Fetches raw NAV JSON from mfapi.in, parses it, and exports data to CSV.
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"🌐 Requesting: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if not data or 'data' not in data or 'meta' not in data:
            print(f"⚠️ Unexpected payload format for scheme {scheme_code}.")
            return None
            
        # Parse Meta & Historical elements
        meta = data['meta']
        nav_list = data['data']
        
        print(f"✅ Successfully retrieved: {meta.get('scheme_name', 'Unknown Scheme')}")
        
        # Flatten into a DataFrame
        df = pd.DataFrame(nav_list)
        # Add tracking metadata features
        df['scheme_code'] = meta.get('scheme_code')
        df['scheme_name'] = meta.get('scheme_name')
        
        # Enforce column positioning
        columns_order = ['scheme_code', 'scheme_name', 'date', 'nav']
        df = df[[col for col in columns_order if col in df.columns]]
        
        # Ensure targeted directory paths exist
        os.makedirs("data/raw", exist_ok=True)
        
        # Output to Raw storage
        output_path = f"data/raw/nav_{filename_suffix}.csv"
        df.to_csv(output_path, index=False)
        print(f"💾 File written successfully to -> {output_path}")
        return df

    except requests.exceptions.RequestException as re:
        print(f"❌ Network or Http failure for scheme {scheme_code}: {re}")
    except Exception as e:
        print(f"❌ Failed processing scheme {scheme_code}: {e}")
    return None

def main():
    print("="*60)
    print(" RUNNING LIVE API INGESTION PIPELINE ")
    print("="*60)
    
    # 1. Fetch Targeted Single Scheme
    print("\n--- Ingesting Single Scheme Target ---")
    fetch_live_nav("125497", "hdfc_top_100_direct")
    
    # 2. Fetch Large Cap Key Benchmarks
    print("\n--- Ingesting Key Large Cap Schemes ---")
    target_schemes = {
        "119551": "sbi_bluechip",
        "120503": "icici_bluechip",
        "118632": "nippon_large_cap",
        "119092": "axis_bluechip",
        "120841": "kotak_bluechip"
    }
    
    for code, label in target_schemes.items():
        fetch_live_nav(code, label)

if __name__ == "__main__":
    main()
