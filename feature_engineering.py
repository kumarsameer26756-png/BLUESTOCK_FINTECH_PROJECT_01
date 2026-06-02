import pandas as pd
import numpy as np
from datetime import datetime
import os

def calculate_returns(df, price_col='nav', date_col='date', periods=[1, 7, 30, 365]):
    """
    Calculates daily, weekly, monthly, and annual returns.
    Returns: Simple returns (%) and Log returns
    """
    print("\n" + "="*60)
    print(" PHASE 1: RETURNS CALCULATION ")
    print("="*60)
    
    df_features = df.copy()
    
    # Ensure date column is datetime
    if date_col in df_features.columns:
        df_features[date_col] = pd.to_datetime(df_features[date_col])
        df_features = df_features.sort_values(date_col)
    
    for period in periods:
        # Simple Returns: (Price_t - Price_t-n) / Price_t-n * 100
        simple_return_col = f'simple_return_{period}d'
        df_features[simple_return_col] = df_features[price_col].pct_change(periods=period) * 100
        
        # Log Returns: ln(Price_t / Price_t-n)
        log_return_col = f'log_return_{period}d'
        df_features[log_return_col] = np.log(df_features[price_col] / df_features[price_col].shift(periods)) * 100
        
        print(f"✅ {period}-day returns calculated (simple & log)")
    
    return df_features

def calculate_moving_averages(df, price_col='nav', windows=[7, 30, 90, 365]):
    """
    Calculates moving averages over specified windows.
    """
    print("\n" + "="*60)
    print(" PHASE 2: MOVING AVERAGES ")
    print("="*60)
    
    df_features = df.copy()
    
    for window in windows:
        ma_col = f'ma_{window}d'
        df_features[ma_col] = df_features[price_col].rolling(window=window, min_periods=1).mean()
        print(f"✅ {window}-day moving average calculated")
    
    return df_features

def calculate_volatility(df, return_col='simple_return_1d', windows=[7, 30, 90]):
    """
    Calculates rolling volatility (standard deviation of returns).
    """
    print("\n" + "="*60)
    print(" PHASE 3: VOLATILITY METRICS ")
    print("="*60)
    
    df_features = df.copy()
    
    if return_col not in df_features.columns:
        # Calculate 1-day returns if not present
        df_features['simple_return_1d'] = df_features['nav'].pct_change() * 100
        return_col = 'simple_return_1d'
    
    for window in windows:
        volatility_col = f'volatility_{window}d'
        df_features[volatility_col] = df_features[return_col].rolling(window=window, min_periods=1).std()
        print(f"✅ {window}-day volatility calculated")
    
    return df_features

def calculate_sharpe_ratio(df, return_col='simple_return_1d', risk_free_rate=6.0, window=365):
    """
    Calculates rolling Sharpe Ratio.
    Sharpe Ratio = (Mean Return - Risk-Free Rate) / Volatility
    """
    print("\n" + "="*60)
    print(" PHASE 4: SHARPE RATIO ")
    print("="*60)
    
    df_features = df.copy()
    
    if return_col not in df_features.columns:
        df_features['simple_return_1d'] = df_features['nav'].pct_change() * 100
        return_col = 'simple_return_1d'
    
    # Calculate rolling mean return and volatility
    rolling_mean = df_features[return_col].rolling(window=window, min_periods=1).mean()
    rolling_std = df_features[return_col].rolling(window=window, min_periods=1).std()
    
    # Sharpe Ratio = (Mean Return - Risk-Free Rate) / Volatility
    daily_rf_rate = risk_free_rate / 365  # Convert annual to daily
    df_features['sharpe_ratio'] = (rolling_mean - daily_rf_rate) / rolling_std
    
    print(f"✅ Sharpe Ratio calculated (risk-free rate: {risk_free_rate}% p.a.)")
    print(f"   Window: {window} days")
    
    return df_features

def calculate_drawdown(df, price_col='nav'):
    """
    Calculates cumulative and rolling drawdown.
    Drawdown = (Current Price - Peak Price) / Peak Price
    """
    print("\n" + "="*60)
    print(" PHASE 5: DRAWDOWN ANALYSIS ")
    print("="*60)
    
    df_features = df.copy()
    
    # Cumulative maximum (running peak)
    cumulative_max = df_features[price_col].cummax()
    
    # Drawdown calculation
    df_features['drawdown'] = (df_features[price_col] - cumulative_max) / cumulative_max * 100
    
    # Maximum drawdown up to that point
    df_features['max_drawdown'] = df_features['drawdown'].cummin()
    
    print(f"✅ Drawdown metrics calculated")
    print(f"   Current drawdown range: [{df_features['drawdown'].min():.2f}%, {df_features['drawdown'].max():.2f}%]")
    
    return df_features

