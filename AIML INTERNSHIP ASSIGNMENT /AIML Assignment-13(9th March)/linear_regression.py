import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Create sample dataset (House prices)
# Features: Square footage, Number of bedrooms, Age of house
# Target: Price

np.random.seed(42)
n_samples = 100

# Generate synthetic data
X = np.random.rand(n_samples, 3) * 100
X[:, 0] = X[:, 0] * 2000 + 1000  # Square footage (1000-3000)
X[:, 1] = np.random.randint(1, 6, n_samples)  # Bedrooms (1-5)
X[:, 2] = np.random.randint(1, 50, n_samples)  # Age (1-50 years)

# Price = 200*sqft/1000 + 50000*bedrooms - 1000*age + noise
y = (X[:, 0]/1000)*200 + X[:, 1]*50000 - X[:, 2]*1000 + np.random.randn(n_samples)*20000

# Create DataFrame for better visualization
df = pd.DataFrame(X, columns=['Square Footage', 'Bedrooms', 'Age (years)'])
df['Price'] = y

print("=" * 60)
print("LINEAR REGRESSION MODEL - HOUSE PRICE PREDICTION")
print("=" * 60)
print("\nDataset Overview:")
print(df.head(10))
print(f"\nDataset Shape: {df.shape}")
print(f"\nPrice Statistics:")
print(df['Price'].describe())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

# Train Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE")
print("=" * 60)

# Display model coefficients
print("\nModel Coefficients:")
print(f"  Square Footage coefficient: ${model.coef_[0]:.2f} per sq ft")
print(f"  Bedrooms coefficient: ${model.coef_[1]:.2f} per bedroom")
print(f"  Age coefficient: ${model.coef_[2]:.2f} per year")
print(f"  Intercept (Base Price): ${model.intercept_:.2f}")

# Make predictions on training data
y_train_pred = model.predict(X_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

# Make predictions on testing data
y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)
print("\nTraining Set Metrics:")
print(f"  RMSE: ${train_rmse:.2f}")
print(f"  R² Score: {train_r2:.4f}")

print("\nTesting Set Metrics:")
print(f"  RMSE: ${test_rmse:.2f}")
print(f"  R² Score: {test_r2:.4f}")

# Test with new input data
print("\n" + "=" * 60)
print("PREDICTION ON NEW DATA")
print("=" * 60)

# Test Case 1: Modern small house
test_input_1 = np.array([[1800, 3, 5]])  # 1800 sq ft, 3 bedrooms, 5 years old
pred_1 = model.predict(test_input_1)[0]
print("\nTest Case 1: Modern Small House")
print(f"  Features: {test_input_1[0, 0]} sq ft, {int(test_input_1[0, 1])} bedrooms, {int(test_input_1[0, 2])} years old")
print(f"  Predicted Price: ${pred_1:.2f}")

# Test Case 2: Large old house
test_input_2 = np.array([[3000, 5, 40]])  # 3000 sq ft, 5 bedrooms, 40 years old
pred_2 = model.predict(test_input_2)[0]
print("\nTest Case 2: Large Old House")
print(f"  Features: {test_input_2[0, 0]} sq ft, {int(test_input_2[0, 1])} bedrooms, {int(test_input_2[0, 2])} years old")
print(f"  Predicted Price: ${pred_2:.2f}")

# Test Case 3: Medium house
test_input_3 = np.array([[2200, 4, 20]])  # 2200 sq ft, 4 bedrooms, 20 years old
pred_3 = model.predict(test_input_3)[0]
print("\nTest Case 3: Medium House")
print(f"  Features: {test_input_3[0, 0]} sq ft, {int(test_input_3[0, 1])} bedrooms, {int(test_input_3[0, 2])} years old")
print(f"  Predicted Price: ${pred_3:.2f}")

# Visualization
plt.figure(figsize=(14, 5))

# Plot 1: Predicted vs Actual (Test Set)
plt.subplot(1, 3, 1)
plt.scatter(y_test, y_test_pred, alpha=0.6, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price ($)')
plt.ylabel('Predicted Price ($)')
plt.title('Predicted vs Actual (Test Set)')
plt.grid(True, alpha=0.3)

# Plot 2: Residuals
plt.subplot(1, 3, 2)
residuals = y_test - y_test_pred
plt.scatter(y_test_pred, residuals, alpha=0.6, color='green')
plt.axhline(y=0, color='r', linestyle='--', lw=2)
plt.xlabel('Predicted Price ($)')
plt.ylabel('Residuals ($)')
plt.title('Residual Plot')
plt.grid(True, alpha=0.3)

# Plot 3: Price distribution
plt.subplot(1, 3, 3)
plt.hist(df['Price'], bins=20, color='purple', alpha=0.7, edgecolor='black')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.title('Price Distribution')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/prajwallawrencedsouza/Documents/AIML INTERNSHIP ASSIGNMENT /AIML Assignment-13(9th March)/model_performance.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved as 'model_performance.png'")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✓ Model trained on {len(X_train)} samples")
print(f"✓ Model tested on {len(X_test)} samples")
print(f"✓ Test R² Score: {test_r2:.4f} (closer to 1 is better)")
print(f"✓ Test RMSE: ${test_rmse:.2f}")
print("✓ Model ready for predictions on new data")
print("=" * 60)
