"""
Model Training and Prediction for Spam Detection
"""

import pickle
from typing import Dict, List, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import warnings

warnings.filterwarnings('ignore')


class SpamDetectionModel:
    """Spam detection model wrapper supporting multiple algorithms"""
    
    def __init__(self, model_type: str = 'random_forest'):
        """
        Initialize model
        
        Args:
            model_type: Type of model ('random_forest', 'gradient_boosting', 'logistic_regression', 'svm')
        """
        self.model_type = model_type
        self.model = self._create_model()
        self.is_trained = False
        self.feature_importance = None
    
    def _create_model(self):
        """Create the selected model"""
        if self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif self.model_type == 'logistic_regression':
            return LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'svm':
            return SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Extract feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = self.model.feature_importances_
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict labels
        
        Args:
            X: Features
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities
        
        Args:
            X: Features
            
        Returns:
            Probability matrix (n_samples, 2)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict_proba(X)
    
    def cross_validate(self, X: np.ndarray, y: np.ndarray, cv: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation
        
        Args:
            X: Features
            y: Labels
            cv: Number of folds
            
        Returns:
            Dictionary with cv scores
        """
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='f1')
        return {
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'scores': scores
        }
    
    def save(self, file_path: str) -> None:
        """
        Save model to file
        
        Args:
            file_path: Path to save model
        """
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(file_path: str) -> 'SpamDetectionModel':
        """
        Load model from file
        
        Args:
            file_path: Path to load model from
            
        Returns:
            Loaded model
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    def get_feature_importance(self, feature_names: List[str], top_k: int = 15) -> List[Tuple[str, float]]:
        """
        Get top K most important features
        
        Args:
            feature_names: List of feature names
            top_k: Number of top features to return
            
        Returns:
            List of (feature_name, importance) tuples
        """
        if self.feature_importance is None:
            return []
        
        importance_dict = dict(zip(feature_names, self.feature_importance))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_importance[:top_k]


class EnsembleSpamDetector:
    """Ensemble of multiple spam detection models"""
    
    def __init__(self, model_types: List[str] = None):
        """
        Initialize ensemble
        
        Args:
            model_types: List of model types to ensemble
        """
        if model_types is None:
            model_types = ['random_forest', 'gradient_boosting', 'logistic_regression']
        
        self.models = [SpamDetectionModel(mt) for mt in model_types]
        self.is_trained = False
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train all models in ensemble
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        for model in self.models:
            model.train(X_train, y_train)
        self.is_trained = True
    
    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Predict using majority voting
        
        Args:
            X: Features
            threshold: Confidence threshold (0-1)
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Models must be trained before prediction")
        
        probas = self.predict_proba(X)
        predictions = (probas > threshold).astype(int)
        
        return predictions
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Average probabilities from all models
        
        Args:
            X: Features
            
        Returns:
            Average probability of spam
        """
        if not self.is_trained:
            raise ValueError("Models must be trained before prediction")
        
        probas = np.array([model.predict_proba(X)[:, 1] for model in self.models])
        return probas.mean(axis=0)
