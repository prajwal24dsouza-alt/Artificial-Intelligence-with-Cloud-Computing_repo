import pandas as pd
import numpy as np

# Read CSV file
df = pd.read_csv('students.csv')

print("=" * 80)
print("ORIGINAL DATA")
print("=" * 80)
print(df)
print(f"\nShape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# Handle missing values by filling with the mean of that column
print("\n" + "=" * 80)
print("HANDLING MISSING VALUES")
print("=" * 80)
df['maths'] = df['maths'].fillna(df['maths'].mean())
df['science'] = df['science'].fillna(df['science'].mean())
df['english'] = df['english'].fillna(df['english'].mean())
print("Missing values filled with column means")
print(f"\nMissing values after handling:\n{df.isnull().sum()}")

# Add Total column (sum of maths, science, english)
df['total'] = df['maths'] + df['science'] + df['english']

# Add Average column (mean of maths, science, english)
df['average'] = df[['maths', 'science', 'english']].mean(axis=1)

print("\n" + "=" * 80)
print("DATA WITH TOTAL AND AVERAGE COLUMNS")
print("=" * 80)
print(df)

# Find top 3 students based on total marks department-wise
print("\n" + "=" * 80)
print("TOP 3 STUDENTS BY TOTAL MARKS (DEPARTMENT-WISE)")
print("=" * 80)
for dept in df['dept'].unique():
    dept_data = df[df['dept'] == dept].nlargest(3, 'total')[['name', 'maths', 'science', 'english', 'total', 'average']]
    print(f"\n{dept}:")
    print(dept_data.to_string(index=False))

# Find students scoring above 75 in all subjects
print("\n" + "=" * 80)
print("STUDENTS SCORING ABOVE 75 IN ALL SUBJECTS")
print("=" * 80)
above_75 = df[(df['maths'] > 75) & (df['science'] > 75) & (df['english'] > 75)][['name', 'maths', 'science', 'english', 'total', 'average', 'dept']]
if len(above_75) > 0:
    print(above_75.to_string(index=False))
else:
    print("No students found scoring above 75 in all subjects")

# Save the processed data
output_file = 'students_processed.csv'
df.to_csv(output_file, index=False)
print(f"\n" + "=" * 80)
print(f"Processed data saved to '{output_file}'")
print("=" * 80)
