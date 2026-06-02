import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def set_visualization_style():
    """
    Sets consistent visualization theme for all plots.
    """
    sns.set_style('whitegrid')
    sns.set_palette('husl')
    plt.rcParams['figure.figsize'] = (14, 8)
    plt.rcParams['font.size'] = 10
    print("✅ Visualization style configured")

def analyze_nav_distribution(df, price_col='nav', dataset_name='NAV Data'):
    """
    Analyzes distribution of NAV prices.
    Generates histogram, Q-Q plot, and distribution statistics.
    """
    print("\n" + "="*60)
    print(f" PHASE 1: NAV DISTRIBUTION ANALYSIS - {dataset_name.upper()} ")
    print("="*60)
    
    # Statistical Summary
    print(f"\n📊 Distribution Statistics:")
    print(f"-" * 40)
    print(f"Mean:           {df[price_col].mean():.4f}")
    print(f"Median:         {df[price_col].median():.4f}")
    print(f"Std Dev:        {df[price_col].std():.4f}")
    print(f"Skewness:       {df[price_col].skew():.4f}")
    print(f"Kurtosis:       {df[price_col].kurtosis():.4f}")
    print(f"Min:            {df[price_col].min():.4f}")
    print(f"Max:            {df[price_col].max():.4f}")
    print(f"Range:          {df[price_col].max() - df[price_col].min():.4f}")
    
    # Normality Test (Shapiro-Wilk)
    if len(df) > 5000:
        sample = df[price_col].sample(5000)
    else:
        sample = df[price_col]
    
    stat, p_value = stats.shapiro(sample.dropna())
    print(f"\n📈 Normality Test (Shapiro-Wilk):")
    print(f"Statistic: {stat:.4f}")
    print(f"P-value: {p_value:.6f}")
    if p_value > 0.05:
        print(f"✅ Data appears normally distributed (p > 0.05)")
    else:
        print(f"⚠️  Data deviates from normality (p < 0.05)")
    
    return {
        'mean': df[price_col].mean(),
        'median': df[price_col].median(),
        'std': df[price_col].std(),
        'skewness': df[price_col].skew(),
        'kurtosis': df[price_col].kurtosis(),
        'normality_p_value': p_value
    }

def analyze_returns_distribution(df, return_col='simple_return_1d', dataset_name='Returns Data'):
    """
    Analyzes distribution of returns.
    Checks for mean-reversion and tail risk.
    """
    print("\n" + "="*60)
    print(f" PHASE 2: RETURNS DISTRIBUTION ANALYSIS - {dataset_name.upper()} ")
    print("="*60)
    
    returns = df[return_col].dropna()
    
    print(f"\n📊 Return Statistics:")
    print(f"-" * 40)
    print(f"Mean Return:        {returns.mean():.4f}%")
    print(f"Median Return:      {returns.median():.4f}%")
    print(f"Std Dev (Vol):      {returns.std():.4f}%")
    print(f"Skewness:           {returns.skew():.4f}")
    print(f"Excess Kurtosis:    {returns.kurtosis():.4f}")
    print(f"Min Return:         {returns.min():.4f}%")
    print(f"Max Return:         {returns.max():.4f}%")
    
    # Value at Risk (VaR) and Conditional VaR
    var_95 = returns.quantile(0.05)
    cvar_95 = returns[returns <= var_95].mean()
    
    print(f"\n⚠️  Risk Metrics:")
    print(f"Value at Risk (95%):    {var_95:.4f}%")
    print(f"Conditional VaR (95%):  {cvar_95:.4f}%")
    print(f"Sharpe-Like Ratio:      {returns.mean() / returns.std():.4f}")
    
    # Positive/Negative day analysis
    positive_days = (returns > 0).sum()
    negative_days = (returns < 0).sum()
    total_days = len(returns)
    
    print(f"\n📈 Win/Loss Analysis:")
    print(f"Positive days:      {positive_days} ({positive_days/total_days*100:.2f}%)")
    print(f"Negative days:      {negative_days} ({negative_days/total_days*100:.2f}%)")
    print(f"Avg positive return: {returns[returns > 0].mean():.4f}%")
    print(f"Avg negative return: {returns[returns < 0].mean():.4f}%")
    
    return {
        'mean_return': returns.mean(),
        'std_return': returns.std(),
        'var_95': var_95,
        'cvar_95': cvar_95,
        'win_rate': positive_days / total_days
    }

