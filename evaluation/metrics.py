import numpy as np
from typing import Dict, List
from difflib import SequenceMatcher

class EvaluationMetrics:
    def __init__(self):
        pass
    
    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using SequenceMatcher."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def calculate_response_length(self, response: str) -> int:
        """Calculate the length of the response in tokens."""
        return len(response.split())
    
    def calculate_response_quality(self, response: str) -> float:
        """Calculate a simple quality score based on length and completeness."""
        words = response.split()
        
        # Base score from length (optimal around 50-200 words)
        length_score = min(len(words) / 100, 1.0)
        
        # Completeness score (ends with punctuation)
        completeness_score = 1.0 if response.strip().endswith(('.', '!', '?')) else 0.7
        
        # Diversity score (unique words ratio)
        unique_words = len(set(words))
        diversity_score = unique_words / max(len(words), 1) if words else 0
        
        return (length_score * 0.4 + completeness_score * 0.3 + diversity_score * 0.3)
    
    def evaluate_responses(self, prompt: str, responses: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """Evaluate all responses using multiple metrics."""
        metrics = {}
        
        for model, response in responses.items():
            # Calculate similarity to prompt
            similarity = self.calculate_similarity_score(prompt, response)
            
            # Calculate response length
            length = self.calculate_response_length(response)
            
            # Calculate quality score
            quality = self.calculate_response_quality(response)
            
            # Combine all metrics
            metrics[model] = {
                'similarity_score': similarity,
                'quality_score': quality,
                'response_length': length,
                'overall_score': (similarity * 0.3 + quality * 0.7)
            }
        
        return metrics 