def calculate_performance_metrics(df, price_col='nav', date_col='date'):
    """
    Aggregates key performance metrics for each scheme.
    """
    print("\n" + "="*60)
    print(" PHASE 6: AGGREGATE PERFORMANCE METRICS ")
    print("="*60)
    
    metrics = {}
    
    # Total return
    if len(df) > 1:
        total_return = ((df[price_col].iloc[-1] - df[price_col].iloc[0]) / df[price_col].iloc[0]) * 100
        metrics['total_return_%'] = total_return
    
    # CAGR (Compound Annual Growth Rate)
    if date_col in df.columns and len(df) > 1:
        start_date = pd.to_datetime(df[date_col].min())
        end_date = pd.to_datetime(df[date_col].max())
        days = (end_date - start_date).days
        years = days / 365.25
        
        if years > 0:
            cagr = (((df[price_col].iloc[-1] / df[price_col].iloc[0]) ** (1/years)) - 1) * 100
            metrics['cagr_%'] = cagr
    
    # Volatility (annualized)
    if 'simple_return_1d' in df.columns:
        annualized_vol = df['simple_return_1d'].std() * np.sqrt(252)  # 252 trading days
        metrics['annualized_volatility_%'] = annualized_vol
    
    # Sharpe Ratio
    if 'sharpe_ratio' in df.columns:
        metrics['avg_sharpe_ratio'] = df['sharpe_ratio'].mean()
    
    # Maximum Drawdown
    if 'max_drawdown' in df.columns:
        metrics['max_drawdown_%'] = df['max_drawdown'].min()
    
    print(f"\n✅ Performance metrics calculated:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.2f}")
    
    return metrics

def enrich_fund_metadata(df, fund_master_df=None):
    """
    Enriches NAV data with fund master metadata.
    """
    print("\n" + "="*60)
    print(" PHASE 7: FUND METADATA ENRICHMENT ")
    print("="*60)
    
    df_enriched = df.copy()
    
    if fund_master_df is not None and 'scheme_code' in df_enriched.columns:
        # Merge with fund master
        df_enriched = df_enriched.merge(
            fund_master_df,
            on='scheme_code',
            how='left',
            suffixes=('', '_master')
        )
        print(f"✅ Fund metadata merged successfully")
    else:
        print(f"⚠️  Fund master data not available for enrichment")
    
    return df_enriched

def save_engineered_features(processed_dfs, output_dir='data/processed'):
    """
    Saves feature-engineered datasets.
    """
    print("\n" + "="*60)
    print(" FEATURE EXPORT ")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    
    for name, df in processed_dfs.items():
        try:
            output_path = f"{output_dir}/{name}_features.csv"
            df.to_csv(output_path, index=False)
            print(f"✅ {name:30} -> {output_path}")
            print(f"   Columns: {len(df.columns)} | Rows: {len(df)}")
        except Exception as e:
            print(f"❌ {name:30} -> Export failed: {e}")

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# FEATURE ENGINEERING PIPELINE - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Example usage
    dates = pd.date_range('2023-01-01', periods=365, freq='D')
    nav_prices = 100 + np.cumsum(np.random.randn(365) * 2)
    
    sample_data = pd.DataFrame({
        'date': dates,
        'nav': nav_prices,
        'scheme_code': [119551] * 365
    })
    
    print(f"\n📥 Sample Data Loaded: {len(sample_data)} records")
    
    # Run feature engineering pipeline
    df_returns = calculate_returns(sample_data)
    df_ma = calculate_moving_averages(df_returns)
    df_volatility = calculate_volatility(df_ma)
    df_sharpe = calculate_sharpe_ratio(df_volatility)
    df_drawdown = calculate_drawdown(df_sharpe)
    metrics = calculate_performance_metrics(df_drawdown)
    df_final = enrich_fund_metadata(df_drawdown)
    
    print("\n" + "="*60)
    print(" FEATURE ENGINEERING COMPLETE ")
    print("="*60)
    print(f"\n✅ Feature engineering pipeline complete")
    print(f"   Total features created: {len(df_final.columns)}")
