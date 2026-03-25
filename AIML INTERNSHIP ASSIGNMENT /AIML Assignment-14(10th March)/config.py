"""
Configuration file for Spam Detection System
"""

# Feature Extraction Settings
FEATURE_CONFIG = {
    'extract_text_stats': True,
    'extract_character_patterns': True,
    'extract_url_features': True,
    'extract_spam_keywords': True,
    'extract_linguistic_features': True,
    'extract_special_patterns': True,
}

# Model Configuration
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 15,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42,
    },
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 5,
        'random_state': 42,
    },
    'logistic_regression': {
        'max_iter': 1000,
        'random_state': 42,
    },
    'svm': {
        'kernel': 'rbf',
        'probability': True,
        'random_state': 42,
    },
}

# Training Configuration
TRAINING_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'stratified_split': True,
    'scale_features': True,
}

# Evaluation Configuration
EVALUATION_CONFIG = {
    'cross_validation_folds': 5,
    'metrics': ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
    'plot_roc_curve': True,
    'plot_pr_curve': True,
    'plot_confusion_matrix': True,
}

# Prediction Configuration
PREDICTION_CONFIG = {
    'default_threshold': 0.5,
    'confidence_threshold': 0.7,
    'ensemble_voting_method': 'average',  # 'average' or 'majority'
}

# Data Configuration
DATA_CONFIG = {
    'synthetic_data_size': 2000,
    'synthetic_spam_ratio': 0.3,
    'balance_data': True,
    'min_email_length': 10,
    'max_email_length': 10000,
}

# Spam Keywords
SPAM_KEYWORDS = {
    'urgent', 'winner', 'congratulations', 'claim reward', 'limited time',
    'act now', 'click here', 'buy now', 'free', 'money', 'password',
    'verify account', 'confirm identity', 'update payment', 'suspended',
    'urgent action required', 'unsubscribe', 'viagra', 'dear friend',
    'gift card', 'exclusive offer', 'risk free', 'no credit card',
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'spam_detection.log',
    'log_predictions': True,
    'save_predictions': True,
}

# Production Configuration
PRODUCTION_CONFIG = {
    'quarantine_emails': True,  # Instead of delete
    'notify_users': True,
    'send_to_admins': False,
    'monitor_metrics': True,
    'alert_on_performance_drop': True,
    'performance_threshold': 0.85,
}
