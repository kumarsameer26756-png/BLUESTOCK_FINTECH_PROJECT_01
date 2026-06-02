# Day 3: Exploratory Data Analysis (EDA)

## 📋 Overview

Day 3 focuses on understanding data patterns, distributions, correlations, and generating actionable insights through comprehensive analysis and visualization.

---

## 🎯 Objectives

1. ✅ Analyze NAV distribution patterns
2. ✅ Study returns distributions & tail risk
3. ✅ Calculate correlations & detect multicollinearity
4. ✅ Identify temporal trends (peaks, troughs, growth)
5. ✅ Classify volatility regimes (low/medium/high)
6. ✅ Compare fund performance across categories
7. ✅ Generate 7 publication-quality visualizations
8. ✅ Produce 4 comprehensive text reports

---

## 📁 New Files Created

### 1. **exploratory_analysis.py** - Statistical Analysis ✨

**7 Core Functions:**

1. **`analyze_nav_distribution(df, price_col='nav', dataset_name='NAV Data')`**
   - Distribution statistics (mean, median, std, skewness, kurtosis)
   - Normality test (Shapiro-Wilk with p-value)
   - Quartile analysis
   - Min/max/range reporting

2. **`analyze_returns_distribution(df, return_col='simple_return_1d', dataset_name='Returns Data')`**
   - Return statistics (mean, median, std, skewness, kurtosis)
   - Value at Risk (VaR 95%) - 5th percentile daily loss
   - Conditional VaR - average loss on worst 5% days
   - Sharpe-like ratio - mean return / volatility
   - Win/loss rate analysis

3. **`analyze_correlation_matrix(df, numeric_cols=None, dataset_name='Dataset')`**
   - Correlation matrix generation
   - High correlation pair detection (|r| > 0.7)
   - Multicollinearity flagging

4. **`analyze_temporal_trends(df, date_col='date', price_col='nav', dataset_name='NAV')`**
   - Time period coverage
   - Start/end price analysis
   - Total return calculation
   - Peak/trough identification with dates
   - CAGR (Compound Annual Growth Rate)

5. **`analyze_volatility_profile(df, volatility_col='volatility_30d', dataset_name='Volatility')`**
   - Volatility statistics
   - Regime classification (low/medium/high)
   - Percentile analysis (25th, 50th, 75th)

6. **`compare_fund_performance(df, group_col='fund_house', metric_col='simple_return_365d')`**
   - Cross-fund metrics
   - Count, mean, median, std, min, max
   - By fund house or category

7. **`generate_summary_statistics(df, dataset_name='Dataset')`**
   - Comprehensive numeric summary
   - Descriptive statistics export

---

### 2. **visualization.py** - Publication-Quality Charts ✨

**7 Visualization Functions:**

1. **`create_distribution_plots(df, price_col='nav')`**
   - 4-panel plot: histogram, KDE, box plot, Q-Q
   - Output: `nav_distribution.png`

2. **`create_time_series_plots(df, date_col='date', price_col='nav')`**
   - 3-panel plot: NAV price, returns, volatility
   - Trend visualization
   - Output: `time_series_analysis.png`

3. **`create_returns_analysis_plots(df)`**
   - 4-panel plot: histogram, cumulative, rolling mean, scatter
   - Output: `returns_analysis.png`

4. **`create_correlation_heatmap(df)`**
   - Correlation matrix visualization
   - Color-coded (-1 to +1)
   - Output: `correlation_heatmap.png`

5. **`create_risk_return_scatter(df)`**
   - Efficient frontier plot
   - Risk vs return positioning
   - Fund labels
   - Output: `risk_return_scatter.png`

6. **`create_performance_ranking(df, metric_col='simple_return_365d')`**
   - Horizontal bar chart (top/bottom performers)
   - Color-coded (green/red for positive/negative)
   - Output: `performance_ranking.png`

7. **`create_category_analysis(df, category_col='category')`**
   - Box plots by category
   - Distribution visualization
   - Output: `category_analysis.png`

---

### 3. **reporting.py** - Automated Report Generation ✨

**4 Report Functions:**