def analyze_correlation_matrix(df, numeric_cols=None, dataset_name='Dataset'):
    """
    Analyzes correlation between numeric columns.
    Identifies multicollinearity issues.
    """
    print("\n" + "="*60)
    print(f" PHASE 3: CORRELATION ANALYSIS - {dataset_name.upper()} ")
    print("="*60)
    
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    corr_matrix = df[numeric_cols].corr()
    
    print(f"\n🔗 Correlation Matrix Shape: {corr_matrix.shape}")
    
    # High correlation pairs (excluding self-correlation)
    print(f"\n📊 High Correlation Pairs (|r| > 0.7):")
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                col_i = corr_matrix.columns[i]
                col_j = corr_matrix.columns[j]
                high_corr_pairs.append((col_i, col_j, corr_val))
                print(f"  {col_i:25} <-> {col_j:25} : {corr_val:7.4f}")
    
    if len(high_corr_pairs) == 0:
        print(f"  ✅ No high correlation pairs detected")
    
    return corr_matrix

def analyze_temporal_trends(df, date_col='date', price_col='nav', dataset_name='NAV'):
    """
    Analyzes price trends over time.
    Identifies periods of growth, stagnation, decline.
    """
    print("\n" + "="*60)
    print(f" PHASE 4: TEMPORAL TREND ANALYSIS - {dataset_name.upper()} ")
    print("="*60)
    
    df_sorted = df.sort_values(date_col).copy()
    
    if date_col in df_sorted.columns:
        date_range = pd.to_datetime(df_sorted[date_col])
        print(f"\n📅 Time Period Coverage:")
        print(f"-" * 40)
        print(f"Start Date:     {date_range.min()}")
        print(f"End Date:       {date_range.max()}")
        print(f"Duration:       {(date_range.max() - date_range.min()).days} days")
        print(f"Total Records:  {len(df_sorted)}")
    
    print(f"\n📈 Price Trend:")
    print(f"-" * 40)
    print(f"Starting Price: {df_sorted[price_col].iloc[0]:.4f}")
    print(f"Ending Price:   {df_sorted[price_col].iloc[-1]:.4f}")
    total_change = ((df_sorted[price_col].iloc[-1] / df_sorted[price_col].iloc[0]) - 1) * 100
    print(f"Total Change:   {total_change:.2f}%")
    
    # Peak and Trough analysis
    peak_idx = df_sorted[price_col].idxmax()
    trough_idx = df_sorted[price_col].idxmin()
    
    print(f"\n📊 Peak/Trough Analysis:")
    print(f"-" * 40)
    print(f"Peak Price:     {df_sorted[price_col].max():.4f}")
    if date_col in df_sorted.columns:
        print(f"Peak Date:      {df_sorted.loc[peak_idx, date_col]}")
    print(f"Trough Price:   {df_sorted[price_col].min():.4f}")
    if date_col in df_sorted.columns:
        print(f"Trough Date:    {df_sorted.loc[trough_idx, date_col]}")
    
    return {
        'start_price': df_sorted[price_col].iloc[0],
        'end_price': df_sorted[price_col].iloc[-1],
        'total_return': total_change,
        'peak': df_sorted[price_col].max(),
        'trough': df_sorted[price_col].min()
    }

