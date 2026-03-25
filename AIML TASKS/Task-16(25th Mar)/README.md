# Smart Text Generator - Task 1

## Overview
A mini Language Model (LLM) that generates intelligent 10-word sentences based on user input using trigram-based prediction logic.

## Features Implemented

### ✅ Feature 1: Sentence Input from User
- Interactive prompt that accepts user seed words or phrases
- Flexible input handling - works with single words or multi-word phrases
- Input validation and error handling
- Loop allows multiple generations without restart

### ✅ Feature 2: Better Prediction Logic
Uses **Trigram-based N-gram model** for superior sentence generation:
- **Trigram Model**: Predicts next word based on the two previous words
  - Structure: `(word1, word2) → word3`
  - Enables more contextually accurate predictions
  
- **Fallback Mechanism**: 
  - If trigram not found, uses Bigram model `(word1) → word2`
  - Random selection if no history exists
  
- **Probability-Based Selection**:
  - Words are selected based on frequency from training data
  - More common word combinations are more likely

- **Smart Seed Handling**:
  - Single-word seeds are expanded with contextual companions
  - Multi-word seeds are processed correctly
  - Invalid inputs gracefully fallback to random generation

### ✅ Feature 3: Generate 10-Word Sentence
- Exactly 10 words per generated sentence
- Capitalized output for readability
- Coherent sentences based on training context

## How It Works

### Model Architecture
```
Training Data → Preprocessing → Build Models → Predict & Generate
```

1. **Preprocessing**: Text is converted to lowercase, words extracted via regex
2. **Model Building**:
   - Trigram pairs and their frequencies counted
   - Bigram pairs as fallback option
   - Vocabulary built from all unique words
3. **Generation**:
   - Start with user seed + extended to 2 words if needed
   - Iteratively predict and append next word until 10 words
   - Return exactly 10 words

### Example Workflow
```
User Input:  "artificial"
     ↓
Seed Processing: ["artificial", "intelligence"]
     ↓
Word Generation (8 more words):
  - (artificial, intelligence) → "is"
  - (intelligence, is) → "transforming"
  - ... continues 6 more times
     ↓
Output: "Artificial intelligence is transforming the world machine learning models learn from"
```

## Usage

```bash
python3 text_generator.py
```

### Interactive Session
```
============================================================
SMART TEXT GENERATOR - Building Smarter LLM
============================================================

📚 Training the model...
✓ Model trained successfully!
✓ Vocabulary size: 47 words

------------------------------------------------------------
🎯 Enter seed word/phrase (or 'quit' to exit): intelligence
🔄 Generating 10-word sentence...
✅ Generated: Intelligence is transforming the world machine learning models learn from data
```

## Key Improvements Over Basic LLM

| Feature | Basic | Smart Generator |
|---------|-------|-----------------|
| Prediction | Random word | Trigram-based probability |
| Context | Single word | Two words (trigram) |
| Fallback | None | Bigram fallback |
| User Input | Not supported | Yes, with validation |
| Output Length | Variable | Exactly 10 words |
| Coherence | Low | Medium-High |

## Technical Stack
- **Language**: Python 3
- **Libraries**: 
  - `collections` (defaultdict, Counter) - for efficient model storage
  - `random` - for probability-based selection
  - `re` - for text preprocessing

## Model Parameters
- **Training data**: 5 complete sentences with 47 unique words
- **Generated sequence**: 10 words
- **Model type**: Trigram with Bigram fallback
- **Vocabulary size**: Dynamic (based on training data)

## Limitations & Future Enhancements
- **Current limitations**:
  - Trigram limited to local context (2 previous words)
  - Small training corpus (47 words)
  - No special token handling

- **Potential improvements**:
  - Load larger training corpus from files
  - Implement n-gram variants (4-gram, 5-gram)
  - Add attention mechanism for better context
  - Use pre-trained embeddings
  - Implement beam search for better candidates
  - Add temperature parameter for randomness control

## Files
- `text_generator.py` - Main implementation

## Version
Version 1.0 - March 25, 2025
