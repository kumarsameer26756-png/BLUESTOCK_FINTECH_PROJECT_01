import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

def create_distribution_plots(df, price_col='nav', output_dir='reports/visualizations'):
    """
    Creates histogram, KDE plot, and Q-Q plot for NAV distribution.
    """
    print("\n" + "="*60)
    print(" PHASE 1: DISTRIBUTION VISUALIZATIONS ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('NAV Distribution Analysis', fontsize=16, fontweight='bold')
    
    # Histogram with KDE
    axes[0, 0].hist(df[price_col].dropna(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('NAV Histogram with KDE')
    axes[0, 0].set_xlabel('NAV Value')
    axes[0, 0].set_ylabel('Frequency')
    
    # KDE plot
    df[price_col].dropna().plot(kind='kde', ax=axes[0, 1], color='darkblue', linewidth=2)
    axes[0, 1].set_title('Kernel Density Estimate')
    axes[0, 1].set_xlabel('NAV Value')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Box plot
    axes[1, 0].boxplot(df[price_col].dropna())
    axes[1, 0].set_title('NAV Box Plot (Outlier Detection)')
    axes[1, 0].set_ylabel('NAV Value')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Q-Q plot
    from scipy import stats
    stats.probplot(df[price_col].dropna(), dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title('Q-Q Plot (Normality Check)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/nav_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✅ Distribution plots saved: {output_dir}/nav_distribution.png")
    plt.close()

def create_time_series_plots(df, date_col='date', price_col='nav', output_dir='reports/visualizations'):
    """
    Creates time series visualizations with trend lines.
    """
    print("\n" + "="*60)
    print(" PHASE 2: TIME SERIES VISUALIZATIONS ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    df_sorted = df.sort_values(date_col).copy()
    df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle('Time Series Analysis', fontsize=16, fontweight='bold')
    
    # NAV Time Series
    axes[0].plot(df_sorted[date_col], df_sorted[price_col], label='NAV', color='darkblue', linewidth=1.5)
    if 'ma_30d' in df_sorted.columns:
        axes[0].plot(df_sorted[date_col], df_sorted['ma_30d'], label='30-day MA', color='red', linewidth=2, alpha=0.7)
    if 'ma_365d' in df_sorted.columns:
        axes[0].plot(df_sorted[date_col], df_sorted['ma_365d'], label='365-day MA', color='green', linewidth=2, alpha=0.7)
    axes[0].set_title('NAV Price with Moving Averages')
    axes[0].set_ylabel('NAV Value')
    axes[0].legend(loc='best')
    axes[0].grid(True, alpha=0.3)
    
    # Returns Time Series
    if 'simple_return_1d' in df_sorted.columns:
        axes[1].plot(df_sorted[date_col], df_sorted['simple_return_1d'], label='Daily Returns', color='darkgreen', linewidth=0.8, alpha=0.7)
        axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
        axes[1].fill_between(df_sorted[date_col], df_sorted['simple_return_1d'], 0, alpha=0.3)
        axes[1].set_title('Daily Returns')
        axes[1].set_ylabel('Return %')
        axes[1].legend(loc='best')
        axes[1].grid(True, alpha=0.3)
    
    # Volatility Time Series
    if 'volatility_30d' in df_sorted.columns:
        axes[2].plot(df_sorted[date_col], df_sorted['volatility_30d'], label='30-day Volatility', color='darkred', linewidth=1.5)
        axes[2].fill_between(df_sorted[date_col], df_sorted['volatility_30d'], alpha=0.3, color='red')
        axes[2].set_title('Rolling Volatility (30-day)')
        axes[2].set_ylabel('Volatility %')
        axes[2].set_xlabel('Date')
        axes[2].legend(loc='best')
        axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/time_series_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ Time series plots saved: {output_dir}/time_series_analysis.png")
    plt.close()

def create_returns_analysis_plots(df, output_dir='reports/visualizations'):
    """
    Creates returns analysis visualizations.
    """
    print("\n" + "="*60)
    print(" PHASE 3: RETURNS ANALYSIS VISUALIZATIONS ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Returns Analysis', fontsize=16, fontweight='bold')
    
    if 'simple_return_1d' in df.columns:
        returns = df['simple_return_1d'].dropna()
        
        # Returns histogram
        axes[0, 0].hist(returns, bins=50, alpha=0.7, color='green', edgecolor='black')
        axes[0, 0].axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns.mean():.4f}%')
        axes[0, 0].set_title('Distribution of Daily Returns')
        axes[0, 0].set_xlabel('Return %')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Cumulative returns
        cum_returns = (1 + returns/100).cumprod() - 1
        axes[0, 1].plot(cum_returns.values, color='darkgreen', linewidth=2)
        axes[0, 1].fill_between(range(len(cum_returns)), cum_returns.values, alpha=0.3)
        axes[0, 1].set_title('Cumulative Returns')
        axes[0, 1].set_xlabel('Days')
        axes[0, 1].set_ylabel('Cumulative Return')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Rolling mean return
        rolling_mean = returns.rolling(30).mean()
        axes[1, 0].plot(rolling_mean.values, color='blue', linewidth=2)
        axes[1, 0].axhline(y=0, color='black', linestyle='--', linewidth=1)
        axes[1, 0].fill_between(range(len(rolling_mean)), rolling_mean.values, 0, alpha=0.3)
        axes[1, 0].set_title('30-day Rolling Mean Return')
        axes[1, 0].set_xlabel('Days')
        axes[1, 0].set_ylabel('Mean Return %')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Scatter: Return vs Volatility
        if 'volatility_30d' in df.columns:
            vol = df['volatility_30d'].dropna()
            common_idx = returns.index.intersection(vol.index)
            axes[1, 1].scatter(vol[common_idx], returns[common_idx], alpha=0.5, s=20)
            axes[1, 1].set_title('Return vs Volatility Scatter')
            axes[1, 1].set_xlabel('Volatility %')
            axes[1, 1].set_ylabel('Return %')
            axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/returns_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ Returns analysis plots saved: {output_dir}/returns_analysis.png")
    plt.close()

def create_correlation_heatmap(df, output_dir='reports/visualizations'):
    """
    Creates correlation matrix heatmap.
    """
    print("\n" + "="*60)
    print(" PHASE 4: CORRELATION HEATMAP ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"✅ Correlation heatmap saved: {output_dir}/correlation_heatmap.png")
    plt.close()

def create_risk_return_scatter(df, output_dir='reports/visualizations'):
    """
    Creates risk vs return scatter plot for all funds.
    """
    print("\n" + "="*60)
    print(" PHASE 5: RISK-RETURN SCATTER ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate aggregate metrics by scheme/fund
    if 'scheme_code' in df.columns or 'scheme_name' in df.columns:
        group_col = 'scheme_name' if 'scheme_name' in df.columns else 'scheme_code'
        
        metrics = df.groupby(group_col).agg({
            'simple_return_365d': 'mean' if 'simple_return_365d' in df.columns else 'mean',
            'volatility_30d': 'mean' if 'volatility_30d' in df.columns else 'std'
        }).dropna()
        
        if len(metrics) > 0:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            scatter = ax.scatter(metrics['volatility_30d'], metrics['simple_return_365d'], 
                               s=150, alpha=0.6, c=range(len(metrics)), cmap='viridis')
            
            for idx, (name, row) in enumerate(metrics.iterrows()):
                ax.annotate(str(name)[:20], 
                           (row['volatility_30d'], row['simple_return_365d']),
                           fontsize=8, alpha=0.7)
            
            ax.set_xlabel('Risk (Volatility %)', fontsize=12)
            ax.set_ylabel('Return (Annual %)', fontsize=12)
            ax.set_title('Risk-Return Profile (Efficient Frontier)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/risk_return_scatter.png', dpi=300, bbox_inches='tight')
            print(f"✅ Risk-return scatter saved: {output_dir}/risk_return_scatter.png")
            plt.close()

def create_performance_ranking(df, metric_col='simple_return_365d', output_dir='reports/visualizations'):
    """
    Creates bar chart of fund performance ranking.
    """
    print("\n" + "="*60)
    print(" PHASE 6: PERFORMANCE RANKING VISUALIZATION ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    if 'scheme_name' in df.columns and metric_col in df.columns:
        performance = df.groupby('scheme_name')[metric_col].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['green' if x > 0 else 'red' for x in performance.values]
        bars = ax.barh(range(len(performance)), performance.values, color=colors, alpha=0.7)
        
        ax.set_yticks(range(len(performance)))
        ax.set_yticklabels([str(x)[:25] for x in performance.index])
        ax.set_xlabel(f'{metric_col.replace("_", " ").title()} (%)', fontsize=12)
        ax.set_title('Fund Performance Ranking', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, performance.values)):
            ax.text(value, i, f' {value:.2f}%', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/performance_ranking.png', dpi=300, bbox_inches='tight')
        print(f"✅ Performance ranking saved: {output_dir}/performance_ranking.png")
        plt.close()

def create_category_analysis(df, category_col='category', metric_col='simple_return_365d', output_dir='reports/visualizations'):
    """
    Creates box plot of performance by category.
    """
    print("\n" + "="*60)
    print(" PHASE 7: CATEGORY ANALYSIS VISUALIZATION ")
    print("="*60)
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    if category_col in df.columns and metric_col in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        df_clean = df[[category_col, metric_col]].dropna()
        categories = df_clean[category_col].unique()
        
        data_by_category = [df_clean[df_clean[category_col] == cat][metric_col].values for cat in categories]
        
        bp = ax.boxplot(data_by_category, labels=[str(x)[:20] for x in categories], patch_artist=True)
        
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)
        
        ax.set_ylabel(f'{metric_col.replace("_", " ").title()} (%)', fontsize=12)
        ax.set_title('Performance Distribution by Category', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/category_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✅ Category analysis saved: {output_dir}/category_analysis.png")
        plt.close()

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# VISUALIZATION MODULE - BLUESTOCK FINTECH")
    print("#"*60)
    
    # Example usage
    dates = pd.date_range('2023-01-01', periods=365, freq='D')
    nav_prices = 100 + np.cumsum(np.random.randn(365) * 2)
    returns = np.random.randn(365) * 1.5
    volatility = np.abs(np.random.randn(365)) * 2 + 1
    
    sample_data = pd.DataFrame({
        'date': dates,
        'nav': nav_prices,
        'simple_return_1d': returns,
        'simple_return_365d': returns * 250,
        'volatility_30d': volatility,
        'ma_30d': pd.Series(nav_prices).rolling(30).mean().values,
        'ma_365d': pd.Series(nav_prices).rolling(365).mean().values,
        'scheme_name': ['Scheme A'] * 365,
        'category': ['Equity-Large Cap'] * 365
    })
    
    print(f"\n📥 Sample Data Loaded: {len(sample_data)} records")
    
    # Create visualizations
    create_distribution_plots(sample_data)
    create_time_series_plots(sample_data)
    create_returns_analysis_plots(sample_data)
    create_correlation_heatmap(sample_data)
    create_risk_return_scatter(sample_data)
    create_performance_ranking(sample_data)
    create_category_analysis(sample_data)
    
    print("\n" + "="*60)
    print(" VISUALIZATION PIPELINE COMPLETE ")
    print("="*60)
