import random
import time

def simulate_trading(df):
    for index, row in df.iterrows():
        print(f"Simulating trade at price {row['Close']}")
        time.sleep(1)  # Simulate a time delay

if __name__ == "__main__":
    df = pd.read_csv("data/engineered_data.csv")
    simulate_trading(df)
