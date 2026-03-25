#!/usr/bin/env python3
"""
Quick Reference Tests for Spam Detection System
Run individual tests to verify system functionality
"""

import sys
import numpy as np
from features import FeatureExtractor, extract_features_batch
from data_loader import DataLoader
from model import SpamDetectionModel, EnsembleSpamDetector
from evaluate import SpamDetectionEvaluator


def test_feature_extraction():
    """Test 1: Feature Extraction"""
    print("\n" + "="*60)
    print("TEST 1: Feature Extraction")
    print("="*60)
    
    sample_emails = [
        "Hi! Your order has shipped.",
        "CONGRATULATIONS!!! YOU WON $1,000,000!!!",
        "Meeting tomorrow at 2pm.",
        "URGENT ACTION NEEDED! CLICK HERE NOW!!!",
    ]
    
    extractor = FeatureExtractor()
    
    for i, email in enumerate(sample_emails, 1):
        features = extractor.extract_all_features(email)
        print(f"\nEmail {i}: {email[:40]}...")
        print(f"  Features extracted: {len(features)}")
        print(f"  Exclamation marks: {features.get('exclamation_count', 0)}")
        print(f"  Capital word ratio: {features.get('capital_char_ratio', 0):.3f}")
        print(f"  Spam keywords: {features.get('spam_keyword_count', 0)}")
    
    print("\n✓ Feature extraction test passed!\n")


def test_data_loading():
    """Test 2: Data Loading & Preprocessing"""
    print("="*60)
    print("TEST 2: Data Loading & Preprocessing")
    print("="*60)
    
    # Generate data
    emails, labels = DataLoader.generate_synthetic_data(n_samples=100, spam_ratio=0.3)
    print(f"\n✓ Generated {len(emails)} emails")
    print(f"  Spam: {sum(labels)}, Ham: {len(labels) - sum(labels)}")
    
    # Extract features
    X, feature_names = extract_features_batch(emails)
    y = np.array(labels)
    print(f"\n✓ Extracted {X.shape[1]} features from {X.shape[0]} emails")
    
    # Preprocess
    X_train, X_test, y_train, y_test, scaler = DataLoader.preprocess_data(X, y, test_size=0.2)
    print(f"\n✓ Data preprocessing complete")
    print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    print(f"  Features scaled: min={X_train.min():.3f}, max={X_train.max():.3f}")
    
    print("\n✓ Data loading test passed!\n")
    return X_train, X_test, y_train, y_test, feature_names


def test_model_training(X_train, X_test, y_train, y_test):
    """Test 3: Model Training"""
    print("="*60)
    print("TEST 3: Model Training")
    print("="*60)
    
    models = ['random_forest', 'gradient_boosting', 'logistic_regression']
    
    for model_type in models:
        model = SpamDetectionModel(model_type=model_type)
        model.train(X_train, y_train)
        accuracy = model.model.score(X_test, y_test)
        print(f"\n✓ {model_type}")
        print(f"  Accuracy: {accuracy:.3f}")
    
    print("\n✓ Model training test passed!\n")


def test_ensemble_model(X_train, X_test, y_train, y_test):
    """Test 4: Ensemble Model"""
    print("="*60)
    print("TEST 4: Ensemble Model")
    print("="*60)
    
    ensemble = EnsembleSpamDetector()
    ensemble.train(X_train, y_train)
    
    predictions = ensemble.predict(X_test)
    probabilities = ensemble.predict_proba(X_test)
    
    print(f"\n✓ Ensemble trained with {len(ensemble.models)} models")
    print(f"  Predictions shape: {predictions.shape}")
    print(f"  Probabilities shape: {probabilities.shape}")
    print(f"  Spam detected: {np.sum(predictions)} out of {len(predictions)}")
    
    metrics = SpamDetectionEvaluator.evaluate(y_test, predictions, probabilities)
    print(f"\n  Metrics:")
    print(f"    Accuracy: {metrics['accuracy']:.3f}")
    print(f"    Precision: {metrics['precision']:.3f}")
    print(f"    Recall: {metrics['recall']:.3f}")
    print(f"    F1-Score: {metrics['f1']:.3f}")
    
    print("\n✓ Ensemble test passed!\n")


def test_predictions():
    """Test 5: Single Email Predictions"""
    print("="*60)
    print("TEST 5: Single Email Predictions")
    print("="*60)
    
    # Train quick model
    emails, labels = DataLoader.generate_synthetic_data(n_samples=500, spam_ratio=0.3)
    X, feature_names = extract_features_batch(emails)
    y = np.array(labels)
    
    X_train, X_test, y_train, y_test, scaler = DataLoader.preprocess_data(X, y)
    
    model = SpamDetectionModel('random_forest')
    model.train(X_train, y_train)
    
    # Test emails
    test_emails = [
        "Your order has been shipped.",
        "CLICK HERE NOW TO WIN $1000000!!!",
        "Meeting scheduled for Friday",
        "URGENT! Verify your account IMMEDIATELY!!!",
    ]
    
    X_test_emails, _ = extract_features_batch(test_emails)
    X_test_emails = scaler.transform(X_test_emails)
    
    print("\nPredictions:")
    for email, prob in zip(test_emails, model.predict_proba(X_test_emails)[:, 1]):
        label = "SPAM" if prob > 0.5 else "HAM"
        print(f"  [{label}] {email[:50]}...")
    
    print("\n✓ Prediction test passed!\n")


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "SPAM DETECTION SYSTEM - TESTS" + " "*16 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        test_feature_extraction()
        X_train, X_test, y_train, y_test, feature_names = test_data_loading()
        test_model_training(X_train, X_test, y_train, y_test)
        test_ensemble_model(X_train, X_test, y_train, y_test)
        test_predictions()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour spam detection system is ready to use!")
        print("Run: python main.py --mode pipeline")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
