"""
Feature Extraction Module for Spam Detection
Extracts text and metadata features from emails
"""

import re
import string
from typing import Dict, List, Tuple
import numpy as np


class FeatureExtractor:
    """Extract various features from email text for spam classification"""
    
    # Common spam keywords
    SPAM_KEYWORDS = {
        'urgent', 'winner', 'congratulations', 'claim reward', 'limited time',
        'act now', 'click here', 'buy now', 'free', 'money', 'password',
        'verify account', 'confirm identity', 'update payment', 'suspended',
        'urgent action required', 'unsubscribe', 'viagra', 'dear friend'
    }
    
    def __init__(self):
        self.feature_names = []
    
    def extract_all_features(self, email_text: str) -> Dict[str, float]:
        """
        Extract all features from email text
        
        Args:
            email_text: Raw email content
            
        Returns:
            Dictionary of feature names and values
        """
        features = {}
        
        # Normalize text
        text_lower = email_text.lower()
        text_clean = self._clean_text(email_text)
        
        # Text statistics
        features.update(self._extract_text_stats(email_text, text_lower, text_clean))
        
        # Character patterns
        features.update(self._extract_character_patterns(email_text))
        
        # URL features
        features.update(self._extract_url_features(text_lower))
        
        # Spam keyword features
        features.update(self._extract_spam_keywords(text_lower))
        
        # Linguistic patterns
        features.update(self._extract_linguistic_features(text_clean))
        
        # Special patterns
        features.update(self._extract_special_patterns(email_text, text_lower))
        
        return features
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove special characters and normalize whitespace"""
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_text_stats(self, text: str, text_lower: str, text_clean: str) -> Dict[str, float]:
        """Extract basic text statistics"""
        words = text_clean.split()
        features = {}
        
        features['char_count'] = len(text)
        features['word_count'] = len(words)
        features['avg_word_length'] = np.mean([len(w) for w in words]) if words else 0
        features['unique_words_ratio'] = len(set(words)) / len(words) if words else 0
        features['sentence_count'] = max(1, len(re.split(r'[.!?]', text)))
        features['avg_sentence_length'] = features['word_count'] / features['sentence_count']
        
        return features
    
    def _extract_character_patterns(self, text: str) -> Dict[str, float]:
        """Extract character-level patterns"""
        features = {}
        
        # Capital letters
        capital_chars = sum(1 for c in text if c.isupper())
        features['capital_char_ratio'] = capital_chars / len(text) if text else 0
        
        # Numbers
        digit_count = sum(1 for c in text if c.isdigit())
        features['digit_ratio'] = digit_count / len(text) if text else 0
        
        # Special characters
        special_chars = sum(1 for c in text if c in string.punctuation)
        features['special_char_ratio'] = special_chars / len(text) if text else 0
        
        # Whitespace
        space_count = text.count(' ')
        features['whitespace_ratio'] = space_count / len(text) if text else 0
        
        # Exclamation marks and question marks (spam indicators)
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['ellipsis_count'] = text.count('...')
        
        return features
    
    def _extract_url_features(self, text: str) -> Dict[str, float]:
        """Extract URL-related features"""
        features = {}
        
        # Find URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        features['url_count'] = len(urls)
        
        # Shortened URLs (common in spam)
        short_url_pattern = r'(?:bit\.ly|tinyurl|goo\.gl|ow\.ly|short\.link)'
        features['short_url_count'] = len(re.findall(short_url_pattern, text))
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        features['email_count'] = len(re.findall(email_pattern, text))
        
        # IP addresses (sometimes used in spam)
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        features['ip_count'] = len(re.findall(ip_pattern, text))
        
        return features
    
    def _extract_spam_keywords(self, text: str) -> Dict[str, float]:
        """Extract spam keyword features"""
        features = {}
        
        spam_keyword_count = 0
        text_words = set(re.findall(r'\b\w+\b', text))
        
        for keyword in self.SPAM_KEYWORDS:
            if keyword in text:
                spam_keyword_count += 1
        
        features['spam_keyword_count'] = spam_keyword_count
        features['spam_keyword_ratio'] = spam_keyword_count / len(text_words) if text_words else 0
        
        return features
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, float]:
        """Extract linguistic patterns"""
        features = {}
        
        words = text.split()
        
        # Repeated characters (like "hhheeeelllooo")
        repeated_char_count = len(re.findall(r'(.)\1{2,}', text))
        features['repeated_char_count'] = repeated_char_count
        
        # Repeated words
        if words:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            repeated_words = sum(1 for count in word_freq.values() if count > 3)
            features['repeated_words_count'] = repeated_words
        else:
            features['repeated_words_count'] = 0
        
        # Pronouns (more common in legitimate emails)
        pronouns = {'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        features['pronoun_count'] = sum(1 for word in words if word.lower() in pronouns)
        
        # All caps words (spam indicator)
        all_caps_words = sum(1 for word in words if len(word) > 1 and word.isupper())
        features['all_caps_words'] = all_caps_words
        
        return features
    
    def _extract_special_patterns(self, text: str, text_lower: str) -> Dict[str, float]:
        """Extract special patterns"""
        features = {}
        
        # HTML tags (common in phishing/spam)
        features['html_tag_count'] = len(re.findall(r'<[^>]+>', text))
        
        # Numbers like "1.5M" or "$100"
        features['monetary_ref_count'] = len(re.findall(r'\$\d+|£\d+|€\d+', text))
        features['numeric_pattern_count'] = len(re.findall(r'\d+\.?\d*', text))
        
        # Requests for action words
        action_words = {'confirm', 'verify', 'validate', 'authenticate', 'update', 'reset'}
        action_count = sum(1 for action in action_words if action in text_lower)
        features['action_request_count'] = action_count
        
        # Urgency words
        urgency_words = {'urgent', 'immediately', 'asap', 'hurry', 'act now', 'quickly'}
        urgency_count = sum(1 for urgency in urgency_words if urgency in text_lower)
        features['urgency_count'] = urgency_count
        
        return features


def extract_features_batch(emails: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Extract features from multiple emails
    
    Args:
        emails: List of email texts
        
    Returns:
        Tuple of (feature matrix, feature names)
    """
    extractor = FeatureExtractor()
    feature_dicts = [extractor.extract_all_features(email) for email in emails]
    
    # Get all feature names
    all_features = set()
    for fd in feature_dicts:
        all_features.update(fd.keys())
    
    feature_names = sorted(list(all_features))
    
    # Create feature matrix
    feature_matrix = []
    for fd in feature_dicts:
        row = [fd.get(fname, 0) for fname in feature_names]
        feature_matrix.append(row)
    
    return np.array(feature_matrix), feature_names
