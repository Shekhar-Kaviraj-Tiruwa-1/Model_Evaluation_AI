# ModelEval.AI Test Pipeline & Recommendation System

A comprehensive testing framework that evaluates LLM performance and provides intelligent model recommendations for optimal response quality.

## 🎯 Features

- **Automated Testing**: Run comprehensive test suites across multiple domains
- **Smart Recommendations**: AI-powered model selection based on prompt analysis
- **Performance Analytics**: Detailed metrics and insights
- **Real-time Integration**: Seamless integration with the main Streamlit app
- **Comprehensive Reporting**: Exportable reports in JSON and Markdown formats

## 🚀 Quick Start

### 1. Run Test Pipeline

```bash
# Quick test with 5 prompts
python tests/run_tests.py --quick

# Full test suite with 15 prompts
python tests/run_tests.py --full --export-report

# Get recommendations for a specific prompt
python tests/run_tests.py --recommendation-only --prompt "Explain electric vehicles"
```

### 2. Interactive Mode

```bash
python tests/run_tests.py
```

Then choose from the interactive menu:
1. Quick test (5 prompts)
2. Full test suite (15 prompts) 
3. Get smart recommendations
4. Test specific prompt

### 3. Integration with Main App

The test pipeline is automatically integrated into the main Streamlit app:
- Access via sidebar "🧪 Test Pipeline" section
- Enable "Smart Model Recommendations" for real-time suggestions
- View recommendation accuracy after each generation

## 📊 Test Categories

The pipeline tests across 5 key domains:

### Electric Vehicles
- EV adoption challenges
- Environmental benefits
- Industry impact analysis

### AI/Technology  
- Healthcare applications
- Financial risks/benefits
- Education transformation

### Climate/Environment
- Renewable energy solutions
- Carbon footprint reduction
- Technology's role in climate action

### Business/Economics
- Digital transformation
- Remote work impact
- Startup vs corporation dynamics

### General Technical
- Quantum computing
- Cybersecurity principles
- Blockchain applications

## 🤖 Model Recommendations

### Smart Selection Algorithm

The recommendation engine analyzes:
- **Prompt Category**: Classifies into 5 domain areas
- **Complexity Score**: Evaluates question difficulty
- **Historical Performance**: Uses past results for accuracy
- **User Preferences**: Considers speed vs detail preferences

### Model Characteristics

#### GPT2
- **Best For**: Complex analysis, detailed explanations
- **Use When**: Need thorough, analytical responses
- **Avoid When**: Need quick, concise answers
- **Processing**: Medium speed

#### DistilGPT2  
- **Best For**: Quick responses, summaries
- **Use When**: Need fast, efficient answers
- **Avoid When**: Need deep analysis
- **Processing**: Fast

#### T5-Small
- **Best For**: Structured responses, organized content
- **Use When**: Need well-organized answers
- **Avoid When**: Need creative content
- **Processing**: Medium speed

#### BERT-Base
- **Best For**: Context understanding, precise analysis
- **Use When**: Need contextually aware responses
- **Avoid When**: Need lengthy explanations
- **Processing**: Medium-slow

## 📈 Performance Metrics

### Quality Metrics
- **Quality Score**: Length, completeness, diversity analysis
- **Similarity Score**: Relevance to prompt
- **Overall Score**: Weighted combination (70% quality, 30% similarity)
- **Response Length**: Word count analysis

### Recommendation Accuracy
- **Category Detection**: Prompt classification accuracy
- **Model Selection**: Historical performance validation
- **User Satisfaction**: Preference alignment scoring

## 📋 Usage Examples

### Command Line Usage

```bash
# Run quick test and export report
python tests/run_tests.py --quick --export-report

# Get recommendations for business topics
python tests/run_tests.py --recommendation-only --prompt "How to improve business efficiency"

# Full test with comprehensive analysis
python tests/run_tests.py --full --export-report
```

### Programmatic Usage

```python
from tests.run_tests import TestRunner
from tests.recommendation_engine import RecommendationEngine

# Run tests
runner = TestRunner()
results = runner.run_quick_test()
print(results['report'])

# Get recommendations
engine = RecommendationEngine()
rec = engine.get_model_recommendation("Explain renewable energy")
print(f"Recommended: {rec['recommended_model']}")
```

### Streamlit Integration

1. Enable "Smart Model Recommendations" in sidebar
2. Type your prompt (>10 characters)
3. View real-time recommendations
4. Use "🔄 Use Recommended Model" or "📊 Compare Top 3"
5. Run "Quick Test Suite" from sidebar for comprehensive analysis

## 📊 Output Files

### JSON Report (`modeleval_report_YYYYMMDD_HHMMSS.json`)
```json
{
  "metadata": {...},
  "executive_summary": {...},
  "detailed_results": {...},
  "actionable_recommendations": {...},
  "implementation_guide": {...}
}
```

### Markdown Report (`modeleval_report_YYYYMMDD_HHMMSS.md`)
- Executive summary
- Performance rankings
- Implementation timeline
- Usage guide

## 🎛️ Configuration

### Environment Variables
```bash
HUGGINGFACE_API_KEY=your_api_key_here
MONGODB_URI=mongodb://localhost:27017/modeleval  # Optional
```

### User Preferences (in Streamlit)
- **Prefer Fast Responses**: Boosts DistilGPT2 selection
- **Prefer Detailed Responses**: Boosts GPT2 selection  
- **Prefer Structured Responses**: Boosts T5-Small selection

## 🔧 Advanced Features

### Custom Test Prompts
Add your own test prompts to `test_pipeline.py`:
```python
custom_prompts = [
    "Your custom prompt here",
    "Another test case"
]
```

### Performance History Updates
The system automatically learns from your usage:
```python
# Updates happen automatically after each generation
engine.update_performance_history(prompt, model, score)
```

### Category Detection
Customize keyword mapping in `recommendation_engine.py`:
```python
categories = {
    "Your Category": {
        "keywords": ["keyword1", "keyword2"],
        "score": 0
    }
}
```

## 📊 Interpreting Results

### Recommendation Confidence
- **>80%**: High confidence, strong historical data
- **60-80%**: Medium confidence, adequate data
- **<60%**: Low confidence, limited data

### Model Performance Scores
- **>0.8**: Excellent performance
- **0.6-0.8**: Good performance  
- **0.4-0.6**: Average performance
- **<0.4**: Below average performance

### Complexity Analysis
- **>70%**: High complexity (favor GPT2)
- **30-70%**: Medium complexity (any model)
- **<30%**: Low complexity (favor DistilGPT2)

## 🛠️ Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure you're in the project root
cd /path/to/ModelEval.AI
python tests/run_tests.py
```

**API Key Issues**
```bash
# Set environment variable
export HUGGINGFACE_API_KEY=your_key_here
```

**No Recommendations**
- Ensure prompt is >10 characters
- Check if recommendation engine is enabled
- Verify test data exists

### Debug Mode
Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Future Enhancements

- Real-time A/B testing framework
- Advanced ensemble methods
- Domain-specific fine-tuning
- Cost optimization features
- Advanced analytics dashboard
- User feedback integration

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify API key configuration

---

**Built for ModelEval.AI** - Intelligent LLM benchmarking and recommendation platform 