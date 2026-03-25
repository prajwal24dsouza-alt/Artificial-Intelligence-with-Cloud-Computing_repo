"""
AIML Assignment-9: Data Visualization & Data Story
- Bar Chart: Average Salary by Department
- Pie Chart: Employee Distribution by City
- Histogram: Age Distribution of Employees
- Data Story: Key trends and insights
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ──────────────────────────────────────────────
# 1. Load the cleaned dataset
# ──────────────────────────────────────────────
df = pd.read_csv(
    "/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT "
    "/AIML Assignment-8(26th Feb)/cleaned_data.csv"
)

print("=" * 60)
print("            DATASET OVERVIEW")
print("=" * 60)
print(df.head())
print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {', '.join(df.columns)}")

# Set a clean visual style
plt.style.use("seaborn-v0_8-whitegrid")
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]

# ──────────────────────────────────────────────
# 2. BAR CHART – Average Salary by Department
# ──────────────────────────────────────────────
avg_salary = df.groupby("Department")["Salary"].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(8, 5))
bars = ax1.bar(avg_salary.index, avg_salary.values, color=colors[:len(avg_salary)],
               edgecolor="white", linewidth=1.2, width=0.55)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height + 500,
             f"${height:,.0f}", ha="center", va="bottom",
             fontsize=11, fontweight="bold")

ax1.set_title("Average Salary by Department", fontsize=15, fontweight="bold", pad=15)
ax1.set_xlabel("Department", fontsize=12)
ax1.set_ylabel("Average Salary ($)", fontsize=12)
ax1.set_ylim(0, avg_salary.max() * 1.15)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(
    "/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT "
    "/AIML Assignment-9(28th Feb)/bar_chart_salary.png",
    dpi=150
)
# plt.show()  # Uncomment if running interactively
print("\n Bar Chart saved: bar_chart_salary.png")

# ──────────────────────────────────────────────
# 3. PIE CHART – Employee Distribution by City
# ──────────────────────────────────────────────
city_counts = df["City"].value_counts()

fig2, ax2 = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax2.pie(
    city_counts.values,
    labels=city_counts.index,
    autopct="%1.1f%%",
    colors=colors[:len(city_counts)],
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2),
    textprops=dict(fontsize=12),
)

for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax2.set_title("Employee Distribution by City", fontsize=15, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig(
    "/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT "
    "/AIML Assignment-9(28th Feb)/pie_chart_city.png",
    dpi=150
)
plt.show()
print("Pie Chart saved: pie_chart_city.png")

# ──────────────────────────────────────────────
# 4. HISTOGRAM – Age Distribution
# ──────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(8, 5))
n, bins, patches = ax3.hist(
    df["Age"], bins=6, color="#4e79a7", edgecolor="white",
    linewidth=1.2, alpha=0.85
)

# Color gradient for bars
cmap = plt.cm.Blues
norm = plt.Normalize(vmin=n.min(), vmax=n.max())
for count, patch in zip(n, patches):
    patch.set_facecolor(cmap(norm(count) * 0.6 + 0.3))

# Add mean & median lines
mean_age = df["Age"].mean()
median_age = df["Age"].median()
ax3.axvline(mean_age, color="#e15759", linestyle="--", linewidth=2,
            label=f"Mean Age: {mean_age:.1f}")
ax3.axvline(median_age, color="#f28e2b", linestyle="-.", linewidth=2,
            label=f"Median Age: {median_age:.1f}")

ax3.set_title("Age Distribution of Employees", fontsize=15, fontweight="bold", pad=15)
ax3.set_xlabel("Age", fontsize=12)
ax3.set_ylabel("Number of Employees", fontsize=12)
ax3.legend(fontsize=11, frameon=True, fancybox=True)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(
    "/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT "
    "/AIML Assignment-9(28th Feb)/histogram_age.png",
    dpi=150
)
plt.show()
print(" Histogram saved: histogram_age.png")

# ──────────────────────────────────────────────
# 5. DATA STORY
# ──────────────────────────────────────────────
top_dept = avg_salary.idxmax()
top_salary = avg_salary.max()
low_dept = avg_salary.idxmin()
low_salary = avg_salary.min()
top_city = city_counts.idxmax()
top_city_pct = (city_counts.max() / city_counts.sum()) * 100

print("\n" + "=" * 60)
print("               DATA STORY")
print("=" * 60)

data_story = f"""
TITLE: Employee Workforce Insights – Salary, Location & Age Trends
----------------------------------------------------------------------

This analysis explores patterns across 17 employees spanning three
departments (Sales, Marketing, Engineering) and four major U.S. cities.

🔹 SALARY TRENDS (Bar Chart)
   • {top_dept} leads with the highest average salary of ${top_salary:,.0f}.
   • {low_dept} has the lowest average salary at ${low_salary:,.0f}.
   • The gap of ${top_salary - low_salary:,.0f} between the top and bottom
     departments suggests significant pay variation, possibly driven by
     market demand and specialization requirements.

🔹 GEOGRAPHIC DISTRIBUTION (Pie Chart)
   • {top_city} is the dominant hiring hub, accounting for {top_city_pct:.1f}%
     of total employees.
   • {', '.join(city_counts.index[1:])} each have smaller but notable shares,
     showing the company's geographic spread across multiple metro areas.
   • The concentration in {top_city} may reflect proximity to offices
     or a larger talent pool.

🔹 AGE DISTRIBUTION (Histogram)
   • Employee ages range from {df['Age'].min()} to {df['Age'].max()} years.
   • The average age is {mean_age:.1f} years (median: {median_age:.1f}),
     indicating a relatively young and mid-career workforce.
   • The distribution is roughly centered around the early-to-mid 30s,
     with most employees concentrated in the 28–38 age bracket.
   • Fewer employees fall in the 40+ range, suggesting either recent
     hiring drives targeting younger talent or higher attrition among
     senior employees.

🔹 KEY TAKEAWAYS
   1. The company invests more in {top_dept} roles, aligning with
      industry compensation norms.
   2. {top_city} serves as the primary talent center — future diversity
      goals may require expanding hiring in other cities.
   3. The workforce is youthful, which presents both growth potential
      and a need for mentorship and retention strategies.
"""

print(data_story)

# Save the data story to a text file
with open(
    "/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT "
    "/AIML Assignment-9(28th Feb)/data_story.txt", "w"
) as f:
    f.write(data_story)

print(" Data Story saved: data_story.txt")
print("=" * 60)
print("All charts and data story generated successfully!")
print("=" * 60)
