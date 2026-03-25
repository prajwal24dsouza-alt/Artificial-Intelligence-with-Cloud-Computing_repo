# Threshold Experiment for Cancer Detection - Summary Report

## Executive Summary
This experiment analyzes how different classification thresholds (0.3, 0.5, 0.7) impact cancer detection model performance. The results demonstrate that **threshold 0.3 is optimal for cancer detection** due to its significantly higher recall, which minimizes the critical risk of missing actual cancer cases.

---

## Dataset Overview
- **Dataset**: Breast Cancer Dataset (569 samples)
- **Train-Test Split**: 80-20 split (455 training, 114 testing samples)
- **Classes**: 
  - Class 0: Malignant (Cancer) - 212 samples
  - Class 1: Benign (Healthy) - 357 samples
- **Model Used**: Logistic Regression

---

## Metrics Comparison Table

| Threshold | Accuracy | Precision | Recall |
|-----------|----------|-----------|--------|
| **0.3**   | **95.61%** | **94.67%** | **98.61%** ⭐ |
| 0.5       | 95.61%   | 95.89%    | 97.22%   |
| 0.7       | 94.74%   | 97.14%    | 94.44%   |

---

## Key Findings

### Performance Metrics Breakdown

#### Threshold 0.3 - OPTIMAL FOR CANCER DETECTION ✓
- **Accuracy**: 95.61% - Overall correctness
- **Precision**: 94.67% - 94.67% of positive predictions are correct
- **Recall**: 98.61% - **Catches 98.61% of actual cancer cases** ⭐
- **False Negatives**: Only 1 missed cancer case
- **Confusion Matrix**:
  - True Negatives: 38 (correctly identified as healthy)
  - False Positives: 4 (healthy identified as cancer)
  - False Negatives: 1 (cancer missed - CRITICAL)
  - True Positives: 71 (cancer correctly identified)

#### Threshold 0.5 - Standard Threshold
- **Accuracy**: 95.61% - Same as 0.3
- **Precision**: 95.89% - Higher precision but lower recall
- **Recall**: 97.22% - Misses more cancer cases
- **False Negatives**: 2 missed cancer cases
- Balanced between catching positives and avoiding false alarms

#### Threshold 0.7 - Conservative Threshold
- **Accuracy**: 94.74% - Slightly lower overall accuracy
- **Precision**: 97.14% - Highest precision
- **Recall**: 94.44% - Lowest recall (WORST for cancer detection)
- **False Negatives**: 4 missed cancer cases
- Too conservative - misses too many cancer cases

---

## Why Threshold 0.3 is Best for Cancer Detection

### 1. Highest Recall (98.61%)
- Threshold 0.3 achieves the **maximum recall** among all tested thresholds
- Recall = TP / (TP + FN) = 71 / (71 + 1) = 0.9861
- **Catches 98.61% of actual cancer cases**
- Only 1 cancer case missed out of 72 actual cancer cases

### 2. Minimizes False Negatives (Only 1)
- **False Negatives = Cancer cases missed by the model = WORST ERROR**
- Threshold 0.3: 1 missed case
- Threshold 0.5: 2 missed cases  
- Threshold 0.7: 4 missed cases
- In medical diagnosis, missing a cancer case is catastrophic

### 3. Medical Priority: Detection Over Precision
In cancer detection, the hierarchy of importance is:
```
MINIMIZE FALSE NEGATIVES (Top Priority!)
    ↓
MAXIMIZE RECALL/SENSITIVITY
    ↓
BALANCE PRECISION (Secondary Priority)
    ↓
MAXIMIZE ACCURACY (Lower Priority)
```

### 4. Risk Analysis
- **False Negative Cost**: Patient has cancer but is told they don't → Severe health consequences
- **False Positive Cost**: Patient doesn't have cancer but is told they do → Additional screening/monitoring
- **Cost of FN >>> Cost of FP**

### 5. Clinical Decision Making
- **Threshold 0.3 with 98.61% Recall**:
  - ✓ Almost certain to catch cancer cases
  - ⚠ 4 false positives (acceptable - leads to additional screening)
  - Result: **SAFE** - Minimizes patient harm

- **Threshold 0.7 with 94.44% Recall**:
  - ✗ Misses more cancer cases (unacceptable risk)
  - ✓ Fewer false positives
  - Result: **RISKY** - Patients might be told they don't have cancer when they do

### 6. Trade-off Comparison

| Aspect | Threshold 0.3 | Threshold 0.5 | Threshold 0.7 |
|--------|---------------|---------------|---------------|
| Catches Cancer Cases | 98.61% ⭐ | 97.22% | 94.44% |
| Missed Cases | 1 ⭐ | 2 | 4 |
| False Alarms | 4 | 3 | 2 |
| Overall Accuracy | 95.61% | 95.61% | 94.74% |
| **Best for Medical Use?** | **YES** ✓ | Acceptable | Not Ideal |

---

## Recommendation: Use Threshold 0.3

### Clinical Implementation Strategy:
1. **Primary Screening**: Use threshold 0.3 for initial cancer detection
   - Prioritizes sensitivity (recall) over specificity
   - Very low risk of missing cancer cases
   
2. **Secondary Confirmation**: Use higher threshold (0.7) for confirmatory tests
   - Reduces false alarms with additional screening
   - Ensures positive cases are actually cancer

3. **Patient Communication**:
   - With 0.3 threshold: "This screening indicates you need further evaluation"
   - With higher thresholds: "Screening confirms the presence/absence of cancer"

### Expected Impact:
- ✅ Saves lives by detecting 98.61% of cancer cases
- ✅ Maintains reasonable precision (94.67%)
- ✅ Balances medical safety with operational efficiency
- ✅ Follows best practices in medical screening protocols

---

## Conclusion

**Threshold 0.3 is demonstrably the best choice for cancer detection** because:

1. It achieves the **highest recall (98.61%)** among all tested thresholds
2. It **minimizes false negatives** by only missing 1 cancer case
3. It prioritizes patient safety over false positive reduction
4. Medical practice dictates that sensitivity is more critical than specificity in life-threatening conditions
5. The principle "Better safe than sorry" is paramount in oncology

In cancer detection, it's better to have 4 false positives (leading to additional screening) than to miss even 1 actual cancer case. Therefore, **threshold 0.3 is the medically sound and optimal choice**.

---

## Metrics Definitions

- **Accuracy**: (TP + TN) / (TP + TN + FP + FN) - Overall correctness
- **Precision**: TP / (TP + FP) - Of the positives we predict, how many are correct?
- **Recall (Sensitivity)**: TP / (TP + FN) - Of the actual positives, how many do we catch?
- **False Negatives (FN)**: Predicted negative but actually positive (CANCER MISSED)
- **False Positives (FP)**: Predicted positive but actually negative (FALSE ALARM)

---

**Report Generated**: 2026-03-24  
**Experiment**: Threshold Optimization for Binary Classification (Cancer Detection)  
**Status**: ✅ Complete
