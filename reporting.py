import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_eda_report(df, dataset_name='Dataset', output_dir='reports'):
    """
    Generates comprehensive EDA report in text format.
    """
    print("\n" + "="*60)
    print(" GENERATING EDA REPORT ")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = f"{output_dir}/eda_report_{dataset_name}.txt"
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("EXPLORATORY DATA ANALYSIS REPORT - BLUESTOCK FINTECH\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Dataset: {dataset_name}\n")
        f.write("="*80 + "\n\n")
        
        # Basic Statistics
        f.write("1. BASIC STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n")
        f.write(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n\n")
        
        # Data Types
        f.write("2. DATA TYPES\n")
        f.write("-" * 80 + "\n")
        f.write(df.dtypes.to_string())
        f.write("\n\n")
        
        # Descriptive Statistics
        f.write("3. DESCRIPTIVE STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(df.describe().to_string())
        f.write("\n\n")
        
        # Missing Values
        f.write("4. MISSING VALUES ANALYSIS\n")
        f.write("-" * 80 + "\n")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Percentage': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        if len(missing_df) > 0:
            f.write(missing_df.to_string(index=False))
        else:
            f.write("No missing values detected.")
        f.write("\n\n")
        
        # Duplicates
        f.write("5. DUPLICATE ANALYSIS\n")
        f.write("-" * 80 + "\n")
        dup_count = df.duplicated().sum()
        f.write(f"Total duplicate rows: {dup_count:,}\n")
        f.write(f"Percentage: {(dup_count/len(df)*100):.2f}%\n\n")
        
        # Correlation Analysis
        f.write("6. CORRELATION ANALYSIS\n")
        f.write("-" * 80 + "\n")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            f.write(corr.to_string())
        else:
            f.write("Not enough numeric columns for correlation analysis.")
        f.write("\n\n")
        
        # Categorical Summary
        f.write("7. CATEGORICAL VARIABLES SUMMARY\n")
        f.write("-" * 80 + "\n")
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            f.write(f"\n{col}:\n")
            f.write(f"Unique values: {df[col].nunique()}\n")
            f.write("Value counts:\n")
            f.write(df[col].value_counts().to_string())
            f.write("\n")
        f.write("\n")
        
        # Key Insights
        f.write("8. KEY INSIGHTS & OBSERVATIONS\n")
        f.write("-" * 80 + "\n")
        
        numeric_data = df.select_dtypes(include=[np.number])
        if len(numeric_data.columns) > 0:
            f.write("\nSkewness & Kurtosis:\n")
            for col in numeric_data.columns:
                skew = numeric_data[col].skew()
                kurt = numeric_data[col].kurtosis()
                f.write(f"  {col}: Skewness={skew:.4f}, Kurtosis={kurt:.4f}\n")
        
        f.write("\nData Quality:\n")
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        f.write(f"  Data Completeness: {completeness:.2f}%\n")
        f.write(f"  Duplication Rate: {(dup_count/len(df)*100):.2f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"✅ EDA report saved: {report_path}")
    return report_path

def generate_fund_comparison_report(df, group_col='fund_house', metric_cols=None, output_dir='reports'):
    """
    Generates fund comparison report.
    """
    print("\n" + "="*60)
    print(" GENERATING FUND COMPARISON REPORT ")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = f"{output_dir}/fund_comparison_report.txt"
    
    if metric_cols is None:
        metric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("FUND COMPARISON REPORT - BLUESTOCK FINTECH\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Comparison by: {group_col}\n")
        f.write("="*80 + "\n\n")
        
        # Group comparison
        f.write(f"PERFORMANCE COMPARISON BY {group_col.upper()}\n")
        f.write("-" * 80 + "\n")
        
        if group_col in df.columns:
            for metric in metric_cols:
                if metric in df.columns:
                    f.write(f"\n{metric}:\n")
                    comparison = df.groupby(group_col)[metric].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
                    f.write(comparison.to_string())
                    f.write("\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"✅ Fund comparison report saved: {report_path}")
    return report_path

def generate_performance_ranking_report(df, metric_col='simple_return_365d', top_n=10, output_dir='reports'):
    """
    Generates performance ranking report.
    """
    print("\n" + "="*60)
    print(" GENERATING PERFORMANCE RANKING REPORT ")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = f"{output_dir}/performance_ranking_report.txt"
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("PERFORMANCE RANKING REPORT - BLUESTOCK FINTECH\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Metric: {metric_col}\n")
        f.write(f"Top {top_n} Funds Displayed\n")
        f.write("="*80 + "\n\n")
        
        if 'scheme_name' in df.columns and metric_col in df.columns:
            ranking = df.groupby('scheme_name')[metric_col].mean().sort_values(ascending=False)
            
            f.write(f"TOP {top_n} BEST PERFORMING FUNDS\n")
            f.write("-" * 80 + "\n")
            for i, (fund, value) in enumerate(ranking.head(top_n).items(), 1):
                f.write(f"{i:2}. {str(fund):40} : {value:10.4f}%\n")
            
            f.write(f"\nBOTTOM {top_n} WORST PERFORMING FUNDS\n")
            f.write("-" * 80 + "\n")
            for i, (fund, value) in enumerate(ranking.tail(top_n).iloc[::-1].items(), 1):
                f.write(f"{i:2}. {str(fund):40} : {value:10.4f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"✅ Performance ranking report saved: {report_path}")
    return report_path

def generate_risk_profile_report(df, volatility_col='volatility_30d', output_dir='reports'):
    """
    Generates risk profile report.
    """
    print("\n" + "="*60)
    print(" GENERATING RISK PROFILE REPORT ")
    print("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    report_path = f"{output_dir}/risk_profile_report.txt"
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("RISK PROFILE REPORT - BLUESTOCK FINTECH\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Volatility Metric: {volatility_col}\n")
        f.write("="*80 + "\n\n")
        
        if volatility_col in df.columns:
            vol = df[volatility_col].dropna()
            
            f.write("VOLATILITY STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Mean Volatility:        {vol.mean():.4f}%\n")
            f.write(f"Median Volatility:      {vol.median():.4f}%\n")
            f.write(f"Std Dev of Volatility:  {vol.std():.4f}%\n")
            f.write(f"Min Volatility:         {vol.min():.4f}%\n")
            f.write(f"Max Volatility:         {vol.max():.4f}%\n")
            
            # Risk tiers
            p25 = vol.quantile(0.25)
            p50 = vol.quantile(0.50)
            p75 = vol.quantile(0.75)
            
            f.write(f"\nVOLATILITY QUARTILES\n")
            f.write("-" * 80 + "\n")
            f.write(f"25th Percentile: {p25:.4f}%\n")
            f.write(f"50th Percentile: {p50:.4f}%\n")
            f.write(f"75th Percentile: {p75:.4f}%\n")
            
            f.write(f"\nRISK CLASSIFICATION\n")
            f.write("-" * 80 + "\n")
            low_vol = (vol < p25).sum()
            mid_vol = ((vol >= p25) & (vol < p75)).sum()
            high_vol = (vol >= p75).sum()
            
            f.write(f"Low Risk (< {p25:.4f}%):     {low_vol:5} days ({low_vol/len(vol)*100:6.2f}%)\n")
            f.write(f"Mid Risk ({p25:.4f}% - {p75:.4f}%): {mid_vol:5} days ({mid_vol/len(vol)*100:6.2f}%)\n")
            f.write(f"High Risk (> {p75:.4f}%):    {high_vol:5} days ({high_vol/len(vol)*100:6.2f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"✅ Risk profile report saved: {report_path}")
    return report_path

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# REPORTING MODULE - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Example usage
    sample_data = pd.DataFrame({
        'scheme_name': ['Fund A', 'Fund B', 'Fund C'] * 100,
        'fund_house': ['SBI', 'ICICI', 'Nippon'] * 100,
        'simple_return_365d': np.random.randn(300) * 5 + 10,
        'volatility_30d': np.abs(np.random.randn(300)) * 2 + 2
    })
    
    print(f"\n📥 Sample Data Loaded: {len(sample_data)} records")
    
    # Generate reports
    generate_eda_report(sample_data)
    generate_fund_comparison_report(sample_data)
    generate_performance_ranking_report(sample_data)
    generate_risk_profile_report(sample_data)
    
    print("\n" + "="*60)
    print(" REPORTING PIPELINE COMPLETE ")
    print("="*60)
