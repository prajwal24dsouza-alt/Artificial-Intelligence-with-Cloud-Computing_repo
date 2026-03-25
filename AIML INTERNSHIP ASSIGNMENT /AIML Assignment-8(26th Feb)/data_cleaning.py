"""
=============================================================================
 DATA CLEANING ASSIGNMENT
 -------------------------
 This script demonstrates essential data cleaning techniques:
   1. Handling missing values
   2. Removing duplicate rows
   3. Standardizing text (casing, whitespace, categories)
   4. Parsing and standardizing dates
   5. Validating and converting data types

 WHY DATA CLEANING MATTERS:
 --------------------------
 Real-world data is messy. Surveys have blank fields, manual entry introduces
 typos and inconsistent formatting, and system migrations mix date formats.
 If we feed dirty data into analysis or machine-learning models, the results
 will be unreliable — "garbage in, garbage out."

 Specifically:
  • Missing values can bias statistics (e.g., mean salary drops if blanks
    are treated as zero) or crash algorithms that can't handle NaN.
  • Duplicates inflate counts and skew distributions, leading to wrong
    conclusions (e.g., "John Smith generated twice the revenue").
  • Inconsistent text means the same category is split into multiple groups
    (e.g., "Sales", "sales", "SALES" appear as three departments),
    breaking groupby aggregations and visualizations.
  • Mixed date formats make time-series analysis impossible until unified.

 Cleaning is typically 60-80% of a data scientist's work, but it is the
 foundation on which every downstream insight depends.
=============================================================================
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# STEP 0 — LOAD THE RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("STEP 0: LOADING RAW (DIRTY) DATA")
print("=" * 70)

df = pd.read_csv("dirty_data.csv")

print(f"\nShape        : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns      : {list(df.columns)}")
print(f"\nFirst 5 rows:\n{df.head().to_string()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values per column:\n{df.isnull().sum()}")
print(f"Total missing values: {df.isnull().sum().sum()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Keep a copy for the before/after comparison
raw_row_count = df.shape[0]
raw_null_count = df.isnull().sum().sum()
raw_dup_count = df.duplicated().sum()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — REMOVE DUPLICATE ROWS
# ─────────────────────────────────────────────────────────────────────────────
# WHY: Duplicates inflate counts and skew aggregations. For example, a
# duplicated employee row would double-count their salary in a department
# total, producing misleading budget reports.
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 1: REMOVING DUPLICATE ROWS")
print("=" * 70)

print(f"\nRows BEFORE removing duplicates: {len(df)}")
duplicated_rows = df[df.duplicated(keep='first')]
print(f"Duplicate rows found: {len(duplicated_rows)}")
if len(duplicated_rows) > 0:
    print(f"\nDuplicate rows:\n{duplicated_rows.to_string()}")

df = df.drop_duplicates(keep='first').reset_index(drop=True)
print(f"Rows AFTER removing duplicates : {len(df)}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — STANDARDIZE TEXT (WHITESPACE + CASING)
# ─────────────────────────────────────────────────────────────────────────────
# WHY: Without standardization, "New York", "new york", " NEW YORK "
# are treated as three different cities. This breaks groupby operations
# and produces fragmented, incorrect aggregations.
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 2: STANDARDIZING TEXT (WHITESPACE & CASING)")
print("=" * 70)

text_columns = ['Name', 'City', 'Department', 'Email']

print("\nBEFORE standardization (unique values):")
for col in ['City', 'Department']:
    print(f"  {col}: {df[col].dropna().unique().tolist()}")

# Strip leading/trailing whitespace from ALL string columns
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# Standardize Name → Title Case (e.g., "john smith" → "John Smith")
df['Name'] = df['Name'].str.title()

# Standardize City → Title Case
df['City'] = df['City'].str.title()

# Standardize Department → Title Case
df['Department'] = df['Department'].str.title()

# Standardize Email → lowercase (emails are case-insensitive)
df['Email'] = df['Email'].str.lower()

# Replace any 'Nan' strings that arose from converting actual NaN to str
for col in text_columns:
    df[col] = df[col].replace('Nan', np.nan)

print("\nAFTER standardization (unique values):")
for col in ['City', 'Department']:
    print(f"  {col}: {df[col].dropna().unique().tolist()}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — HANDLE MISSING VALUES
# ─────────────────────────────────────────────────────────────────────────────
# WHY: Missing data can cause errors in calculations (mean, sum) and crash
# many ML algorithms. The strategy depends on the column:
#   • Numeric (Age, Salary) → fill with the median (robust to outliers)
#   • Categorical (Department) → fill with the mode (most frequent value)
#   • Dates / identifiers → fill or flag, depending on context
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 3: HANDLING MISSING VALUES")
print("=" * 70)

print(f"\nMissing values BEFORE handling:\n{df.isnull().sum()}")
print(f"Total: {df.isnull().sum().sum()}")

# 3a. Age — fill with median
age_median = df['Age'].median()
print(f"\n  → Filling missing Age with median: {age_median}")
df['Age'] = df['Age'].fillna(age_median).astype(int)

# 3b. Salary — fill with median
salary_median = df['Salary'].median()
print(f"  → Filling missing Salary with median: {salary_median}")
df['Salary'] = df['Salary'].fillna(salary_median).astype(int)

# 3c. Department — fill with mode (most common department)
dept_mode = df['Department'].mode()[0]
print(f"  → Filling missing Department with mode: '{dept_mode}'")
df['Department'] = df['Department'].fillna(dept_mode)

# 3d. Join_Date — fill with a placeholder or leave; here we fill with 'Unknown'
print(f"  → Filling missing Join_Date with 'Unknown'")
df['Join_Date'] = df['Join_Date'].fillna('Unknown')

print(f"\nMissing values AFTER handling:\n{df.isnull().sum()}")
print(f"Total: {df.isnull().sum().sum()}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — STANDARDIZE DATE FORMATS
# ─────────────────────────────────────────────────────────────────────────────
# WHY: Mixed formats like "2023-01-15" and "15/02/2023" prevent sorting,
# time-series analysis, and date arithmetic. We unify them to YYYY-MM-DD.
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 4: STANDARDIZING DATE FORMATS")
print("=" * 70)

print(f"\nJoin_Date values BEFORE:\n{df['Join_Date'].unique().tolist()}")

def parse_date(val):
    """Try to parse a date string; return standardized format or 'Unknown'."""
    if val == 'Unknown':
        return val
    try:
        # Try ISO format (YYYY-MM-DD) first to avoid ambiguity
        return pd.to_datetime(val, format='%Y-%m-%d').strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        pass
    try:
        # Then try DD/MM/YYYY format
        return pd.to_datetime(val, format='%d/%m/%Y').strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return 'Unknown'

df['Join_Date'] = df['Join_Date'].apply(parse_date)

print(f"Join_Date values AFTER :\n{df['Join_Date'].unique().tolist()}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — VALIDATE DATA TYPES
# ─────────────────────────────────────────────────────────────────────────────
# WHY: Ensuring correct dtypes prevents subtle bugs — e.g., if Age is stored
# as a string, "28" + "34" = "2834" instead of 62.
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 5: VALIDATING DATA TYPES")
print("=" * 70)

df['Age'] = df['Age'].astype(int)
df['Salary'] = df['Salary'].astype(int)

print(f"\nFinal data types:\n{df.dtypes}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — EXPORT CLEANED DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 6: EXPORTING CLEANED DATA")
print("=" * 70)

df.to_csv("cleaned_data.csv", index=False)
print("\n✅ Cleaned data saved to 'cleaned_data.csv'")

# ─────────────────────────────────────────────────────────────────────────────
# BEFORE / AFTER SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("BEFORE / AFTER SUMMARY")
print("=" * 70)

print(f"""
  Metric                  BEFORE      AFTER
  ─────────────────────   ─────────   ─────────
  Total rows              {raw_row_count:<11} {len(df)}
  Duplicate rows          {raw_dup_count:<11} {df.duplicated().sum()}
  Total missing values    {raw_null_count:<11} {df.isnull().sum().sum()}
  Unique cities           see above   {df['City'].nunique()}
  Unique departments      see above   {df['Department'].nunique()}
""")

print("Cleaned dataset preview (first 10 rows):")
print(df.head(10).to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# WHY DATA CLEANING MATTERS — RECAP
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("WHY DATA CLEANING MATTERS — KEY TAKEAWAYS")
print("=" * 70)
print("""
1. ACCURACY    — Dirty data leads to wrong statistics, misleading charts,
                 and flawed business decisions.

2. CONSISTENCY — Standardized text ensures groupby, joins, and filters
                 work correctly (e.g., one "Sales" group, not three).

3. COMPLETENESS — Handling missing values prevents NaN errors and ensures
                  every record is usable in analysis and ML models.

4. RELIABILITY — Removing duplicates stops inflated counts and ensures
                 each entity is represented exactly once.

5. EFFICIENCY  — Clean data requires less post-hoc debugging, making
                 downstream analysis faster and more trustworthy.

In practice, data cleaning consumes 60-80% of a data project's time,
but it is the single most important step for producing reliable insights.
""")
