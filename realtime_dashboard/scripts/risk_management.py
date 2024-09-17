def calculate_position_size(account_balance, risk_percentage, stop_loss):
    risk_amount = account_balance * risk_percentage
    position_size = risk_amount / stop_loss
    return position_size
