"""
Main Script: Complete Spam Detection System Pipeline
"""

import numpy as np
import argparse
from features import extract_features_batch, FeatureExtractor
from data_loader import DataLoader
from model import SpamDetectionModel, EnsembleSpamDetector
from evaluate import SpamDetectionEvaluator


def main():
    """Run the complete spam detection pipeline"""
    
    print("\n" + "="*70)
    print("🚀 SPAM DETECTION SYSTEM - COMPLETE PIPELINE")
    print("="*70)
    
    # ==================== DATA LOADING ====================
    print("\n📥 STEP 1: Loading and Preparing Data...")
    
    # Generate synthetic data for demonstration
    emails, labels = DataLoader.generate_synthetic_data(n_samples=2000, spam_ratio=0.3)
    print(f"   ✓ Generated {len(emails)} emails")
    print(f"   ✓ Class distribution: {sum(labels)} spam, {len(labels) - sum(labels)} ham")
    
    # ==================== FEATURE EXTRACTION ====================
    print("\n🔍 STEP 2: Extracting Features...")
    
    X, feature_names = extract_features_batch(emails)
    y = np.array(labels)
    
    print(f"   ✓ Extracted {X.shape[1]} features from {X.shape[0]} emails")
    print(f"   ✓ Feature names: {feature_names[:5]}... (showing first 5)")
    
    # ==================== DATA PREPROCESSING ====================
    print("\n⚙️  STEP 3: Preprocessing Data...")
    
    X_train, X_test, y_train, y_test, scaler = DataLoader.preprocess_data(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"   ✓ Training set: {X_train.shape[0]} samples")
    print(f"   ✓ Test set: {X_test.shape[0]} samples")
    print(f"   ✓ Features scaled using StandardScaler")
    
    # ==================== MODEL TRAINING ====================
    print("\n🤖 STEP 4: Training Models...")
    
    # Train individual models
    print("\n   Training individual models:")
    model_rf = SpamDetectionModel(model_type='random_forest')
    model_rf.train(X_train, y_train)
    print("   ✓ Random Forest trained")
    
    model_gb = SpamDetectionModel(model_type='gradient_boosting')
    model_gb.train(X_train, y_train)
    print("   ✓ Gradient Boosting trained")
    
    model_lr = SpamDetectionModel(model_type='logistic_regression')
    model_lr.train(X_train, y_train)
    print("   ✓ Logistic Regression trained")
    
    # Train ensemble
    print("\n   Training ensemble model:")
    ensemble = EnsembleSpamDetector()
    ensemble.train(X_train, y_train)
    print("   ✓ Ensemble model trained")
    
    # ==================== PREDICTIONS ====================
    print("\n🎯 STEP 5: Making Predictions...")
    
    # Predictions on test set
    y_pred_rf = model_rf.predict(X_test)
    y_proba_rf = model_rf.predict_proba(X_test)[:, 1]
    
    y_proba_ensemble = ensemble.predict_proba(X_test)
    y_pred_ensemble = (y_proba_ensemble > 0.5).astype(int)
    
    print(f"   ✓ Random Forest predictions: {np.sum(y_pred_rf)} spam detected")
    print(f"   ✓ Ensemble predictions: {np.sum(y_pred_ensemble)} spam detected")
    
    # ==================== EVALUATION ====================
    print("\n📊 STEP 6: Evaluating Model Performance...\n")
    
    print("RANDOM FOREST MODEL:")
    SpamDetectionEvaluator.print_report(y_test, y_pred_rf, y_proba_rf)
    
    print("\nENSEMBLE MODEL:")
    SpamDetectionEvaluator.print_report(y_test, y_pred_ensemble, y_proba_ensemble)
    
    # Feature importance
    print("\n📈 STEP 7: Feature Importance (Random Forest)...")
    top_features = model_rf.get_feature_importance(feature_names, top_k=10)
    print("\n   Top 10 Most Important Features:")
    for i, (feature, importance) in enumerate(top_features, 1):
        print(f"   {i:2d}. {feature:<30s} {importance:.4f}")
    
    # Threshold sensitivity analysis
    print("\n\n🔧 STEP 8: Threshold Sensitivity Analysis...")
    thresholds = [0.3, 0.5, 0.7, 0.9]
    results = SpamDetectionEvaluator.analyze_threshold_sensitivity(y_test, y_proba_ensemble, thresholds)
    SpamDetectionEvaluator.print_threshold_analysis(results)
    
    # ==================== EXAMPLE PREDICTIONS ====================
    print("\n💡 STEP 9: Example Predictions on New Emails...\n")
    
    test_emails = [
        "Hi! Your order has been shipped. Track it here: https://example.com/track/123456",
        "CONGRATULATIONS!!! YOU HAVE WON $1,000,000!!! CLICK HERE NOW!!!",
        "Meeting scheduled for tomorrow at 2 PM. Bring the quarterly report.",
        "URGENT!!! Verify your account IMMEDIATELY!!! Click bit.ly/secure123",
        "Your appointment reminder: Dr. Smith on March 20 at 10:00 AM"
    ]
    
    # Extract features
    X_test_email = extract_features_batch(test_emails)[0]
    X_test_email = scaler.transform(X_test_email)
    
    # Predictions
    predictions = ensemble.predict_proba(X_test_email)
    
    for i, (email, prob_spam) in enumerate(zip(test_emails, predictions), 1):
        email_short = email[:60] + "..." if len(email) > 60 else email
        label = "🚨 SPAM" if prob_spam > 0.5 else "✅ HAM"
        confidence = prob_spam if prob_spam > 0.5 else (1 - prob_spam)
        print(f"{i}. [{label}] (Confidence: {confidence:.1%})")
        print(f"   Email: {email_short}\n")
    
    # ==================== SAVING MODEL ====================
    print("💾 STEP 10: Saving Model...")
    model_rf.save('spam_detector_model.pkl')
    print("   ✓ Model saved as 'spam_detector_model.pkl'")
    
    print("\n" + "="*70)
    print("✨ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70 + "\n")


def predict_single_email(email_text: str, model_path: str = 'spam_detector_model.pkl'):
    """
    Predict on a single email
    
    Args:
        email_text: Email content to classify
        model_path: Path to saved model
    """
    # Load model
    model = SpamDetectionModel.load(model_path)
    
    # Extract features
    extractor = FeatureExtractor()
    features = extractor.extract_all_features(email_text)
    
    # Predict
    prediction = model.predict(np.array([list(features.values())]))
    probability = model.predict_proba(np.array([list(features.values())]))
    
    label = "SPAM" if prediction[0] == 1 else "HAM"
    confidence = probability[0][prediction[0]]
    
    print(f"\nEmail Classification:")
    print(f"  Label: {label}")
    print(f"  Spam Probability: {probability[0][1]:.2%}")
    print(f"  Confidence: {confidence:.2%}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spam Detection System')
    parser.add_argument('--mode', type=str, default='pipeline', 
                       choices=['pipeline', 'predict'],
                       help='Mode: pipeline (full training) or predict (single email)')
    parser.add_argument('--email', type=str, help='Email text for prediction mode')
    parser.add_argument('--model', type=str, default='spam_detector_model.pkl',
                       help='Path to saved model')
    
    args = parser.parse_args()
    
    if args.mode == 'pipeline':
        main()
    elif args.mode == 'predict':
        if not args.email:
            print("Error: --email argument required for prediction mode")
            exit(1)
        predict_single_email(args.email, args.model)
