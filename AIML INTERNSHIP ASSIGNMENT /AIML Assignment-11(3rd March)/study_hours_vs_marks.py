"""
Assignment 11: Study Hours vs Marks — Predict the Relationship
==============================================================
Steps:
  1. Create a sample dataset (Study Hours → Marks)
  2. Identify Features (X) and Labels (y)
  3. Train a Linear Regression model
  4. Evaluate the model (MSE, R² Score)
  5. Predict marks for new study-hour values
  6. Visualize data + regression line
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ──────────────────────────────────────────────
# 1. CREATE THE DATASET
# ──────────────────────────────────────────────
data = {
    "Study_Hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                    1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5],
    "Marks":       [10, 20, 30, 35, 45, 55, 60, 70, 80, 90,
                    15, 22, 32, 40, 50, 58, 65, 75, 82, 92]
}

df = pd.DataFrame(data)

print("=" * 55)
print("        STUDY HOURS vs MARKS — DATASET")
print("=" * 55)
print(df.to_string(index=False))
print(f"\nDataset shape : {df.shape}")
print(f"Total samples : {len(df)}")

# ──────────────────────────────────────────────
# 2. IDENTIFY FEATURES & LABELS
# ──────────────────────────────────────────────
X = df[["Study_Hours"]]   # Feature  (independent variable)
y = df["Marks"]            # Label    (dependent variable)

print("\n" + "=" * 55)
print("        FEATURES & LABELS")
print("=" * 55)
print(f"Feature (X) : Study_Hours  → shape {X.shape}")
print(f"Label   (y) : Marks        → shape {y.shape}")
print("\nWhy?")
print("  • Study_Hours is the INPUT we use to make predictions.")
print("  • Marks is the OUTPUT (target) we want to predict.")

# ──────────────────────────────────────────────
# 3. SPLIT INTO TRAINING & TESTING SETS
# ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\n" + "=" * 55)
print("        TRAIN / TEST SPLIT")
print("=" * 55)
print(f"Training set : {len(X_train)} samples (80%)")
print(f"Testing  set : {len(X_test)} samples  (20%)")

# ──────────────────────────────────────────────
# 4. TRAIN A LINEAR REGRESSION MODEL
# ──────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

slope     = model.coef_[0]
intercept = model.intercept_

print("\n" + "=" * 55)
print("        MODEL TRAINING RESULTS")
print("=" * 55)
print(f"Equation : Marks = {slope:.2f} × Study_Hours + {intercept:.2f}")
print(f"Slope (m)     = {slope:.4f}  (marks gained per extra hour)")
print(f"Intercept (b) = {intercept:.4f}")

# ──────────────────────────────────────────────
# 5. EVALUATE THE MODEL
# ──────────────────────────────────────────────
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print("\n" + "=" * 55)
print("        MODEL EVALUATION")
print("=" * 55)
print(f"Mean Squared Error (MSE) : {mse:.4f}")
print(f"R² Score                 : {r2:.4f}")

if r2 >= 0.9:
    print("→ Excellent fit! The model explains the data very well.")
elif r2 >= 0.7:
    print("→ Good fit. The model captures most of the variance.")
else:
    print("→ Moderate fit. More data or features may improve results.")

# ──────────────────────────────────────────────
# 6. PREDICT FOR NEW VALUES
# ──────────────────────────────────────────────
new_hours = pd.DataFrame({"Study_Hours": [3, 5.5, 8, 11, 12]})
predictions = model.predict(new_hours)

print("\n" + "=" * 55)
print("        PREDICTIONS FOR NEW STUDY HOURS")
print("=" * 55)
print(f"{'Study Hours':>12}  {'Predicted Marks':>15}")
print("-" * 30)
for h, p in zip(new_hours["Study_Hours"], predictions):
    print(f"{h:>12.1f}  {p:>15.2f}")

# ──────────────────────────────────────────────
# 7. ACTUAL vs PREDICTED (TEST SET)
# ──────────────────────────────────────────────
comparison = pd.DataFrame({
    "Study_Hours":    X_test["Study_Hours"].values,
    "Actual_Marks":   y_test.values,
    "Predicted_Marks": np.round(y_pred, 2)
})
comparison.sort_values("Study_Hours", inplace=True)

print("\n" + "=" * 55)
print("        ACTUAL vs PREDICTED (TEST SET)")
print("=" * 55)
print(comparison.to_string(index=False))

# ──────────────────────────────────────────────
# 8. VISUALIZATION
# ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Plot 1: Scatter + Regression Line ---
ax1 = axes[0]
ax1.scatter(X, y, color="royalblue", edgecolors="black",
            s=80, label="Actual Data", zorder=3)
line_x = np.linspace(0, 12, 100).reshape(-1, 1)
line_y = model.predict(line_x)
ax1.plot(line_x, line_y, color="crimson", linewidth=2,
         label=f"Regression Line (y = {slope:.2f}x + {intercept:.2f})")
ax1.set_xlabel("Study Hours", fontsize=12)
ax1.set_ylabel("Marks", fontsize=12)
ax1.set_title("Study Hours vs Marks — Linear Regression", fontsize=13, fontweight="bold")
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Plot 2: Actual vs Predicted (Test Set) ---
ax2 = axes[1]
ax2.scatter(y_test, y_pred, color="forestgreen", edgecolors="black",
            s=80, label="Predicted vs Actual", zorder=3)
min_val = min(y_test.min(), y_pred.min()) - 5
max_val = max(y_test.max(), y_pred.max()) + 5
ax2.plot([min_val, max_val], [min_val, max_val], color="gray",
         linestyle="--", linewidth=1.5, label="Perfect Prediction Line")
ax2.set_xlabel("Actual Marks", fontsize=12)
ax2.set_ylabel("Predicted Marks", fontsize=12)
ax2.set_title(f"Actual vs Predicted (R² = {r2:.4f})", fontsize=13, fontweight="bold")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("study_hours_vs_marks_plot.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n Plot saved as 'study_hours_vs_marks_plot.png'")
print("=" * 55)
print("                    SUMMARY")
print("=" * 55)
print(f"  Feature : Study_Hours (independent variable)")
print(f"  Label   : Marks       (dependent variable)")
print(f"  Model   : Linear Regression")
print(f"  Equation: Marks = {slope:.2f} × Study_Hours + {intercept:.2f}")
print(f"  R² Score: {r2:.4f}")
print(f"  Insight : For every extra hour of study,")
print(f"            marks increase by ~{slope:.2f} points.")
print("=" * 55)
