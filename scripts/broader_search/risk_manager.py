def calculate_stop_loss(entry_price, risk_percentage):
    return entry_price * (1 - risk_percentage / 100)

def calculate_take_profit(entry_price, reward_percentage):
    return entry_price * (1 + reward_percentage / 100)

if __name__ == "__main__":
    entry_price = 1000
    stop_loss = calculate_stop_loss(entry_price, 2)  # 2% risk
    take_profit = calculate_take_profit(entry_price, 5)  # 5% reward
    
    print(f"Stop Loss: {stop_loss}, Take Profit: {take_profit}")
