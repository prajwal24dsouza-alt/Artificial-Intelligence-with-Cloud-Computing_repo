# Word Importance Explorer: TF-IDF Analysis
## AIML Assignment - March 24

### 📋 Assignment Overview

This assignment implements a **Word Importance Explorer** using **TF-IDF (Term Frequency-Inverse Document Frequency)** to identify and analyze the most important keywords across 5 documents.

**Objective:** Use TF-IDF on 5 documents and identify top keywords with detailed explanations.

---

## 📚 What is TF-IDF?

### Definition
TF-IDF is a numerical statistic that reflects how important a word is to a document in a collection of documents. It combines two metrics:

### Components

#### 1. **Term Frequency (TF)**
- Measures how often a term appears in a specific document
- Formula: `TF(t,d) = (count of term t in document d) / (total terms in document d)`
- Range: 0 to 1
- **Higher TF** = word appears frequently in the document

#### 2. **Inverse Document Frequency (IDF)**
- Measures how unique/rare a term is across all documents
- Formula: `IDF(t) = log(total documents / documents containing term t)`
- **Higher IDF** = word is rare across the corpus (more distinctive)
- **Lower IDF** = word appears in many documents (common word)

#### 3. **TF-IDF Score**
- Combined metric: `TF-IDF(t,d) = TF(t,d) × IDF(t)`
- Highlights important, distinctive words for each document
- Automatically filters out common words like "the", "is", "and"

### Why TF-IDF?
- 🎯 **Identifies key concepts** without manual curation
- 📊 **Provides numerical representation** for machine learning
- 🔍 **Distinguishes document topics** effectively
- 🚀 **Scalable** to large document collections
- 🔗 **Works well** regardless of document length

---

## 📁 Project Files

### 1. **TF_IDF_Analysis.ipynb**
A Jupyter Notebook with complete analysis including:
- Step-by-step implementation
- Interactive visualizations
- Detailed explanations
- Code outputs and insights

**How to use:**
```bash
jupyter notebook TF_IDF_Analysis.ipynb
```

### 2. **tfidf_analysis.py**
A standalone Python script that can be run independently:
- Complete TF-IDF analysis
- Console output with detailed statistics
- Visualization generation
- No Jupyter dependency required

**How to use:**
```bash
python3 tfidf_analysis.py
```

### 3. **README.md** (This file)
Documentation and explanation of the assignment

---

## 📊 Analysis Structure

### Section 1: Import Required Libraries
- **Libraries Used:** NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn
- **Purpose:** Essential data processing and visualization tools

### Section 2: Load and Prepare Documents
- **Documents:** 5 sample documents covering diverse topics
  1. **Document 1:** Machine Learning
  2. **Document 2:** Python Programming
  3. **Document 3:** Climate Change
  4. **Document 4:** Basketball
  5. **Document 5:** Brain Science
- **Preprocessing:** Lowercasing, punctuation handling, tokenization

### Section 3: Calculate TF-IDF Scores
- **Method:** TfidfVectorizer from scikit-learn
- **Parameters:**
  - `stop_words='english'` - Remove common English words
  - `max_df=0.8` - Ignore very common terms
  - `min_df=1` - Include terms appearing at least once
  - `sublinear_tf=True` - Apply sublinear scaling
- **Output:** TF-IDF matrix (5 documents × 150 unique terms)

### Section 4: Extract and Visualize Top Keywords
- **Method:** Identify top 10 keywords per document
- **Visualization:** Horizontal bar charts showing TF-IDF scores
- **Insights:** Clear observation of document-specific keywords

### Section 5: Explain TF-IDF Results
- **Detailed Analysis:**
  - TF-IDF score statistics per document
  - Document distinctiveness analysis
  - Common vs unique terms identification
- **Interpretations:** What the scores tell us about document topics

---

## 🔍 Key Findings

### Document-Specific Keywords

| Document | Top Keywords | Theme |
|----------|-------------|-------|
| 1 | machine, learning, algorithms, data, neural | Machine Learning |
| 2 | python, language, programming, libraries, community | Python Programming |
| 3 | climate, change, global, renewable, carbon | Climate Change |
| 4 | basketball, shooting, players, team, score | Basketball |
| 5 | brain, neurons, cognitive, complexity, functions | Brain Science |

### Important Observations

1. **Stop Words Filtering**: Common words like "a", "the", "is" have very low TF-IDF scores
2. **Topic Differentiation**: Each document clearly distinguished by its unique vocabulary
3. **Distinctiveness**: Domain-specific terms receive high TF-IDF scores
4. **Effectiveness**: TF-IDF successfully identifies meaningful keywords

---

