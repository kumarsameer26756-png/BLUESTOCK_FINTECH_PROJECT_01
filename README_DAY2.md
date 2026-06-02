# Day 2: Data Transformation & Cleaning - Comprehensive Guide

## 📋 Overview

Day 2 focuses on preparing raw data for analysis through systematic transformation, cleaning, and validation.

### Objectives
1. ✅ Standardize data types across all datasets
2. ✅ Normalize date formats to ISO 8601
3. ✅ Validate numeric ranges
4. ✅ Handle missing values intelligently
5. ✅ Detect and flag outliers
6. ✅ Remove duplicate records
7. ✅ Flag data anomalies
8. ✅ Generate comprehensive cleaning reports

---

## 📁 New Files Created

### 1. **data_transformation.py** - Type & Format Standardization

**Functions:**

#### `standardize_data_types(df, schema_config=None)`
Converts columns to optimal types:
- **Datetime**: Columns with 'date', 'nav_date', 'transaction_date' keywords
- **Float**: 'nav', 'price', 'value', 'return', 'aum', 'expense_ratio'
- **Integer**: 'scheme_code', 'isin', 'holding_count', 'units'
- **Category**: 'fund_house', 'category', 'risk_grade', 'scheme_name', 'status'

**Output:**
```
PHASE 1: DATA TYPE STANDARDIZATION
✅ scheme_code              → Int64
✅ fund_house               → category
✅ date                     → datetime64[ns]
✅ nav                      → float64
✅ expense_ratio            → float64

📊 Transformation Summary:
  Datetime columns:     1
  Float columns:        2
  Integer columns:      1
  Category columns:     2
  Failed conversions:   0
```

#### `normalize_date_formats(df, date_columns=None)`
Converts all dates to ISO 8601 format (YYYY-MM-DD)

**Output:**
```
PHASE 2: DATE FORMAT NORMALIZATION
✅ date                     normalized to YYYY-MM-DD
   Min date: 2020-01-01
   Max date: 2024-12-31
```

#### `validate_numeric_ranges(df, numeric_columns=None)`
Validates ranges and flags anomalies

**Output:**
```
PHASE 3: NUMERIC RANGE VALIDATION
📈 Column: nav
   Range:   [50.000000, 500.000000]
   Stats:   Mean=250.123456, Std=120.456789
   Quality: 0 nulls, 0 negatives
```

#### `encode_categorical_variables(df, categorical_columns=None)`
Creates label encodings for categorical columns

**Output:**
```
PHASE 4: CATEGORICAL VARIABLE ENCODING
📂 Column: fund_house
   Unique values: 10
   Values: ['SBI', 'ICICI', 'Nippon', ...]
   ✅ Label encoding created
```

---

### 2. **data_cleaning.py** - Quality Assurance & Anomaly Handling

**Functions:**

#### `handle_missing_values(df, strategy='auto', threshold=0.5)`
Fills missing values intelligently:
- **Datetime**: Forward fill
- **Numeric**: Median fill
- **Categorical**: Mode fill
- **Drops columns** with >50% missing

**Output:**
```
PHASE 1: MISSING VALUE HANDLING
📊 Missing Value Summary:
Total missing values: 150

❌ expense_ratio         → 75.00% missing (DROPPED)

📝 Filling remaining missing values...
✅ nav                  → Median fill: 250.5000 (25 values)
✅ fund_house           → Mode fill: SBI (5 values)

✅ Remaining missing values: 0
```

#### `detect_outliers(df, numeric_columns=None, method='iqr', threshold=1.5)`
Detects outliers using IQR (default) or Z-score methods

**Output:**
```
PHASE 2: OUTLIER DETECTION
🔍 Detecting outliers using IQR method...

✅ nav                 → No outliers detected
⚠️  expense_ratio      → 5 outliers (2.50%)
    Bounds: [0.1000, 1.5000]
```

#### `remove_duplicate_records(df, subset=None, keep='first')`
Removes exact duplicate rows

**Output:**
```
PHASE 3: DUPLICATE RECORD REMOVAL
🔄 Deduplication Summary:
Initial rows:         10,000
Duplicate rows:       125 (1.25%)
Final rows:           9,875

✅ Removed 125 duplicate records
```

#### `flag_anomalies(df, numeric_columns=None)`
Flags data quality issues:
- Negative NAV values
- Future dates
- Large jumps (>20%)

**Output:**
```
PHASE 4: ANOMALY FLAGGING
⚠️  Negative NAV detected: 2 records
⚠️  Large NAV jumps (>20%): 5 records

🚩 Total anomaly flags set: 7
```

