import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import ssl

# Handle SSL certificate issues for NLTK data downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Simple word tokenizer using regex instead of punkt
import re

def simple_tokenize(text):
    """Simple word tokenizer using regex"""
    return re.findall(r'\b\w+\b', text)

def preprocess_text(text):
    """
    Preprocesses text by:
    1. Converting to lowercase
    2. Removing punctuation
    3. Tokenizing text
    4. Removing stopwords
    5. Applying stemming
    """
    
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Step 3: Tokenize text (using simple regex-based tokenizer)
    tokens = simple_tokenize(text)
    
    # Step 4: Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Step 5: Apply stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    
    return stemmed_tokens

# Main execution
if __name__ == "__main__":
    input_text = "I am learning NLP and it is very exciting!!"
    
    print(f"Input: {input_text}")
    result = preprocess_text(input_text)
    print(f"Output: {result}")
