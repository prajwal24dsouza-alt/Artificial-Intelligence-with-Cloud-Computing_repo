"""
Advanced Smart Text Generator with Extended Features
- Load training data from files
- Configurable n-gram models
- Save/load models
- Batch generation
"""

import random
from collections import defaultdict, Counter
import re
import json
from pathlib import Path

class AdvancedSmartTextGenerator:
    """Extended version with more features and flexibility."""
    
    def __init__(self, n_gram_order=3, seed_length=2):
        """
        Initialize the generator.
        
        Args:
            n_gram_order: Use n-gram model (default 3 = trigram)
            seed_length: Number of words to keep for context
        """
        self.n_gram_order = n_gram_order
        self.seed_length = seed_length
        self.model = defaultdict(Counter)
        self.bigram_model = defaultdict(Counter)
        self.all_words = set()
        self.vocab_freq = Counter()
        self.training_data = ""
    
    def load_training_data(self, text=None, filepath=None):
        """
        Load training data from text or file.
        
        Args:
            text: Direct text string
            filepath: Path to text file
        """
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.training_data = f.read()
        elif text:
            self.training_data = text
        else:
            # Default training data
            self.training_data = """The quick brown fox jumps over the lazy dog.
Artificial intelligence is transforming the world.
Machine learning models learn from data.
Python is a powerful programming language.
Data science is fascinating and challenging.
Natural language processing enables computers to understand text.
Deep learning networks learn representations.
Neural networks are inspired by the brain."""
    
    def preprocess_text(self, text):
        """Preprocess text to extract words."""
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def build_model(self):
        """Build n-gram model from training data."""
        words = self.preprocess_text(self.training_data)
        self.all_words = set(words)
        self.vocab_freq = Counter(words)
        
        # Build n-gram model
        for i in range(len(words) - self.n_gram_order):
            key = tuple(words[i:i + self.n_gram_order - 1])
            next_word = words[i + self.n_gram_order - 1]
            self.model[key][next_word] += 1
        
        # Build bigram fallback
        for i in range(len(words) - 1):
            self.bigram_model[words[i]][words[i + 1]] += 1
        
        print(f"✓ Model built with {len(self.all_words)} unique words")
        print(f"✓ {self.n_gram_order}-gram entries: {len(self.model)}")
        print(f"✓ Bigram entries: {len(self.bigram_model)}")
    
    def predict_next_word(self, context):
        """Predict next word based on context."""
        context_tuple = tuple(context[-self.n_gram_order + 1:])
        
        if context_tuple in self.model:
            candidates = self.model[context_tuple]
            total = sum(candidates.values())
            r = random.uniform(0, total)
            cumsum = 0
            for word, count in candidates.most_common():
                cumsum += count
                if r <= cumsum:
                    return word
        
        # Fallback to bigram
        if context[-1] in self.bigram_model:
            candidates = self.bigram_model[context[-1]]
            total = sum(candidates.values())
            r = random.uniform(0, total)
            cumsum = 0
            for word, count in candidates.most_common():
                cumsum += count
                if r <= cumsum:
                    return word
        
        return random.choice(list(self.all_words))
    
    def generate_sentence(self, seed, target_length=10):
        """Generate sentence of target length from seed."""
        words = self.preprocess_text(seed)
        
        if len(words) == 0:
            words = random.sample(list(self.all_words), min(2, len(self.all_words)))
        elif len(words) == 1:
            # Extend single word
            if words[0] in self.bigram_model:
                next_w = random.choice(list(self.bigram_model[words[0]].keys()))
                words.append(next_w)
            else:
                words.append(random.choice(list(self.all_words)))
        
        while len(words) < target_length:
            next_word = self.predict_next_word(words)
            words.append(next_word)
        
        return ' '.join(words[:target_length])
    
    def batch_generate(self, seeds, target_length=10):
        """Generate multiple sentences from multiple seeds."""
        results = {}
        for seed in seeds:
            results[seed] = self.generate_sentence(seed, target_length)
        return results
    
    def save_model(self, filepath):
        """Save model to JSON file."""
        state = {
            'model': {str(k): dict(v) for k, v in self.model.items()},
            'bigram_model': {k: dict(v) for k, v in self.bigram_model.items()},
            'all_words': list(self.all_words),
            'vocab_freq': dict(self.vocab_freq),
            'n_gram_order': self.n_gram_order,
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"✓ Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model from JSON file."""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.model = defaultdict(Counter)
        for k_str, v_dict in state['model'].items():
            key = eval(k_str)
            self.model[key] = Counter(v_dict)
        
        self.bigram_model = {k: Counter(v) for k, v in state['bigram_model'].items()}
        self.all_words = set(state['all_words'])
        self.vocab_freq = Counter(state['vocab_freq'])
        self.n_gram_order = state['n_gram_order']
        print(f"✓ Model loaded from {filepath}")
    
    def get_stats(self):
        """Return model statistics."""
        return {
            'vocabulary_size': len(self.all_words),
            'n_gram_entries': len(self.model),
            'bigram_entries': len(self.bigram_model),
            'n_gram_order': self.n_gram_order,
            'training_words': sum(self.vocab_freq.values()),
            'top_words': self.vocab_freq.most_common(10),
        }


def main_advanced():
    """Advanced demo with multiple features."""
    print("\n" + "=" * 70)
    print("ADVANCED SMART TEXT GENERATOR")
    print("=" * 70)
    
    # Create generator with trigram
    gen = AdvancedSmartTextGenerator(n_gram_order=3)
    print("\n📚 Loading training data...")
    gen.load_training_data()
    print("🔨 Building model...")
    gen.build_model()
    
    # Display statistics
    print("\n" + "-" * 70)
    print("MODEL STATISTICS")
    print("-" * 70)
    stats = gen.get_stats()
    for key, value in stats.items():
        if key != 'top_words':
            print(f"  {key}: {value}")
    print("\n  Top 10 words:")
    for word, count in stats['top_words']:
        print(f"    - {word}: {count} occurrences")
    
    # Batch generation
    print("\n" + "-" * 70)
    print("BATCH GENERATION (5 Different Seeds)")
    print("-" * 70)
    seeds = ['artificial', 'learning', 'python', 'deep', 'networks']
    results = gen.batch_generate(seeds)
    for i, (seed, sentence) in enumerate(results.items(), 1):
        print(f"\n{i}. Seed: '{seed}'")
        print(f"   → {sentence.capitalize()}")
    
    # Interactive mode option
    print("\n" + "-" * 70)
    print("INTERACTIVE MODE (Enter 'done' to exit)")
    print("-" * 70)
    
    try:
        while True:
            seed = input("\nEnter seed word/phrase: ").strip()
            if seed.lower() == 'done':
                break
            if seed:
                sentence = gen.generate_sentence(seed)
                print(f"→ {sentence.capitalize()}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Program interrupted by user.")
    
    print("\n" + "=" * 70)
    print("Thank you for using Advanced Smart Text Generator!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main_advanced()
