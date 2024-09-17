import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

def calculate_metrics(returns):
    # Calculate Sharpe Ratio
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    
    # Calculate Sortino Ratio (assuming a minimal acceptable return of 0 for simplicity)
    downside_returns = returns.copy()
    downside_returns[downside_returns > 0] = 0
    sortino_ratio = np.sqrt(252) * (returns.mean() / downside_returns.std())
    
    # Calculate Total Return
    total_return = (1 + returns).prod() - 1
    
    # Calculate Annualized Return
    annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
    
    # Calculate Max Drawdown
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    
    # Skewness and Kurtosis
    skewness = skew(returns)
    kurt = kurtosis(returns)
    
    # Create a dictionary with all metrics
    metrics = {
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Max Drawdown': max_drawdown,
        'Skewness': skewness,
        'Kurtosis': kurt
    }
    
    return metrics

if __name__ == "__main__":
    df = pd.read_csv('backtest_results.csv')
    # Assuming 'Strategy_Return' is the column with your strategy's returns
    strategy_returns = df['Strategy_Return'].dropna()
    
    metrics = calculate_metrics(strategy_returns)
    
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")
