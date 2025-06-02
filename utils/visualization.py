import pandas as pd
from typing import Dict, Any

def create_leaderboard(metrics: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """Create a pandas DataFrame from metrics for display."""
    if not metrics:
        return pd.DataFrame()
        
    # Convert metrics to DataFrame
    df = pd.DataFrame.from_dict(metrics, orient='index')
    
    # Round values for better display
    for col in df.columns:
        if col != 'response_length':
            df[col] = df[col].round(3)
    
    # Sort by overall score
    if 'overall_score' in df.columns:
        df = df.sort_values('overall_score', ascending=False)
    
    return df

def plot_metrics_comparison(metrics: Dict[str, Dict[str, float]]) -> Dict:
    """Create a simple dictionary for metrics comparison (placeholder for plotly)."""
    if not metrics:
        return {}
    return {"chart_type": "radar", "data": metrics}

def plot_response_lengths(metrics: Dict[str, Dict[str, float]]) -> Dict:
    """Create a simple dictionary for response lengths (placeholder for plotly)."""
    if not metrics:
        return {}
    
    models = list(metrics.keys())
    lengths = [metrics[model].get('response_length', 0) for model in models]
    
    return {
        "chart_type": "bar",
        "labels": models,
        "values": lengths,
        "title": "Response Length Comparison"
    } 