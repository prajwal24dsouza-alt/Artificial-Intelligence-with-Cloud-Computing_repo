"""
Spam Detection API - Simple interface for using the spam detector
"""

from typing import Dict, List, Tuple
import numpy as np
from features import FeatureExtractor, extract_features_batch
from model import SpamDetectionModel, EnsembleSpamDetector
from data_loader import DataLoader
from evaluate import SpamDetectionEvaluator
import os


class SpamDetectorAPI:
    """
    Simple API for spam detection
    
    Usage:
        detector = SpamDetectorAPI()
        result = detector.classify("Your email text here")
    """
    
    def __init__(self, model_path: str = 'spam_detector_model.pkl'):
        """
        Initialize detector with pre-trained model
        
        Args:
            model_path: Path to saved model
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_extractor = FeatureExtractor()
        
        if os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """
        Load pre-trained model
        
        Args:
            model_path: Path to model file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.model = SpamDetectionModel.load(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def train_from_data(self, emails: List[str], labels: List[int], 
                       model_type: str = 'random_forest') -> Dict:
        """
        Train a new model from email data
        
        Args:
            emails: List of email texts
            labels: List of labels (0=ham, 1=spam)
            model_type: Type of model to train
            
        Returns:
            Dictionary with training results
        """
        # Extract features
        X, feature_names = extract_features_batch(emails)
        y = np.array(labels)
        
        # Preprocess
        X_train, X_test, y_train, y_test, scaler = DataLoader.preprocess_data(X, y)
        
        # Train
        self.model = SpamDetectionModel(model_type=model_type)
        self.model.train(X_train, y_train)
        self.scaler = scaler
        
        # Evaluate
        predictions = self.model.predict(X_test)
        metrics = SpamDetectionEvaluator.evaluate(y_test, predictions)
        
        return {
            'status': 'success',
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1'],
            'feature_count': X.shape[1],
            'training_samples': X_train.shape[0],
            'test_samples': X_test.shape[0],
        }
    
    def classify(self, email_text: str, threshold: float = 0.5) -> Dict:
        """
        Classify a single email
        
        Args:
            email_text: Email content to classify
            threshold: Decision threshold (0-1)
            
        Returns:
            Dictionary with classification result
        """
        if self.model is None:
            return {
                'status': 'error',
                'message': 'Model not loaded. Call load_model() first.'
            }
        
        # Extract features
        features = self.feature_extractor.extract_all_features(email_text)
        feature_vector = np.array([list(features.values())])
        
        # Scale features
        if self.scaler:
            feature_vector = self.scaler.transform(feature_vector)
        
        # Predict
        prediction = self.model.predict(feature_vector)[0]
        probability = self.model.predict_proba(feature_vector)[0]
        
        spam_prob = probability[1]
        is_spam = spam_prob > threshold
        confidence = spam_prob if is_spam else (1 - spam_prob)
        
        return {
            'status': 'success',
            'is_spam': bool(is_spam),
            'spam_probability': float(spam_prob),
            'ham_probability': float(probability[0]),
            'confidence': float(confidence),
            'label': 'SPAM' if is_spam else 'HAM',
            'threshold': threshold,
        }
    
    def classify_batch(self, emails: List[str], 
                      threshold: float = 0.5) -> List[Dict]:
        """
        Classify multiple emails
        
        Args:
            emails: List of email texts
            threshold: Decision threshold (0-1)
            
        Returns:
            List of classification results
        """
        if self.model is None:
            return [{'status': 'error', 'message': 'Model not loaded'}]
        
        results = []
        for email in emails:
            results.append(self.classify(email, threshold))
        
        return results
    
    def analyze_email(self, email_text: str) -> Dict:
        """
        Detailed analysis of email features
        
        Args:
            email_text: Email content to analyze
            
        Returns:
            Dictionary with feature analysis
        """
        features = self.feature_extractor.extract_all_features(email_text)
        
        # Categorize features
        analysis = {
            'basic_stats': {
                'character_count': int(features.get('char_count', 0)),
                'word_count': int(features.get('word_count', 0)),
                'sentence_count': int(features.get('sentence_count', 0)),
                'avg_word_length': float(features.get('avg_word_length', 0)),
            },
            'spam_indicators': {
                'exclamation_marks': int(features.get('exclamation_count', 0)),
                'question_marks': int(features.get('question_count', 0)),
                'caps_words': int(features.get('all_caps_words', 0)),
                'spam_keywords': int(features.get('spam_keyword_count', 0)),
                'urls': int(features.get('url_count', 0)),
                'short_urls': int(features.get('short_url_count', 0)),
            },
            'ratios': {
                'capital_chars': float(features.get('capital_char_ratio', 0)),
                'special_chars': float(features.get('special_char_ratio', 0)),
                'digits': float(features.get('digit_ratio', 0)),
                'spam_keywords': float(features.get('spam_keyword_ratio', 0)),
            },
            'linguistic': {
                'pronoun_count': int(features.get('pronoun_count', 0)),
                'repeated_chars': int(features.get('repeated_char_count', 0)),
                'repeated_words': int(features.get('repeated_words_count', 0)),
            },
            'special_patterns': {
                'html_tags': int(features.get('html_tag_count', 0)),
                'monetary_refs': int(features.get('monetary_ref_count', 0)),
                'action_requests': int(features.get('action_request_count', 0)),
                'urgency_words': int(features.get('urgency_count', 0)),
            }
        }
        
        return analysis
    
    def get_feature_importance(self, top_k: int = 15) -> List[Tuple[str, float]]:
        """
        Get most important features for spam detection
        
        Args:
            top_k: Number of top features to return
            
        Returns:
            List of (feature_name, importance) tuples
        """
        # Get feature names from a sample
        dummy_email = "test"
        features = self.feature_extractor.extract_all_features(dummy_email)
        feature_names = list(features.keys())
        
        if self.model:
            return self.model.get_feature_importance(feature_names, top_k)
        return []
    
    def save_model(self, file_path: str) -> bool:
        """
        Save trained model
        
        Args:
            file_path: Path to save model
            
        Returns:
            True if successful
        """
        if self.model:
            self.model.save(file_path)
            return True
        return False


# Quick functions for simple usage
def classify(email_text: str, model_path: str = 'spam_detector_model.pkl') -> str:
    """Quick classification function"""
    detector = SpamDetectorAPI(model_path)
    result = detector.classify(email_text)
    return result['label']


def get_spam_probability(email_text: str, 
                         model_path: str = 'spam_detector_model.pkl') -> float:
    """Get spam probability for email"""
    detector = SpamDetectorAPI(model_path)
    result = detector.classify(email_text)
    return result['spam_probability']


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("SPAM DETECTION API - EXAMPLE USAGE")
    print("="*70)
    
    # Train new model
    print("\n1️⃣  Training new model...")
    detector = SpamDetectorAPI()
    
    emails, labels = DataLoader.generate_synthetic_data(n_samples=500, spam_ratio=0.3)
    result = detector.train_from_data(emails, labels)
    
    print(f"   Training completed!")
    print(f"   Accuracy: {result['accuracy']:.2%}")
    print(f"   F1-Score: {result['f1_score']:.2%}")
    
    # Classify emails
    print("\n2️⃣  Classifying emails...")
    test_emails = [
        "Hi! Your order has shipped.",
        "CONGRATULATIONS! YOU WON $1,000,000!!!",
        "Meeting scheduled for tomorrow.",
        "URGENT! Verify your account NOW!!!",
    ]
    
    results = detector.classify_batch(test_emails)
    for email, result in zip(test_emails, results):
        print(f"\n   Email: {email[:50]}...")
        print(f"   Label: {result['label']}")
        print(f"   Spam Probability: {result['spam_probability']:.1%}")
        print(f"   Confidence: {result['confidence']:.1%}")
    
    # Analyze email
    print("\n3️⃣  Detailed email analysis...")
    analysis = detector.analyze_email(test_emails[3])
    print(f"\n   Spam Indicators:")
    for key, value in analysis['spam_indicators'].items():
        print(f"      {key}: {value}")
    
    # Feature importance
    print("\n4️⃣  Feature importance...")
    top_features = detector.get_feature_importance(top_k=5)
    print(f"\n   Top 5 Features for Spam Detection:")
    for i, (feature, importance) in enumerate(top_features, 1):
        print(f"      {i}. {feature}: {importance:.4f}")
    
    # Save model
    print("\n5️⃣  Saving model...")
    detector.save_model('spam_detector_api.pkl')
    print(f"   ✓ Model saved as 'spam_detector_api.pkl'")
    
    print("\n" + "="*70)
    print("✨ API EXAMPLE COMPLETED!")
    print("="*70 + "\n")
