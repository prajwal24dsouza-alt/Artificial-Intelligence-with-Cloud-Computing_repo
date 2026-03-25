# 📖 Spam Detection System - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Detailed Examples](#detailed-examples)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Step 1: Clone/Download Project
```bash
cd path/to/AIML Assignment-14
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
python -c "import numpy, sklearn, matplotlib; print('✓ All dependencies installed')"
```

---

## Quick Start

### Run Complete Pipeline (Recommended)
```bash
python main.py --mode pipeline
```

**Output includes:**
- Model training on 2000 emails (70% ham, 30% spam)
- Performance metrics for Random Forest and Ensemble models
- Feature importance analysis
- Example predictions on 5 test emails
- Model saved as `spam_detector_model.pkl`

### Predict Single Email
```bash
python main.py --mode predict --email "Your email text here"
```

**Example:**
```bash
python main.py --mode predict --email "CONGRATULATIONS! You won $1,000,000! Click here!"
```

---

## Detailed Examples

### Example 1: Basic Usage with Python Script

```python
from features import FeatureExtractor, extract_features_batch
from model import SpamDetectionModel
from data_loader import DataLoader
import numpy as np

# Generate synthetic data
emails, labels = DataLoader.generate_synthetic_data(n_samples=500, spam_ratio=0.3)

# Extract features
X, feature_names = extract_features_batch(emails)
y = np.array(labels)

# Split and preprocess
X_train, X_test, y_train, y_test, scaler = DataLoader.preprocess_data(X, y)

# Train model
model = SpamDetectionModel(model_type='random_forest')
model.train(X_train, y_train)

# Predict
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

print(f"Accuracy: {(predictions == y_test).mean():.2%}")
```

### Example 2: Using Ensemble Model

```python
from model import EnsembleSpamDetector
from evaluate import SpamDetectionEvaluator

# Train ensemble with multiple models
ensemble = EnsembleSpamDetector(
    model_types=['random_forest', 'gradient_boosting', 'logistic_regression']
)
ensemble.train(X_train, y_train)

# Get predictions
spam_probabilities = ensemble.predict_proba(X_test)
predictions = (spam_probabilities > 0.5).astype(int)

# Evaluate
SpamDetectionEvaluator.print_report(y_test, predictions, spam_probabilities)
```

### Example 3: Feature Importance Analysis

```python
from model import SpamDetectionModel

model = SpamDetectionModel(model_type='random_forest')
model.train(X_train, y_train)

# Get top 15 important features
top_features = model.get_feature_importance(feature_names, top_k=15)

print("Most Important Features for Spam Detection:")
for i, (feature, importance) in enumerate(top_features, 1):
    bar = "█" * int(importance * 50)
    print(f"{i:2d}. {feature:<30s} {bar} {importance:.4f}")
```

### Example 4: Threshold Optimization

```python
from evaluate import SpamDetectionEvaluator

# Test different thresholds
thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
results = SpamDetectionEvaluator.analyze_threshold_sensitivity(
    y_test, 
    spam_probabilities, 
    thresholds
)

SpamDetectionEvaluator.print_threshold_analysis(results)

# Find optimal threshold (maximize F1-score)
best_threshold = max(results.keys(), 
                     key=lambda t: results[t]['f1'])
print(f"\n✓ Optimal threshold: {best_threshold:.2f}")
```

### Example 5: Load Data from CSV

```python
from data_loader import DataLoader

# Load your own data
emails, labels = DataLoader.load_from_csv('sample_emails.csv')

print(f"Loaded {len(emails)} emails")
print(f"Spam count: {sum(labels)}, Ham count: {len(labels) - sum(labels)}")
```

### Example 6: Batch Email Classification

```python
from features import extract_features_batch
from model import SpamDetectionModel

# List of emails to classify
emails = [
    "Your order has shipped. Track it here: example.com/track/123",
    "URGENT! Verify your account NOW!!!",
    "Meeting scheduled for tomorrow at 2pm",
]

# Extract features and predict
X, _ = extract_features_batch(emails)
X_scaled = scaler.transform(X)

for email, prob in zip(emails, model.predict_proba(X_scaled)[:, 1]):
    label = "🚨 SPAM" if prob > 0.5 else "✅ HAM"
    print(f"{label} ({prob:.1%}): {email[:50]}...")
```

