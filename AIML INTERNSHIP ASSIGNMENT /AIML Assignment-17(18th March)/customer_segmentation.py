"""
============================================================
  Assignment: Customer Segmentation using K-Means Clustering
  Dataset   : Mall Customers (synthetic, mimicking UCI dataset)
  Goal      : Cluster customers by Annual Income & Spending Score
              and describe each customer group.
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings("ignore")

# ── 0. Reproducibility ────────────────────────────────────────────────────────
np.random.seed(42)

# ── 1. Create Synthetic Mall-Customer Dataset ─────────────────────────────────
def create_mall_dataset(n=200):
    """
    Generates a realistic mall-customer dataset with 5 natural clusters:
      Group A – Low income, Low spending   (budget shoppers)
      Group B – Low income, High spending  (impulsive buyers)
      Group C – Mid income, Mid spending   (average customers)
      Group D – High income, Low spending  (careful savers)
      Group E – High income, High spending (premium shoppers)
    """
    groups = [
        # (n, income_mean, income_std, score_mean, score_std, gender_ratio)
        (40,  28, 6,  25, 8,  0.55),   # A
        (40,  25, 6,  75, 8,  0.30),   # B
        (40,  55, 8,  50, 10, 0.50),   # C
        (40,  85, 8,  18, 7,  0.60),   # D
        (40,  88, 7,  82, 7,  0.40),   # E
    ]
    records = []
    cid = 1
    for idx, (cnt, im, istd, sm, sstd, gratio) in enumerate(groups):
        for _ in range(cnt):
            gender = "Male" if np.random.rand() < gratio else "Female"
            age    = int(np.clip(np.random.normal(35 + idx * 5, 10), 18, 70))
            income = int(np.clip(np.random.normal(im, istd), 15, 140))
            score  = int(np.clip(np.random.normal(sm, sstd), 1, 100))
            records.append([cid, gender, age, income, score])
            cid += 1

    df = pd.DataFrame(records,
                      columns=["CustomerID", "Gender", "Age",
                               "Annual Income (k$)", "Spending Score (1-100)"])
    return df

# ── 2. Load / preview data ────────────────────────────────────────────────────
print("=" * 60)
print("   CUSTOMER SEGMENTATION – K-MEANS CLUSTERING")
print("=" * 60)

df = create_mall_dataset()
print(f"\n Dataset Shape  : {df.shape}")
print(f" Columns        : {list(df.columns)}")
print("\n First 5 Rows:")
print(df.head().to_string(index=False))
print("\n Basic Statistics:")
print(df.describe().round(2).to_string())

# ── 3. Select Features for Clustering ────────────────────────────────────────
X = df[["Annual Income (k$)", "Spending Score (1-100)"]].values

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── 4. Elbow Method – find optimal k ─────────────────────────────────────────
inertia = []
sil_scores = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    km.fit(X_scaled)
    inertia.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, km.labels_))

# ── 5. Train final K-Means model (k=5) ────────────────────────────────────────
OPTIMAL_K = 5
km_final = KMeans(n_clusters=OPTIMAL_K, init="k-means++",
                  n_init=10, random_state=42)
km_final.fit(X_scaled)
df["Cluster"] = km_final.labels_

sil_final = silhouette_score(X_scaled, km_final.labels_)
print(f"\n Optimal Clusters (k) : {OPTIMAL_K}")
print(f" Silhouette Score     : {sil_final:.4f}  (closer to 1 is better)")

# ── 6. Cluster Summary ────────────────────────────────────────────────────────
CLUSTER_LABELS = {
    0: " Budget Shoppers",
    1: " Premium Shoppers",
    2: "  Average Customers",
    3: " Careful Savers",
    4: " Impulsive Buyers",
}

summary = (df.groupby("Cluster")
             .agg(Count=("CustomerID", "count"),
                  Avg_Income=("Annual Income (k$)", "mean"),
                  Avg_Score=("Spending Score (1-100)", "mean"),
                  Avg_Age=("Age", "mean"))
             .round(1))
summary["Label"] = summary.index.map(CLUSTER_LABELS)
print("\n Cluster Summary:\n")
print(summary.to_string())

# ── 7. Remap labels to meaningful names (sort by income & score) ──────────────
# Sort clusters by income to assign consistent labels
cluster_income = df.groupby("Cluster")["Annual Income (k$)"].mean().sort_values()
cluster_score  = df.groupby("Cluster")["Spending Score (1-100)"].mean()

low_inc  = cluster_income.index[:2].tolist()      # 2 lowest income clusters
high_inc = cluster_income.index[3:].tolist()      # 2 highest income clusters
mid_inc  = cluster_income.index[2:3].tolist()     # middle income

label_map = {}
# Among low-income: lower score → budget, higher score → impulsive
low_inc_by_score = sorted(low_inc, key=lambda c: cluster_score[c])
label_map[low_inc_by_score[0]] = " Budget Shoppers"
label_map[low_inc_by_score[1]] = " Impulsive Buyers"
# Middle
label_map[mid_inc[0]] = "⚖️  Average Customers"
# Among high-income: lower score → careful savers, higher → premium
high_inc_by_score = sorted(high_inc, key=lambda c: cluster_score[c])
label_map[high_inc_by_score[0]] = " Careful Savers"
label_map[high_inc_by_score[1]] = " Premium Shoppers"

df["Segment"] = df["Cluster"].map(label_map)

# ── 8. Visualizations ─────────────────────────────────────────────────────────
COLORS = ["#E74C3C", "#2ECC71", "#3498DB", "#F39C12", "#9B59B6"]
CLUSTER_COLOR = {c: COLORS[i] for i, c in enumerate(sorted(df["Cluster"].unique()))}

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Mall Customer Segmentation – K-Means Clustering",
             fontsize=16, fontweight="bold", y=1.01)

# ── 8a. Elbow Curve ────────────────────────────────────────────────────────
ax = axes[0, 0]
ax.plot(K_range, inertia, "o-", color="#E74C3C", linewidth=2, markersize=7)
ax.axvline(OPTIMAL_K, linestyle="--", color="gray", alpha=0.7, label=f"Optimal k={OPTIMAL_K}")
ax.set_title("Elbow Method – Optimal k Selection", fontweight="bold")
ax.set_xlabel("Number of Clusters (k)")
ax.set_ylabel("Inertia (WCSS)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

# ── 8b. Silhouette Scores ─────────────────────────────────────────────────
ax = axes[0, 1]
bar_colors = ["#27AE60" if k == OPTIMAL_K else "#AED6F1" for k in K_range]
bars = ax.bar(K_range, sil_scores, color=bar_colors, edgecolor="white", linewidth=0.5)
ax.set_title("Silhouette Scores per k", fontweight="bold")
ax.set_xlabel("Number of Clusters (k)")
ax.set_ylabel("Silhouette Score")
ax.set_xticks(list(K_range))
ax.grid(True, axis="y", linestyle="--", alpha=0.5)
for bar, score in zip(bars, sil_scores):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{score:.2f}", ha="center", va="bottom", fontsize=8)

# ── 8c. Cluster Scatter Plot ──────────────────────────────────────────────
ax = axes[1, 0]
for cluster_id in sorted(df["Cluster"].unique()):
    mask = df["Cluster"] == cluster_id
    seg_name = label_map[cluster_id]
    ax.scatter(df.loc[mask, "Annual Income (k$)"],
               df.loc[mask, "Spending Score (1-100)"],
               c=CLUSTER_COLOR[cluster_id], label=seg_name,
               s=70, alpha=0.8, edgecolors="white", linewidth=0.4)

# Plot centroids (inverse transform to original scale)
centroids_orig = scaler.inverse_transform(km_final.cluster_centers_)
ax.scatter(centroids_orig[:, 0], centroids_orig[:, 1],
           c="black", marker="X", s=200, zorder=5, label="Centroids")
ax.set_title("Customer Clusters (Income vs Spending Score)", fontweight="bold")
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1–100)")
ax.legend(fontsize=7, loc="upper left")
ax.grid(True, linestyle="--", alpha=0.4)

# ── 8d. Segment Distribution Bar Chart ───────────────────────────────────
ax = axes[1, 1]
seg_counts = df["Segment"].value_counts()
ordered_labels = [label_map[c] for c in sorted(df["Cluster"].unique())]
ordered_counts = [seg_counts.get(label_map[c], 0) for c in sorted(df["Cluster"].unique())]
bars2 = ax.barh(ordered_labels, ordered_counts,
                color=[CLUSTER_COLOR[c] for c in sorted(df["Cluster"].unique())],
                edgecolor="white", linewidth=0.5)
ax.set_title("Customer Count per Segment", fontweight="bold")
ax.set_xlabel("Number of Customers")
ax.grid(True, axis="x", linestyle="--", alpha=0.5)
for bar, cnt in zip(bars2, ordered_counts):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            str(cnt), va="center", fontsize=9)

plt.tight_layout()
plt.savefig("customer_segmentation_plots.png", dpi=150, bbox_inches="tight")
print("\n Visualisation saved → customer_segmentation_plots.png")
plt.show()

# ── 9. Detailed Segment Descriptions ──────────────────────────────────────────
print("\n" + "=" * 60)
print("   CUSTOMER SEGMENT DESCRIPTIONS")
print("=" * 60)

descriptions = {
    "💸 Budget Shoppers": {
        "income":  "Low  (~$25k–$35k)",
        "score":   "Low  (10–35)",
        "profile": "Price-conscious shoppers who visit the mall rarely "
                   "and spend cautiously. They respond well to heavy discounts, "
                   "clearance sales, and value-for-money deals.",
        "strategy": "Offer loyalty discounts, bundle deals & low-cost product lines.",
    },
    "🎯 Impulsive Buyers": {
        "income":  "Low  (~$20k–$30k)",
        "score":   "High (65–90)",
        "profile": "Despite modest incomes these customers spend heavily, "
                   "driven by emotions, trends, and peer influence. "
                   "They are frequent visitors and impulse purchasers.",
        "strategy": "Use targeted promotions, flash sales & social-media campaigns.",
    },
    "⚖️  Average Customers": {
        "income":  "Medium (~$45k–$65k)",
        "score":   "Medium (40–60)",
        "profile": "Balanced customers who represent the typical mall visitor. "
                   "They shop regularly but don't over-spend. "
                   "Stability and quality drive their decisions.",
        "strategy": "Provide consistent quality, seasonal offers & reward programs.",
    },
    "💰 Careful Savers": {
        "income":  "High (~$75k–$100k)",
        "score":   "Low  (10–30)",
        "profile": "High earners who are very selective and financially disciplined. "
                   "They visit less frequently and prefer quality over quantity.",
        "strategy": "Highlight premium products, offer exclusive memberships & VIP events.",
    },
    "🌟 Premium Shoppers": {
        "income":  "High (~$80k–$110k)",
        "score":   "High (70–95)",
        "profile": "The most valuable segment – affluent customers who shop "
                   "frequently and spend generously. They seek luxury, exclusivity, "
                   "and superior experiences.",
        "strategy": "Focus on luxury brands, personalised offers & top-tier service.",
    },
}

for seg, info in descriptions.items():
    subset = df[df["Segment"] == seg]
    print(f"\n{'─'*55}")
    print(f"  {seg}")
    print(f"{'─'*55}")
    print(f"   Customers      : {len(subset)}")
    print(f"   Annual Income  : {info['income']}")
    print(f"  Spending Score : {info['score']}")
    print(f"   Profile        : {info['profile']}")
    print(f"  Strategy       : {info['strategy']}")

print(f"\n{'='*60}")
print("  ✅ Clustering Complete! Check the saved PNG for visuals.")
print(f"{'='*60}\n")
