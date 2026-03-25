
import random
from collections import defaultdict, Counter
import re

class SmartTextGenerator:
    """A smart text generator using trigram-based prediction logic."""
    
    def __init__(self):
        self.trigram_model = defaultdict(Counter)
        self.bigram_model = defaultdict(Counter)
        self.all_words = []
        self.training_data = """The quick brown fox jumps over the lazy dog. The dog sleeps under the tree.
Artificial intelligence is transforming the world. Machine learning models learn from data.
Python is a powerful programming language. Data science is fascinating and challenging.
Natural language processing enables computers to understand text. Text generation is amazing.
Deep learning networks learn representations. Neural networks inspired by the brain."""
    
    def preprocess_text(self, text):
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def build_model(self):
        words = self.preprocess_text(self.training_data)
        self.all_words = list(set(words))
        
        for i in range(len(words) - 2):
            key = (words[i], words[i + 1])
            next_word = words[i + 2]
            self.trigram_model[key][next_word] += 1
        
        for i in range(len(words) - 1):
            key = words[i]
            next_word = words[i + 1]
            self.bigram_model[key][next_word] += 1
    
    def predict_next_word(self, word1, word2):
        key = (word1, word2)
        
        if key in self.trigram_model:
            next_words = self.trigram_model[key]
            total = sum(next_words.values())
            r = random.uniform(0, total)
            cumsum = 0
            for word, count in next_words.most_common():
                cumsum += count
                if r <= cumsum:
                    return word
        
        if word2 in self.bigram_model:
            next_words = self.bigram_model[word2]
            total = sum(next_words.values())
            r = random.uniform(0, total)
            cumsum = 0
            for word, count in next_words.most_common():
                cumsum += count
                if r <= cumsum:
                    return word
        
        return random.choice(self.all_words)
    
    def generate_sentence(self, seed_phrase, num_words=10):
        words = seed_phrase.lower().split()
        words = [w for w in words if w in self.all_words]
        
        if len(words) < 2:
            words = random.sample(self.all_words, min(2, len(self.all_words)))
        
        while len(words) < num_words:
            next_word = self.predict_next_word(words[-2], words[-1])
            words.append(next_word)
        
        return ' '.join(words[:num_words])
    
    def generate_from_seed(self, seed):
        seed_words = self.preprocess_text(seed)
        
        if not seed_words:
            print("Invalid seed. Using random start.")
            seed_words = random.sample(self.all_words, min(2, len(self.all_words)))
        
        if len(seed_words) == 1:
            matching_pairs = [key for key in self.bigram_model.keys() 
                            if key.startswith(seed_words[0])]
            if matching_pairs:
                seed_words = list(random.choice(matching_pairs))
            else:
                seed_words = [seed_words[0], random.choice(self.all_words)]
        
        return self.generate_sentence(' '.join(seed_words), num_words=10)

def main():
    print("=" * 60)
    print("SMART TEXT GENERATOR - Building Smarter LLM")
    print("=" * 60)
    
    generator = SmartTextGenerator()
    print("\n📚 Training the model...")
    generator.build_model()
    print("✓ Model trained successfully!")
    print(f"✓ Vocabulary size: {len(generator.all_words)} words\n")
    
    try:
        while True:
            print("-" * 60)
            user_input = input("🎯 Enter seed word/phrase (or 'quit' to exit): ").strip()
            
            if user_input.lower() == 'quit':
                print("Thank you! Goodbye!")
                break
            
            if not user_input:
                print("❌ Please enter a valid seed phrase.")
                continue
            
            print("\n🔄 Generating 10-word sentence...")
            generated_sentence = generator.generate_from_seed(user_input)
            print(f"✅ Generated: {generated_sentence.capitalize()}\n")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user.")
        print("Thank you! Goodbye!")

if __name__ == "__main__":
    main()
