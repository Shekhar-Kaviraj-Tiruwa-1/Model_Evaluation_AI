#!/usr/bin/env python3
"""
ModelEval.AI Test Runner
========================

Comprehensive testing pipeline for the ModelEval.AI platform.
This script runs automated tests, evaluates model performance,
and generates actionable recommendations for users.

Usage:
    python tests/run_tests.py [--quick] [--export-report] [--recommendation-only]
"""

import sys
import os
import argparse
import json
from datetime import datetime
from typing import Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tests.test_pipeline import TestPipeline
from tests.recommendation_engine import RecommendationEngine

class TestRunner:
    """Main test runner that orchestrates the testing pipeline."""
    
    def __init__(self):
        self.test_pipeline = TestPipeline()
        self.recommendation_engine = RecommendationEngine()
        self.results = {}
    
    def run_quick_test(self) -> Dict:
        """Run a quick test with a subset of prompts."""
        print("🚀 Running Quick Test Suite")
        print("=" * 40)
        
        quick_prompts = [
            "Explain electric vehicle adoption challenges",
            "How does AI impact healthcare?", 
            "What are climate change solutions?",
            "Analyze digital transformation strategies",
            "Explain quantum computing basics"
        ]
        
        results = []
        for prompt in quick_prompts:
            result = self.test_pipeline.run_single_test(prompt)
            results.append(result)
        
        return self._process_results(results)
    
    def run_full_test(self) -> Dict:
        """Run the complete test suite."""
        print("🚀 Running Full Test Suite")
        print("=" * 40)
        
        results = self.test_pipeline.run_full_test_suite()
        return self._process_results(results)
    
    def _process_results(self, results: List) -> Dict:
        """Process test results and generate insights."""
        if not results:
            return {"error": "No test results to process"}
        
        # Store results in pipeline
        self.test_pipeline.test_results = results
        
        # Generate analysis
        analysis = self.test_pipeline.analyze_results()
        report = self.test_pipeline.generate_recommendation_report()
        
        # Generate recommendations for each category
        category_recommendations = {}
        for category in ["Electric Vehicles", "AI/Technology", "Climate/Environment", "Business/Economics", "General Technical"]:
            sample_prompt = self._get_sample_prompt_for_category(category)
            if sample_prompt:
                rec = self.recommendation_engine.get_model_recommendation(sample_prompt)
                category_recommendations[category] = rec
        
        return {
            "test_results": results,
            "analysis": analysis,
            "report": report,
            "category_recommendations": category_recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_sample_prompt_for_category(self, category: str) -> str:
        """Get a sample prompt for testing category recommendations."""
        samples = {
            "Electric Vehicles": "What are the benefits of electric vehicles?",
            "AI/Technology": "How does artificial intelligence work?",
            "Climate/Environment": "What are renewable energy solutions?",
            "Business/Economics": "How do businesses adapt to digital transformation?",
            "General Technical": "Explain machine learning algorithms"
        }
        return samples.get(category, "")
    
    def generate_user_recommendations(self, user_prompt: str = None) -> Dict:
        """Generate smart recommendations for a specific user prompt or general guidance."""
        if user_prompt:
            # Specific recommendation
            rec = self.recommendation_engine.get_model_recommendation(user_prompt)
            multi_rec = self.recommendation_engine.get_multi_model_recommendation(user_prompt)
            
            return {
                "prompt": user_prompt,
                "single_recommendation": rec,
                "multi_model_recommendation": multi_rec,
                "summary": self.recommendation_engine.generate_recommendation_summary(user_prompt)
            }
        else:
            # General recommendations
            general_recs = {}
            for category in ["Electric Vehicles", "AI/Technology", "Climate/Environment", "Business/Economics", "General Technical"]:
                sample_prompt = self._get_sample_prompt_for_category(category)
                if sample_prompt:
                    rec = self.recommendation_engine.get_model_recommendation(sample_prompt)
                    general_recs[category] = {
                        "best_model": rec["recommended_model"],
                        "confidence": rec["confidence"],
                        "characteristics": rec["model_characteristics"]["response_style"]
                    }
            
            return {
                "general_recommendations": general_recs,
                "usage_guide": self._generate_usage_guide()
            }
    
    def _generate_usage_guide(self) -> Dict:
        """Generate a comprehensive usage guide for users."""
        return {
            "when_to_use_each_model": {
                "GPT2": {
                    "best_for": "Complex analysis, detailed explanations, comprehensive coverage",
                    "use_when": "You need thorough, analytical responses with multiple perspectives",
                    "avoid_when": "You need quick, concise answers"
                },
                "DistilGPT2": {
                    "best_for": "Quick responses, summaries, straightforward explanations",
                    "use_when": "You need fast, efficient answers for simple questions",
                    "avoid_when": "You need deep analysis or comprehensive coverage"
                },
                "T5-Small": {
                    "best_for": "Structured responses, organized content, clear formatting",
                    "use_when": "You need well-organized, systematically structured answers",
                    "avoid_when": "You need creative or highly analytical content"
                },
                "BERT-Base": {
                    "best_for": "Context understanding, nuanced analysis, precise responses",
                    "use_when": "You need contextually aware answers with subtle distinctions",
                    "avoid_when": "You need creative generation or lengthy explanations"
                }
            },
            "optimization_tips": [
                "Use GPT2 for complex, multi-faceted questions requiring detailed analysis",
                "Choose DistilGPT2 when speed is more important than depth",
                "Select T5-Small for technical documentation or structured explanations",
                "Pick BERT-Base for questions requiring deep contextual understanding",
                "Consider running multiple models for important decisions",
                "Review historical performance data for your specific use cases"
            ],
            "prompt_engineering_tips": [
                "Be specific about the type of response you want",
                "Include context when asking technical questions",
                "Use clear, well-structured questions for better results",
                "Specify desired length or format when needed",
                "Consider the complexity of your question when selecting models"
            ]
        }
    
    def export_comprehensive_report(self, results: Dict, filename: str = None) -> str:
        """Export a comprehensive report with all findings and recommendations."""
        if filename is None:
            filename = f"modeleval_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Create comprehensive report
        comprehensive_report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "platform": "ModelEval.AI",
                "version": "1.0",
                "test_type": "Comprehensive Model Evaluation"
            },
            "executive_summary": self._generate_executive_summary(results),
            "detailed_results": results,
            "actionable_recommendations": self._generate_actionable_recommendations(results),
            "implementation_guide": self._generate_implementation_guide(),
            "appendix": {
                "model_characteristics": self.recommendation_engine.model_characteristics,
                "performance_history": self.recommendation_engine.performance_history
            }
        }
        
        # Save to file
        filepath = os.path.join("data", filename)
        os.makedirs("data", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(comprehensive_report, f, indent=2)
        
        # Also create a markdown summary
        md_filename = filename.replace('.json', '.md')
        md_filepath = os.path.join("data", md_filename)
        
        with open(md_filepath, 'w') as f:
            f.write(self._generate_markdown_report(comprehensive_report))
        
        return filepath
    
    def _generate_executive_summary(self, results: Dict) -> Dict:
        """Generate executive summary from test results."""
        if "analysis" not in results:
            return {"error": "No analysis available"}
        
        analysis = results["analysis"]
        summary = analysis.get("summary", {})
        
        return {
            "key_findings": [
                f"Evaluated {summary.get('models_tested', 0)} models across {summary.get('total_tests', 0)} test scenarios",
                f"Best overall performer: {summary.get('best_overall_model', 'Unknown')} with {summary.get('best_overall_score', 0):.3f} average score",
                "Identified optimal model recommendations for each domain category",
                "Generated actionable insights for model selection and optimization"
            ],
            "performance_highlights": analysis.get("model_performance", {}),
            "category_insights": analysis.get("category_recommendations", {}),
            "business_impact": [
                "Improved response quality through intelligent model selection",
                "Reduced response time by matching complexity to model capabilities",
                "Enhanced user experience through optimized model routing",
                "Data-driven decision making for model deployment strategies"
            ]
        }
    
    def _generate_actionable_recommendations(self, results: Dict) -> Dict:
        """Generate specific, actionable recommendations."""
        if "analysis" not in results:
            return {"error": "No analysis available"}
        
        analysis = results["analysis"]
        
        return {
            "immediate_actions": [
                f"Set {analysis['summary'].get('best_overall_model', 'GPT2')} as the default model",
                "Implement domain-based model routing for specialized queries",
                "Add user preference settings for speed vs. detail trade-offs",
                "Create model performance monitoring dashboard"
            ],
            "optimization_strategies": [
                "Use A/B testing to validate model selection algorithms",
                "Implement caching for frequently asked questions",
                "Add user feedback loops to improve recommendation accuracy",
                "Develop domain-specific fine-tuning strategies"
            ],
            "monitoring_metrics": [
                "Response quality scores by model and category",
                "User satisfaction ratings for model recommendations",
                "Response time and throughput metrics",
                "Cost-effectiveness analysis per model"
            ],
            "future_enhancements": [
                "Integrate real-time model performance tracking",
                "Develop ensemble methods for complex queries",
                "Add support for domain-specific model fine-tuning",
                "Implement advanced prompt engineering assistance"
            ]
        }
    
    def _generate_implementation_guide(self) -> Dict:
        """Generate implementation guide for the recommendations."""
        return {
            "phase_1_immediate": {
                "timeline": "1-2 weeks",
                "actions": [
                    "Deploy smart model recommendation system",
                    "Update UI to show recommended models",
                    "Add performance metrics to responses",
                    "Implement basic user preferences"
                ]
            },
            "phase_2_optimization": {
                "timeline": "1-2 months", 
                "actions": [
                    "Add advanced domain detection",
                    "Implement A/B testing framework",
                    "Deploy performance monitoring",
                    "Add user feedback collection"
                ]
            },
            "phase_3_advanced": {
                "timeline": "3-6 months",
                "actions": [
                    "Develop ensemble model strategies",
                    "Implement real-time learning",
                    "Add cost optimization features",
                    "Deploy advanced analytics dashboard"
                ]
            }
        }
    
    def _generate_markdown_report(self, report: Dict) -> str:
        """Generate markdown version of the report."""
        md_content = f"""# ModelEval.AI Comprehensive Test Report

**Generated:** {report['metadata']['generated_at']}  
**Platform:** {report['metadata']['platform']}  
**Version:** {report['metadata']['version']}  

## Executive Summary

### Key Findings
"""
        
        for finding in report['executive_summary']['key_findings']:
            md_content += f"- {finding}\n"
        
        md_content += f"""
### Performance Highlights

**Best Overall Model:** {report['detailed_results']['analysis']['summary'].get('best_overall_model', 'Unknown')}  
**Average Score:** {report['detailed_results']['analysis']['summary'].get('best_overall_score', 0):.3f}  

## Actionable Recommendations

### Immediate Actions
"""
        
        for action in report['actionable_recommendations']['immediate_actions']:
            md_content += f"1. {action}\n"
        
        md_content += """
### Implementation Timeline

#### Phase 1 (1-2 weeks)
- Deploy smart model recommendation system
- Update UI with recommended models
- Add performance metrics display

#### Phase 2 (1-2 months)  
- Advanced domain detection
- A/B testing framework
- Performance monitoring

#### Phase 3 (3-6 months)
- Ensemble strategies
- Real-time learning
- Advanced analytics

## Model Usage Guide

### When to Use Each Model

"""
        
        usage_guide = self._generate_usage_guide()
        for model, info in usage_guide['when_to_use_each_model'].items():
            md_content += f"#### {model}\n"
            md_content += f"**Best for:** {info['best_for']}\n"
            md_content += f"**Use when:** {info['use_when']}\n"
            md_content += f"**Avoid when:** {info['avoid_when']}\n\n"
        
        md_content += """
## Optimization Tips

"""
        for tip in usage_guide['optimization_tips']:
            md_content += f"- {tip}\n"
        
        return md_content

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="ModelEval.AI Test Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python tests/run_tests.py --quick
    python tests/run_tests.py --full --export-report
    python tests/run_tests.py --recommendation-only --prompt "Explain electric vehicles"
        """
    )
    
    parser.add_argument('--quick', action='store_true', help='Run quick test suite')
    parser.add_argument('--full', action='store_true', help='Run full test suite')
    parser.add_argument('--export-report', action='store_true', help='Export comprehensive report')
    parser.add_argument('--recommendation-only', action='store_true', help='Generate recommendations only')
    parser.add_argument('--prompt', type=str, help='Specific prompt for recommendation')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.recommendation_only:
        print("🎯 Generating Smart Recommendations")
        print("=" * 40)
        
        recommendations = runner.generate_user_recommendations(args.prompt)
        
        if args.prompt:
            print(f"\n📝 Prompt: {args.prompt}")
            print(recommendations['summary'])
        else:
            print("\n📊 General Model Recommendations:")
            for category, rec in recommendations['general_recommendations'].items():
                print(f"• {category}: {rec['best_model']} ({rec['confidence']:.1%} confidence)")
    
    elif args.quick:
        results = runner.run_quick_test()
        print("\n" + results.get('report', 'No report generated'))
        
        if args.export_report:
            filename = runner.export_comprehensive_report(results)
            print(f"\n💾 Report exported to: {filename}")
    
    elif args.full:
        results = runner.run_full_test()
        print("\n" + results.get('report', 'No report generated'))
        
        if args.export_report:
            filename = runner.export_comprehensive_report(results)
            print(f"\n💾 Report exported to: {filename}")
    
    else:
        # Interactive mode
        print("🧪 ModelEval.AI Test Pipeline")
        print("Choose an option:")
        print("1. Quick test (5 prompts)")
        print("2. Full test suite (15 prompts)")
        print("3. Get smart recommendations")
        print("4. Test specific prompt")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            results = runner.run_quick_test()
            print("\n" + results.get('report', 'No report generated'))
            
        elif choice == "2":
            results = runner.run_full_test()
            print("\n" + results.get('report', 'No report generated'))
            
            export = input("\nExport comprehensive report? (y/n): ").strip().lower()
            if export == 'y':
                filename = runner.export_comprehensive_report(results)
                print(f"💾 Report exported to: {filename}")
                
        elif choice == "3":
            recommendations = runner.generate_user_recommendations()
            print("\n📊 Smart Model Recommendations:")
            for category, rec in recommendations['general_recommendations'].items():
                print(f"• {category}: {rec['best_model']} ({rec['confidence']:.1%})")
                
        elif choice == "4":
            prompt = input("Enter your prompt: ").strip()
            if prompt:
                recommendations = runner.generate_user_recommendations(prompt)
                print(recommendations['summary'])
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main() 