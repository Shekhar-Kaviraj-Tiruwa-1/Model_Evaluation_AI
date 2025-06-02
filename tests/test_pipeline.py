import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.llm_engine import LLMEngine
from evaluation.metrics import EvaluationMetrics
from utils.database import Database

@dataclass
class TestResult:
    """Data class to store test results."""
    prompt: str
    model_responses: Dict[str, str]
    metrics: Dict[str, Dict[str, float]]
    best_model: str
    best_score: float
    execution_time: float
    timestamp: datetime

class TestPipeline:
    """Comprehensive test pipeline for ModelEval.AI platform."""
    
    def __init__(self):
        self.engine = LLMEngine()
        self.evaluator = EvaluationMetrics()
        self.db = Database()
        self.test_results = []
        
        # Test prompts covering different domains
        self.test_prompts = [
            # Electric Vehicles
            "Explain the future of electric vehicles and their impact on the automotive industry.",
            "What are the main challenges facing electric vehicle adoption globally?",
            "Compare the environmental benefits of electric vehicles versus traditional cars.",
            
            # AI/Technology
            "How is artificial intelligence transforming healthcare?",
            "Explain the potential risks and benefits of machine learning in finance.",
            "What role will AI play in education over the next decade?",
            
            # Climate/Environment
            "Describe renewable energy solutions for sustainable development.",
            "How can businesses reduce their carbon footprint effectively?",
            "Explain the role of technology in fighting climate change.",
            
            # Business/Economics
            "What factors drive successful digital transformation in enterprises?",
            "Analyze the impact of remote work on business productivity.",
            "How do startups compete with established corporations?",
            
            # General Technical
            "Explain quantum computing in simple terms.",
            "What are the key principles of cybersecurity?",
            "How does blockchain technology work and what are its applications?"
        ]
        
        self.test_models = ["GPT2", "DistilGPT2", "T5-Small", "BERT-Base"]
    
    def run_single_test(self, prompt: str, models: List[str] = None) -> TestResult:
        """Run a single test with the given prompt."""
        if models is None:
            models = self.test_models
            
        print(f"\n🧪 Running test: {prompt[:50]}...")
        start_time = time.time()
        
        # Generate responses from all models
        responses = {}
        for model in models:
            try:
                print(f"  📡 Testing {model}...")
                response = self.engine.generate_response(model, prompt)
                responses[model] = response
                print(f"    ✅ {model}: {len(response)} chars")
            except Exception as e:
                print(f"    ❌ {model}: Error - {str(e)}")
                responses[model] = f"Error: {str(e)}"
        
        # Evaluate responses
        metrics = self.evaluator.evaluate_responses(prompt, responses)
        
        # Find best model
        best_model = max(metrics.keys(), key=lambda m: metrics[m]['overall_score'])
        best_score = metrics[best_model]['overall_score']
        
        execution_time = time.time() - start_time
        
        # Create test result
        result = TestResult(
            prompt=prompt,
            model_responses=responses,
            metrics=metrics,
            best_model=best_model,
            best_score=best_score,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        
        self.test_results.append(result)
        print(f"  🏆 Best: {best_model} (Score: {best_score:.3f})")
        
        return result
    
    def run_full_test_suite(self) -> List[TestResult]:
        """Run the complete test suite with all prompts."""
        print("🚀 Starting ModelEval.AI Test Pipeline")
        print(f"📋 Testing {len(self.test_prompts)} prompts across {len(self.test_models)} models")
        print("=" * 60)
        
        results = []
        total_start = time.time()
        
        for i, prompt in enumerate(self.test_prompts, 1):
            print(f"\n[{i}/{len(self.test_prompts)}] {prompt}")
            result = self.run_single_test(prompt)
            results.append(result)
            
            # Progress indicator
            progress = (i / len(self.test_prompts)) * 100
            print(f"Progress: {progress:.1f}%")
        
        total_time = time.time() - total_start
        print(f"\n✅ Test suite completed in {total_time:.2f} seconds")
        
        return results
    
    def analyze_results(self) -> Dict:
        """Analyze test results and generate recommendations."""
        if not self.test_results:
            return {"error": "No test results available"}
        
        # Model performance analysis
        model_wins = {}
        model_scores = {}
        model_categories = {}
        
        for result in self.test_results:
            # Count wins
            winner = result.best_model
            model_wins[winner] = model_wins.get(winner, 0) + 1
            
            # Aggregate scores
            for model, metrics in result.metrics.items():
                if model not in model_scores:
                    model_scores[model] = []
                model_scores[model].append(metrics['overall_score'])
                
                # Category analysis
                category = self._categorize_prompt(result.prompt)
                if model not in model_categories:
                    model_categories[model] = {}
                if category not in model_categories[model]:
                    model_categories[model][category] = []
                model_categories[model][category].append(metrics['overall_score'])
        
        # Calculate average scores
        model_avg_scores = {
            model: sum(scores) / len(scores)
            for model, scores in model_scores.items()
        }
        
        # Find overall best model
        best_overall = max(model_avg_scores.keys(), key=lambda m: model_avg_scores[m])
        
        # Category recommendations
        category_recommendations = {}
        for category in ["Electric Vehicles", "AI/Technology", "Climate/Environment", "Business/Economics", "General Technical"]:
            category_scores = {}
            for model in self.test_models:
                if model in model_categories and category in model_categories[model]:
                    scores = model_categories[model][category]
                    category_scores[model] = sum(scores) / len(scores)
            
            if category_scores:
                best_for_category = max(category_scores.keys(), key=lambda m: category_scores[m])
                category_recommendations[category] = {
                    "best_model": best_for_category,
                    "score": category_scores[best_for_category],
                    "all_scores": category_scores
                }
        
        return {
            "summary": {
                "total_tests": len(self.test_results),
                "models_tested": len(self.test_models),
                "best_overall_model": best_overall,
                "best_overall_score": model_avg_scores[best_overall]
            },
            "model_performance": {
                "wins": model_wins,
                "average_scores": model_avg_scores,
                "total_scores": {model: len(scores) for model, scores in model_scores.items()}
            },
            "category_recommendations": category_recommendations,
            "execution_stats": {
                "total_execution_time": sum(r.execution_time for r in self.test_results),
                "average_per_test": sum(r.execution_time for r in self.test_results) / len(self.test_results)
            }
        }
    
    def _categorize_prompt(self, prompt: str) -> str:
        """Categorize a prompt based on its content."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["electric", "ev", "vehicle", "automotive", "car"]):
            return "Electric Vehicles"
        elif any(word in prompt_lower for word in ["ai", "artificial", "intelligence", "machine", "learning"]):
            return "AI/Technology"
        elif any(word in prompt_lower for word in ["climate", "environment", "renewable", "sustainability", "energy"]):
            return "Climate/Environment"
        elif any(word in prompt_lower for word in ["business", "enterprise", "startup", "economic", "finance"]):
            return "Business/Economics"
        else:
            return "General Technical"
    
    def generate_recommendation_report(self) -> str:
        """Generate a comprehensive recommendation report."""
        analysis = self.analyze_results()
        
        if "error" in analysis:
            return analysis["error"]
        
        report = []
        report.append("🔬 MODELEVAL.AI - TEST PIPELINE REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        summary = analysis["summary"]
        report.append("📊 EXECUTIVE SUMMARY")
        report.append(f"• Total Tests Conducted: {summary['total_tests']}")
        report.append(f"• Models Evaluated: {summary['models_tested']}")
        report.append(f"• Best Overall Model: {summary['best_overall_model']}")
        report.append(f"• Best Overall Score: {summary['best_overall_score']:.3f}")
        report.append("")
        
        # Model Performance
        performance = analysis["model_performance"]
        report.append("🏆 MODEL PERFORMANCE RANKING")
        sorted_models = sorted(performance["average_scores"].items(), key=lambda x: x[1], reverse=True)
        
        for i, (model, score) in enumerate(sorted_models, 1):
            wins = performance["wins"].get(model, 0)
            report.append(f"{i}. {model}: {score:.3f} avg score ({wins} wins)")
        report.append("")
        
        # Category Recommendations
        report.append("💡 DOMAIN-SPECIFIC RECOMMENDATIONS")
        for category, rec in analysis["category_recommendations"].items():
            report.append(f"• {category}: Use {rec['best_model']} (Score: {rec['score']:.3f})")
        report.append("")
        
        # Performance Insights
        report.append("🔍 KEY INSIGHTS")
        best_model = summary['best_overall_model']
        worst_model = min(performance["average_scores"].keys(), key=lambda m: performance["average_scores"][m])
        
        report.append(f"• {best_model} consistently delivers the highest quality responses")
        report.append(f"• {worst_model} shows the lowest average performance")
        report.append(f"• Average response time: {analysis['execution_stats']['average_per_test']:.2f}s per test")
        report.append("")
        
        # Recommendations
        report.append("🎯 ACTIONABLE RECOMMENDATIONS")
        report.append(f"1. Use {best_model} as the default model for general queries")
        report.append("2. Implement domain-specific routing based on prompt analysis")
        report.append("3. Consider response time vs quality trade-offs for user experience")
        report.append("4. Monitor model performance trends over time")
        
        return "\n".join(report)
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """Save test results to a JSON file."""
        if filename is None:
            filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert results to serializable format
        serializable_results = []
        for result in self.test_results:
            serializable_results.append({
                "prompt": result.prompt,
                "model_responses": result.model_responses,
                "metrics": result.metrics,
                "best_model": result.best_model,
                "best_score": result.best_score,
                "execution_time": result.execution_time,
                "timestamp": result.timestamp.isoformat()
            })
        
        # Include analysis
        data = {
            "test_results": serializable_results,
            "analysis": self.analyze_results(),
            "report": self.generate_recommendation_report()
        }
        
        filepath = os.path.join("data", filename)
        os.makedirs("data", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath

def main():
    """Main function to run the test pipeline."""
    pipeline = TestPipeline()
    
    print("🧪 ModelEval.AI Test Pipeline")
    print("Choose an option:")
    print("1. Run full test suite")
    print("2. Run single test")
    print("3. Load and analyze previous results")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        # Run full test suite
        results = pipeline.run_full_test_suite()
        
        # Generate and display report
        report = pipeline.generate_recommendation_report()
        print("\n" + report)
        
        # Save results
        filename = pipeline.save_results()
        print(f"\n💾 Results saved to: {filename}")
        
    elif choice == "2":
        # Run single test
        prompt = input("Enter your test prompt: ").strip()
        if prompt:
            result = pipeline.run_single_test(prompt)
            print(f"\n🏆 Winner: {result.best_model}")
            print(f"📊 Score: {result.best_score:.3f}")
            print(f"⏱️  Time: {result.execution_time:.2f}s")
    
    elif choice == "3":
        # Load previous results
        data_dir = "data"
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.startswith("test_results") and f.endswith(".json")]
            if files:
                print("\nAvailable result files:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                
                try:
                    file_choice = int(input("\nSelect file number: ")) - 1
                    if 0 <= file_choice < len(files):
                        filepath = os.path.join(data_dir, files[file_choice])
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                        print("\n" + data.get("report", "No report found in file"))
                    else:
                        print("Invalid file selection")
                except ValueError:
                    print("Invalid input")
            else:
                print("No test result files found")
        else:
            print("No data directory found")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main() 