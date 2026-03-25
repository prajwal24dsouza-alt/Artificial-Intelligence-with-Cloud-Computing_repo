"""
Dataset Analysis Script
========================
This script loads the Titanic dataset, displays the top rows,
finds the column with the highest value, counts missing values,
and shares 5 key insights from the data.
"""

import pandas as pd
import numpy as np
import ssl
import urllib.request
from io import StringIO

# ================================================================
# 1. LOAD THE DATASET
# ================================================================
print("=" * 70)
print("STEP 1: LOADING THE DATASET")
print("=" * 70)

# Load Titanic dataset from a public URL (with SSL workaround)
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib.request.urlopen(url, context=ctx)
csv_data = response.read().decode("utf-8")
df = pd.read_csv(StringIO(csv_data))

print(f"\n Dataset loaded successfully!")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Columns: {list(df.columns)}")

# ================================================================
# 2. DISPLAY TOP ROWS
# ================================================================
print("\n" + "=" * 70)
print("STEP 2: DISPLAYING TOP 5 ROWS")
print("=" * 70)

print(df.head().to_string())

print("\n--- Data Types ---")
print(df.dtypes.to_string())

# ================================================================
# 3. FIND THE COLUMN WITH THE HIGHEST VALUE
# ================================================================
print("\n" + "=" * 70)
print("STEP 3: FINDING THE COLUMN WITH THE HIGHEST VALUE")
print("=" * 70)

# Select only numeric columns
numeric_cols = df.select_dtypes(include=[np.number])

# Find the max value in each numeric column
max_values = numeric_cols.max()
print("\nMaximum value in each numeric column:")
print(max_values.to_string())

# Find which column has the overall highest value
highest_col = max_values.idxmax()
highest_val = max_values.max()

print(f"\n Column with the highest value: '{highest_col}' (max = {highest_val})")

# ================================================================
# 4. COUNT MISSING VALUES
# ================================================================
print("\n" + "=" * 70)
print("STEP 4: COUNTING MISSING VALUES")
print("=" * 70)

missing_counts = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df) * 100).round(2)

missing_df = pd.DataFrame({
    "Missing Count": missing_counts,
    "Missing %": missing_percent
})

print(missing_df.to_string())

total_missing = df.isnull().sum().sum()
total_cells = df.shape[0] * df.shape[1]
print(f"\n Total missing values: {total_missing} out of {total_cells} cells "
      f"({(total_missing / total_cells * 100):.2f}%)")

# ================================================================
# 5. FIVE KEY INSIGHTS FROM THE DATA
# ================================================================
print("\n" + "=" * 70)
print("STEP 5: FIVE KEY INSIGHTS")
print("=" * 70)

# Insight 1: Survival rate
survival_rate = df["Survived"].mean() * 100
print(f"\n Insight 1 — Overall Survival Rate")
print(f"   Only {survival_rate:.1f}% of passengers survived the Titanic disaster.")
print(f"   That means {100 - survival_rate:.1f}% of passengers did not survive.")

# Insight 2: Survival by gender
survival_by_gender = df.groupby("Sex")["Survived"].mean() * 100
print(f"\n Insight 2 — Survival Rate by Gender")
for gender, rate in survival_by_gender.items():
    print(f"   {gender.capitalize()}: {rate:.1f}% survived")
print(f"   Women had a significantly higher survival rate than men,")
print(f"   consistent with the 'women and children first' policy.")

# Insight 3: Survival by passenger class
survival_by_class = df.groupby("Pclass")["Survived"].mean() * 100
print(f"\n Insight 3 — Survival Rate by Passenger Class")
for pclass, rate in survival_by_class.items():
    label = {1: "1st Class", 2: "2nd Class", 3: "3rd Class"}[pclass]
    print(f"   {label}: {rate:.1f}% survived")
print(f"   Higher-class passengers had a much better chance of survival.")

# Insight 4: Age distribution
avg_age = df["Age"].mean()
median_age = df["Age"].median()
youngest = df["Age"].min()
oldest = df["Age"].max()
print(f"\n Insight 4 — Age Distribution")
print(f"   Average age: {avg_age:.1f} years")
print(f"   Median age:  {median_age:.1f} years")
print(f"   Youngest:    {youngest:.1f} years")
print(f"   Oldest:      {oldest:.1f} years")
print(f"   The age column has {df['Age'].isnull().sum()} missing values "
      f"({df['Age'].isnull().mean() * 100:.1f}% of all records).")

# Insight 5: Fare analysis
avg_fare = df["Fare"].mean()
median_fare = df["Fare"].median()
max_fare = df["Fare"].max()
fare_by_class = df.groupby("Pclass")["Fare"].mean()
print(f"\n Insight 5 — Fare Analysis")
print(f"   Average fare: ${avg_fare:.2f}")
print(f"   Median fare:  ${median_fare:.2f}")
print(f"   Maximum fare: ${max_fare:.2f}")
print(f"   Average fare by class:")
for pclass, fare in fare_by_class.items():
    label = {1: "1st Class", 2: "2nd Class", 3: "3rd Class"}[pclass]
    print(f"     {label}: ${fare:.2f}")
print(f"   The large gap between mean and median suggests the fare")
print(f"   distribution is right-skewed, with a few very expensive tickets.")

# ================================================================
# SUMMARY
# ================================================================
print("\n" + "=" * 70)
print("SUMMARY OF ANALYSIS")
print("=" * 70)
print(f"""
Dataset:          Titanic Passenger Data
Total Records:    {df.shape[0]}
Total Features:   {df.shape[1]}
Highest Value In: '{highest_col}' column (max = {highest_val})
Total Missing:    {total_missing} values ({(total_missing / total_cells * 100):.2f}%)

Key Takeaways:
  1. Only {survival_rate:.1f}% of passengers survived.
  2. Women survived at a much higher rate than men.
  3. 1st class passengers had the best survival odds.
  4. Average passenger age was {avg_age:.1f} years (with {df['Age'].isnull().sum()} missing).
  5. Fare distribution is heavily skewed — median ${median_fare:.2f} vs mean ${avg_fare:.2f}.
""")
