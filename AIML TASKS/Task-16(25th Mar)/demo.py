"""
Demonstration and Testing Script for Smart Text Generator
Shows various seed inputs and generated outputs
"""

from text_generator import SmartTextGenerator

def demo():
    """Run demonstration with various seed phrases."""
    
    print("\n" + "=" * 70)
    print("SMART TEXT GENERATOR - DEMONSTRATION")
    print("=" * 70)
    
    # Initialize generator
    generator = SmartTextGenerator()
    print("\n📚 Building and training the model...")
    generator.build_model()
    print(f"✓ Model trained with {len(generator.all_words)} unique words")
    print(f"✓ Trigram pairs: {len(generator.trigram_model)}")
    print(f"✓ Bigram pairs: {len(generator.bigram_model)}")
    
    # Test cases with different seed phrases
    test_seeds = [
        "artificial",
        "learning",
        "data",
        "python",
        "deep",
        "neural",
        "programming",
        "text",
        "intelligence",
        "language"
    ]
    
    print("\n" + "-" * 70)
    print("DEMONSTRATION: 10 Generated Sentences from Different Seeds")
    print("-" * 70)
    
    for i, seed in enumerate(test_seeds, 1):
        generated = generator.generate_from_seed(seed)
        print(f"\n{i}. Seed: '{seed}'")
        print(f"   → {generated.capitalize()}")
    
    # Test edge cases
    print("\n" + "-" * 70)
    print("EDGE CASES & SPECIAL INPUTS")
    print("-" * 70)
    
    edge_cases = [
        ("single", "Single word seed"),
        ("machine learning", "Two-word phrase"),
        ("Deep neural network learning", "Three-word phrase"),
    ]
    
    for seed, description in edge_cases:
        generated = generator.generate_from_seed(seed)
        print(f"\n{description}: '{seed}'")
        print(f"→ {generated.capitalize()}")
    
    # Statistics
    print("\n" + "-" * 70)
    print("MODEL STATISTICS")
    print("-" * 70)
    print(f"Vocabulary size:        {len(generator.all_words)} words")
    print(f"Trigram model entries:  {len(generator.trigram_model)}")
    print(f"Bigram model entries:   {len(generator.bigram_model)}")
    print(f"Generated output:       Exactly 10 words per sentence")
    
    # Show vocabulary
    print("\n" + "-" * 70)
    print("VOCABULARY (Sorted)")
    print("-" * 70)
    vocab_sorted = sorted(generator.all_words)
    words_per_line = 8
    for i in range(0, len(vocab_sorted), words_per_line):
        print("  " + ", ".join(vocab_sorted[i:i+words_per_line]))
    
    print("\n" + "=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demo()