## 💡 TF-IDF Advantages Demonstrated

✓ **Automatic relevance weighting** based on document statistics
✓ **No manual keyword selection** required
✓ **Numerical representation** suitable for machine learning
✓ **Length-independent** - works with documents of varying sizes
✓ **Scalable** - efficient even with large document collections
✓ **Interpretable** - understand why terms are important

---

## 🎯 Real-World Applications

### 1. **Search Engines**
- Rank documents by relevance to search queries
- TF-IDF scores determine page ranking

### 2. **Document Classification**
- Categorize documents based on important keywords
- Use TF-IDF vectors as features for classifiers

### 3. **Content Recommendation**
- Find similar documents in a corpus
- Calculate document similarity using TF-IDF vectors

### 4. **Information Extraction**
- Automatically extract key terms for metadata
- Generate document summaries based on keyword importance

### 5. **Text Mining**
- Analyze patterns in large document collections
- Identify trends in text data

---

## 📈 Technical Implementation

### Vectorization Parameters Explained

```python
TfidfVectorizer(
    max_features=None,          # Keep all features
    stop_words='english',        # Remove common English words
    lowercase=True,             # Convert to lowercase
    min_df=1,                   # Minimum doc frequency
    max_df=0.8,                 # Maximum doc frequency (80%)
    ngram_range=(1, 1),        # Use single words
    sublinear_tf=True           # Apply sublinear scaling
)
```

### Why These Parameters?

- **stop_words='english'**: Removes words that appear in all documents (low information value)
- **max_df=0.8**: Excludes terms appearing in >80% of documents (too common)
- **sublinear_tf=True**: Reduces impact of highly frequent terms within a document
- **ngram_range=(1, 1)**: Focuses on individual words (unigrams)

---

## 📊 Visualization Guide

The generated charts show:
- **X-axis**: TF-IDF Score (0.0 to 0.5)
- **Y-axis**: Keywords for each document
- **Colors**: Different color for each rank position
- **Values**: Exact TF-IDF scores displayed on bars
- **Order**: Keywords sorted by importance (top = highest score)

---

## 🚀 Running the Project

### Requirements
```bash
pip install numpy pandas scikit-learn matplotlib seaborn
```

### Option 1: Jupyter Notebook
```bash
# Install Jupyter if needed
pip install jupyter

# Start the notebook
jupyter notebook TF_IDF_Analysis.ipynb
```

### Option 2: Python Script
```bash
python3 tfidf_analysis.py
```

### Expected Output
- Console output with detailed statistics
- TF-IDF score rankings for each document
- Analysis of common and unique terms
- Visualization saved as PNG file

---

## 📝 Assignment Completion Checklist

- ✅ Loaded and prepared 5 sample documents
- ✅ Implemented TF-IDF using scikit-learn
- ✅ Calculated TF-IDF scores for all terms
- ✅ Extracted top 10 keywords per document
- ✅ Created comprehensive visualizations
- ✅ Provided detailed TF-IDF explanations
- ✅ Analyzed document distinctiveness
- ✅ Discussed real-world applications
- ✅ Demonstrated TF-IDF advantages

---

## 📚 Further Learning

### Related Topics
- **Latent Semantic Analysis (LSA)**: Alternative dimensionality reduction technique
- **Word2Vec & embeddings**: Neural network-based word representations
- **BERT & Transformers**: Modern approach to NLP using deep learning
- **Topic Modeling (LDA)**: Identifying themes in document collections

### Recommended Reading
- "Information Retrieval: Implementing and Evaluating Search Engines" - Search engine fundamentals
- Scikit-learn documentation: Feature extraction and text processing
- Natural Language Processing with Python (NLTK book)

---

## 🔗 References

1. **TF-IDF Concept**: Wikipedia - Tf–idf
2. **Scikit-learn**: https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
3. **Information Retrieval**: https://en.wikipedia.org/wiki/Information_retrieval
4. **Text Mining**: Introduction to Data Mining (Tan, Steinbach, Kumar)

---

## 📧 Notes

- The notebook and script produce identical results
- All 5 documents are included in the code (no external files needed)
- Visualizations are automatically saved during execution
- Results are deterministic and reproducible

---

## ✨ Conclusion

This assignment successfully demonstrates:
1. How TF-IDF works as a text analysis technique
2. Implementation using industry-standard libraries
3. Practical application to real documents
4. Interpretation of results for meaningful insights
5. Visualization of complex mathematical concepts

The TF-IDF approach is foundational in NLP and information retrieval, making this assignment a valuable introduction to text mining and machine learning with text data.

---

**Created:** March 30, 2026
**Status:** ✅ Complete
