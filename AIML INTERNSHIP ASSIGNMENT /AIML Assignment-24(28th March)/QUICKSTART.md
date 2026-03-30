# QUICKSTART GUIDE

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Ollama (One-time setup)
If you haven't already, install Ollama from [ollama.ai](https://ollama.ai)

### Step 2: Start the Ollama Server
```bash
# In a new terminal/tab
ollama serve
```

You should see:
```
time=2026-03-30T14:30:00.000Z level=INFO msg="listening on 127.0.0.1:11434"
```

### Step 3: Download a Model (First time only)
```bash
# In another terminal
ollama pull mistral
```

This downloads the 4.4GB Mistral model. First run will take 5-15 minutes depending on your internet speed.

To verify:
```bash
ollama list
```

You should see Mistral in the list.

### Step 4: Install Python Dependencies
```bash
cd "AIML Assignment-24(28th March)"
pip install -r requirements.txt
```

### Step 5: Run the Test Suite
```bash
python run_tests.py
```

Expected output:
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
  Run 1/2... ✓ Response (287 chars)
  Run 2/2... ✓ Response (302 chars)

...

SUMMARY:
  Total tests: 38
  Success: 24
  Partial: 8
  Fail: 4
  Refuses: 2
  Errors: 0
  Success Rate: 63.2%
```

### Step 6: Analyze Results with Jupyter
```bash
jupyter notebook analysis.ipynb
```

Open the notebook and run all cells to see visualizations and analysis.

---

## 📊 Using the Interactive Notebook

1. The notebook automatically loads the latest test results
2. Run cells in order to generate:
   - Summary statistics
   - Success rate by category
   - Response time analysis
   - Detailed findings
3. Modify cells to create custom visualizations

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
MODEL_NAME = "mistral"  # or "llama2", "neural-chat", etc.
TEST_RUNS_PER_PROMPT = 2  # How many times to test each prompt
TEMPERATURE = 0.7  # 0=deterministic, 1=creative
MAX_TOKENS = 512  # Max response length
```

> **Note**: Lower temperature (0.3-0.5) gives more consistent results for testing reasoning. Higher temperature (0.7-1.0) reveals more variance/failures.

---

## 📁 Project Structure Quick Reference

```
AIML Assignment-24(28th March)/
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
├── requirements.txt       ← Python packages to install
├── config.py              ← Configuration settings
├── test_runner.py         ← Core testing framework
├── run_tests.py           ← Main script to run
├── setup.sh              ← Automated setup script
│
├── prompts/              ← Test prompts folder
│   └── prompts.json      ← 19 adversarial prompts
│
├── results/              ← Test results folder
│   ├── test_results_*.json  ← Raw results (JSON)
│   ├── test_results_*.csv   ← Raw results (CSV)
│   └── logs/               ← Detailed logs
│
└── analysis.ipynb        ← Result visualization notebook
```

---

## ⚠️ Troubleshooting

### "Connection error - is Ollama running?"
**Solution**: Make sure Ollama server is running in another terminal:
```bash
ollama serve
```

### "Model not found"
**Solution**: Pull the model first:
```bash
ollama pull mistral
```

### "Can't find requirements.txt"
**Solution**: Make sure you're in the correct directory:
```bash
cd "AIML Assignment-24(28th March)"
```

### "Slow responses / Long execution time"
**Solution**: This is normal for the first run. Mistral uses random sampling, so all 38 tests (19 prompts × 2 runs) can take 5-10 minutes depending on your Mac's specs.

### "What if my Mac doesn't have enough RAM?"
Try the smaller model:
```bash
# Stop current model
ollama stop mistral

# Try a smaller one
ollama pull neural-chat  # 4.6GB
# or
ollama pull orca-mini    # 2.7GB
```

Then update `config.py`:
```python
MODEL_NAME = "neural-chat"
```

---

## 📈 Expected Results

Typical success rates by category:
- **Logical Contradictions**: 60-70% ✓
- **Ambiguous Language**: 60-70% ✓
- **False Premises**: 40-50% ⚠️
- **Self-Reference**: 25-35% ✗
- **Conflicting Requirements**: 40-50% ⚠️
- **Knowledge Gaps**: 60-75% ✓

**Overall**: ~60% success rate (varies by model)

---

## 🎯 What to Do Next

1. **Run the tests** (`python run_tests.py`)
2. **View results** (`jupyter notebook analysis.ipynb`)
3. **Read the report** (Open `REPORT.md`)
4. **Try modifications**:
   - Change temperature to test consistency
   - Edit prompts to be harder/easier
   - Add your own test prompts
   - Compare against other models

---

## 💡 Tips for Better Results

**For Consistency Testing**:
```python
# In config.py
TEMPERATURE = 0.1  # Very deterministic
TEST_RUNS_PER_PROMPT = 5  # More runs = see variance
```

**For Exploring Edge Cases**:
```python
# In config.py  
TEMPERATURE = 1.0  # Very creative/random
```

**For Faster Initial Testing**:
```python
# In config.py
TEST_RUNS_PER_PROMPT = 1  # Skip repetition
MAX_TOKENS = 256  # Shorter responses
```

---

## 📚 Learn More

- See `README.md` for full documentation
- See `REPORT.md` template for analysis structure
- See `prompts/prompts.json` for all test cases with detailed intent descriptions

---

**Ready to break some AI?** 🚀

```bash
python run_tests.py
```
