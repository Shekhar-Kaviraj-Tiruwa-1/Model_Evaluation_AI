import streamlit as st
import os
from dotenv import load_dotenv
from models.llm_engine import LLMEngine
from evaluation.metrics import EvaluationMetrics
from utils.database import Database
from utils.visualization import create_leaderboard, plot_metrics_comparison, plot_response_lengths
from tests.recommendation_engine import RecommendationEngine

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="ModelEval.AI", page_icon="🧠", layout="wide")
    
    st.title("🧠 ModelEval.AI")
    st.markdown("> ⚖️ A real-time benchmarking platform for comparing outputs from multiple LLMs")
    
    # Initialize session state
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {}
    if 'last_prompt' not in st.session_state:
        st.session_state.last_prompt = ""
    if 'recommendation_engine' not in st.session_state:
        st.session_state.recommendation_engine = RecommendationEngine()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Check API key
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        st.sidebar.error("❌ Hugging Face API key not found!")
        st.sidebar.info("Please set HUGGINGFACE_API_KEY in your environment")
        st.stop()
    else:
        st.sidebar.success("✅ API key loaded")
    
    st.sidebar.info("📝 **Demo Mode**: Using fallback responses for consistent demonstration")
    
    # User preferences for recommendations
    st.sidebar.subheader("🎯 Smart Recommendations")
    enable_recommendations = st.sidebar.checkbox("Enable Smart Model Recommendations", value=True)
    
    user_preferences = {}
    if enable_recommendations:
        user_preferences["prefer_speed"] = st.sidebar.checkbox("Prefer Fast Responses")
        user_preferences["prefer_detail"] = st.sidebar.checkbox("Prefer Detailed Responses") 
        user_preferences["prefer_structure"] = st.sidebar.checkbox("Prefer Structured Responses")
    
    selected_models = st.sidebar.multiselect(
        "Select Models to Compare",
        ["GPT2", "DistilGPT2", "T5-Small", "BERT-Base"],
        default=["GPT2", "DistilGPT2"]
    )
    
    max_length = st.sidebar.slider("Max Response Length", 50, 300, 150)
    
    # Test pipeline access
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧪 Test Pipeline")
    if st.sidebar.button("Run Quick Test Suite"):
        st.sidebar.info("Running test pipeline in background...")
        with st.spinner("Running comprehensive tests..."):
            try:
                from tests.run_tests import TestRunner
                runner = TestRunner()
                results = runner.run_quick_test()
                st.sidebar.success("✅ Test complete! Check main area for results.")
                
                # Store results for display
                st.session_state.test_results = results
            except Exception as e:
                st.sidebar.error(f"❌ Test failed: {str(e)}")
    
    # Debug info in sidebar
    if st.session_state.responses:
        st.sidebar.success(f"✅ {len(st.session_state.responses)} responses stored")
        for model in st.session_state.responses.keys():
            st.sidebar.text(f"• {model}")
    
    # Main input section
    st.header("📝 Enter Your Prompt")
    prompt = st.text_area("Type your prompt here:", height=150, 
                         placeholder="e.g., Explain quantum computing in simple terms...")
    
    # Smart recommendations section
    if enable_recommendations and prompt and len(prompt.strip()) > 10:
        st.markdown("---")
        st.subheader("🎯 Smart Model Recommendations")
        
        try:
            recommendation = st.session_state.recommendation_engine.get_model_recommendation(
                prompt, user_preferences if user_preferences else None
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"""
                **🏆 Recommended Model**: {recommendation['recommended_model']}  
                **📊 Category**: {recommendation['category']}  
                **💪 Confidence**: {recommendation['confidence']:.1%}  
                **📏 Expected Length**: ~{recommendation['expected_response_length']} words  
                **⏱️ Processing**: {recommendation['model_characteristics']['processing_time']}  
                """)
                
                st.markdown(f"**Why {recommendation['recommended_model']}?**")
                st.write(recommendation['reason'])
            
            with col2:
                st.markdown("**Alternative Options:**")
                for alt in recommendation['alternatives']:
                    st.write(f"• {alt}")
                
                if st.button("🔄 Use Recommended Model"):
                    selected_models = [recommendation['recommended_model']]
                    st.rerun()
                
                if st.button("📊 Compare Top 3"):
                    multi_rec = st.session_state.recommendation_engine.get_multi_model_recommendation(prompt)
                    top_models = [rec['model'] for rec in multi_rec['recommendations'][:3]]
                    selected_models = top_models
                    st.rerun()
        
        except Exception as e:
            st.warning(f"⚠️ Could not generate recommendation: {str(e)}")
    
    # Generate button
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_clicked = st.button("🚀 Generate & Compare", type="primary")
    with col2:
        if st.session_state.responses:
            st.info(f"Last evaluation: {len(st.session_state.responses)} models completed")
    
    # Generation process
    if generate_clicked:
        if not prompt:
            st.warning("⚠️ Please enter a prompt first!")
            st.stop()
            
        if not selected_models:
            st.warning("⚠️ Please select at least one model!")
            st.stop()
            
        # Clear previous results
        st.session_state.responses = {}
        st.session_state.metrics = {}
        st.session_state.last_prompt = prompt
        
        st.info("🤔 Generating responses...")
        
        try:
            # Initialize LLM engine
            engine = LLMEngine()
            
            # Generate responses
            responses = {}
            progress_bar = st.progress(0)
            status_container = st.container()
            
            for i, model in enumerate(selected_models):
                with status_container:
                    st.write(f"📡 Generating response from **{model}**...")
                
                try:
                    response = engine.generate_response(model, prompt, max_length)
                    responses[model] = response
                    
                    with status_container:
                        st.success(f"✅ {model} completed: {len(response)} characters")
                    
                    progress_bar.progress((i + 1) / len(selected_models))
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    responses[model] = error_msg
                    
                    with status_container:
                        st.error(f"❌ {model} failed: {str(e)}")
            
            # Store responses
            st.session_state.responses = responses
            
            # Evaluate responses
            if responses:
                evaluator = EvaluationMetrics()
                metrics = evaluator.evaluate_responses(prompt, responses)
                st.session_state.metrics = metrics
                
                # Update recommendation engine with new performance data
                if enable_recommendations:
                    for model, model_metrics in metrics.items():
                        if not responses[model].startswith("Error:"):
                            st.session_state.recommendation_engine.update_performance_history(
                                prompt, model, model_metrics['overall_score']
                            )
                
                # Store in database
                try:
                    db = Database()
                    db.store_evaluation(prompt, responses, metrics)
                except Exception as e:
                    st.warning(f"⚠️ Could not store in database: {e}")
                
                st.success("✅ Evaluation complete! Results displayed below.")
                st.rerun()  # Refresh to show results
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Show test results if available
    if hasattr(st.session_state, 'test_results') and st.session_state.test_results:
        st.markdown("---")
        st.header("🧪 Test Pipeline Results")
        
        test_data = st.session_state.test_results
        if 'report' in test_data:
            with st.expander("📊 View Full Test Report", expanded=False):
                st.text(test_data['report'])
        
        if 'analysis' in test_data and 'summary' in test_data['analysis']:
            summary = test_data['analysis']['summary']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tests Conducted", summary.get('total_tests', 0))
            with col2:
                st.metric("Best Model", summary.get('best_overall_model', 'Unknown'))
            with col3:
                st.metric("Best Score", f"{summary.get('best_overall_score', 0):.3f}")
        
        # Clear test results
        if st.button("🗑️ Clear Test Results"):
            if hasattr(st.session_state, 'test_results'):
                del st.session_state.test_results
            st.rerun()
    
    # Always show results if they exist
    if st.session_state.responses:
        st.markdown("---")
        st.header("📋 Model Responses")
        
        # Show prompt that was used
        if st.session_state.last_prompt:
            st.info(f"**Prompt:** {st.session_state.last_prompt}")
        
        # Show recommendation accuracy if available
        if enable_recommendations and st.session_state.last_prompt:
            try:
                rec = st.session_state.recommendation_engine.get_model_recommendation(st.session_state.last_prompt)
                if rec['recommended_model'] in st.session_state.metrics:
                    actual_best = max(st.session_state.metrics.keys(), 
                                    key=lambda m: st.session_state.metrics[m]['overall_score'])
                    
                    if rec['recommended_model'] == actual_best:
                        st.success(f"🎯 **Recommendation Accuracy**: Perfect! Recommended {rec['recommended_model']} was the best performer.")
                    else:
                        st.info(f"🎯 **Recommendation**: Suggested {rec['recommended_model']}, actual best was {actual_best}")
            except:
                pass
        
        # Show each response clearly
        for i, (model, response) in enumerate(st.session_state.responses.items()):
            st.markdown(f"### 🤖 {model}")
            
            # Response box
            with st.container():
                st.markdown("**Response:**")
                if response.startswith("Error:"):
                    st.error(response)
                else:
                    st.write(response)
                
                # Metrics if available
                if model in st.session_state.metrics:
                    metrics = st.session_state.metrics[model]
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Quality", f"{metrics.get('quality_score', 0):.3f}")
                    with col2:
                        st.metric("Similarity", f"{metrics.get('similarity_score', 0):.3f}")
                    with col3:
                        st.metric("Overall", f"{metrics.get('overall_score', 0):.3f}")
                    with col4:
                        st.metric("Length", f"{metrics.get('response_length', 0)} words")
            
            if i < len(st.session_state.responses) - 1:
                st.markdown("---")
        
        # Summary section
        if st.session_state.metrics:
            st.markdown("---")
            st.header("📊 Summary & Analysis")
            
            # Leaderboard
            st.subheader("🏆 Leaderboard")
            df = create_leaderboard(st.session_state.metrics)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # Winner announcement
                winner = df.index[0]
                winner_score = df.loc[winner, 'overall_score']
                st.success(f"🏆 **Top Performer**: {winner} with score {winner_score:.3f}")
                
                # Show recommendation insights
                if enable_recommendations:
                    st.markdown("**💡 Insights for Future Use:**")
                    try:
                        category = st.session_state.recommendation_engine.categorize_prompt(st.session_state.last_prompt)
                        complexity = st.session_state.recommendation_engine.analyze_prompt_complexity(st.session_state.last_prompt)
                        
                        insights = []
                        if winner == "GPT2":
                            insights.append("GPT2 excels at comprehensive analysis - consider it for complex topics")
                        elif winner == "DistilGPT2":
                            insights.append("DistilGPT2 provides efficient responses - great for quick queries") 
                        elif winner == "T5-Small":
                            insights.append("T5-Small delivers structured content - ideal for organized responses")
                        elif winner == "BERT-Base":
                            insights.append("BERT-Base shows strong contextual understanding")
                        
                        insights.append(f"This prompt was categorized as '{category}' with {complexity['complexity_score']:.1%} complexity")
                        
                        for insight in insights:
                            st.info(f"• {insight}")
                    except:
                        pass
            
            # Response lengths chart
            st.subheader("📏 Response Lengths")
            length_data = plot_response_lengths(st.session_state.metrics)
            if length_data and 'labels' in length_data:
                chart_data = dict(zip(length_data['labels'], length_data['values']))
                st.bar_chart(chart_data)
    
    # Clear results button
    if st.session_state.responses:
        if st.button("🗑️ Clear Results"):
            st.session_state.responses = {}
            st.session_state.metrics = {}
            st.session_state.last_prompt = ""
            st.rerun()

if __name__ == "__main__":
    main()