1. **`generate_eda_report(df, dataset_name='Dataset')`**
   - Complete statistical summary
   - Data types, descriptive stats
   - Missing values, duplicates
   - Correlation matrix
   - Categorical summaries

2. **`generate_fund_comparison_report(df, group_col='fund_house')`**
   - Cross-fund metrics
   - Performance by fund house
   - Statistical comparison

3. **`generate_performance_ranking_report(df, metric_col='simple_return_365d', top_n=10)`**
   - Top 10 best performers
   - Bottom 10 worst performers
   - Ranked list with metrics

4. **`generate_risk_profile_report(df, volatility_col='volatility_30d')`**
   - Volatility statistics
   - Risk classification
   - Quartile analysis
   - Low/medium/high risk distribution

---

### 4. **README_DAY3.md** - Complete Documentation

- Overview & objectives
- Function reference (all 18+ functions)
- Step-by-step execution guide
- Output structure
- Visualization explanations
- Key metrics definitions
- Git workflow
- Checklist

---

## 🚀 Quick Execution

```bash
# Step 1: Run exploratory analysis
python exploratory_analysis.py
# Output: Console statistics for all 7 analyses

# Step 2: Generate all visualizations
python visualization.py
# Output: 7 PNG files in reports/visualizations/

# Step 3: Generate all text reports
python reporting.py
# Output: 4 text files in reports/

# Step 4: Review outputs
ls -lh reports/
ls -lh reports/visualizations/

# Step 5: Commit to Git
git add exploratory_analysis.py visualization.py reporting.py README_DAY3.md
git commit -m "Day 3: Exploratory data analysis complete"
git push origin main
```

---

## 📊 Output Files

### Visualizations (reports/visualizations/)
```
✅ nav_distribution.png              # 4-panel distribution analysis
✅ time_series_analysis.png          # Price, returns, volatility trends
✅ returns_analysis.png              # Return distributions & correlations
✅ correlation_heatmap.png           # Feature correlation matrix
✅ risk_return_scatter.png           # Efficient frontier
✅ performance_ranking.png           # Top/bottom performers
✅ category_analysis.png             # Distribution by category
```

### Reports (reports/)
```
✅ eda_report_*.txt                  # Complete statistical summary
✅ fund_comparison_report.txt        # Cross-fund metrics
✅ performance_ranking_report.txt    # Top/bottom 10 rankings
✅ risk_profile_report.txt           # Volatility classification
```

---

## 🎯 Key Metrics Explained

### Distribution Analysis
- **Histogram**: Frequency distribution of values
- **KDE (Kernel Density Estimate)**: Smooth probability density
- **Q-Q Plot**: Normality assessment (straight line = normal)
- **Box Plot**: Outlier detection via IQR
- **Shapiro-Wilk Test**: p > 0.05 = normally distributed

### Returns Metrics
- **Win Rate**: % of days with positive returns
- **VaR (95%)**: Worst 5th percentile daily loss
- **CVaR**: Average loss on worst 5% days
- **Sharpe Ratio**: (Mean Return - Risk-Free Rate) / Volatility

### Correlation
- **High Correlation**: |r| > 0.7 (redundant features)
- **Moderate**: 0.3 < |r| < 0.7
- **Low**: |r| < 0.3 (independent)

### Volatility Regimes
- **Low**: Bottom 25% volatility
- **Medium**: Middle 50% volatility
- **High**: Top 25% volatility

---

## ✅ Day 3 Checklist

- [ ] exploratory_analysis.py created and tested
- [ ] visualization.py created and tested
- [ ] reporting.py created and tested
- [ ] All 7 visualizations generated
- [ ] All 4 reports generated
- [ ] README_DAY3.md created
- [ ] All files reviewed
- [ ] Git commit created
- [ ] Push to main branch

---

## 📈 Project Progress

```
Day 1: Data Ingestion              ✅ COMPLETE
Day 2: Transformation & Cleaning   ✅ COMPLETE
Day 3: EDA & Reporting             ✅ COMPLETE (TODAY)
Day 4: Dashboard Development       ⏳ UPCOMING
Day 5: Final Insights              ⏳ UPCOMING
```

---

**Estimated Time**: 2-3 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Days 1-2 complete, pandas + matplotlib knowledge
