"""
Evaluation Metrics for Spam Detection
"""

import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, auc,
    classification_report, accuracy_score
)
import matplotlib.pyplot as plt


class SpamDetectionEvaluator:
    """Evaluate spam detection model performance"""
    
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> Dict[str, float]:
        """
        Compute comprehensive evaluation metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities (optional)
            
        Returns:
            Dictionary of metrics
        """
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        metrics['precision'] = precision_score(y_true, y_pred, zero_division=0)
        metrics['recall'] = recall_score(y_true, y_pred, zero_division=0)
        metrics['f1'] = f1_score(y_true, y_pred, zero_division=0)
        
        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        metrics['true_negatives'] = int(tn)
        metrics['false_positives'] = int(fp)
        metrics['false_negatives'] = int(fn)
        metrics['true_positives'] = int(tp)
        
        # Additional metrics
        metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
        metrics['false_positive_rate'] = fp / (fp + tn) if (fp + tn) > 0 else 0
        metrics['false_negative_rate'] = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        # ROC-AUC if probabilities provided
        if y_proba is not None and len(np.unique(y_true)) == 2:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba)
        
        return metrics
    
    @staticmethod
    def print_report(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> None:
        """
        Print detailed evaluation report
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities (optional)
        """
        metrics = SpamDetectionEvaluator.evaluate(y_true, y_pred, y_proba)
        
        print("\n" + "="*60)
        print("SPAM DETECTION MODEL EVALUATION REPORT")
        print("="*60)
        
        print("\n📊 PERFORMANCE METRICS:")
        print(f"  Accuracy:              {metrics['accuracy']:.4f}")
        print(f"  Precision:             {metrics['precision']:.4f}")
        print(f"  Recall (Sensitivity):  {metrics['recall']:.4f}")
        print(f"  F1-Score:              {metrics['f1']:.4f}")
        print(f"  Specificity:           {metrics['specificity']:.4f}")
        
        if 'roc_auc' in metrics:
            print(f"  ROC-AUC:               {metrics['roc_auc']:.4f}")
        
        print("\n📈 CONFUSION MATRIX:")
        print(f"  True Negatives:        {metrics['true_negatives']:5d}")
        print(f"  False Positives:       {metrics['false_positives']:5d}")
        print(f"  False Negatives:       {metrics['false_negatives']:5d}")
        print(f"  True Positives:        {metrics['true_positives']:5d}")
        
        print("\n⚠️  ERROR RATES:")
        print(f"  False Positive Rate:   {metrics['false_positive_rate']:.4f}")
        print(f"  False Negative Rate:   {metrics['false_negative_rate']:.4f}")
        
        print("\n📋 CLASSIFICATION REPORT:")
        print(classification_report(y_true, y_pred, 
                                  target_names=['Ham (Legitimate)', 'Spam']))
        print("="*60 + "\n")
    
    @staticmethod
    def plot_roc_curve(y_true: np.ndarray, y_proba: np.ndarray, save_path: str = None) -> None:
        """
        Plot ROC curve
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            save_path: Path to save figure (optional)
        """
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve - Spam Detection')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def plot_precision_recall_curve(y_true: np.ndarray, y_proba: np.ndarray, 
                                   save_path: str = None) -> None:
        """
        Plot Precision-Recall curve
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            save_path: Path to save figure (optional)
        """
        precision, recall, _ = precision_recall_curve(y_true, y_proba)
        pr_auc = auc(recall, precision)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='green', lw=2, label=f'PR curve (AUC = {pr_auc:.3f})')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve - Spam Detection')
        plt.legend(loc="best")
        plt.grid(alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, save_path: str = None) -> None:
        """
        Plot confusion matrix heatmap
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            save_path: Path to save figure (optional)
        """
        try:
            import seaborn as sns
        except ImportError:
            print("seaborn not installed. Skipping confusion matrix plot.")
            return
        
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                   xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
        plt.title('Confusion Matrix - Spam Detection')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def analyze_threshold_sensitivity(y_true: np.ndarray, y_proba: np.ndarray,
                                     thresholds: List[float] = None) -> Dict[float, Dict[str, float]]:
        """
        Analyze model performance across different thresholds
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            thresholds: List of thresholds to test
            
        Returns:
            Dictionary mapping threshold to metrics
        """
        if thresholds is None:
            thresholds = np.arange(0.1, 1.0, 0.1)
        
        results = {}
        for threshold in thresholds:
            y_pred = (y_proba >= threshold).astype(int)
            metrics = SpamDetectionEvaluator.evaluate(y_true, y_pred, y_proba)
            results[threshold] = metrics
        
        return results
    
    @staticmethod
    def print_threshold_analysis(results: Dict[float, Dict[str, float]]) -> None:
        """
        Print threshold sensitivity analysis
        
        Args:
            results: Results from analyze_threshold_sensitivity
        """
        print("\n" + "="*80)
        print("THRESHOLD SENSITIVITY ANALYSIS")
        print("="*80)
        print(f"{'Threshold':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'FP Rate':<12}")
        print("-"*80)
        
        for threshold in sorted(results.keys()):
            m = results[threshold]
            print(f"{threshold:<12.2f} {m['precision']:<12.4f} {m['recall']:<12.4f} "
                  f"{m['f1']:<12.4f} {m['false_positive_rate']:<12.4f}")
        
        print("="*80 + "\n")
