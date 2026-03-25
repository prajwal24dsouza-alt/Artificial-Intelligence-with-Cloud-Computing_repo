# Spam Detection System

A complete machine learning system for detecting spam emails using feature extraction, multiple classification algorithms, and ensemble methods.

## 📋 Project Structure

```
├── features.py           # Feature extraction module
├── data_loader.py        # Data loading and preprocessing
├── model.py              # Model training and prediction
├── evaluate.py           # Evaluation metrics and visualization
├── main.py               # Complete pipeline script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run Complete Pipeline

```bash
# Train models and evaluate on synthetic data
python main.py --mode pipeline
```

### Predict Single Email

```bash
# Classify a single email (after training)
python main.py --mode predict --email "your email text here"
```

## 📊 System Components

### 1. **Feature Extraction** (`features.py`)

Extracts 30+ features from email text:

#### Text Statistics
- Character count, word count, average word length
- Unique words ratio, sentence count, average sentence length

#### Character Patterns
- Capital letter ratio, digit ratio, special character ratio
- Exclamation marks, question marks, ellipsis counts

#### URL Features
- Total URLs, shortened URLs (bit.ly, tinyurl, etc.)
- Email addresses and IP addresses

#### Spam Indicators
- Spam keyword count (25+ predefined keywords)
- Spam keyword ratio relative to total words

#### Linguistic Patterns
- Repeated characters and words
- Pronoun usage, all-caps words

#### Special Patterns
- HTML tags, monetary references
- Action request words (confirm, verify, update)
- Urgency words (urgent, immediately, asap)

### 2. **Data Loading & Preprocessing** (`data_loader.py`)

- **CSV Loading**: Load emails from CSV files
- **Synthetic Data Generation**: Create realistic spam/ham examples for testing
- **Data Splitting**: Train/test split with stratification
- **Feature Scaling**: Normalize features using StandardScaler
- **Class Balancing**: Handle imbalanced datasets

### 3. **Model Training** (`model.py`)

Supports multiple algorithms:

#### Single Models
- **Random Forest**: 100 trees, max_depth=15
- **Gradient Boosting**: 100 estimators, learning_rate=0.1
- **Logistic Regression**: L2 regularization, max_iter=1000
- **SVM**: RBF kernel with probability estimation

#### Ensemble Model
- Combines multiple models using probability averaging
- More robust predictions with reduced overfitting

Features:
- Train single or multiple models
- Cross-validation support
- Feature importance extraction
- Model persistence (save/load)

### 4. **Evaluation** (`evaluate.py`)

Comprehensive metrics:
- **Accuracy, Precision, Recall, F1-Score**
- **Specificity, False Positive/Negative Rate**
- **ROC-AUC Score**
- **Confusion Matrix Analysis**
- **Threshold Sensitivity Analysis**

Visualizations:
- ROC Curve
- Precision-Recall Curve
- Confusion Matrix Heatmap

### 5. **Main Pipeline** (`main.py`)

10-Step Complete Pipeline:
1. Data loading and preparation
2. Feature extraction
3. Data preprocessing and scaling
4. Model training (individual + ensemble)
5. Predictions on test set
6. Performance evaluation
7. Feature importance analysis
8. Threshold sensitivity analysis
9. Example predictions on new emails
10. Model persistence

## 📈 Key Metrics Explained

| Metric | Definition | Importance |
|--------|-----------|-----------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| **Precision** | TP/(TP+FP) | When model says spam, is it right? |
| **Recall** | TP/(TP+FN) | Catches all actual spam? |
| **F1-Score** | 2×(Precision×Recall)/(Precision+Recall) | Balanced measure |
| **Specificity** | TN/(TN+FP) | Avoids false positives |
| **ROC-AUC** | Area under ROC curve | Model discrimination ability |

### Confusion Matrix
```
                Predicted
                Spam    Ham
Actual  Spam    TP      FN
        Ham     FP      TN
```

## ⚠️ Common Issues & Solutions

### Issue: Imbalanced Dataset
**Solution**: Use class weights or SMOTE balancing
```python
from data_loader import DataLoader
X_balanced, y_balanced = DataLoader.balance_data(X, y)
```

### Issue: High False Positives
**Solution**: Adjust prediction threshold
```python
# Lower threshold = more emails marked as spam
y_pred = (y_proba > 0.6).astype(int)  # Instead of 0.5
```

### Issue: Poor Generalization
**Solution**: Use ensemble models
```python
from model import EnsembleSpamDetector
ensemble = EnsembleSpamDetector(['random_forest', 'gradient_boosting'])
ensemble.train(X_train, y_train)
```

## 🔧 Customization

### Add Custom Features
```python
from features import FeatureExtractor

class CustomFeatureExtractor(FeatureExtractor):
    def _extract_custom_features(self, text):
        # Your custom logic
        return features
```

### Use Different Algorithm
```python
from model import SpamDetectionModel

model = SpamDetectionModel(model_type='svm')
model.train(X_train, y_train)
```

### Load CSV Data
```python
from data_loader import DataLoader

emails, labels = DataLoader.load_from_csv('your_emails.csv')
```

## 📊 Example Output

```
RANDOM FOREST MODEL:
============================================================
SPAM DETECTION MODEL EVALUATION REPORT
============================================================

📊 PERFORMANCE METRICS:
  Accuracy:              0.9650
  Precision:             0.9531
  Recall (Sensitivity):  0.9667
  F1-Score:              0.9599
  Specificity:           0.9641

📈 CONFUSION MATRIX:
  True Negatives:         2727
  False Positives:          51
  False Negatives:          16
  True Positives:         206

⚠️  ERROR RATES:
  False Positive Rate:   0.0185
  False Negative Rate:   0.0718
```

## 🎯 Best Practices

1. **Monitor False Positives**: Set appropriate thresholds
2. **Regular Retraining**: Update models monthly with new spam patterns
3. **Feature Engineering**: Add domain-specific features for better performance
4. **Ensemble Methods**: Combine models for robustness
5. **Audit Trail**: Log classification decisions for debugging
6. **A/B Testing**: Test threshold changes with small user groups
7. **Performance Tracking**: Monitor metrics in production continuously

## 📚 Feature Reference

### High-Spam Indicators
- Exclamation marks and question marks (>3 each)
- ALL CAPS words (>5)
- Spam keywords (winner, claim, verify, etc.)
- Shortened URLs (bit.ly, tinyurl, etc.)
- HTML tags (phishing indicator)
- Urgency words (immediate, urgent, NOW!!!)

### High-Legitimate Indicators
- Balanced case (not all caps)
- Proper grammar and spelling
- No repeated characters (heeeeello)
- Personal pronouns (I, you, we)
- Clear subject and body structure

## 🤝 Contributing

To add improvements:
1. Create feature extraction functions in `features.py`
2. Add new models to `model.py`
3. Include evaluation metrics in `evaluate.py`
4. Update pipeline in `main.py`

## 📄 License

This project is provided as-is for educational purposes.

## 🔗 References

- [Spam Datasets](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Feature Engineering for Text](https://towardsdatascience.com/)

---

**Version**: 1.0  
**Last Updated**: March 2026
