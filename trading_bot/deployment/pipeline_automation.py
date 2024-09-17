import subprocess

def run_pipeline():
    subprocess.run(['python', 'model_improvement/feature_engineering.py'])
    subprocess.run(['python', 'model_improvement/hyperparameter_tuning.py'])
    subprocess.run(['python', 'backtesting/backtesting.py'])
    subprocess.run(['python', 'backtesting/performance_metrics.py'])

if __name__ == "__main__":
    run_pipeline()
    print("Pipeline automation completed.")
