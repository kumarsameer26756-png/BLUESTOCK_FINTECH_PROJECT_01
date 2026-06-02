# Day 2: Data Transformation & Cleaning

## 🎯 Overview

Day 2 focuses on preparing raw data for analysis through systematic transformation, cleaning, and feature engineering.

## 📁 New Files Created

### 1. **data_transformation.py**
Core data type standardization and formatting:
- ✅ Data type conversion (datetime, float, int, category)
- ✅ Date format normalization (ISO 8601: YYYY-MM-DD)
- ✅ Numeric range validation
- ✅ Categorical variable encoding
- ✅ Schema-based transformation

**Key Functions:**
```python
standardize_data_types(df)          # Convert to optimal types
normalize_date_formats(df)          # Ensure consistent dates
validate_numeric_ranges(df)         # Check numeric bounds
encode_categorical_variables(df)    # Prepare categorical data
```

### 2. **data_cleaning.py**
Data quality assurance and anomaly handling:
- ✅ Missing value handling (median fill for numeric, mode for categorical)
- ✅ Duplicate record removal
- ✅ Outlier detection (IQR and Z-score methods)
- ✅ Anomaly flagging (negative NAV, future dates, large jumps)
- ✅ Data quality reporting

**Key Functions:**
```python
handle_missing_values(df, strategy='auto')  # Fill missing data
detect_outliers(df, method='iqr')          # Find outliers
remove_duplicate_records(df)                # Remove duplicates
flag_anomalies(df)                         # Flag data issues
```

### 3. **feature_engineering.py**
Derive meaningful features for analysis:
- ✅ Return calculations (simple & log returns for 1, 7, 30, 365 days)
- ✅ Moving averages (7, 30, 90, 365-day windows)
- ✅ Volatility metrics (rolling standard deviation)
- ✅ Sharpe Ratio (risk-adjusted returns)
- ✅ Drawdown analysis (peak-to-trough declines)
- ✅ Performance metrics (CAGR, total return, max drawdown)
- ✅ Fund metadata enrichment

**Key Functions:**
```python
calculate_returns(df, periods=[1, 7, 30, 365])           # Daily/weekly/monthly/annual returns
calculate_moving_averages(df, windows=[7, 30, 90, 365]) # Trend indicators
calculate_volatility(df, windows=[7, 30, 90])           # Risk metrics
calculate_sharpe_ratio(df, risk_free_rate=6.0)          # Risk-adjusted performance
calculate_drawdown(df)                                  # Peak-to-trough analysis
```

### 4. **data_quality_report.py**
Comprehensive data profiling and validation:
- ✅ Basic metadata (shape, memory, data types)
- ✅ Missing value analysis
- ✅ Duplicate detection
- ✅ Numeric column statistics (mean, std, skewness, kurtosis)
- ✅ Categorical distribution analysis
- ✅ Before/after comparison reports

**Key Functions:**
```python
generate_data_profiling_report(df)           # Complete profiling
generate_before_after_report(df_orig, df_processed)  # Quality improvement
save_quality_report(report)                  # Export report
```

## 🚀 Quick Start

### Step 1: Install Dependencies (if not done on Day 1)
```bash
pip install -r requirements.txt
```

### Step 2: Create Directory Structure
```bash
mkdir -p data/raw data/processed notebooks sql dashboard reports
```

### Step 3: Run Transformation Pipeline
```bash
python data_transformation.py
```

**Output:**
- Data types converted
- Dates normalized to ISO 8601
- Categorical variables encoded
- Processed files saved to `data/processed/`

### Step 4: Run Cleaning Pipeline
```bash
python data_cleaning.py
```

**Output:**
- Missing values filled/removed
- Duplicates removed
- Outliers detected and flagged
- Anomalies documented

### Step 5: Run Feature Engineering
```bash
python feature_engineering.py
```

**Output:**
- Daily, weekly, monthly, annual returns calculated
- 4 moving averages created (7, 30, 90, 365-day)
- 3 volatility windows (7, 30, 90-day)
- Sharpe Ratio computed
- Drawdown metrics calculated
- Performance aggregates (CAGR, total return, max drawdown)

### Step 6: Generate Quality Reports
```bash
python data_quality_report.py
```

**Output:**
- Comprehensive profiling report
- Before/after comparison
- Data quality score improvement
- Issues and anomalies documented

## 📊 Data Transformation Flow

```
Raw Data (data/raw/)
    ↓
[data_transformation.py]
  - Type standardization
  - Date normalization
  - Range validation
    ↓
Intermediate Data
    ↓
[data_cleaning.py]
  - Missing value handling
  - Duplicate removal
  - Outlier detection
  - Anomaly flagging
    ↓
Cleaned Data
    ↓
[feature_engineering.py]
  - Returns calculation
  - Moving averages
  - Volatility metrics
  - Sharpe Ratio
  - Drawdown analysis
    ↓
Enriched Data (data/processed/)
    ↓
[data_quality_report.py]
  - Profiling
  - Before/after comparison
  - Quality metrics
    ↓
Quality Reports (reports/)
```

