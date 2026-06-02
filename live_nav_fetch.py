import os
import json
import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries(retries=3, backoff_factor=0.5, timeout=15):
    """
    Creates a requests session with automatic retry strategy.
    Handles network failures and server errors gracefully.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_live_nav(scheme_code, filename_suffix, session=None, delay=1.0):
    """
    Fetches raw NAV JSON from mfapi.in, parses it, and exports data to CSV.
    
    Args:
        scheme_code (str): AMFI scheme code (e.g., "125497")
        filename_suffix (str): Suffix for output CSV filename
        session (requests.Session): Optional session with retry logic
        delay (float): Delay in seconds between API requests (rate limiting)
    
    Returns:
        pd.DataFrame: Loaded NAV data or None if failed
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"\n🌐 Requesting: {url}")
    
    # Add delay for rate limiting
    time.sleep(delay)
    
    try:
        if session is None:
            session = create_session_with_retries()
        
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Validate response structure
        if not data or 'data' not in data or 'meta' not in data:
            print(f"  ⚠️ Unexpected payload format for scheme {scheme_code}")
            print(f"     Response keys: {list(data.keys()) if data else 'Empty'}")
            return None
        
        # Extract metadata and history
        meta = data['meta']
        nav_list = data['data']
        
        scheme_name = meta.get('scheme_name', 'Unknown Scheme')
        scheme_type = meta.get('scheme_type', 'Unknown')
        
        print(f"  ✅ Successfully retrieved: {scheme_name}")
        print(f"     Type: {scheme_type}")
        print(f"     Records: {len(nav_list):,} NAV entries")
        
        # Flatten into DataFrame
        df = pd.DataFrame(nav_list)
        
        # Add tracking metadata
        df['scheme_code'] = meta.get('scheme_code')
        df['scheme_name'] = scheme_name
        
        # Reorder columns
        columns_order = ['scheme_code', 'scheme_name', 'date', 'nav']
        df = df[[col for col in columns_order if col in df.columns]]
        
        # Ensure data directory exists
        os.makedirs("data/raw", exist_ok=True)
        
        # Save to CSV
        output_path = f"data/raw/nav_{filename_suffix}.csv"
        df.to_csv(output_path, index=False)
        
        print(f"  💾 File saved: {output_path}")
        print(f"     Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        return df

    except requests.exceptions.Timeout:
        print(f"  ❌ Request timeout for scheme {scheme_code} (>15 seconds)")
        print(f"     mfapi.in may be temporarily unavailable")
        return None
    
    except requests.exceptions.ConnectionError as ce:
        print(f"  ❌ Connection error for scheme {scheme_code}")
        print(f"     Details: {ce}")
        return None
    
    except requests.exceptions.HTTPError as he:
        print(f"  ❌ HTTP error {response.status_code} for scheme {scheme_code}")
        if response.status_code == 404:
            print(f"     Scheme code not found on mfapi.in")
        elif response.status_code == 429:
            print(f"     Rate limit exceeded - try again later")
        return None
    
    except json.JSONDecodeError as je:
        print(f"  ❌ Invalid JSON response for scheme {scheme_code}")
        print(f"     Details: {je}")
        return None
    
    except Exception as e:
        print(f"  ❌ Unexpected error for scheme {scheme_code}")
        print(f"     Details: {type(e).__name__}: {e}")
        return None

def main():
    """
    Main execution: Fetches NAV data for all target schemes.
    """
    print("\n" + "="*70)
    print(" DAY 1: LIVE NAV INGESTION PIPELINE - BLUESTOCK FINTECH PROJECT")
    print("="*70)
    
    # Create session with retry logic
    session = create_session_with_retries(retries=3, backoff_factor=1.0)
    
    # Define target schemes
    target_schemes = {
        "125497": "hdfc_top_100_direct",      # HDFC Top 100 Direct
        "119551": "sbi_bluechip",              # SBI Bluechip
        "120503": "icici_bluechip",            # ICICI Bluechip
        "118632": "nippon_large_cap",          # Nippon Large Cap
        "119092": "axis_bluechip",             # Axis Bluechip
        "120841": "kotak_bluechip"             # Kotak Bluechip
    }
    
    print(f"\n📋 Target Schemes ({len(target_schemes)}):")
    print("-" * 70)
    for code, label in target_schemes.items():
        print(f"  {code:6} → {label}")
    
    # Fetch NAV for all schemes
    print("\n\n🔄 Fetching Live NAV Data...")
    print("-" * 70)
    
    results = {}
    for idx, (code, label) in enumerate(target_schemes.items(), 1):
        print(f"\n[{idx}/{len(target_schemes)}] Scheme Code: {code}")
        df = fetch_live_nav(code, label, session=session, delay=2.0)
        results[code] = {
            'label': label,
            'success': df is not None,
            'rows': len(df) if df is not None else 0
        }
    
    # Print summary report
    print("\n\n" + "="*70)
    print(" EXECUTION SUMMARY ")
    print("="*70)
    
    successful = sum(1 for r in results.values() if r['success'])
    total_records = sum(r['rows'] for r in results.values())
    
    print(f"\n✅ Successful Downloads: {successful}/{len(target_schemes)}")
    print(f"   Total NAV Records:   {total_records:,}")
    
    print(f"\n📊 Scheme-wise Breakdown:")
    print("-" * 70)
    for code, result in results.items():
        status = "✅" if result['success'] else "❌"
        print(f"  {status} {code}: {result['label']:30} ({result['rows']:,} records)")
    
    print(f"\n📁 Output Location: data/raw/")
    print(f"   Files created: {successful}")
    
    if successful == len(target_schemes):
        print(f"\n🎉 All schemes fetched successfully!")
    else:
        print(f"\n⚠️ {len(target_schemes) - successful} scheme(s) failed.")
        print(f"   Possible causes:")
        print(f"   • Scheme code may be invalid")
        print(f"   • API temporarily unavailable")
        print(f"   • Network connectivity issues")
        print(f"   • Rate limiting by mfapi.in")
    
    print("\n" + "="*70)
    
    return results

if __name__ == "__main__":
    main()