---

## Advanced Usage

### Custom Feature Extraction

```python
from features import FeatureExtractor
import re

class CustomFeatureExtractor(FeatureExtractor):
    def _extract_custom_features(self, text):
        """Add your custom features here"""
        features = {}
        
        # Example: Count discount keywords
        discount_keywords = {'discount', 'sale', 'offer', 'deal'}
        features['discount_keyword_count'] = sum(
            1 for keyword in discount_keywords if keyword in text.lower()
        )
        
        # Example: Check for common phishing patterns
        phishing_patterns = [
            r'verify.*account',
            r'confirm.*identity',
            r'update.*payment'
        ]
        features['phishing_pattern_count'] = sum(
            1 for pattern in phishing_patterns 
            if re.search(pattern, text.lower())
        )
        
        return features
```

### Multi-Model Comparison

```python
from model import SpamDetectionModel
from evaluate import SpamDetectionEvaluator

models_to_test = ['random_forest', 'gradient_boosting', 'logistic_regression', 'svm']
results = {}

for model_type in models_to_test:
    model = SpamDetectionModel(model_type=model_type)
    model.train(X_train, y_train)
    
    predictions = model.predict(X_test)
    metrics = SpamDetectionEvaluator.evaluate(y_test, predictions)
    
    results[model_type] = metrics

# Compare F1 scores
print("\nModel Comparison:")
print("-" * 40)
for model_type, metrics in sorted(results.items(), 
                                 key=lambda x: x[1]['f1'], 
                                 reverse=True):
    print(f"{model_type:<25} F1: {metrics['f1']:.4f}")
```

### Cross-Validation

```python
from model import SpamDetectionModel

model = SpamDetectionModel(model_type='random_forest')
cv_results = model.cross_validate(X_train, y_train, cv=5)

print(f"Cross-Validation Results (5-fold):")
print(f"  Mean F1-Score: {cv_results['mean_score']:.4f}")
print(f"  Std Dev:       {cv_results['std_score']:.4f}")
print(f"  Scores:        {cv_results['scores']}")
```

### Save and Load Models

```python
from model import SpamDetectionModel

# Train model
model = SpamDetectionModel(model_type='random_forest')
model.train(X_train, y_train)

# Save model
model.save('my_spam_detector.pkl')

# Later: Load and use model
loaded_model = SpamDetectionModel.load('my_spam_detector.pkl')
predictions = loaded_model.predict(X_test)
```

---

## Troubleshooting

### Problem: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution:**
```bash
pip install scikit-learn
```

### Problem: Memory Error on Large Dataset
```python
# Use smaller batches
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2
)
model.train(X_train, y_train)
```

### Problem: Poor Model Performance
```python
# Try ensemble instead of single model
from model import EnsembleSpamDetector

ensemble = EnsembleSpamDetector()
ensemble.train(X_train, y_train)

# Or balance imbalanced data
X_balanced, y_balanced = DataLoader.balance_data(X_train, y_train)
model.train(X_balanced, y_balanced)
```

### Problem: Too Many False Positives
```python
# Increase prediction threshold
predictions = (spam_proba > 0.7).astype(int)  # Instead of 0.5

# Or adjust model parameters
model = SpamDetectionModel('gradient_boosting')
model.train(X_train, y_train)
```

### Problem: Features Missing for Some Emails
```python
# Handle missing features with fillna
from features import extract_features_batch
import numpy as np

X, _ = extract_features_batch(emails)
X = np.nan_to_num(X, nan=0)  # Replace NaN with 0
```

---

## Tips for Production Deployment

1. **Monitor False Positives Closely**
   - Start with threshold=0.7 to be conservative
   - Gradually lower as confidence increases

2. **Version Control Models**
   ```python
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   model.save(f'spam_detector_{timestamp}.pkl')
   ```

3. **Log Predictions**
   ```python
   import logging
   logging.info(f"Email classified as SPAM with {prob:.2%} confidence")
   ```

4. **Regular Retraining**
   - Collect misclassified emails
   - Retrain monthly with new data
   - Compare new vs. old model performance

5. **A/B Testing**
   - Test new threshold with 10% of users
   - Monitor error rates before full rollout

---

## Questions?

Refer to the main [README.md](README.md) for architecture and metrics explanation.

---

**Last Updated**: March 2026
