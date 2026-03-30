# Movie Review Sentiment Analyzer - Assignment Summary

## Overview
A simple sentiment analyzer for movie reviews that classifies reviews as Positive, Negative, or Neutral based on word-level sentiment analysis.

## Implementation Details

### Architecture
The analyzer uses a **lexicon-based sentiment analysis approach** with:
- **Positive word lexicon**: Contains 50+ positive sentiment words (e.g., "amazing", "excellent", "love")
- **Negative word lexicon**: Contains 50+ negative sentiment words (e.g., "terrible", "boring", "waste")
- **Intensifiers**: Words that amplify sentiment ("very", "extremely", "absolutely")
- **Negation handling**: Words like "not", "never" that reverse sentiment polarity

### Sentiment Scoring
1. **Word-level scoring**: Each sentiment word is assigned +1.0 (positive) or -1.0 (negative)
2. **Intensifier boost**: Sentiment words preceded by intensifiers get a 1.5x multiplier
3. **Negation handling**: Sentiment words after negation words have their polarity flipped
4. **Compound score**: Calculated as `(positive_score - negative_score) / total_score`, ranging from -1.0 to 1.0
5. **Classification**:
   - Positive: compound score ≥ 0.1
   - Negative: compound score ≤ -0.1
   - Neutral: compound score between -0.1 and 0.1

### Files Created

#### 1. `sentiment_analyzer.py`
Main sentiment analyzer module with the `MovieReviewAnalyzer` class.

**Key Methods:**
- `__init__()`: Initializes sentiment word dictionaries
- `analyze(review_text)`: Analyzes a single review and returns sentiment classification
- `analyze_multiple(reviews)`: Analyzes multiple reviews at once
- `print_analysis(result)`: Pretty-prints analysis results

#### 2. `test_reviews.py`
Test script that evaluates the analyzer on 5 diverse movie reviews.

**Test Reviews:**
1. **Review #1**: Highly positive ("amazing", "superb", "engaging") → **Positive** (Score: 1.0)
2. **Review #2**: Highly negative ("terrible", "boring", "awful") → **Negative** (Score: -1.0)
3. **Review #3**: Mixed sentiment ("good" vs "slow", "predictable") → **Negative** (Score: -0.33)
4. **Review #4**: Very positive ("masterpiece", "outstanding", "powerful") → **Positive** (Score: 1.0)
5. **Review #5**: Highly negative ("disappointing", "dull", "uninteresting") → **Negative** (Score: -1.0)

### Test Results

```
Total Reviews Analyzed: 5
Positive Sentiments: 2
Negative Sentiments: 3
Neutral Sentiments: 0
Average Compound Score: -0.0667
```

## How to Use

### Basic Usage
```python
from sentiment_analyzer import MovieReviewAnalyzer

analyzer = MovieReviewAnalyzer()
review = "This movie was fantastic and exceeded my expectations!"
result = analyzer.analyze(review)
print(f"Sentiment: {result['sentiment']}")
print(f"Compound Score: {result['compound_score']}")
```

### Batch Analysis
```python
reviews = [review1, review2, review3]
results = analyzer.analyze_multiple(reviews)
for result in results:
    analyzer.print_analysis(result)
```

### Run Tests
```bash
python3 test_reviews.py
```

## Advantages
- ✅ **No external dependencies**: Uses only Python's standard library
- ✅ **Fast execution**: No model training required
- ✅ **Transparent**: Easy to understand how sentiment is calculated
- ✅ **Customizable**: Easy to add/remove sentiment words

## Limitations
- Doesn't understand sarcasm or irony
- Limited context awareness
- May struggle with complex sentence structures
- Depends on predefined word lists

## Future Enhancements
- Add support for sarcasm detection
- Expand sentiment word lexicon
- Implement phrase-level analysis
- Add aspect-based sentiment analysis
