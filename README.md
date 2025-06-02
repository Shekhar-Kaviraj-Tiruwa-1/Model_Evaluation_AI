# 🧠 ModelEval.AI

**A real-time benchmarking platform for comparing outputs from multiple Large Language Models (LLMs)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Transformers-yellow)](https://huggingface.co)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **🎯 Smart Model Recommendations • 📊 Performance Analytics • 🧪 Automated Testing**

## 🌟 Key Features

### 🤖 **Multi-Model LLM Comparison**
- **4 Pre-integrated Models**: GPT2, DistilGPT2, T5-Small, BERT-Base
- **Real-time Response Generation** with contextual fallbacks
- **Side-by-side Comparison** with detailed metrics
- **Performance Leaderboards** and analytics

### 🎯 **Smart Recommendation System** ⭐ *NEW*
- **Intelligent Model Selection** based on prompt analysis
- **Domain Classification** (Electric Vehicles, AI/Technology, Climate/Environment, Business/Economics, General Technical)
- **Complexity Analysis** with automatic model matching
- **User Preference Learning** (Speed vs Detail vs Structure)
- **Real-time Recommendations** with confidence scoring

### 🧪 **Comprehensive Test Pipeline** ⭐ *NEW*
- **Automated Testing** across 15 diverse prompts
- **Performance Benchmarking** with detailed metrics
- **Exportable Reports** (JSON + Markdown)
- **Command-line Tools** for batch testing
- **Historical Performance Tracking**

### 📊 **Advanced Analytics**
- **Quality Metrics**: Content completeness, length optimization, diversity
- **Similarity Scoring**: Prompt relevance analysis  
- **Overall Performance**: Weighted scoring system
- **Visual Dashboards**: Charts, leaderboards, insights

### 🔧 **Production Features**
- **Environment Configuration** with secure API key management
- **Database Integration** (MongoDB + local JSON fallback)
- **Error Handling** with graceful degradation
- **Responsive UI** with modern design
- **Extensible Architecture** for adding new models

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/ModelEval.AI.git
cd ModelEval.AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create .env file
echo "HUGGINGFACE_API_KEY=your_huggingface_api_key_here" > .env
echo "MONGODB_URI=mongodb://localhost:27017/modeleval" >> .env  # Optional
```

### 3. Launch Application
```bash
# Start the Streamlit app
streamlit run app.py

# Your app will be available at http://localhost:8501
```

### 4. Start Evaluating! 🎉
1. **Enable Smart Recommendations** in the sidebar
2. **Enter your prompt** (>10 characters for recommendations)
3. **View intelligent model suggestions** with reasoning
4. **Generate & compare responses** across multiple models
5. **Analyze results** with detailed metrics and insights

## 🎯 Smart Recommendations in Action

```
🎯 Prompt: "Explain electric vehicle adoption challenges"
📊 Recommendation: GPT2 (100% confidence)
📝 Reason: Best historical performance for Electric Vehicles (0.785)
⚡ Expected: ~180 words, Medium processing time

🏆 Actual Results: GPT2 won with 0.565 score! ✅
```

## 📊 Performance Results

### Latest Test Results (5 Prompts):
| Model | Avg Score | Wins | Best For |
|-------|-----------|------|----------|
| **GPT2** | 0.553 | 5/5 🏆 | Complex analysis, detailed explanations |
| **DistilGPT2** | 0.539 | 0/5 | Quick responses, efficient processing |
| **T5-Small** | 0.537 | 0/5 | Structured content, organized responses |
| **BERT-Base** | 0.541 | 0/5 | Context understanding, precise analysis |

### Domain-Specific Champions:
- **Electric Vehicles** → GPT2 (0.785 historical score)
- **AI/Technology** → GPT2 (0.820 historical score)
- **Climate/Environment** → T5-Small (0.723 historical score)
- **Business/Economics** → GPT2 (0.792 historical score)

## 🧪 Test Pipeline Usage

### Command Line Testing
```bash
# Quick test (5 prompts)
python tests/run_tests.py --quick

# Full test suite (15 prompts + comprehensive report)
python tests/run_tests.py --full --export-report

# Get smart recommendation for any prompt
python tests/run_tests.py --recommendation-only --prompt "Your question here"

# Interactive mode
python tests/run_tests.py
```

### Programmatic Usage
```python
from tests.recommendation_engine import RecommendationEngine
from tests.run_tests import TestRunner

# Get smart recommendations
engine = RecommendationEngine()
rec = engine.get_model_recommendation("Explain renewable energy solutions")
print(f"Recommended: {rec['recommended_model']} ({rec['confidence']:.1%} confidence)")

# Run automated tests
runner = TestRunner()
results = runner.run_quick_test()
print(results['report'])
```

## 🎛️ User Interface Features

### 🎯 Smart Recommendations Panel
- **Real-time Analysis** as you type
- **Category Detection** with confidence levels
- **Model Characteristics** display
- **One-click Model Selection**
- **Top 3 Comparison** option

### 📊 Results Dashboard
- **Response Comparison** with metrics
- **Performance Leaderboard** 
- **Recommendation Accuracy** tracking
- **Insights & Tips** for future use
- **Visual Analytics** with charts

### 🧪 Testing Integration
- **Sidebar Test Runner** for quick analysis
- **Progress Tracking** with real-time updates
- **Comprehensive Reports** with exportable results
- **Historical Performance** monitoring

## 🏗️ Architecture

```
ModelEval.AI/
├── app.py                          # Main Streamlit application
├── models/
│   └── llm_engine.py              # LLM inference engine
├── evaluation/
│   └── metrics.py                 # Evaluation metrics system
├── utils/
│   ├── database.py                # Database management
│   └── visualization.py           # Charts and analytics
├── tests/                         # 🆕 Test Pipeline & Recommendations
│   ├── test_pipeline.py           # Automated testing framework
│   ├── recommendation_engine.py   # Smart model selection
│   ├── run_tests.py              # Test runner with CLI
│   └── README.md                 # Testing documentation
├── data/                          # Generated reports and results
├── static/                        # Static assets
└── requirements.txt               # Python dependencies
```

## 📈 Evaluation Metrics

### Quality Assessment
- **Content Quality**: Length optimization, completeness, diversity
- **Relevance Scoring**: Semantic similarity to prompt
- **Response Analysis**: Word count, structure, complexity
- **Overall Performance**: Weighted combination (70% quality + 30% similarity)

### Recommendation Intelligence
- **Category Classification**: 5-domain prompt analysis
- **Complexity Scoring**: Technical depth assessment
- **Historical Performance**: Learning from past results
- **User Preference**: Speed/Detail/Structure optimization

## 🔧 Configuration

### Environment Variables
```bash
# Required
HUGGINGFACE_API_KEY=your_api_key_here

# Optional
MONGODB_URI=mongodb://localhost:27017/modeleval
DEBUG=true
```

### User Preferences
- **Prefer Fast Responses** → Boosts DistilGPT2 selection
- **Prefer Detailed Responses** → Boosts GPT2 selection
- **Prefer Structured Responses** → Boosts T5-Small selection

## 📊 Sample Outputs

### Smart Recommendation Example
```
🎯 Smart Model Recommendation

For your prompt about Electric Vehicles:
• Recommended Model: GPT2
• Confidence: 100.0%
• Expected Response Length: ~180 words

Why GPT2?
Best historical performance for Electric Vehicles (0.785); 
Model strengths: comprehensive analysis, detailed explanations; 
Complexity match: 0.25

Model Characteristics:
• Style: Detailed and comprehensive
• Strengths: comprehensive analysis, detailed explanations, versatile reasoning
• Processing Time: Medium

Alternative Options: DistilGPT2, T5-Small
```

### Test Pipeline Report
```
🔬 MODELEVAL.AI - TEST PIPELINE REPORT
==================================================
Generated: 2025-06-02 02:29:33

📊 EXECUTIVE SUMMARY
• Total Tests Conducted: 5
• Models Evaluated: 4
• Best Overall Model: GPT2
• Best Overall Score: 0.544

🏆 MODEL PERFORMANCE RANKING
1. GPT2: 0.544 avg score (4 wins)
2. BERT-Base: 0.532 avg score (1 wins)
3. DistilGPT2: 0.531 avg score (0 wins)
4. T5-Small: 0.530 avg score (0 wins)

💡 DOMAIN-SPECIFIC RECOMMENDATIONS
• Electric Vehicles: Use GPT2 (Score: 0.563)
• AI/Technology: Use GPT2 (Score: 0.541)
• Climate/Environment: Use BERT-Base (Score: 0.527)
• General Technical: Use GPT2 (Score: 0.527)
```

## 🚀 Advanced Features

### Custom Model Integration
```python
# Add new models to the engine
class LLMEngine:
    def __init__(self):
        self.model_paths = {
            "GPT2": "gpt2",
            "Your-Model": "your-huggingface-model-path"
        }
```

### Custom Test Cases
```python
# Add domain-specific test prompts
custom_prompts = [
    "Your industry-specific question",
    "Another test case for validation"
]
```

### Performance Monitoring
```python
# Track recommendation accuracy
engine.update_performance_history(prompt, model, score)

# Export comprehensive reports
runner.export_comprehensive_report(results, "custom_report.json")
```

## 📚 Documentation

- **[Testing Guide](TESTING_GUIDE.md)** - Complete testing and recommendation usage
- **[Test Pipeline README](tests/README.md)** - Technical documentation for the test system
- **[API Documentation](docs/API.md)** - Integration and development guide

## 🛠️ Development

### Adding New Models
1. Update `models/llm_engine.py` with new model paths
2. Add model characteristics to `tests/recommendation_engine.py`
3. Update test configurations in `tests/test_pipeline.py`

### Extending Test Cases
1. Add prompts to `test_pipeline.py`
2. Update category mappings in `recommendation_engine.py`
3. Configure evaluation metrics in `evaluation/metrics.py`

### Custom Metrics
1. Implement new metrics in `evaluation/metrics.py`
2. Update visualization in `utils/visualization.py`
3. Modify reporting in `tests/run_tests.py`

## 📞 Support & Contributing

### Issues & Questions
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Share use cases and best practices
- **Documentation**: Comprehensive guides and examples

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for providing the model infrastructure
- **Streamlit** for the amazing web framework
- **Open Source Community** for inspiration and tools

---

## 🎯 Ready to Evaluate?

```bash
git clone https://github.com/your-username/ModelEval.AI.git
cd ModelEval.AI
pip install -r requirements.txt
echo "HUGGINGFACE_API_KEY=your_key_here" > .env
streamlit run app.py
```

**Start comparing LLMs intelligently with data-driven recommendations!** 🚀

---

<p align="center">
  <strong>Built with ❤️ for the AI community</strong><br>
  <em>Making LLM evaluation accessible, intelligent, and actionable</em>
</p>
