portfolio = {
    'BTC': 0.4,  # 40% in BTC
    'ETH': 0.3,  # 30% in ETH
    'USDT': 0.3  # 30% in USDT
}

def rebalance_portfolio(current_allocation, target_allocation):
    for asset, target in target_allocation.items():
        current = current_allocation.get(asset, 0)
        if current != target:
            print(f"Rebalance {asset}: Current allocation is {current}, target is {target}.")
            # Add logic for rebalancing trades

if __name__ == "__main__":
    current_allocation = {'BTC': 0.35, 'ETH': 0.25, 'USDT': 0.4}
    rebalance_portfolio(current_allocation, portfolio)