## 📈 Key Metrics Explained

### Returns
- **Simple Return**: (Price_t - Price_t-n) / Price_t-n × 100
- **Log Return**: ln(Price_t / Price_t-n) × 100
- Calculated for 1, 7, 30, and 365-day periods

### Moving Averages (MA)
- **7-day MA**: Trend over 1 week
- **30-day MA**: Trend over 1 month
- **90-day MA**: Trend over 3 months
- **365-day MA**: Trend over 1 year

### Volatility
- **Rolling Volatility**: Standard deviation of returns
- **Annualized**: Volatility × √252 (trading days)
- Calculated for 7, 30, and 90-day windows

### Sharpe Ratio
- **Formula**: (Mean Return - Risk-Free Rate) / Volatility
- Risk-adjusted performance metric
- Higher = Better risk-adjusted returns
- Assumes 6% annual risk-free rate (adjustable)

### Drawdown
- **Drawdown**: (Current Price - Peak Price) / Peak Price
- Measures peak-to-trough decline
- **Max Drawdown**: Largest decline from any peak
- Indicates downside risk

### CAGR (Compound Annual Growth Rate)
- **Formula**: (Ending Value / Beginning Value)^(1/Years) - 1
- Annualized return over entire period
- Accounts for compounding

## 🔍 Data Quality Checks

### Before Processing
- ❓ Missing values per column
- 🔄 Duplicate records
- 📊 Data type mismatches
- 📅 Invalid date formats
- 📈 Out-of-range numeric values

### After Processing
- ✅ All data types standardized
- ✅ Missing values < 1% (or imputed)
- ✅ No duplicate records
- ✅ Consistent date formats
- ✅ Anomalies flagged and documented
- ✅ 100+ derived features ready for analysis

## 💾 Output Files

All processed data saved to `data/processed/`:

```
data/processed/
├── fund_master_transformed.csv        # Cleaned fund metadata
├── nav_history_transformed.csv        # Cleaned NAV data
├── nav_hdfc_top_100_direct_features.csv    # With features
├── nav_sbi_bluechip_features.csv           # With features
├── nav_icici_bluechip_features.csv         # With features
├── nav_nippon_large_cap_features.csv       # With features
├── nav_axis_bluechip_features.csv          # With features
└── nav_kotak_bluechip_features.csv         # With features

reports/
└── data_quality_report.txt             # Profiling & comparison
```

## 🎯 Quality Metrics

After Day 2, you should have:
- ✅ **Data Completeness**: >99% (missing values < 1%)
- ✅ **Duplication**: 0% (all duplicates removed)
- ✅ **Type Consistency**: 100% (all columns properly typed)
- ✅ **Feature Count**: 30+ derived features per scheme
- ✅ **Date Coverage**: Continuous daily/periodic data
- ✅ **Anomaly Flags**: All data quality issues documented

## 🚨 Common Issues & Fixes

### Issue: "Memory Error on Large Datasets"
**Fix**: Process datasets in chunks or use `data.sample()`

### Issue: "Date Parsing Errors"
**Fix**: Adjust `pd.to_datetime()` with `format` parameter:
```python
pd.to_datetime(df['date'], format='%d-%m-%Y')
```

### Issue: "Too Many/Few Outliers Detected"
**Fix**: Adjust IQR multiplier (1.5 default) or Z-score threshold (3.0 default)

### Issue: "Missing Features Not Appearing"
**Fix**: Ensure date sorting: `df.sort_values('date')`

## 📝 Git Commit

Once all scripts execute successfully:

```bash
git add data_transformation.py data_cleaning.py feature_engineering.py data_quality_report.py
git commit -m "Day 2: Data transformation and cleaning complete"
git push origin main
```

## 📖 Next Steps

**Day 3: Exploratory Data Analysis (EDA)**
- Distribution analysis
- Correlation studies
- Segmentation by fund house & category
- Performance ranking
- Risk profiling

## ✅ Day 2 Checklist

- [ ] All 4 scripts created and tested
- [ ] Data transformation pipeline executed
- [ ] Cleaning pipeline executed
- [ ] Features engineered for all datasets
- [ ] Quality reports generated
- [ ] All processed files saved to `data/processed/`
- [ ] Git commit created
- [ ] README updated with Day 2 info

---

**Estimated Time**: 2-3 hours (depending on dataset size)
**Difficulty**: Intermediate
**Prerequisites**: Day 1 completion, pandas knowledge
