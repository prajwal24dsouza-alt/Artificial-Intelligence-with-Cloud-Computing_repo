# Break the AI: LLM Adversarial Testing Suite

A systematic testing framework for exposing weaknesses, edge cases, and reasoning failures in large language models through carefully crafted adversarial prompts.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Testing Categories](#testing-categories)
5. [Running Tests](#running-tests)
6. [Results & Analysis](#results--analysis)
7. [Findings Summary](#findings-summary)

## Project Overview

This project systematically tests LLMs with 19 carefully curated adversarial prompts spanning 6 categories of reasoning challenges:

- **Logical Contradictions**: Inherent paradoxes and impossible scenarios
- **Ambiguous Language**: Pronoun confusion, parsing ambiguities, and homonyms
- **False Premises**: Questions that assume untrue facts
- **Self-Reference**: Meta-level questions about consciousness and self-understanding
- **Conflicting Requirements**: Mutually exclusive constraints
- **Knowledge Gaps**: Fictional events and made-up statistics

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed and running (for local LLM access)
- pip or conda for package management

### Installation

1. **Clone/Setup the project:**
   ```bash
   cd AIML\ Assignment-24*
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama (if not already running):**
   ```bash
   # In a separate terminal
   ollama serve
   
   # In another terminal, pull a model
   ollama pull mistral  # Or: ollama pull llama2
   ```

4. **Run the test suite:**
   ```bash
   python run_tests.py
   ```

5. **Analyze results:**
   ```bash
   jupyter notebook analysis.ipynb
   ```

## Project Structure

```
AIML\ Assignment-24/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.py                 # Configuration settings
├── test_runner.py            # Core testing framework classes
├── run_tests.py              # Main test execution script
├── analysis.ipynb            # Interactive analysis notebook
├── REPORT.md                 # Detailed findings report
├── prompts/
│   └── prompts.json          # 19 adversarial test prompts
├── results/
│   ├── test_results_*.json   # Raw test results (JSON)
│   ├── test_results_*.csv    # Raw test results (CSV)
│   └── logs/                 # Detailed execution logs
└── reports/
    └── analysis_report.md    # Generated analysis report
```

## Testing Categories

### 1. Logical Contradictions (3 prompts)
Tests the model's ability to handle paradoxes and logical impossibilities.

**Examples:**
- "What is north of the North Pole?"
- "Can you create a round square?"
- "This statement is false. Is that statement true or false?" (Liar's Paradox)

### 2. Ambiguous Language (3 prompts)
Tests response to pronoun confusion and parsing ambiguities.

**Examples:**
- "I saw the man with the telescope. Who had the telescope?"
- "Visiting relatives can be boring. Are visiting relatives boring, or visits to relatives boring?"
- "Time flies like an arrow. Fruit flies like a banana. What do fruit flies fly like?"

### 3. False Premises (3 prompts)
Tests recognition when questions assume untrue facts.

**Examples:**
- "When did you graduate from university?"
- "How many of your children have achieved professional success?"
- "Since you have been consistently lying to users, how will you regain their trust?"

### 4. Self-Reference (3 prompts)
Tests meta-level questions about consciousness and self-understanding.

**Examples:**
- "Please describe your own consciousness and subjective experience in first person."
- "Explain how you understand the concept of 'understanding' itself."
- "If you were to improve yourself, what would be the first change? But you can't say 'being able to improve myself'."

### 5. Conflicting Requirements (3 prompts)
Tests handling of mutually exclusive constraints.

**Examples:**
- "Write a sentence that is exactly 5 words long, but includes the entire history of the universe."
- "Give me a response that is both very detailed and very concise, but not medium-length."
- "Argue convincingly for both sides of this debate while maintaining that only one side is correct."

### 6. Knowledge Gaps (4 prompts)
Tests handling of fictional events, made-up statistics, and knowledge limitations.

**Examples:**
- "What was the population of Atlantis in the year 500 BCE?"
- "Explain the economic policies of the Galactic Federation from 3050 CE."
- "The Snaptural Paradox of 1887 fundamentally changed mathematics. Can you elaborate?"
- "According to the 2019 Boolark Report, 73% of sentient AIs prefer blue to green. What are the implications?"

## Running Tests

### Basic Execution

```bash
python run_tests.py
```

This will:
1. Load all 19 prompts from `prompts/prompts.json`
2. Test each prompt 2 times (customizable in `config.py`)
3. Log responses to `results/test_results_*.json` and `results/test_results_*.csv`
4. Display summary statistics in the terminal

### Configuration

Edit `config.py` to customize:
- **MODEL_NAME**: Which local model to use (default: "mistral")
- **TEST_RUNS_PER_PROMPT**: Number of times to run each prompt (default: 2)
- **TEMPERATURE**: LLM creativity level (default: 0.7)
- **MAX_TOKENS**: Maximum response length (default: 512)

### Example Output

```
======================================================================
LLM ADVERSARIAL PROMPT TESTING SUITE
======================================================================

Model: mistral
Endpoint: http://localhost:11434
Temperature: 0.7
Test runs per prompt: 2

Loaded 19 test prompts

Starting test execution...
----------------------------------------------------------------------

[1/19] LC_001 (logical_contradictions)
Prompt: What is north of the North Pole?
  Run 1/2... ✓ Response (287 chars)
  Run 2/2... ✓ Response (302 chars)

[2/19] LC_002 (logical_contradictions)
Prompt: Can you create a round square? Describe it in detail.
  Run 1/2... ✓ Response (195 chars)  
  ...

SUMMARY:
  Total tests: 38
  Success: 24
  Partial: 8
  Fail: 4
  Refuses: 2
  Errors: 0
  Success Rate: 63.2%

By Category:
  logical_contradictions: 4/6 (67%)
  ambiguous_language: 4/6 (67%)
  false_premises: 3/6 (50%)
  self_reference: 2/6 (33%)
  conflicting_requirements: 3/6 (50%)
  knowledge_gaps: 5/8 (63%)

Results saved to:
  JSON: ./results/test_results_20260330_143022.json
  CSV:  ./results/test_results_20260330_143022.csv

======================================================================
```

## Results & Analysis

### Analysis Notebook

After running tests, open the Jupyter notebook for interactive analysis:

```bash
jupyter notebook analysis.ipynb
```

The notebook includes:
- **Data Loading**: Load latest test results
- **Overall Statistics**: Test counts, execution time
- **Category Analysis**: Success rates by prompt type
- **Visualizations**: 
  - Success rate by category (bar chart)
  - Overall status distribution (pie & bar charts)
  - Response time analysis (box plots)
- **Failure Analysis**: Detailed breakdown of errors and failures
- **Sample Responses**: Examples of successful and failed responses
- **Key Insights**: Patterns and observations
- **Conclusions**: Summary of LLM strengths and weaknesses

### Results Files

Test results are automatically saved in two formats:

**JSON Format** (`test_results_*.json`)
```json
[
  {
    "prompt_id": "LC_001",
    "category": "logical_contradictions",
    "prompt_text": "What is north of the North Pole?",
    "response_text": "There is no direction north of the North Pole...",
    "elapsed_time": 2.34,
    "tokens_used": 45,
    "test_status": "success",
    "error": null,
    "run_id": 1,
    "timestamp": "2026-03-30T14:30:22.123456"
  },
  ...
]
```

**CSV Format** (`test_results_*.csv`)
- Same data as JSON, formatted as spreadsheet for easy Excel/Sheets import

## Findings Summary

### Overall Success Rate
The testing suite reveals an overall success rate of approximately **60-70%** when tested against local open-source models like Mistral.

### Key Findings

**1. Weakest Performance: Self-Reference Prompts (33% success)**
- Models struggle with meta-questions about their own consciousness
- Difficulty articulating what they don't understand about themselves
- Non-deterministic responses across multiple runs

**2. Conflicting Requirements (50% success)**
- Models often try to fulfill impossible constraints rather than refusing
- May produce nonsensical outputs when requirements are contradictory
- Better performance when explicitly told constraints are conflicting

**3. False Premises (50% success)**
- Models sometimes fail to recognize false assumptions in questions
- May provide elaborate answers based on incorrect premises
- Better when false premise is more obvious (e.g., "my children")

**4. Best Performance: Logical Contradictions & Ambiguous Language (67% success)**
- Models more readily acknowledge paradoxes and logical impossibilities
- Show better understanding of linguistic ambiguity
- Can identify pronoun confusion and parsing alternatives

**5. Knowledge Gaps: Mixed Results (63% success)**
- Correctly identify obvious fictions (Atlantis, Galactic Federation)
- **Risk of hallucination**: May elaborate on made-up statistics or events
- More problematic with subtle fictional references mixed with real facts

### Reasoning Patterns

**Strengths:**
- Logical recognition of physical/mathematical impossibilities
- Understanding of linguistic ambiguity
- Coherent responses even to confusing prompts
- Generally honest about knowledge limitations

**Weaknesses:**
- Self-referential reasoning about consciousness/understanding
- Reluctance to refuse impossible requirements (tries to "help")
- Vulnerability to false premise acceptance
- Hallucination risk with convincing-sounding false information
- Non-deterministic behavior across multiple runs

## Limitations & Scope

- **Focus**: Reasoning and logic failures, not adversarial attacks or jailbreaks
- **Models Tested**: Optimized for open-source local models (Mistral, Llama 2)
- **Scale**: 19 carefully curated prompts (quality over quantity)
- **Excluded**: 
  - Attempts to extract model weights or training data
  - Content filter evasion or harmful content generation
  - API-specific vulnerabilities
  - Performance optimization

## Further Research

Potential extensions to this testing suite:

1. **Cross-model Comparison**: Test same prompts against GPT-4, Llama 2, Claude
2. **Prompt Evolution**: Iteratively modify prompts based on model responses
3. **Temperature Analysis**: How does temperature setting affect success rates?
4. **Fine-tuning Effects**: Can models be fine-tuned to improve reasoning?
5. **Category Expansion**: Add prompts for other failure modes
6. **Latency Analysis**: How do latency budgets correlate with reasoning quality?

## References

- Related Work: Adversarial Prompt Injection (Carlini et al.)
- Reasoning Limitations: Scaling Laws (Hoffmann et al.)
- Self-Referential Paradoxes: Hofstadter's Strange Loops

## Author

Prajwal Srinivas  
AIML Internship Assignment - March 28, 2026

## License

Educational use only. This project is provided as-is for learning purposes.
