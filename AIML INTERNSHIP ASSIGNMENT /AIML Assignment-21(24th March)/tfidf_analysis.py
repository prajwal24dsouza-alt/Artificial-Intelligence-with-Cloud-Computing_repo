#!/usr/bin/env python3
"""
Word Importance Explorer: TF-IDF Analysis
==========================================
AIML Assignment: Use TF-IDF on 5 documents and identify top keywords with explanation.

This script demonstrates the application of TF-IDF (Term Frequency-Inverse Document Frequency)
to identify the most important keywords across 5 documents.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings

warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def main():
    print("\n" + "=" * 80)
    print("WORD IMPORTANCE EXPLORER: TF-IDF ANALYSIS")
    print("=" * 80)
    
    # ==================== SECTION 1: IMPORT AND SETUP ====================
    print("\n[1/5] Importing libraries...")
    print("✓ Libraries imported successfully!")
    
    # ==================== SECTION 2: LOAD DOCUMENTS ====================
    print("\n[2/5] Loading and preparing documents...")
    
    documents = [
        """Machine learning is a subset of artificial intelligence that enables systems to learn 
        and improve from experience without being explicitly programmed. Machine learning algorithms 
        analyze patterns in data and make predictions or decisions based on that data. Deep learning, 
        neural networks, and supervised learning are key components of machine learning applications.""",
        
        """Python is a high-level programming language known for its simplicity and readability. 
        Python is widely used in web development, data science, artificial intelligence, and automation. 
        The Python community provides extensive libraries like NumPy, Pandas, and TensorFlow for various tasks. 
        Python's flexible syntax makes it popular among both beginners and experienced programmers.""",
        
        """Climate change poses significant challenges to our environment and society. Rising global temperatures, 
        melting ice caps, and increasing frequency of extreme weather events are major consequences of climate change. 
        Sustainable development, renewable energy, and carbon reduction are essential strategies to combat climate change. 
        International cooperation is crucial for addressing this global crisis.""",
        
        """Basketball is a team sport played between two teams of five players each on a rectangular court. 
        The objective is to score points by shooting the basketball through the opponent's hoop. Basketball requires 
        skills like dribbling, shooting, passing, and defensive strategies. Professional basketball leagues like the 
        NBA showcase the highest level of basketball competition worldwide.""",
        
        """The human brain is one of the most complex organs in the body, containing approximately 86 billion neurons. 
        The brain controls all bodily functions including movement, sensation, emotions, and cognition. 
        Neuroplasticity allows the brain to reorganize and form new neural connections throughout life. 
        Understanding brain function is essential for treating neurological diseases and improving cognitive health."""
    ]
    
    doc_names = [f"Document {i+1}" for i in range(5)]
    
    print("\n" + "-" * 80)
    print("DOCUMENT OVERVIEW")
    print("-" * 80)
    print(f"Total Documents: {len(documents)}")
    print(f"Topics: Machine Learning, Python, Climate Change, Basketball, Brain Science\n")
    
    for i, (name, doc) in enumerate(zip(doc_names, documents)):
        word_count = len(doc.split())
        print(f"  {name}: {word_count} words")
    
    print("\n✓ Documents loaded successfully!")
    
    # ==================== SECTION 3: CALCULATE TF-IDF ====================
    print("\n[3/5] Calculating TF-IDF scores...")
    print("-" * 80)
    
    tfidf_vectorizer = TfidfVectorizer(
        max_features=None,
        stop_words='english',
        lowercase=True,
        min_df=1,
        max_df=0.8,
        ngram_range=(1, 1),
        sublinear_tf=True
    )
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_array = tfidf_matrix.toarray()
    
    print(f"Vectorizer Parameters:")
    print(f"  - Total unique terms: {len(feature_names)}")
    print(f"  - TF-IDF Matrix shape: {tfidf_matrix.shape} (Documents × Terms)")
    print(f"  - Sample features: {', '.join(feature_names[:10])}")
    
    print("\n✓ TF-IDF calculation completed!")
    
    # ==================== SECTION 4: EXTRACT TOP KEYWORDS ====================
    print("\n[4/5] Extracting top keywords for each document...")
    print("-" * 80)
    
    n_top_keywords = 10
    top_keywords_dict = {}
    
    for doc_idx, doc_name in enumerate(doc_names):
        tfidf_scores = tfidf_array[doc_idx]
        top_indices = np.argsort(tfidf_scores)[-n_top_keywords:][::-1]
        
        top_terms = feature_names[top_indices]
        top_scores = tfidf_scores[top_indices]
        
        top_keywords_dict[doc_name] = list(zip(top_terms, top_scores))
        
        print(f"\n{doc_name}:")
        print("  Rank | Keyword                  | TF-IDF Score")
        print("  " + "-" * 55)
        for rank, (term, score) in enumerate(zip(top_terms, top_scores), 1):
            print(f"  {rank:2d}   | {term:24s} | {score:.6f}")
    
    print("\n✓ Top keywords extracted!")
    
    # ==================== SECTION 5: DETAILED ANALYSIS ====================
    print("\n[5/5] Performing detailed analysis...")
    print("-" * 80)
    
    # Statistics
    print("\nTF-IDF SCORE STATISTICS:")
    for doc_idx, doc_name in enumerate(doc_names):
        tfidf_scores = tfidf_array[doc_idx]
        non_zero_scores = tfidf_scores[tfidf_scores > 0]
        
        print(f"\n{doc_name}:")
        print(f"  • Non-zero TF-IDF scores: {len(non_zero_scores)}")
        print(f"  • Maximum score: {non_zero_scores.max():.6f}")
        print(f"  • Average score: {non_zero_scores.mean():.6f}")
        print(f"  • Minimum score: {non_zero_scores.min():.6f}")
    
    # Distinctiveness
    print("\n\nDOCUMENT DISTINCTIVENESS:")
    for doc_idx, doc_name in enumerate(doc_names):
        tfidf_scores = tfidf_array[doc_idx]
        top_5_indices = np.argsort(tfidf_scores)[-5:][::-1]
        
        print(f"\n{doc_name} (Top 5 distinctive keywords):")
        for i, idx in enumerate(top_5_indices, 1):
            term = feature_names[idx]
            score = tfidf_scores[idx]
            other_docs = sum(1 for d_idx in range(len(documents)) 
                           if d_idx != doc_idx and tfidf_array[d_idx, idx] > 0)
            
            if other_docs == 0:
                status = "Uniquely distinctive"
            elif other_docs <= 1:
                status = "Highly distinctive"
            else:
                status = "Moderately distinctive"
            
            print(f"  {i}. '{term}' (Score: {score:.4f}) - {status}")
    
    # Common vs Unique
    print("\n\nCOMMON VS UNIQUE TERMS:")
    term_document_count = {}
    for col_idx, term in enumerate(feature_names):
        count = sum(1 for row_idx in range(len(documents)) if tfidf_array[row_idx, col_idx] > 0)
        term_document_count[term] = count
    
    common_terms = [term for term, count in term_document_count.items() if count == 5]
    unique_terms = [term for term, count in term_document_count.items() if count == 1]
    
    print(f"  • Terms in all 5 documents: {len(common_terms)}")
    if common_terms:
        print(f"    Examples: {', '.join(common_terms[:5])}")
    
    print(f"  • Terms in only 1 document: {len(unique_terms)}")
    if unique_terms:
        print(f"    Examples: {', '.join(unique_terms[:5])}")
    
    print(f"  • Terms in 2-4 documents: {sum(1 for c in term_document_count.values() if 1 < c < 5)}")
    
    # ==================== VISUALIZATION ====================
    print("\n\nGenerating visualization...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    colors = plt.cm.Set3(np.linspace(0, 1, n_top_keywords))
    
    for idx, (doc_name, keywords) in enumerate(top_keywords_dict.items()):
        if idx < 5:
            terms, scores = zip(*keywords)
            ax = axes[idx]
            bars = ax.barh(range(len(terms)), scores, color=colors[::-1])
            ax.set_yticks(range(len(terms)))
            ax.set_yticklabels(terms)
            ax.set_xlabel('TF-IDF Score', fontsize=10, fontweight='bold')
            ax.set_title(doc_name, fontsize=12, fontweight='bold')
            ax.invert_yaxis()
            
            for i, (bar, score) in enumerate(zip(bars, scores)):
                ax.text(score, i, f' {score:.4f}', va='center', fontsize=9)
    
    axes[5].remove()
    plt.tight_layout()
    plt.savefig('tfidf_analysis_visualization.png', dpi=300, bbox_inches='tight')
    print("✓ Visualization saved as 'tfidf_analysis_visualization.png'")
    plt.show()
    
    # ==================== CONCLUSION ====================
    print("\n" + "=" * 80)
    print("ASSIGNMENT COMPLETION SUMMARY")
    print("=" * 80)
    print(f"""
✓ ASSIGNMENT SUCCESSFULLY COMPLETED

Key Achievements:
  • Analyzed 5 distinct documents covering different topics
  • Extracted {len(feature_names)} unique terms from the corpus
  • Calculated TF-IDF scores for all term-document pairs
  • Identified top 10 keywords for each document
  • Generated comprehensive visualizations
  • Provided detailed analysis of TF-IDF results

TF-IDF Insights Demonstrated:
  1. Each document has a unique set of important keywords
  2. Common English words are automatically downweighted
  3. Domain-specific terms receive high TF-IDF scores
  4. The algorithm effectively identifies document topics
  5. TF-IDF is valuable for information retrieval and classification

Applications of TF-IDF:
  • Search engine ranking
  • Document classification
  • Information extraction
  • Text clustering and similarity
  • Feature extraction for machine learning
    """)
    print("=" * 80)

if __name__ == "__main__":
    main()
