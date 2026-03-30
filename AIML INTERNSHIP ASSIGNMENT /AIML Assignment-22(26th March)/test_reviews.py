"""
Test the sentiment analyzer with 5 movie reviews
"""

from sentiment_analyzer import MovieReviewAnalyzer


def test_movie_reviews():
    """Test sentiment analyzer with 5 different movie reviews"""
    
    analyzer = MovieReviewAnalyzer()
    
    # 5 test reviews with different sentiments
    test_reviews = [
        # Positive review
        "This movie was absolutely amazing! The acting was superb, the plot was engaging, "
        "and I was on the edge of my seat the entire time. Highly recommend!",
        
        # Negative review
        "Terrible film. Boring plot, awful acting, and a complete waste of time. "
        "I walked out halfway through and I want my money back.",
        
        # Mixed/Neutral review
        "The movie had some good moments but also some slow parts. "
        "The acting was decent but the ending was predictable.",
        
        # Very positive review
        "Masterpiece! This film exceeded all my expectations. Outstanding cinematography, "
        "powerful performances, and a compelling story. A must-watch!",
        
        # Negative review
        "Disappointing and dull. The storyline fell flat, and the characters were uninteresting. "
        "Not worth the hype."
    ]
    
    print("\n" + "="*80)
    print("MOVIE REVIEW SENTIMENT ANALYSIS TEST")
    print("="*80)
    
    # Analyze all reviews
    results = analyzer.analyze_multiple(test_reviews)
    
    # Print detailed results
    for i, result in enumerate(results, 1):
        print(f"\n{'='*80}")
        print(f"REVIEW #{i}")
        print(f"{'='*80}")
        analyzer.print_analysis(result)
    
    # Print summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    sentiments = [r['sentiment'] for r in results]
    positive_count = sentiments.count('Positive')
    negative_count = sentiments.count('Negative')
    neutral_count = sentiments.count('Neutral')
    
    print(f"Total Reviews Analyzed: {len(results)}")
    print(f"Positive Sentiments: {positive_count}")
    print(f"Negative Sentiments: {negative_count}")
    print(f"Neutral Sentiments: {neutral_count}")
    
    avg_compound = sum([r['compound_score'] for r in results]) / len(results)
    print(f"Average Compound Score: {round(avg_compound, 4)}")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_movie_reviews()