def analyze_volatility_profile(df, volatility_col='volatility_30d', dataset_name='Volatility'):
    """
    Analyzes volatility patterns and regimes.
    """
    print("\n" + "="*60)
    print(f" PHASE 5: VOLATILITY PROFILE ANALYSIS - {dataset_name.upper()} ")
    print("="*60)
    
    vol = df[volatility_col].dropna()
    
    print(f"\n📊 Volatility Statistics:")
    print(f"-" * 40)
    print(f"Mean Volatility:    {vol.mean():.4f}%")
    print(f"Median Volatility:  {vol.median():.4f}%")
    print(f"Std Dev:            {vol.std():.4f}%")
    print(f"Min Volatility:     {vol.min():.4f}%")
    print(f"Max Volatility:     {vol.max():.4f}%")
    
    # Volatility regimes
    p25 = vol.quantile(0.25)
    p50 = vol.quantile(0.50)
    p75 = vol.quantile(0.75)
    
    low_vol = (vol < p25).sum()
    medium_vol = ((vol >= p25) & (vol < p75)).sum()
    high_vol = (vol >= p75).sum()
    
    print(f"\n📈 Volatility Regimes:")
    print(f"-" * 40)
    print(f"Low Vol (< {p25:.4f}%):     {low_vol:5} days ({low_vol/len(vol)*100:6.2f}%)")
    print(f"Mid Vol ({p25:.4f}% - {p75:.4f}%): {medium_vol:5} days ({medium_vol/len(vol)*100:6.2f}%)")
    print(f"High Vol (> {p75:.4f}%):    {high_vol:5} days ({high_vol/len(vol)*100:6.2f}%)")
    
    return {
        'mean_vol': vol.mean(),
        'std_vol': vol.std(),
        'vol_of_vol': vol.std() / vol.mean()
    }

def compare_fund_performance(df, group_col='fund_house', metric_col='simple_return_365d'):
    """
    Compares performance across fund houses/categories.
    """
    print("\n" + "="*60)
    print(f" PHASE 6: COMPARATIVE PERFORMANCE ANALYSIS ")
    print("="*60)
    
    if group_col not in df.columns:
        print(f"⚠️  Column '{group_col}' not found in dataset")
        return None
    
    print(f"\n📊 Performance by {group_col.replace('_', ' ').title()}:")
    print(f"-" * 60)
    
    performance = df.groupby(group_col)[metric_col].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(4)
    
    print(performance)
    
    return performance

def generate_summary_statistics(df, dataset_name='Dataset'):
    """
    Generates comprehensive summary statistics.
    """
    print("\n" + "="*60)
    print(f" PHASE 7: SUMMARY STATISTICS - {dataset_name.upper()} ")
    print("="*60)
    
    print(f"\n📊 Overall Dataset Summary:")
    print(f"-" * 40)
    print(df.describe().to_string())
    
    return df.describe()

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# EXPLORATORY DATA ANALYSIS - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Set visualization style
    set_visualization_style()
    
    # Example usage
    dates = pd.date_range('2023-01-01', periods=365, freq='D')
    nav_prices = 100 + np.cumsum(np.random.randn(365) * 2)
    returns = np.random.randn(365) * 1.5
    volatility = np.abs(np.random.randn(365)) * 2 + 1
    
    sample_data = pd.DataFrame({
        'date': dates,
        'nav': nav_prices,
        'simple_return_1d': returns,
        'simple_return_365d': returns,
        'volatility_30d': volatility,
        'fund_house': np.random.choice(['SBI', 'ICICI', 'Nippon'], 365)
    })
    
    print(f"\n📥 Sample Data Loaded: {len(sample_data)} records")
    
    # Run EDA pipeline
    set_visualization_style()
    nav_dist = analyze_nav_distribution(sample_data)
    returns_dist = analyze_returns_distribution(sample_data)
    corr_matrix = analyze_correlation_matrix(sample_data)
    temporal_trends = analyze_temporal_trends(sample_data)
    vol_profile = analyze_volatility_profile(sample_data)
    performance = compare_fund_performance(sample_data)
    summary = generate_summary_statistics(sample_data)
    
    print("\n" + "="*60)
    print(" EDA PIPELINE COMPLETE ")
    print("="*60)
    print(f"\n✅ Exploratory Data Analysis complete")
