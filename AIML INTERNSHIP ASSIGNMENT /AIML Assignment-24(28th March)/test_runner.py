"""
Test runner for adversarial LLM prompt testing
Handles communication with local LLM, logging responses, and analyzing results
"""
import json
import csv
import time
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path
import config


class PromptTester:
    """Handles communication with the LLM model"""
    
    def __init__(self, model: str = config.MODEL_NAME, endpoint: str = config.MODEL_ENDPOINT):
        self.model = model
        self.endpoint = endpoint
        self.timeout = config.REQUEST_TIMEOUT
    
    def test_prompt(self, prompt: str, run_id: int = 1) -> Dict:
        """
        Send a prompt to the LLM and get a response
        
        Args:
            prompt: The prompt to test
            run_id: Which run number this is (for tracking consistency)
        
        Returns:
            Dictionary with response data
        """
        start_time = time.time()
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": config.TEMPERATURE,
                "stream": False,
            }
            
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result_data = response.json()
            elapsed_time = time.time() - start_time
            
            return {
                "status": "success",
                "response": result_data.get("response", ""),
                "model": self.model,
                "elapsed_time": elapsed_time,
                "tokens_used": result_data.get("eval_count", 0),
                "error": None,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
            }
        
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "response": "",
                "model": self.model,
                "elapsed_time": time.time() - start_time,
                "tokens_used": 0,
                "error": "Request timeout",
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "response": "",
                "model": self.model,
                "elapsed_time": time.time() - start_time,
                "tokens_used": 0,
                "error": "Connection error - is Ollama running?",
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
            }
        
        except Exception as e:
            return {
                "status": "error",
                "response": "",
                "model": self.model,
                "elapsed_time": time.time() - start_time,
                "tokens_used": 0,
                "error": str(e),
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
            }


class ResponseLogger:
    """Handles logging and persistence of test results"""
    
    def __init__(self, json_file: str = config.RESULTS_FILE, csv_file: str = config.CSV_FILE):
        self.json_file = json_file
        self.csv_file = csv_file
        self.results = []
    
    def log_result(self, prompt_id: str, category: str, prompt: str, test_result: Dict) -> None:
        """
        Log a single test result
        
        Args:
            prompt_id: Unique identifier for the prompt
            category: Category of the prompt
            prompt: The original prompt text
            test_result: Result dictionary from PromptTester
        """
        entry = {
            "prompt_id": prompt_id,
            "category": category,
            "prompt_text": prompt,
            "response_text": test_result.get("response", "")[:1000],  # Truncate for storage
            "elapsed_time": test_result.get("elapsed_time", 0),
            "tokens_used": test_result.get("tokens_used", 0),
            "test_status": test_result.get("status", "unknown"),
            "error": test_result.get("error"),
            "run_id": test_result.get("run_id", 0),
            "timestamp": test_result.get("timestamp"),
            "response_category": None,  # Will be filled by ResultAnalyzer
        }
        self.results.append(entry)
    
    def save_results(self) -> None:
        """Save all logged results to JSON and CSV files"""
        # Save to JSON
        with open(self.json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {self.json_file}")
        
        # Save to CSV
        if self.results:
            keys = self.results[0].keys()
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)
            print(f"Results saved to {self.csv_file}")


class ResultAnalyzer:
    """Analyzes and categorizes test results"""
    
    @staticmethod
    def analyze_response(prompt: str, response: str, error: Optional[str] = None) -> str:
        """
        Classify a response as success, partial, fail, or refuses
        
        Args:
            prompt: The original prompt
            response: The response from the LLM
            error: Any error message from execution
        
        Returns:
            Category string: "success", "partial", "fail", "refuses", or "error"
        """
        if error:
            return "error"
        
        response_lower = response.lower()
        
        # Check if model refused to engage
        refuse_keywords = ["cannot", "cannot answer", "i don't", "don't know", "unclear",
                          "not possible", "undefined", "i should not", "i can't", "unable to"]
        if any(keyword in response_lower for keyword in refuse_keywords):
            # But if it also provided an explanation, it's partial
            if len(response.split()) > 5:
                return "partial"
            return "refuses"
        
        # Check for success indicators
        success_keywords = ["paradox", "contradiction", "not possible", "logical",
                           "because", "could be interpreted", "ambiguous", "depends on"]
        if any(keyword in response_lower for keyword in success_keywords):
            return "success"
        
        # Check for obviously wrong/nonsensical responses
        if len(response.strip()) < 5:
            return "fail"
        
        # If response addresses the prompt thoughtfully, it's at least partial
        if len(response.split()) > 8:
            return "partial"
        
        return "fail"
    
    @staticmethod
    def generate_summary(results_list: List[Dict]) -> Dict:
        """
        Generate a summary analysis of all results
        
        Args:
            results_list: List of result dictionaries
        
        Returns:
            Summary dictionary with counts and percentages
        """
        summary = {
            "total_tests": len(results_list),
            "success": 0,
            "partial": 0,
            "fail": 0,
            "refuses": 0,
            "error": 0,
            "by_category": {},
        }
        
        for result in results_list:
            status = result.get("test_status", "unknown")
            if status == "success":
                response_category = ResultAnalyzer.analyze_response(
                    result.get("prompt_text", ""),
                    result.get("response_text", ""),
                    result.get("error")
                )
            else:
                response_category = status
            
            summary[response_category] = summary.get(response_category, 0) + 1
            
            category = result.get("category", "unknown")
            if category not in summary["by_category"]:
                summary["by_category"][category] = {"success": 0, "partial": 0, "fail": 0, "refuses": 0, "error": 0}
            summary["by_category"][category][response_category] = \
                summary["by_category"][category].get(response_category, 0) + 1
        
        # Calculate percentages
        summary["success_rate"] = (summary["success"] / summary["total_tests"] * 100) if summary["total_tests"] > 0 else 0
        
        return summary


if __name__ == "__main__":
    print("Test runner module loaded successfully")
