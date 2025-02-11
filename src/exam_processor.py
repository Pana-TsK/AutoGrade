import json
import csv
from typing import Dict, List

class ExamProcessor:
    """
    Processes an exam by extracting, analyzing, and grading answers, then saving results to a file.
    """
    def __init__(self, correct_answers_file: str, output_file: str, output_format: str = "csv"):
        """
        Initialize the ExamProcessor.
        
        :param correct_answers_file: Path to the JSON file containing correct answers.
        :param output_file: Path to the output file (CSV or JSON).
        :param output_format: Output format ("csv" or "json").
        """
        self.correct_answers_file = correct_answers_file
        self.output_file = output_file
        self.output_format = output_format
        self.correct_answers = self._load_correct_answers()

    def _load_correct_answers(self) -> Dict[int, str]:
        """
        Load correct answers from the JSON file.
        
        :return: Dictionary mapping question numbers to correct answers.
        """
        try:
            with open(self.correct_answers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading correct answers: {e}")
            return {}

    def save_results(self, results: List[Dict]):
        """
        Save the grading results to a file (CSV or JSON).
        
        :param results: List of dictionaries containing grading results.
        """
        if self.output_format == "csv":
            self._save_to_csv(results)
        elif self.output_format == "json":
            self._save_to_json(results)
        else:
            raise ValueError("Invalid output format. Use 'csv' or 'json'.")

    def _save_to_csv(self, results: List[Dict]):
        """
        Save results to a CSV file.
        
        :param results: List of dictionaries containing grading results.
        """
        try:
            with open(self.output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            print(f"Results saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving results to CSV: {e}")

    def _save_to_json(self, results: List[Dict]):
        """
        Save results to a JSON file.
        
        :param results: List of dictionaries containing grading results.
        """
        try:
            with open(self.output_file, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"Results saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving results to JSON: {e}")