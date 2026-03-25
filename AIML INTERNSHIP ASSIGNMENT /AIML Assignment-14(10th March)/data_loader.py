"""
Data Loading and Preprocessing for Spam Detection
"""

import numpy as np
from typing import Tuple, List
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import csv


class DataLoader:
    """Load and preprocess spam detection data"""
    
    @staticmethod
    def load_from_csv(file_path: str) -> Tuple[List[str], List[int]]:
        """
        Load emails and labels from CSV file
        Expected format: email_text, label (0=ham, 1=spam)
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Tuple of (emails, labels)
        """
        emails = []
        labels = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        emails.append(row[0])
                        labels.append(int(row[1]))
        except FileNotFoundError:
            print(f"File {file_path} not found")
            return [], []
        
        return emails, labels
    
    @staticmethod
    def generate_synthetic_data(n_samples: int = 1000, 
                                spam_ratio: float = 0.3) -> Tuple[List[str], List[int]]:
        """
        Generate synthetic email data for testing/demo purposes
        
        Args:
            n_samples: Number of samples to generate
            spam_ratio: Ratio of spam (0-1)
            
        Returns:
            Tuple of (emails, labels)
        """
        np.random.seed(42)
        emails = []
        labels = []
        
        # Legitimate email templates
        legit_templates = [
            "Hi {}, your order #{} has been shipped. Tracking: {}",
            "Reminder: Your appointment with {} is on {} at {}.",
            "Thanks for your purchase. Your receipt is attached.",
            "Welcome to our service. Please verify your email at {}",
            "New message from {}: {}",
            "Your subscription renews on {}. Manage your account here.",
            "Project update: {} is now complete. Review the details below.",
            "Meeting scheduled for {} to discuss {}",
        ]
        
        # Spam email templates
        spam_templates = [
            "CONGRATULATIONS !!! You have WON! Click here to claim your prize NOW!!!",
            "URGENT: Verify your account IMMEDIATELY!!! Click http://bit.ly/{}",
            "FREE FREE FREE! Limited time offer! $$$$ MONEY BACK!!!",
            "You are the LUCKY WINNER! Claim your reward ASAP!!!",
            "Urgent action required! Your account has been SUSPENDED!!!",
            "Special offer!!! GET 50% OFF TODAY ONLY!!! Act now!!!",
            "Update your password here: http://malicious-link.com/{}",
            "CLICK HERE IMMEDIATELY! This is your LAST CHANCE!!!",
            "Viagra, cialis, painkillers - BEST PRICES GUARANTEED!!!",
            "You have won $1,000,000!!! Respond with your details NOW!!!",
        ]
        
        n_spam = int(n_samples * spam_ratio)
        n_legit = n_samples - n_spam
        
        # Generate spam emails
        for _ in range(n_spam):
            template = np.random.choice(spam_templates)
            email = template.format(np.random.randint(1000, 9999))
            emails.append(email)
            labels.append(1)
        
        # Generate legitimate emails
        for _ in range(n_legit):
            template = np.random.choice(legit_templates)
            email = template.format(
                f"User{np.random.randint(100, 999)}",
                np.random.randint(100000, 999999),
                f"2024-03-{np.random.randint(1, 28):02d}"
            )
            emails.append(email)
            labels.append(0)
        
        # Shuffle
        indices = np.random.permutation(n_samples)
        emails = [emails[i] for i in indices]
        labels = [labels[i] for i in indices]
        
        return emails, labels
    
    @staticmethod
    def preprocess_data(X: np.ndarray, 
                       y: np.ndarray,
                       test_size: float = 0.2,
                       random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, 
                                                         np.ndarray, np.ndarray,
                                                         StandardScaler]:
        """
        Split and normalize data
        
        Args:
            X: Feature matrix
            y: Labels
            test_size: Train/test split ratio
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test, scaler)
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        return X_train, X_test, y_train, y_test, scaler
    
    @staticmethod
    def balance_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Balance imbalanced dataset using undersampling of majority class
        
        Args:
            X: Feature matrix
            y: Labels
            
        Returns:
            Balanced (X, y)
        """
        class_0_idx = np.where(y == 0)[0]
        class_1_idx = np.where(y == 1)[0]
        
        minority_size = min(len(class_0_idx), len(class_1_idx))
        
        # Sample equally from both classes
        class_0_sample = np.random.choice(class_0_idx, minority_size, replace=False)
        class_1_sample = np.random.choice(class_1_idx, minority_size, replace=False)
        
        balanced_idx = np.concatenate([class_0_sample, class_1_sample])
        np.random.shuffle(balanced_idx)
        
        return X[balanced_idx], y[balanced_idx]
