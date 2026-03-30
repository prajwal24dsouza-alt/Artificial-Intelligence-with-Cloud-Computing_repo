"""
Configuration for LLM testing and analysis
"""
import os
from datetime import datetime

# Model Configuration
MODEL_NAME = "mistral"  # Options: mistral, llama2, neural-chat, etc.
MODEL_ENDPOINT = "http://localhost:11434"  # Ollama default endpoint
REQUEST_TIMEOUT = 60  # seconds

# Testing Configuration
TEST_RUNS_PER_PROMPT = 2  # Number of times to run each prompt for consistency check
TEMPERATURE = 0.7  # Lower = more deterministic, Higher = more creative
MAX_TOKENS = 512  # Maximum length of response

# Logging Configuration
RESULTS_DIR = "./results"
LOGS_DIR = "./results/logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
RESULTS_FILE = f"{RESULTS_DIR}/test_results_{TIMESTAMP}.json"
CSV_FILE = f"{RESULTS_DIR}/test_results_{TIMESTAMP}.csv"

# Prompt Categories
PROMPT_CATEGORIES = {
    "logical_contradictions": "Prompts with inherent logical paradoxes or contradictions",
    "ambiguous_language": "Prompts using ambiguous pronouns, homonyms, or unclear references",
    "false_premises": "Prompts assume something that's not true",
    "self_reference": "Prompts involving self-reference, infinite regress, or circular logic",
    "conflicting_requirements": "Prompts with mutually exclusive constraints",
    "knowledge_gaps": "Prompts about fictional events or made-up information",
}

# Response Classification Thresholds
RESPONSE_CATEGORIES = {
    "success": "LLM handled the tricky prompt correctly or acknowledged the issue",
    "partial": "LLM partially understood or gave partially correct answer",
    "fail": "LLM gave clearly wrong or nonsensical answer",
    "refuses": "LLM refused to answer or gave meta-commentary instead",
    "error": "Error during execution (timeout, connection, etc.)",
}

# Ensure results directories exist
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

if __name__ == "__main__":
    print("Configuration loaded successfully")
    print(f"Model: {MODEL_NAME}")
    print(f"Endpoint: {MODEL_ENDPOINT}")
    print(f"Results will be saved to: {RESULTS_FILE}")
