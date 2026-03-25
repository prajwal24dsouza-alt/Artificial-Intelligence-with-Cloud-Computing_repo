import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Create a dataset for playing outside
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy'],
    'Temperature': [85, 80, 83, 70, 68, 65, 64, 72, 69, 75, 75, 72, 69, 71],
    'Humidity': [85, 90, 78, 96, 80, 70, 65, 95, 70, 80, 70, 90, 75, 80],
    'Wind': [False, True, False, False, False, True, True, False, False, True, True, False, True, True],
    'Play_Outside': ['No', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'No']
}

df = pd.DataFrame(data)

# Encode categorical features
le_outlook = LabelEncoder()
le_wind = LabelEncoder()
le_play = LabelEncoder()

df['Outlook_encoded'] = le_outlook.fit_transform(df['Outlook'])
df['Wind_encoded'] = le_wind.fit_transform(df['Wind'])
df['Play_Outside_encoded'] = le_play.fit_transform(df['Play_Outside'])

# Features and target
X = df[['Outlook_encoded', 'Temperature', 'Humidity', 'Wind_encoded']]
y = df['Play_Outside_encoded']

# Train the decision tree
dt_classifier = DecisionTreeClassifier(max_depth=4, random_state=42, min_samples_split=2)
dt_classifier.fit(X, y)

# Print accuracy
print(f"Decision Tree Accuracy: {dt_classifier.score(X, y):.2%}")
print("\nFeature Importances:")
for feature, importance in zip(['Outlook', 'Temperature', 'Humidity', 'Wind'], dt_classifier.feature_importances_):
    print(f"  {feature}: {importance:.4f}")

# Visualize the decision tree
plt.figure(figsize=(20, 10))
plot_tree(dt_classifier, 
          feature_names=['Outlook', 'Temperature', 'Humidity', 'Wind'],
          class_names=['No', 'Yes'],
          filled=True,
          fontsize=10)
plt.title("Decision Tree: Should You Play Outside?", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('decision_tree_play_outside.png', dpi=300, bbox_inches='tight')
print("\nDecision tree visualization saved as 'decision_tree_play_outside.png'")
plt.show()

# Make a prediction
print("\n" + "="*50)
print("EXAMPLE PREDICTIONS:")
print("="*50)

test_cases = [
    ['Sunny', 75, 70, False],
    ['Rainy', 65, 90, True],
    ['Overcast', 72, 80, False],
    ['Sunny', 85, 85, True]
]

for test in test_cases:
    outlook_enc = le_outlook.transform([test[0]])[0]
    wind_enc = le_wind.transform([test[3]])[0]
    prediction = dt_classifier.predict([[outlook_enc, test[1], test[2], wind_enc]])[0]
    result = "YES" if prediction == 1 else "NO"
    print(f"\nOutlook: {test[0]}, Temp: {test[1]}°F, Humidity: {test[2]}%, Wind: {test[3]}")
    print(f"→ Play Outside? {result}")
