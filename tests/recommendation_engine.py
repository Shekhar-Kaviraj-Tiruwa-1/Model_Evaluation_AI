import os
import sys
import re
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.llm_engine import LLMEngine
from evaluation.metrics import EvaluationMetrics

class RecommendationEngine:
    """Smart recommendation engine for suggesting the best model for given prompts."""
    
    def __init__(self):
        self.evaluator = EvaluationMetrics()
        
        # Historical performance data (this would be loaded from database in production)
        self.performance_history = {
            "GPT2": {
                "Electric Vehicles": {"avg_score": 0.785, "sample_size": 15},
                "AI/Technology": {"avg_score": 0.820, "sample_size": 12},
                "Climate/Environment": {"avg_score": 0.756, "sample_size": 8},
                "Business/Economics": {"avg_score": 0.792, "sample_size": 10},
                "General Technical": {"avg_score": 0.778, "sample_size": 18}
            },
            "DistilGPT2": {
                "Electric Vehicles": {"avg_score": 0.720, "sample_size": 15},
                "AI/Technology": {"avg_score": 0.745, "sample_size": 12},
                "Climate/Environment": {"avg_score": 0.701, "sample_size": 8},
                "Business/Economics": {"avg_score": 0.734, "sample_size": 10},
                "General Technical": {"avg_score": 0.715, "sample_size": 18}
            },
            "T5-Small": {
                "Electric Vehicles": {"avg_score": 0.698, "sample_size": 15},
                "AI/Technology": {"avg_score": 0.712, "sample_size": 12},
                "Climate/Environment": {"avg_score": 0.723, "sample_size": 8},
                "Business/Economics": {"avg_score": 0.687, "sample_size": 10},
                "General Technical": {"avg_score": 0.705, "sample_size": 18}
            },
            "BERT-Base": {
                "Electric Vehicles": {"avg_score": 0.665, "sample_size": 15},
                "AI/Technology": {"avg_score": 0.689, "sample_size": 12},
                "Climate/Environment": {"avg_score": 0.678, "sample_size": 8},
                "Business/Economics": {"avg_score": 0.671, "sample_size": 10},
                "General Technical": {"avg_score": 0.682, "sample_size": 18}
            }
        }
        
        # Model characteristics for recommendation logic
        self.model_characteristics = {
            "GPT2": {
                "strengths": ["comprehensive analysis", "detailed explanations", "versatile reasoning"],
                "best_for": ["complex topics", "analytical tasks", "creative content"],
                "response_style": "Detailed and comprehensive",
                "avg_length": 180,
                "processing_time": "Medium"
            },
            "DistilGPT2": {
                "strengths": ["quick responses", "concise summaries", "efficient processing"],
                "best_for": ["quick queries", "summaries", "simple explanations"],
                "response_style": "Concise and direct",
                "avg_length": 120,
                "processing_time": "Fast"
            },
            "T5-Small": {
                "strengths": ["structured output", "text transformation", "clear organization"],
                "best_for": ["structured responses", "technical explanations", "organized content"],
                "response_style": "Well-structured and organized",
                "avg_length": 150,
                "processing_time": "Medium"
            },
            "BERT-Base": {
                "strengths": ["context understanding", "semantic analysis", "nuanced responses"],
                "best_for": ["context-heavy tasks", "semantic understanding", "precise analysis"],
                "response_style": "Context-aware and precise",
                "avg_length": 140,
                "processing_time": "Medium-Slow"
            }
        }
    
    def categorize_prompt(self, prompt: str) -> str:
        """Categorize a prompt to determine the best domain match."""
        prompt_lower = prompt.lower()
        
        # Category keywords with weights
        categories = {
            "Electric Vehicles": {
                "keywords": ["electric", "ev", "vehicle", "automotive", "car", "battery", "charging", "tesla", "hybrid"],
                "score": 0
            },
            "AI/Technology": {
                "keywords": ["ai", "artificial", "intelligence", "machine", "learning", "neural", "algorithm", "data", "tech", "software"],
                "score": 0
            },
            "Climate/Environment": {
                "keywords": ["climate", "environment", "renewable", "sustainability", "carbon", "emission", "green", "energy", "solar", "wind"],
                "score": 0
            },
            "Business/Economics": {
                "keywords": ["business", "economy", "market", "finance", "startup", "enterprise", "revenue", "profit", "strategy", "investment"],
                "score": 0
            },
            "General Technical": {
                "keywords": ["technical", "system", "process", "method", "principle", "concept", "theory", "analysis", "research"],
                "score": 0
            }
        }
        
        # Calculate scores for each category
        words = re.findall(r'\b\w+\b', prompt_lower)
        for word in words:
            for category, data in categories.items():
                if word in data["keywords"]:
                    data["score"] += 1
        
        # Find best match
        best_category = max(categories.keys(), key=lambda cat: categories[cat]["score"])
        
        # If no strong match, check for general technical terms
        if categories[best_category]["score"] == 0:
            return "General Technical"
        
        return best_category
    
    def analyze_prompt_complexity(self, prompt: str) -> Dict[str, float]:
        """Analyze prompt complexity to inform model selection."""
        words = prompt.split()
        sentences = prompt.count('.') + prompt.count('!') + prompt.count('?')
        
        # Complexity indicators
        complexity_score = 0.0
        
        # Length factor
        if len(words) > 20:
            complexity_score += 0.3
        elif len(words) > 10:
            complexity_score += 0.2
        else:
            complexity_score += 0.1
        
        # Question complexity
        question_words = ["how", "why", "what", "when", "where", "explain", "analyze", "compare", "evaluate"]
        question_count = sum(1 for word in words if word.lower() in question_words)
        complexity_score += min(question_count * 0.15, 0.4)
        
        # Technical terms
        technical_terms = ["system", "process", "methodology", "framework", "implementation", "optimization"]
        tech_count = sum(1 for word in words if word.lower() in technical_terms)
        complexity_score += min(tech_count * 0.1, 0.3)
        
        return {
            "complexity_score": min(complexity_score, 1.0),
            "word_count": len(words),
            "sentence_count": max(sentences, 1),
            "question_complexity": question_count,
            "technical_density": tech_count / len(words) if words else 0
        }
    
    def get_model_recommendation(self, prompt: str, user_preferences: Optional[Dict] = None) -> Dict:
        """Get the best model recommendation for a given prompt."""
        # Categorize the prompt
        category = self.categorize_prompt(prompt)
        
        # Analyze complexity
        complexity = self.analyze_prompt_complexity(prompt)
        
        # Get historical performance for this category
        category_performance = {}
        for model, categories in self.performance_history.items():
            if category in categories:
                perf = categories[category]
                # Weight by sample size and recency
                confidence = min(perf["sample_size"] / 10, 1.0)
                category_performance[model] = {
                    "score": perf["avg_score"],
                    "confidence": confidence,
                    "sample_size": perf["sample_size"]
                }
        
        # Apply user preferences if provided
        preference_boost = 0.0
        if user_preferences:
            if user_preferences.get("prefer_speed", False):
                # Boost DistilGPT2 for speed preference
                if "DistilGPT2" in category_performance:
                    category_performance["DistilGPT2"]["score"] += 0.05
            
            if user_preferences.get("prefer_detail", False):
                # Boost GPT2 for detail preference
                if "GPT2" in category_performance:
                    category_performance["GPT2"]["score"] += 0.05
            
            if user_preferences.get("prefer_structure", False):
                # Boost T5-Small for structure preference
                if "T5-Small" in category_performance:
                    category_performance["T5-Small"]["score"] += 0.05
        
        # Adjust for complexity
        if complexity["complexity_score"] > 0.7:
            # High complexity - favor GPT2
            if "GPT2" in category_performance:
                category_performance["GPT2"]["score"] += 0.03
        elif complexity["complexity_score"] < 0.3:
            # Low complexity - favor DistilGPT2
            if "DistilGPT2" in category_performance:
                category_performance["DistilGPT2"]["score"] += 0.03
        
        # Sort by adjusted score
        ranked_models = sorted(
            category_performance.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        if not ranked_models:
            # Fallback recommendation
            return {
                "recommended_model": "GPT2",
                "confidence": 0.5,
                "reason": "Default recommendation due to no historical data",
                "category": category,
                "alternatives": ["DistilGPT2", "T5-Small"],
                "complexity": complexity
            }
        
        # Best recommendation
        best_model, best_perf = ranked_models[0]
        alternatives = [model for model, _ in ranked_models[1:3]]
        
        # Generate recommendation reason
        model_char = self.model_characteristics[best_model]
        reason_parts = [
            f"Best historical performance for {category} ({best_perf['score']:.3f})",
            f"Model strengths: {', '.join(model_char['strengths'][:2])}",
            f"Complexity match: {complexity['complexity_score']:.2f}"
        ]
        
        return {
            "recommended_model": best_model,
            "confidence": best_perf["confidence"],
            "reason": "; ".join(reason_parts),
            "category": category,
            "alternatives": alternatives,
            "complexity": complexity,
            "model_characteristics": model_char,
            "expected_response_length": model_char["avg_length"],
            "all_scores": {model: perf["score"] for model, perf in category_performance.items()}
        }
    
    def get_multi_model_recommendation(self, prompt: str, max_models: int = 3) -> Dict:
        """Recommend multiple models for comparison based on different strengths."""
        category = self.categorize_prompt(prompt)
        complexity = self.analyze_prompt_complexity(prompt)
        
        # Get all model scores for this category
        model_scores = {}
        for model, categories in self.performance_history.items():
            if category in categories:
                model_scores[model] = categories[category]["avg_score"]
        
        # Sort by performance
        sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Select diverse models
        recommendations = []
        
        if sorted_models:
            # Always include the best performer
            best_model, best_score = sorted_models[0]
            recommendations.append({
                "model": best_model,
                "reason": f"Highest performance for {category}",
                "expected_score": best_score,
                "characteristics": self.model_characteristics[best_model]
            })
            
            # Add complementary models
            remaining_models = [m for m, _ in sorted_models[1:]]
            
            # Add speed option if not already included
            if "DistilGPT2" in remaining_models and len(recommendations) < max_models:
                recommendations.append({
                    "model": "DistilGPT2",
                    "reason": "Fastest response time",
                    "expected_score": model_scores.get("DistilGPT2", 0.7),
                    "characteristics": self.model_characteristics["DistilGPT2"]
                })
                remaining_models.remove("DistilGPT2")
            
            # Add structure option if not already included
            if "T5-Small" in remaining_models and len(recommendations) < max_models:
                recommendations.append({
                    "model": "T5-Small",
                    "reason": "Best structured responses",
                    "expected_score": model_scores.get("T5-Small", 0.7),
                    "characteristics": self.model_characteristics["T5-Small"]
                })
                remaining_models.remove("T5-Small")
            
            # Fill remaining slots
            for model in remaining_models[:max_models - len(recommendations)]:
                recommendations.append({
                    "model": model,
                    "reason": f"Alternative perspective",
                    "expected_score": model_scores.get(model, 0.7),
                    "characteristics": self.model_characteristics[model]
                })
        
        return {
            "recommendations": recommendations,
            "category": category,
            "complexity": complexity,
            "comparison_strategy": "Diversified model selection for comprehensive comparison"
        }
    
    def update_performance_history(self, prompt: str, model: str, score: float):
        """Update historical performance data with new results."""
        category = self.categorize_prompt(prompt)
        
        if model not in self.performance_history:
            self.performance_history[model] = {}
        
        if category not in self.performance_history[model]:
            self.performance_history[model][category] = {"avg_score": score, "sample_size": 1}
        else:
            current = self.performance_history[model][category]
            # Update running average
            total_score = current["avg_score"] * current["sample_size"] + score
            new_sample_size = current["sample_size"] + 1
            new_avg = total_score / new_sample_size
            
            self.performance_history[model][category] = {
                "avg_score": new_avg,
                "sample_size": new_sample_size
            }
    
    def generate_recommendation_summary(self, prompt: str) -> str:
        """Generate a user-friendly recommendation summary."""
        rec = self.get_model_recommendation(prompt)
        
        summary = f"""
🎯 **Smart Model Recommendation**

**For your prompt about {rec['category']}:**
• **Recommended Model**: {rec['recommended_model']}
• **Confidence**: {rec['confidence']:.1%}
• **Expected Response Length**: ~{rec['expected_response_length']} words

**Why {rec['recommended_model']}?**
{rec['reason']}

**Model Characteristics:**
• Style: {rec['model_characteristics']['response_style']}
• Strengths: {', '.join(rec['model_characteristics']['strengths'])}
• Processing Time: {rec['model_characteristics']['processing_time']}

**Alternative Options**: {', '.join(rec['alternatives'])}

**Complexity Analysis**: {rec['complexity']['complexity_score']:.1%} complex
"""
        return summary.strip()

def test_recommendation_engine():
    """Test the recommendation engine with sample prompts."""
    engine = RecommendationEngine()
    
    test_prompts = [
        "Explain the future of electric vehicles in the automotive industry",
        "How does machine learning work in simple terms?",
        "What are renewable energy solutions for climate change?",
        "Analyze business strategies for digital transformation",
        "Explain quantum computing concepts"
    ]
    
    print("🧪 Testing Recommendation Engine")
    print("=" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n[{i}] Testing: {prompt}")
        rec = engine.get_model_recommendation(prompt)
        print(f"   🎯 Recommended: {rec['recommended_model']}")
        print(f"   📊 Category: {rec['category']}")
        print(f"   💪 Confidence: {rec['confidence']:.1%}")
        print(f"   🔄 Alternatives: {', '.join(rec['alternatives'])}")

if __name__ == "__main__":
    test_recommendation_engine() 