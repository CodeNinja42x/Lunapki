import pandas as pd

def analyze_sustainability(trades):
    df = pd.DataFrame(trades)
    df['price'] = pd.to_numeric(df['price'])
    average_price = df['price'].mean()
    return average_price

if __name__ == "__main__":
    trades = [...]  # Placeholder for fetched data
    average_price = analyze_sustainability(trades)
    print(f"Average Price: {average_price}")
