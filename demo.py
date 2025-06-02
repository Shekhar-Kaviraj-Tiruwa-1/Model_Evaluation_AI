#!/usr/bin/env python3
"""
ModelEval.AI Demo Script
=======================

This script demonstrates the key features of ModelEval.AI platform:
1. Smart Model Recommendations
2. Test Pipeline Execution
3. Performance Analysis
4. Report Generation

Run this script to see the platform in action!
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(__file__))

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n🔹 {title}")
    print("-" * 40)

def demo_recommendations():
    """Demonstrate the smart recommendation system."""
    from tests.recommendation_engine import RecommendationEngine
    
    print_header("🎯 SMART RECOMMENDATION SYSTEM DEMO")
    
    engine = RecommendationEngine()
    
    demo_prompts = [
        "How do electric vehicles impact the environment?",
        "Explain machine learning algorithms briefly",
        "What are renewable energy solutions?",
        "Analyze business digital transformation",
        "Quantum computing concepts"
    ]
    
    for i, prompt in enumerate(demo_prompts, 1):
        print_section(f"Example {i}: {prompt}")
        
        rec = engine.get_model_recommendation(prompt)
        
        print(f"🏆 Recommended Model: {rec['recommended_model']}")
        print(f"📊 Category: {rec['category']}")
        print(f"💪 Confidence: {rec['confidence']:.1%}")
        print(f"📝 Reasoning: {rec['reason']}")
        print(f"⚡ Expected Length: ~{rec['expected_response_length']} words")
        print(f"🔄 Alternatives: {', '.join(rec['alternatives'])}")

def demo_test_pipeline():
    """Demonstrate the test pipeline execution."""
    from tests.run_tests import TestRunner
    
    print_header("🧪 TEST PIPELINE DEMO")
    
    runner = TestRunner()
    
    print_section("Running Quick Test Suite (5 prompts)")
    print("⏳ Executing automated tests across all models...")
    
    # Run quick test
    results = runner.run_quick_test()
    
    print_section("Test Results Summary")
    if 'analysis' in results:
        analysis = results['analysis']
        summary = analysis.get('summary', {})
        
        print(f"✅ Tests Completed: {summary.get('total_tests', 0)}")
        print(f"🏆 Best Model: {summary.get('best_overall_model', 'Unknown')}")
        print(f"📊 Best Score: {summary.get('best_overall_score', 0):.3f}")
        
        # Show model ranking
        if 'model_performance' in analysis:
            performance = analysis['model_performance']
            print_section("Model Performance Ranking")
            
            sorted_models = sorted(
                performance['average_scores'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for i, (model, score) in enumerate(sorted_models, 1):
                wins = performance['wins'].get(model, 0)
                print(f"{i}. {model}: {score:.3f} avg score ({wins} wins)")
        
        # Show domain recommendations
        if 'category_recommendations' in analysis:
            print_section("Domain-Specific Recommendations")
            for category, rec in analysis['category_recommendations'].items():
                print(f"• {category}: Use {rec['best_model']} (Score: {rec['score']:.3f})")

def demo_report_generation():
    """Demonstrate report generation capabilities."""
    from tests.run_tests import TestRunner
    
    print_header("📊 REPORT GENERATION DEMO")
    
    runner = TestRunner()
    
    print_section("Generating Comprehensive Report")
    
    # Create sample results for demonstration
    sample_results = {
        "analysis": {
            "summary": {
                "total_tests": 5,
                "models_tested": 4,
                "best_overall_model": "GPT2",
                "best_overall_score": 0.553
            },
            "model_performance": {
                "wins": {"GPT2": 5, "DistilGPT2": 0, "T5-Small": 0, "BERT-Base": 0},
                "average_scores": {
                    "GPT2": 0.553,
                    "DistilGPT2": 0.539,
                    "T5-Small": 0.537,
                    "BERT-Base": 0.541
                }
            }
        }
    }
    
    # Generate report
    try:
        filename = runner.export_comprehensive_report(sample_results)
        print(f"✅ Report generated: {filename}")
        print(f"📁 Location: data/{os.path.basename(filename)}")
        
        # Show report structure
        print_section("Report Contents")
        print("📋 Executive Summary")
        print("📊 Performance Analysis") 
        print("💡 Actionable Recommendations")
        print("🛠️ Implementation Guide")
        print("📈 Model Characteristics")
        print("📚 Usage Examples")
        
    except Exception as e:
        print(f"⚠️ Report generation demo: {str(e)}")

def demo_usage_examples():
    """Show practical usage examples."""
    print_header("💡 PRACTICAL USAGE EXAMPLES")
    
    print_section("1. Getting Smart Recommendations")
    print("""
from tests.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
rec = engine.get_model_recommendation("Explain renewable energy solutions")
print(f"Best model: {rec['recommended_model']}")
print(f"Confidence: {rec['confidence']:.1%}")
""")
    
    print_section("2. Running Automated Tests")
    print("""
from tests.run_tests import TestRunner

runner = TestRunner()
results = runner.run_quick_test()
print(results['report'])
""")
    
    print_section("3. Command Line Usage")
    print("""
# Quick test
python tests/run_tests.py --quick

# Get recommendation  
python tests/run_tests.py --recommendation-only --prompt "Your question"

# Full test with report
python tests/run_tests.py --full --export-report
""")
    
    print_section("4. Streamlit Integration")
    print("""
1. Enable "Smart Model Recommendations" in sidebar
2. Type your prompt (>10 characters)  
3. View real-time recommendations with reasoning
4. Click "Use Recommended Model" or "Compare Top 3"
5. Generate responses and view analytics
""")

def main():
    """Main demo function."""
    print("🧠 ModelEval.AI Platform Demo")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Demo 1: Smart Recommendations
        demo_recommendations()
        
        # Demo 2: Test Pipeline  
        demo_test_pipeline()
        
        # Demo 3: Report Generation
        demo_report_generation()
        
        # Demo 4: Usage Examples
        demo_usage_examples()
        
        print_header("🎉 DEMO COMPLETE")
        print("✅ All features demonstrated successfully!")
        print("🚀 Ready for GitHub deployment!")
        
        print_section("Next Steps")
        print("1. Review generated reports in data/ directory")
        print("2. Start the Streamlit app: streamlit run app.py")
        print("3. Test the smart recommendations in the UI")
        print("4. Run your own test cases with custom prompts")
        
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("💡 Make sure all dependencies are installed and API key is set")

if __name__ == "__main__":
    main() 