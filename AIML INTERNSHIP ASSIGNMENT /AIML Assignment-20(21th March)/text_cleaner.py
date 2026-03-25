"""
Assignment: Build a Text Cleaner
Description: Remove punctuation, lowercase text, remove stopwords, and test it.
"""

import string
import re
import unittest

# ─────────────────────────────────────────────
# STOPWORDS (common English words to remove)
# ─────────────────────────────────────────────
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "up", "about", "into", "through", "during",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "shall", "should", "may", "might",
    "must", "can", "could", "i", "me", "my", "we", "our", "you", "your",
    "he", "she", "it", "they", "them", "their", "this", "that", "these",
    "those", "not", "no", "so", "if", "as", "than", "then", "just", "more",
    "also", "very", "too", "its", "s", "t"
}


# ─────────────────────────────────────────────
# TEXT CLEANING FUNCTIONS
# ─────────────────────────────────────────────

def to_lowercase(text: str) -> str:
    """Convert all characters in text to lowercase."""
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Remove all punctuation characters from text."""
    # Remove standard punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove any extra whitespace left behind
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text: str, stopwords: set = STOPWORDS) -> str:
    """Remove common stopwords from text."""
    words = text.split()
    filtered = [word for word in words if word.lower() not in stopwords]
    return " ".join(filtered)


def clean_text(text: str, stopwords: set = STOPWORDS) -> str:
    """
    Full text cleaning pipeline:
      1. Convert to lowercase
      2. Remove punctuation
      3. Remove stopwords
    """
    text = to_lowercase(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text, stopwords)
    return text


# ─────────────────────────────────────────────
# UNIT TESTS
# ─────────────────────────────────────────────

class TestTextCleaner(unittest.TestCase):

    # --- to_lowercase ---
    def test_lowercase_basic(self):
        self.assertEqual(to_lowercase("Hello World"), "hello world")

    def test_lowercase_all_upper(self):
        self.assertEqual(to_lowercase("MACHINE LEARNING"), "machine learning")

    def test_lowercase_already_lower(self):
        self.assertEqual(to_lowercase("python"), "python")

    def test_lowercase_mixed(self):
        self.assertEqual(to_lowercase("PyThOn Is FuN"), "python is fun")

    def test_lowercase_numbers_unchanged(self):
        self.assertEqual(to_lowercase("ABC123"), "abc123")

    # --- remove_punctuation ---
    def test_remove_punctuation_basic(self):
        self.assertEqual(remove_punctuation("Hello, World!"), "Hello World")

    def test_remove_punctuation_question(self):
        self.assertEqual(remove_punctuation("How are you?"), "How are you")

    def test_remove_punctuation_multiple(self):
        self.assertEqual(remove_punctuation("Wow!!! Amazing..."), "Wow Amazing")

    def test_remove_punctuation_no_punct(self):
        self.assertEqual(remove_punctuation("no punctuation here"), "no punctuation here")

    def test_remove_punctuation_only_punct(self):
        self.assertEqual(remove_punctuation("!!!???..."), "")

    def test_remove_punctuation_apostrophe(self):
        result = remove_punctuation("It's a test.")
        self.assertNotIn(".", result)
        self.assertNotIn("'", result)

    # --- remove_stopwords ---
    def test_remove_stopwords_basic(self):
        result = remove_stopwords("the cat sat on the mat")
        self.assertNotIn("the", result.split())
        self.assertNotIn("on", result.split())

    def test_remove_stopwords_keeps_content_words(self):
        result = remove_stopwords("cat sat mat")
        self.assertIn("cat", result)
        self.assertIn("sat", result)
        self.assertIn("mat", result)

    def test_remove_stopwords_all_stopwords(self):
        result = remove_stopwords("the and or but")
        self.assertEqual(result.strip(), "")

    def test_remove_stopwords_custom_set(self):
        custom = {"hello", "world"}
        result = remove_stopwords("hello beautiful world", custom)
        self.assertNotIn("hello", result)
        self.assertNotIn("world", result)
        self.assertIn("beautiful", result)

    def test_remove_stopwords_empty_string(self):
        self.assertEqual(remove_stopwords(""), "")

    # --- clean_text (full pipeline) ---
    def test_clean_text_full_pipeline(self):
        raw = "The Quick Brown Fox Jumps Over the Lazy Dog!"
        result = clean_text(raw)
        self.assertEqual(result, result.lower())          # lowercase
        self.assertNotIn("!", result)                     # no punctuation
        self.assertNotIn("the", result.split())           # no stopwords

    def test_clean_text_sentence(self):
        raw = "I am learning Machine Learning, and it is very exciting!"
        result = clean_text(raw)
        # Should keep meaningful words
        self.assertIn("learning", result)
        self.assertIn("machine", result)
        self.assertIn("exciting", result)
        # Should remove stopwords & punctuation
        self.assertNotIn("i", result.split())
        self.assertNotIn("and", result.split())
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)

    def test_clean_text_already_clean(self):
        raw = "data science rocks"
        # none of these words are stopwords
        result = clean_text(raw)
        self.assertEqual(result, "data science rocks")

    def test_clean_text_empty_string(self):
        self.assertEqual(clean_text(""), "")

    def test_clean_text_only_stopwords_and_punct(self):
        raw = "The, and! or? but."
        result = clean_text(raw)
        self.assertEqual(result.strip(), "")


# ─────────────────────────────────────────────
# DEMO — Run cleaning on sample sentences
# ─────────────────────────────────────────────

SAMPLE_SENTENCES = [
    "The Quick Brown Fox Jumps Over the Lazy Dog!",
    "I am learning Natural Language Processing, and it is very exciting!",
    "Hello!!! How are you doing today? I hope you're well.",
    "Python is the BEST programming language for Data Science.",
    "Stop-words, punctuation, and UPPERCASE text make NLP harder.",
]


def run_demo():
    print("=" * 60)
    print("        TEXT CLEANER — DEMO")
    print("=" * 60)
    for i, sentence in enumerate(SAMPLE_SENTENCES, 1):
        print(f"\n[{i}] Original  : {sentence}")
        print(f"    Lowercase : {to_lowercase(sentence)}")
        print(f"    No Punct  : {remove_punctuation(to_lowercase(sentence))}")
        print(f"    Cleaned   : {clean_text(sentence)}")
    print("\n" + "=" * 60)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Run demo first
    run_demo()

    # Then run unit tests
    print("\n        RUNNING UNIT TESTS\n" + "=" * 60)
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromTestCase(TestTextCleaner)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
