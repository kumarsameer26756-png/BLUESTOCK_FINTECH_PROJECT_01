# BlueStock FinTech Project 01 - Day 1: Data Ingestion

This project implements a production-ready data ingestion pipeline for analyzing Indian mutual funds using AMFI scheme codes and live NAV data.

## 📁 Project Structure

```
BLUESTOCK_FINTECH_PROJECT_01/
├── data/
│   ├── raw/              # Raw CSV datasets and live API fetches
│   └── processed/        # Cleaned and transformed data
├── notebooks/            # Jupyter notebooks for exploration
├── sql/                  # SQL queries for database operations
├── dashboard/            # Dashboard configuration files
├── reports/              # Generated reports and analysis
├── data_ingestion.py     # Load and validate 10 CSV datasets
├── live_nav_fetch.py     # Fetch live NAV from mfapi.in
├── requirements.txt      # Python dependencies
├── .gitignore           # Exclude data/ and environment files
└── README.md            # This file
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Place your 10 CSV datasets in `data/raw/` directory:
- `fund_master.csv` - Scheme metadata (fund house, category, risk grade)
- `nav_history.csv` - Historical NAV data
- 8 additional datasets (adjust paths in `data_ingestion.py` as needed)

### 3. Run Data Ingestion Pipeline

**Phase 1: Load & Profile Local Datasets**
```bash
python data_ingestion.py
```

This will:
- ✅ Load all CSV files from `data/raw/`
- ✅ Print shape, data types, and first 3 rows for each dataset
- ✅ Detect missing values and duplicate rows
- ✅ Validate AMFI scheme code referential integrity

**Phase 2: Fetch Live NAV Data**
```bash
python live_nav_fetch.py
```

This will:
- ✅ Fetch HDFC Top 100 Direct (125497) from mfapi.in
- ✅ Fetch 5 key Large Cap schemes:
  - SBI Bluechip (119551)
  - ICICI Bluechip (120503)
  - Nippon Large Cap (118632)
  - Axis Bluechip (119092)
  - Kotak Bluechip (120841)
- ✅ Parse JSON responses and save as raw CSVs

## 📊 Key Features

### AMFI Scheme Code Validation
- Unique 6-digit numeric identifiers assigned by Association of Mutual Funds in India
- Master data maps codes to structural metadata (fund house, category, sub-category, risk grade)
- Historical tables map codes to time-series NAV data
- Referential integrity checks ensure every scheme in master exists in history

### Data Quality Validation
- Missing value detection
- Duplicate row identification
- Structural anomaly reporting
- Referential integrity validation across datasets

### Live Data Integration
- Real-time NAV fetching from mfapi.in
- Automatic CSV export
- Metadata enrichment with scheme codes and names

## 📋 Dependencies

| Package | Version |
|---------|----------|
| pandas | 2.2.2 |
| numpy | 1.26.4 |
| matplotlib | 3.8.4 |
| seaborn | 0.13.2 |
| plotly | 5.22.0 |
| sqlalchemy | 2.0.30 |
| requests | 2.32.2 |
| scipy | 1.13.0 |
| jupyter | 1.0.0 |

## 🔍 Expected Outputs

After running the pipeline, you'll have:

1. **Profiling reports** - Dataset metadata and anomalies
2. **CSV files** - Live NAV data in `data/raw/`:
   - `nav_hdfc_top_100_direct.csv`
   - `nav_sbi_bluechip.csv`
   - `nav_icici_bluechip.csv`
   - `nav_nippon_large_cap.csv`
   - `nav_axis_bluechip.csv`
   - `nav_kotak_bluechip.csv`
3. **Validation summary** - AMFI code integrity and data quality metrics

## 📝 Git Workflow

Initial setup:
```bash
git clone https://github.com/kumarsameer26756-png/BLUESTOCK_FINTECH_PROJECT_01.git
cd BLUESTOCK_FINTECH_PROJECT_01
pip install -r requirements.txt
```

## ⚙️ Configuration

Edit these scripts to customize:

**data_ingestion.py**
- Update `target_csvs` list with your actual dataset paths
- Adjust column name matching for scheme codes if needed

**live_nav_fetch.py**
- Modify `target_schemes` dictionary to fetch different schemes
- Adjust timeout (currently 15 seconds) if needed

## 🛠️ Troubleshooting

**Files not found**: Ensure CSV files are placed in `data/raw/` directory

**API errors**: mfapi.in may have rate limiting. Add delays between requests if needed.

**Column mismatch**: If your CSV headers differ from expected names, update column matching in validation functions.

## 📖 Next Steps

- Day 2: Data Transformation & Cleaning
- Day 3: Feature Engineering & Analysis
- Day 4: Dashboard Development
- Day 5: Reporting & Insights

## 📄 License

This project is part of the BlueStock FinTech initiative for mutual fund analysis.

---

**Created**: June 2, 2026  
**Author**: kumarsameer26756-png  
**Repository**: BLUESTOCK_FINTECH_PROJECT_01
