# Day 3: Exploratory Data Analysis (EDA)

## 🎯 Overview

Day 3 focuses on understanding data patterns, distributions, correlations, and generating actionable insights through comprehensive analysis.

## 📋 New Files Created

### 1. **exploratory_analysis.py**
Core EDA functions for statistical analysis:
- ✅ NAV distribution analysis (histogram, KDE, normality tests)
- ✅ Returns distribution analysis (positive/negative days, VaR, Sharpe ratio)
- ✅ Correlation matrix analysis (multicollinearity detection)
- ✅ Temporal trend analysis (peak/trough identification)
- ✅ Volatility profile analysis (regime classification)
- ✅ Comparative performance analysis (by fund house/category)
- ✅ Summary statistics generation

**Key Functions:**
```python
analyze_nav_distribution(df)              # Price distribution analysis
analyze_returns_distribution(df)          # Returns patterns & tail risk
analyze_correlation_matrix(df)            # Multicollinearity detection
analyze_temporal_trends(df)               # Time-based patterns
analyze_volatility_profile(df)            # Risk regimes
compare_fund_performance(df)              # Cross-fund comparison
```

### 2. **visualization.py**
Comprehensive visualization functions:
- ✅ Distribution plots (histogram, KDE, Q-Q, box plots)
- ✅ Time series plots (NAV, returns, volatility with moving averages)
- ✅ Returns analysis (histogram, cumulative returns, scatter plots)
- ✅ Correlation heatmap (multicollinearity visualization)
- ✅ Risk-return scatter (efficient frontier analysis)
- ✅ Performance ranking bars (best/worst performers)
- ✅ Category analysis box plots (distribution by fund type)

**Key Functions:**
```python
create_distribution_plots(df)          # 4-panel distribution analysis
create_time_series_plots(df)           # Price trends with MAs
create_returns_analysis_plots(df)      # Return distributions
create_correlation_heatmap(df)         # Correlation matrix viz
create_risk_return_scatter(df)         # Efficient frontier
create_performance_ranking(df)         # Top/bottom performers
create_category_analysis(df)           # Box plots by category
```

### 3. **reporting.py**
Automated report generation:
- ✅ Comprehensive EDA reports (text format)
- ✅ Fund comparison reports
- ✅ Performance ranking reports (top 10 / bottom 10)
- ✅ Risk profile reports (volatility classification)

**Key Functions:**
```python
generate_eda_report(df)                     # Complete EDA summary
generate_fund_comparison_report(df)         # Cross-fund metrics
generate_performance_ranking_report(df)     # Best/worst performers
generate_risk_profile_report(df)            # Risk classification
```

## 🚀 Quick Start

### Step 1: Run EDA Analysis
```bash
python exploratory_analysis.py
```

**Output:**
- NAV distribution statistics
- Returns analysis (VaR, Sharpe ratio, win rates)
- Correlation matrix with high-correlation pair detection
- Temporal trends (peak, trough, total return)
- Volatility regime analysis
- Fund performance comparison

### Step 2: Generate Visualizations
```bash
python visualization.py
```

**Output (saved to `reports/visualizations/`):**
- `nav_distribution.png` - Distribution with histogram, KDE, box plot, Q-Q
- `time_series_analysis.png` - Price trends, returns, volatility
- `returns_analysis.png` - Return distributions & scatter
- `correlation_heatmap.png` - Feature correlation matrix
- `risk_return_scatter.png` - Efficient frontier analysis
- `performance_ranking.png` - Best/worst performer bars
- `category_analysis.png` - Distribution by fund category

### Step 3: Generate Reports
```bash
python reporting.py
```

**Output (saved to `reports/`):**
- `eda_report_*.txt` - Complete statistical summary
- `fund_comparison_report.txt` - Cross-fund metrics
- `performance_ranking_report.txt` - Top/bottom 10 funds
- `risk_profile_report.txt` - Volatility classification

## 📊 Key Metrics Explained

### Distribution Analysis
- **Histogram**: Frequency distribution of values
- **KDE (Kernel Density Estimate)**: Smooth probability density
- **Q-Q Plot**: Normality assessment (straight line = normal)
- **Box Plot**: Outlier detection via interquartile range

### Returns Metrics
- **Win Rate**: % of days with positive returns
- **VaR (Value at Risk, 95%)**: 5th percentile daily loss
- **CVaR (Conditional VaR)**: Average loss on worst 5% days
- **Sharpe-like Ratio**: Mean return / volatility

### Correlation Analysis
- **High Correlation**: |r| > 0.7 indicates redundancy
- **Multicollinearity**: Too many correlated features cause instability
- **Zero Correlation**: Independent variables

### Volatility Regimes
- **Low Vol**: Bottom 25% volatility (stable periods)
- **Mid Vol**: Middle 50% volatility (normal periods)
- **High Vol**: Top 25% volatility (stressed periods)

## 📁 Output Structure

```
reports/
├── eda_report_*.txt
├── fund_comparison_report.txt
├── performance_ranking_report.txt
├── risk_profile_report.txt
└── visualizations/
    ├── nav_distribution.png
    ├── time_series_analysis.png
    ├── returns_analysis.png
    ├── correlation_heatmap.png
    ├── risk_return_scatter.png
    ├── performance_ranking.png
    └── category_analysis.png
```

## 🎯 Analysis Checklist

- [ ] Run exploratory_analysis.py
- [ ] Generate all visualizations
- [ ] Review distribution plots (normality)
- [ ] Analyze correlation matrix (multicollinearity)
- [ ] Examine time series trends
- [ ] Study risk-return scatter (efficient frontier)
- [ ] Rank fund performance
- [ ] Generate all text reports
- [ ] Create executive summary
- [ ] Git commit

## 🔍 Key Questions Answered by EDA

1. **Distribution**: Are returns normally distributed?
2. **Correlation**: Which features are redundant?
3. **Trends**: Which periods show growth vs decline?
4. **Risk**: How volatile is each fund?
5. **Performance**: Which funds outperform?
6. **Regimes**: When are markets stressed?
7. **Outliers**: Are there anomalies in the data?

## 🚨 Common Insights

### Distribution Patterns
- **Positive Skew**: Tail to the right (occasional extreme gains)
- **Negative Skew**: Tail to the left (occasional extreme losses)
- **High Kurtosis**: Fat tails (extreme events more common)

### Correlation Findings
- Moving averages highly correlated (expected)
- Returns metrics somewhat independent
- Volatility metrics cluster together

### Performance Rankings
- Top performers: Consistent growth + low volatility
- Poor performers: High volatility + negative returns
- "Sweet spot": Moderate risk, above-average returns

## 📝 Git Commit

Once all analysis complete:

```bash
git add exploratory_analysis.py visualization.py reporting.py README_DAY3.md
git commit -m "Day 3: Exploratory data analysis complete"
git push origin main
```

## 🎓 Next Steps

**Day 4: Dashboard Development**
- Interactive Plotly dashboards
- Real-time metrics
- Filter/drill-down capabilities
- Fund comparison tools

**Day 5: Reporting & Insights**
- Executive summaries
- Fund recommendations
- Risk alerts
- Performance attribution

## ✅ Day 3 Completion Criteria

- [ ] All 3 Python scripts created and tested
- [ ] EDA functions executed on sample data
- [ ] 7 visualization PNG files generated
- [ ] 4 text reports created
- [ ] Insights documented
- [ ] Git commit pushed
- [ ] README updated

---

**Estimated Time**: 2-3 hours
**Difficulty**: Intermediate
**Prerequisites**: Day 1-2 completion, pandas + matplotlib knowledge
