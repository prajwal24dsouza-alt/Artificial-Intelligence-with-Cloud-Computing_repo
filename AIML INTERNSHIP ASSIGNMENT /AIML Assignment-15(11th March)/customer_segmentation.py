"""
Customer Segmentation using K-Means Clustering
================================================
Perform K-Means clustering on the Mall Customers dataset
and describe the resulting customer groups.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                       # non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D     # noqa: F401  (needed for 3D projection)

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Mall_Customers.csv")
PLOT_DIR  = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# ============================================================================
# 1.  LOAD DATA
# ============================================================================
print("=" * 60)
print("1. Loading dataset")
print("=" * 60)
df = pd.read_csv(DATA_PATH)
print(f"   Shape : {df.shape}")
print(f"   Columns : {list(df.columns)}")
print(df.head(10).to_string(index=False))

# ============================================================================
# 2.  EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
print("\n" + "=" * 60)
print("2. Exploratory Data Analysis")
print("=" * 60)

# 2a. Summary statistics
print("\n--- Summary Statistics ---")
print(df.describe().to_string())

# 2b. Check for missing values
print("\n--- Missing Values ---")
print(df.isnull().sum().to_string())

# 2c. Gender distribution
print("\n--- Gender Distribution ---")
print(df["Gender"].value_counts().to_string())

# 2d. Distribution plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, col, color in zip(
    axes,
    ["Age", "Annual Income (k$)", "Spending Score (1-100)"],
    ["#6C5CE7", "#00CEC9", "#FD79A8"],
):
    sns.histplot(df[col], bins=20, kde=True, color=color, ax=ax, edgecolor="white")
    ax.set_title(f"Distribution of {col}", fontsize=13, fontweight="bold")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "distributions.png"), dpi=150)
plt.close()
print("\n   ✓ Saved distributions.png")

# 2e. Gender-based box plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, col in zip(
    axes, ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
):
    sns.boxplot(x="Gender", y=col, data=df, ax=ax, palette="Set2")
    ax.set_title(f"{col} by Gender", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "boxplots_by_gender.png"), dpi=150)
plt.close()
print("   ✓ Saved boxplots_by_gender.png")

# 2f. Correlation heatmap
plt.figure(figsize=(8, 6))
numeric_cols = df.select_dtypes(include=[np.number])
corr = numeric_cols.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f",
            linewidths=0.5, square=True)
plt.title("Correlation Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "correlation_heatmap.png"), dpi=150)
plt.close()
print("   ✓ Saved correlation_heatmap.png")

# 2g. Pairplot
pair = sns.pairplot(df, hue="Gender",
                    vars=["Age", "Annual Income (k$)", "Spending Score (1-100)"],
                    palette="husl", diag_kind="kde")
pair.fig.suptitle("Pairplot of Numerical Features", y=1.02, fontsize=14, fontweight="bold")
pair.savefig(os.path.join(PLOT_DIR, "pairplot.png"), dpi=150)
plt.close("all")
print("   ✓ Saved pairplot.png")

# ============================================================================
# 3.  FEATURE SELECTION & SCALING  (2-D: Income vs Spending Score)
# ============================================================================
print("\n" + "=" * 60)
print("3. Feature Selection & Scaling")
print("=" * 60)

X_2d = df[["Annual Income (k$)", "Spending Score (1-100)"]].values
scaler_2d = StandardScaler()
X_2d_scaled = scaler_2d.fit_transform(X_2d)
print("   Features selected : Annual Income (k$), Spending Score (1-100)")
print("   Scaling            : StandardScaler applied")

# ============================================================================
# 4.  ELBOW METHOD  — find optimal k
# ============================================================================
print("\n" + "=" * 60)
print("4. Elbow Method")
print("=" * 60)

wcss = []
K_RANGE = range(1, 11)
for k in K_RANGE:
    km = KMeans(n_clusters=k, init="k-means++", max_iter=300,
                n_init=10, random_state=42)
    km.fit(X_2d_scaled)
    wcss.append(km.inertia_)
    print(f"   k = {k:2d}  →  WCSS = {km.inertia_:.2f}")

plt.figure(figsize=(10, 6))
plt.plot(K_RANGE, wcss, "o-", color="#6C5CE7", linewidth=2, markersize=8)
plt.title("Elbow Method — Optimal Number of Clusters", fontsize=14, fontweight="bold")
plt.xlabel("Number of Clusters (k)", fontsize=12)
plt.ylabel("Within-Cluster Sum of Squares (WCSS)", fontsize=12)
plt.xticks(K_RANGE)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "elbow_method.png"), dpi=150)
plt.close()
print("\n   ✓ Saved elbow_method.png")

# Choose optimal k (elbow at 5)
OPTIMAL_K = 5
print(f"\n   >>> Optimal k chosen = {OPTIMAL_K}")

# ============================================================================
# 5.  K-MEANS CLUSTERING  (2-D)
# ============================================================================
print("\n" + "=" * 60)
print("5. K-Means Clustering (2-D)")
print("=" * 60)

kmeans_2d = KMeans(n_clusters=OPTIMAL_K, init="k-means++", max_iter=300,
                   n_init=10, random_state=42)
labels_2d = kmeans_2d.fit_predict(X_2d_scaled)
df["Cluster_2D"] = labels_2d

# Inverse-transform centroids to original scale for interpretability
centroids_orig = scaler_2d.inverse_transform(kmeans_2d.cluster_centers_)
print("\n   Cluster centroids (original scale):")
print(f"   {'Cluster':>8}  {'Avg Income (k$)':>16}  {'Avg Spending Score':>19}")
for i, c in enumerate(centroids_orig):
    print(f"   {i:>8}  {c[0]:>16.1f}  {c[1]:>19.1f}")

# ============================================================================
# 6.  CLUSTER VISUALISATION (2-D)
# ============================================================================
print("\n" + "=" * 60)
print("6. Cluster Visualisation (2-D)")
print("=" * 60)

COLORS = ["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#00B894"]
SEGMENT_LABELS = {}

# Assign descriptive labels based on each centroid's income & spending
med_income   = np.median(centroids_orig[:, 0])
med_spending = np.median(centroids_orig[:, 1])

for i, (inc, sp) in enumerate(centroids_orig):
    hi_inc = inc > med_income * 1.15
    lo_inc = inc < med_income * 0.85
    hi_sp  = sp  > med_spending * 1.15
    lo_sp  = sp  < med_spending * 0.85

    if hi_inc and hi_sp:
        SEGMENT_LABELS[i] = "High Income, High Spending"
    elif hi_inc and lo_sp:
        SEGMENT_LABELS[i] = "High Income, Low Spending"
    elif lo_inc and hi_sp:
        SEGMENT_LABELS[i] = "Low Income, High Spending"
    elif lo_inc and lo_sp:
        SEGMENT_LABELS[i] = "Low Income, Low Spending"
    else:
        SEGMENT_LABELS[i] = "Medium Income, Medium Spending"

plt.figure(figsize=(12, 8))
for i in range(OPTIMAL_K):
    mask = labels_2d == i
    plt.scatter(
        X_2d[mask, 0], X_2d[mask, 1],
        s=80, c=COLORS[i], label=SEGMENT_LABELS[i],
        edgecolors="white", linewidth=0.5, alpha=0.85,
    )

plt.scatter(
    centroids_orig[:, 0], centroids_orig[:, 1],
    s=300, c="red", marker="X", edgecolors="black",
    linewidth=1.5, label="Centroids", zorder=5,
)
plt.title("Customer Segments — K-Means Clustering (k=5)",
          fontsize=15, fontweight="bold")
plt.xlabel("Annual Income (k$)", fontsize=12)
plt.ylabel("Spending Score (1-100)", fontsize=12)
plt.legend(fontsize=10, loc="upper left", framealpha=0.9)
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "clusters_2d.png"), dpi=150)
plt.close()
print("   ✓ Saved clusters_2d.png")

# ============================================================================
# 7.  CLUSTER DESCRIPTION
# ============================================================================
print("\n" + "=" * 60)
print("7. Cluster Descriptions")
print("=" * 60)

cluster_summary = df.groupby("Cluster_2D").agg(
    Count=("CustomerID", "count"),
    Avg_Age=("Age", "mean"),
    Avg_Income=("Annual Income (k$)", "mean"),
    Avg_Spending=("Spending Score (1-100)", "mean"),
    Male_Pct=("Gender", lambda x: (x == "Male").mean() * 100),
).round(1)

cluster_summary["Segment"] = cluster_summary.index.map(SEGMENT_LABELS)
cluster_summary = cluster_summary[["Segment", "Count", "Avg_Age",
                                    "Avg_Income", "Avg_Spending", "Male_Pct"]]
print("\n" + cluster_summary.to_string())

print("\n--- Detailed Segment Descriptions ---\n")
descriptions = {
    "Low Income, Low Spending":
        "Careful Customers — These customers have low annual income and also\n"
        "    spend very little. They are budget-conscious shoppers who prioritise\n"
        "    saving over spending. Marketing strategies like discount offers and\n"
        "    loyalty reward programmes may help engage this group.",

    "Low Income, High Spending":
        "Impulsive / Young Spenders — Despite having lower incomes, these\n"
        "    customers have high spending scores. They may be younger shoppers who\n"
        "    enjoy spending on lifestyle products. Targeted promotions and\n"
        "    instalment-based payment options could resonate with them.",

    "Medium Income, Medium Spending":
        "Average Customers — The mainstream group with moderate income and\n"
        "    moderate spending. They form the largest portion and represent the\n"
        "    'general' customer base. Broad marketing campaigns and seasonal\n"
        "    sales will work well for this segment.",

    "High Income, Low Spending":
        "Cautious High-Earners — High earners who spend very little at the\n"
        "    mall. They might prefer other shopping channels or simply aren't\n"
        "    finding products that appeal to them. Premium brand partnerships\n"
        "    and personalised recommendations could unlock this segment.",

    "High Income, High Spending":
        "VIP / Premium Customers — The most valuable segment with both high\n"
        "    income and high spending. These are the ideal target customers.\n"
        "    VIP programmes, exclusive launches, and concierge services should\n"
        "    be directed at this group to maximise lifetime value.",
}

for cluster_id in range(OPTIMAL_K):
    lbl = SEGMENT_LABELS[cluster_id]
    print(f"  Cluster {cluster_id} — {lbl}")
    print(f"    {descriptions[lbl]}")
    print()

# ============================================================================
# 8.  OPTIONAL — 3-D CLUSTERING  (Age + Income + Spending Score)
# ============================================================================
print("=" * 60)
print("8. 3-D Clustering (Age + Income + Spending Score)")
print("=" * 60)

X_3d = df[["Age", "Annual Income (k$)", "Spending Score (1-100)"]].values
scaler_3d = StandardScaler()
X_3d_scaled = scaler_3d.fit_transform(X_3d)

# Elbow for 3-D
wcss_3d = []
for k in K_RANGE:
    km = KMeans(n_clusters=k, init="k-means++", max_iter=300,
                n_init=10, random_state=42)
    km.fit(X_3d_scaled)
    wcss_3d.append(km.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(K_RANGE, wcss_3d, "o-", color="#E17055", linewidth=2, markersize=8)
plt.title("Elbow Method — 3-D Features", fontsize=14, fontweight="bold")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("WCSS")
plt.xticks(K_RANGE)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "elbow_method_3d.png"), dpi=150)
plt.close()
print("   ✓ Saved elbow_method_3d.png")

OPTIMAL_K_3D = 6
kmeans_3d = KMeans(n_clusters=OPTIMAL_K_3D, init="k-means++", max_iter=300,
                   n_init=10, random_state=42)
labels_3d = kmeans_3d.fit_predict(X_3d_scaled)
df["Cluster_3D"] = labels_3d

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection="3d")
COLORS_3D = ["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#00B894", "#E17055"]
for i in range(OPTIMAL_K_3D):
    mask = labels_3d == i
    ax.scatter(
        X_3d[mask, 0], X_3d[mask, 1], X_3d[mask, 2],
        s=60, c=COLORS_3D[i], label=f"Cluster {i}",
        edgecolors="white", linewidth=0.3, alpha=0.8,
    )
ax.set_title("Customer Segments — 3-D K-Means (k=6)",
             fontsize=14, fontweight="bold", pad=20)
ax.set_xlabel("Age", fontsize=11, labelpad=10)
ax.set_ylabel("Annual Income (k$)", fontsize=11, labelpad=10)
ax.set_zlabel("Spending Score", fontsize=11, labelpad=10)
ax.legend(fontsize=9, loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "clusters_3d.png"), dpi=150)
plt.close()
print("   ✓ Saved clusters_3d.png")

# 3-D cluster summary
cluster_summary_3d = df.groupby("Cluster_3D").agg(
    Count=("CustomerID", "count"),
    Avg_Age=("Age", "mean"),
    Avg_Income=("Annual Income (k$)", "mean"),
    Avg_Spending=("Spending Score (1-100)", "mean"),
).round(1)
print("\n   3-D Cluster Summary:")
print(cluster_summary_3d.to_string())

# ============================================================================
# 9.  SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("✅  ANALYSIS COMPLETE")
print("=" * 60)
print(f"   Dataset        : {DATA_PATH}")
print(f"   Total customers: {len(df)}")
print(f"   2-D clusters   : {OPTIMAL_K}   (Income vs Spending Score)")
print(f"   3-D clusters   : {OPTIMAL_K_3D} (Age + Income + Spending Score)")
print(f"   Plots saved in : {PLOT_DIR}/")
print("=" * 60)