---

## 🚀 Execution Guide

### Prerequisites
```bash
# Ensure Day 1 is complete
ls -la data/raw/
# Should show fund_master.csv, nav_history.csv, + 8 more files
# Plus 6 nav_*.csv files from live_nav_fetch.py
```

### Step 1: Run Data Transformation
```bash
python data_transformation.py
```

**Expected Output:**
- All columns converted to optimal types
- Dates normalized to ISO 8601
- Categorical encodings created
- Detailed transformation summary

### Step 2: Run Data Cleaning
```bash
python data_cleaning.py
```

**Expected Output:**
- Missing values filled/removed
- Outliers detected and reported
- Duplicates removed
- Anomalies flagged
- Data quality improvement summary

### Step 3: Process All Day 1 Output Files
Create a batch processing script:

```bash
# Create process_day2.py to apply to all data/raw/*.csv files
for file in data/raw/*.csv; do
    echo "Processing $file"
    python -c "import pandas as pd; import data_transformation as dt; df = pd.read_csv('$file'); df_t = dt.standardize_data_types(df); df_t.to_csv('data/processed/$(basename $file .csv)_transformed.csv', index=False)"
done
```

---

## 📊 Data Quality Metrics

### Before Day 2
- ❓ Data type mismatches
- ❓ Inconsistent date formats
- ❓ Missing values (unknown handling)
- ❓ Potential duplicates
- ❓ Unexplained anomalies

### After Day 2
- ✅ All types standardized
- ✅ Dates in ISO 8601 format
- ✅ Missing values: <1% (imputed)
- ✅ Duplicates: 0%
- ✅ Anomalies: Flagged and documented
- ✅ Data Completeness: >99%

---

## 🔧 Configuration

### Customize Data Type Schema

```python
from data_transformation import standardize_data_types

custom_schema = {
    'date': ['date', 'nav_date', 'your_date_col'],
    'float': ['nav', 'price', 'your_numeric_col'],
    'int': ['scheme_code', 'your_int_col'],
    'category': ['fund_house', 'your_category_col']
}

df_transformed = standardize_data_types(df, schema_config=custom_schema)
```

### Adjust Missing Value Strategy

```python
from data_cleaning import handle_missing_values

# Drop columns with >70% missing (default is 50%)
df_cleaned = handle_missing_values(df, threshold=0.70)
```

### Configure Outlier Detection

```python
from data_cleaning import detect_outliers

# Use Z-score method with threshold of 2.5
outliers = detect_outliers(df, method='zscore', threshold=2.5)
```

---

## 📁 Output Structure

```
data/processed/
├── fund_master_transformed.csv
├── nav_history_transformed.csv
├── dataset3_transformed.csv
├── dataset4_transformed.csv
├── ...
├── nav_hdfc_top_100_direct_transformed.csv
├── nav_sbi_bluechip_transformed.csv
├── nav_icici_bluechip_transformed.csv
├── nav_nippon_large_cap_transformed.csv
├── nav_axis_bluechip_transformed.csv
└── nav_kotak_bluechip_transformed.csv
```

---

## ✅ Day 2 Checklist

- [ ] requirements.txt contains all dependencies
- [ ] data_transformation.py created and tested
- [ ] data_cleaning.py created and tested
- [ ] All data/raw/*.csv files accessible
- [ ] data_transformation.py runs successfully
- [ ] data_cleaning.py runs successfully
- [ ] All transformed files in data/processed/
- [ ] Data quality report generated
- [ ] Git commit created: "Day 2: Data transformation and cleaning complete"
- [ ] Push to main branch

---

## 🎯 Performance Notes

- **Memory Usage**: Pipeline works with up to 1GB datasets
- **Processing Time**: ~1-2 minutes for 100K rows
- **Scalability**: Can process in chunks for larger files

---

## 📝 Git Workflow

```bash
# Stage files
git add data_transformation.py data_cleaning.py README_DAY2.md

# Commit
git commit -m "Day 2: Data transformation and cleaning complete"

# Push to main
git push origin main
```

---

## 🔗 Repository Status

**Current Branch**: `main`
**Previous Commits**:
- Day 1 enhancements (data_ingestion.py, live_nav_fetch.py)

**Next**: Day 3 - Exploratory Data Analysis

---

**Estimated Time**: 1-2 hours  
**Difficulty**: Beginner  
**Prerequisites**: Day 1 complete, Python 3.8+, pandas
