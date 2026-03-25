# Movie Review Classifier - TF-IDF Sentiment Analysis

## Project Overview
This project implements a machine learning-based movie review classifier that categorizes reviews into three sentiment classes: **Positive**, **Negative**, and **Neutral**. The model uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization for feature extraction and Multinomial Naive Bayes for classification.

## ✅ Requirements Met

### 1. **Dataset** (20+ Sentences)
- Created a dataset with **24 movie review sentences**
- Balanced distribution: 8 positive, 8 negative, 8 neutral reviews
- Reviews cover various aspects like acting, cinematography, plot, and overall experience

### 2. **Classification Classes** (3 Classes)
- **Positive**: Reviews expressing satisfaction and praise
- **Negative**: Reviews expressing dissatisfaction and criticism  
- **Neutral**: Reviews expressing mixed or average opinions

### 3. **Bonus: TF-IDF Vectorization** ✨
- Implemented using `TfidfVectorizer` from scikit-learn
- **Advantages over CountVectorizer:**
  - Reduces impact of frequently occurring words with low discriminative value
  - Weights terms by their importance and rarity across documents
  - Better for text classification by emphasizing distinctive terms
  - Produces normalized feature vectors

## Project Structure

### Notebook: `Movie_Review_Classifier.ipynb`

#### Section 1: Import Required Libraries
- pandas, numpy for data manipulation
- scikit-learn for ML algorithms and feature extraction
- nltk for text processing
- matplotlib, seaborn for visualization

#### Section 2: Load and Explore Dataset
- Creates 24 movie reviews with balanced sentiment labels
- Displays dataset shape, class distribution, and sample reviews
- Shows data statistics

#### Section 3: Preprocess Text Data
- Converts text to lowercase
- Removes punctuation and special characters
- Removes English stopwords
- Demonstrates original vs. processed review comparison

#### Section 4: Vectorize with TF-IDF
- Initializes `TfidfVectorizer` with optimized parameters:
  - max_features: 100 (top 100 features)
  - ngram_range: (1, 2) (unigrams and bigrams)
- Displays feature matrix shape and sample TF-IDF scores
- Shows top features for first document

#### Section 5: Split Data
- Divides dataset: 80% training (19 samples), 20% testing (5 samples)
- Uses stratified split to maintain class distribution
- Displays class distribution for both sets

#### Section 6: Train Classification Model
- Algorithm: **Multinomial Naive Bayes**
- Trains on TF-IDF transformed training data
- Shows training and testing accuracy

#### Section 7: Evaluate Performance
- **Metrics Calculated:**
  - Overall Accuracy
  - Weighted Precision, Recall, F1-Score
  - Detailed classification report per class
  - Confusion matrix
- **Visualization:** Confusion matrix heatmap

#### Section 8: Test with Custom Reviews
- Tests model on 6 new custom movie reviews
- Displays predicted sentiment and confidence scores for each class
- Demonstrates real-world usage capability

## Model Performance

### Classification Results
The model successfully classifies movie reviews with high confidence:

**Example Predictions:**
- ✅ "This movie is a masterpiece! I absolutely loved it!" → **Positive** (79.81% confidence)
- ✅ "Terrible film, waste of time and money. Very disappointing." → **Negative** (93.68% confidence)
- ✅ "It was okay, neither good nor bad. Just average." → **Neutral** (92.07% confidence)
- ✅ "Outstanding performance by all actors! Best movie ever!" → **Positive** (73.24% confidence)

## Key Features

### TF-IDF Advantages
```
Why TF-IDF over CountVectorizer:
1. Normalization: Handles documents of different lengths
2. Inverse Document Frequency: Down-weights common words across corpus
3. Better Discrimination: Emphasizes unique/distinctive terms
4. Improved Accuracy: Better feature representation for classification
```

### Model Architecture
```
Raw Text → Preprocessing → TF-IDF Vectorization → Naive Bayes Classifier → Sentiment Prediction
```

## Technologies Used
- **Python 3.14.3**
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **nltk**: Natural Language Toolkit
- **matplotlib & seaborn**: Data visualization

## How to Use

### Prerequisites
```bash
pip install pandas numpy scikit-learn nltk matplotlib seaborn
```

### Running the Notebook
1. Open `Movie_Review_Classifier.ipynb` in Jupyter Notebook
2. Run cells sequentially from top to bottom
3. The notebook will:
   - Train the model
   - Display evaluation metrics
   - Test with custom reviews

### Making Predictions
```python
# Preprocess your review
processed_review = preprocess_text("your review text here")

# Vectorize it
vectorized = tfidf_vectorizer.transform([processed_review])

# Predict sentiment
prediction = model.predict(vectorized)[0]
probabilities = model.predict_proba(vectorized)[0]

print(f"Predicted: {prediction}")
print(f"Confidence: {max(probabilities):.4f}")
```

## Dataset Information

### Sample Reviews

**Positive Reviews:**
- "This movie was absolutely fantastic! I loved every minute of it."
- "The acting was superb and the storyline was engaging from start to finish."
- "What an amazing film! The cinematography was breathtaking and moving."

**Negative Reviews:**
- "This movie was a complete waste of time. Absolutely terrible."
- "The plot was boring and the acting was dreadful throughout."
- "The worst movie experience of my life. Total disaster."

**Neutral Reviews:**
- "The movie was okay, nothing special but decent enough."
- "It had some good moments but also some of the plot was tedious."
- "Average film. Some parts were interesting, others were forgettable."

## Conclusion

This project successfully demonstrates:
✅ Complete text classification pipeline
✅ TF-IDF feature extraction (bonus requirement)
✅ Multi-class sentiment analysis
✅ Model training and evaluation
✅ Custom review prediction capability

The classifier effectively categorizes movie reviews into positive, negative, and neutral sentiments with good confidence scores on real-world examples.

---

**Created:** March 24, 2026
**Dataset Size:** 24 reviews (3 classes, balanced)
**Feature Extraction:** TF-IDF
**Algorithm:** Multinomial Naive Bayes
