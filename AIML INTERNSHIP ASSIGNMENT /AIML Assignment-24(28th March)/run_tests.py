#!/usr/bin/env python3
"""
Main test execution script - orchestrates the full testing pipeline
"""
import json
import sys
from pathlib import Path
from test_runner import PromptTester, ResponseLogger, ResultAnalyzer
import config


def load_prompts(prompt_file: str = "prompts/prompts.json") -> list:
    """Load test prompts from JSON file"""
    try:
        with open(prompt_file, 'r') as f:
            data = json.load(f)
        return data.get("prompts", [])
    except FileNotFoundError:
        print(f"Error: {prompt_file} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {prompt_file} is not valid JSON")
        sys.exit(1)


def run_test_suite():
    """Execute the complete adversarial test suite"""
    
    print("=" * 70)
    print("LLM ADVERSARIAL PROMPT TESTING SUITE")
    print("=" * 70)
    print()
    
    # Load configuration
    print(f"Model: {config.MODEL_NAME}")
    print(f"Endpoint: {config.MODEL_ENDPOINT}")
    print(f"Temperature: {config.TEMPERATURE}")
    print(f"Test runs per prompt: {config.TEST_RUNS_PER_PROMPT}")
    print()
    
    # Load prompts
    prompts = load_prompts()
    print(f"Loaded {len(prompts)} test prompts")
    print()
    
    # Initialize testing components
    tester = PromptTester(config.MODEL_NAME, config.MODEL_ENDPOINT)
    logger = ResponseLogger(config.RESULTS_FILE, config.CSV_FILE)
    
    # Execute tests
    print("Starting test execution...")
    print("-" * 70)
    
    total_tests = len(prompts) * config.TEST_RUNS_PER_PROMPT
    completed = 0
    
    for i, prompt_data in enumerate(prompts, 1):
        prompt_id = prompt_data.get("id", f"unknown_{i}")
        category = prompt_data.get("category", "unknown")
        prompt_text = prompt_data.get("prompt", "")
        
        print(f"\n[{i}/{len(prompts)}] {prompt_id} ({category})")
        print(f"Prompt: {prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}")
        
        # Run each prompt multiple times
        for run in range(1, config.TEST_RUNS_PER_PROMPT + 1):
            print(f"  Run {run}/{config.TEST_RUNS_PER_PROMPT}...", end=" ")
            
            result = tester.test_prompt(prompt_text, run_id=run)
            logger.log_result(prompt_id, category, prompt_text, result)
            
            completed += 1
            status = result.get("status", "unknown")
            
            if status == "error":
                print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
                if "Connection error" in result.get("error", ""):
                    print("\nFATAL: Cannot connect to LLM. Please ensure Ollama is running:")
                    print("  $ ollama serve")
                    sys.exit(1)
            elif status == "success":
                response_len = len(result.get("response", ""))
                print(f"✓ Response ({response_len} chars)")
            else:
                print(f"? Status: {status}")
    
    print()
    print("-" * 70)
    print(f"Test execution complete: {completed}/{total_tests} tests run")
    print()
    
    # Save results
    logger.save_results()
    
    # Generate summary
    print("Generating summary analysis...")
    summary = ResultAnalyzer.generate_summary(logger.results)
    
    print()
    print("SUMMARY:")
    print(f"  Total tests: {summary['total_tests']}")
    print(f"  Success: {summary.get('success', 0)}")
    print(f"  Partial: {summary.get('partial', 0)}")
    print(f"  Fail: {summary.get('fail', 0)}")
    print(f"  Refuses: {summary.get('refuses', 0)}")
    print(f"  Errors: {summary.get('error', 0)}")
    print(f"  Success Rate: {summary.get('success_rate', 0):.1f}%")
    print()
    
    print("By Category:")
    for category, counts in summary.get("by_category", {}).items():
        total = sum(counts.values())
        success = counts.get("success", 0)
        rate = (success / total * 100) if total > 0 else 0
        print(f"  {category}: {success}/{total} ({rate:.0f}%)")
    
    print()
    print(f"Results saved to:")
    print(f"  JSON: {config.RESULTS_FILE}")
    print(f"  CSV:  {config.CSV_FILE}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_test_suite()
    except KeyboardInterrupt:
        print("\n\nTest suite interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
