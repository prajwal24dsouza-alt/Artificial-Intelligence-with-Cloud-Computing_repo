"""
Movie Review Sentiment Analyzer
Uses a lexicon-based approach with built-in sentiment word lists
"""

import re


class MovieReviewAnalyzer:
    """Analyzes sentiment of movie reviews using lexicon-based approach"""
    
    def __init__(self):
        """Initialize the sentiment analyzer with built-in word lists"""
        # Positive sentiment words
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic',
            'wonderful', 'outstanding', 'brilliant', 'perfect', 'best', 'love',
            'loved', 'beautiful', 'gorgeous', 'stunning', 'impressive', 'incredible',
            'superb', 'magnificent', 'masterpiece', 'exceptional', 'splendid',
            'marvelous', 'remarkable', 'fabulous', 'delightful', 'enjoy',
            'enjoyed', 'engaging', 'compelling', 'powerful', 'hilarious',
            'funny', 'entertaining', 'thrilling', 'exciting', 'recommend',
            'recommended', 'worthy', 'worthwhile', 'moving', 'touching',
            'beautiful', 'breathtaking', 'emotional', 'genuine', 'gripping'
        }
        
        # Negative sentiment words
        self.negative_words = {
            'bad', 'terrible', 'horrible', 'awful', 'poor', 'disappointing',
            'disappointed', 'boring', 'bored', 'dull', 'boring', 'tedious',
            'waste', 'wasted', 'predictable', 'weak', 'pathetic', 'lame',
            'stupid', 'ridiculous', 'annoying', 'annoyed', 'irritating',
            'frustrating', 'frustrated', 'pathetic', 'mediocre', 'forgettable',
            'uninteresting', 'slow', 'dragging', 'drag', 'pointless',
            'meaningless', 'uninspired', 'uninspiring', 'pretentious',
            'overrated', 'overhyped', 'underperform', 'fails', 'failed',
            'flop', 'trash', 'garbage', 'atrocious', 'abominable', 'worst',
            'hate', 'hated', 'dislike', 'disliked', 'regret', 'refund'
        }
        
        # Intensifier words (amplify sentiment)
        self.intensifiers = {'very', 'extremely', 'absolutely', 'totally', 'really', 'incredibly'}
        
        # Negation words
        self.negations = {'not', 'no', 'never', "n't"}
    
    def analyze(self, review_text):
        """
        Analyze sentiment of a movie review
        
        Args:
            review_text (str): The review text to analyze
            
        Returns:
            dict: Contains sentiment scores and classification
        """
        # Convert to lowercase and split into words
        words = review_text.lower().split()
        
        positive_score = 0
        negative_score = 0
        
        # Track if previous word was negation
        is_negated = False
        
        for i, word in enumerate(words):
            # Remove punctuation
            clean_word = re.sub(r'[^\w]', '', word)
            
            # Check for negation
            if clean_word in self.negations:
                is_negated = True
                continue
            
            # Check for intensifier
            intensifier_boost = 1.5 if clean_word in self.intensifiers else 1.0
            
            # Score positive words
            if clean_word in self.positive_words:
                score = 1.0 * intensifier_boost
                if is_negated:
                    negative_score += score
                else:
                    positive_score += score
                is_negated = False
            
            # Score negative words
            elif clean_word in self.negative_words:
                score = 1.0 * intensifier_boost
                if is_negated:
                    positive_score += score
                else:
                    negative_score += score
                is_negated = False
            
            # Reset negation if we encounter a word that's not a sentiment word
            elif clean_word not in self.intensifiers:
                is_negated = False
        
        # Calculate compound score (-1 to 1)
        total_score = positive_score + negative_score
        if total_score == 0:
            compound_score = 0.0
        else:
            compound_score = (positive_score - negative_score) / total_score
        
        # Normalize scores
        total = max(1, positive_score + negative_score)
        pos_norm = positive_score / total
        neg_norm = negative_score / total
        neu_norm = 1 - pos_norm - neg_norm
        
        # Classify sentiment based on compound score
        if compound_score >= 0.1:
            sentiment = 'Positive'
        elif compound_score <= -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'text': review_text,
            'sentiment': sentiment,
            'compound_score': round(compound_score, 4),
            'positive': round(pos_norm, 4),
            'negative': round(neg_norm, 4),
            'neutral': round(neu_norm, 4)
        }
    
    def analyze_multiple(self, reviews):
        """
        Analyze multiple reviews
        
        Args:
            reviews (list): List of review texts
            
        Returns:
            list: List of analysis results
        """
        return [self.analyze(review) for review in reviews]
    
    def print_analysis(self, result):
        """Pretty print analysis result"""
        print(f"\nReview: {result['text']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Compound Score: {result['compound_score']}")
        print(f"Positive: {result['positive']}, Negative: {result['negative']}, Neutral: {result['neutral']}")
        print("-" * 80)


if __name__ == "__main__":
    analyzer = MovieReviewAnalyzer()
    
    # Example usage
    sample_review = "This movie was absolutely fantastic! Best film I've seen all year."
    result = analyzer.analyze(sample_review)
    analyzer.print_analysis(result)
