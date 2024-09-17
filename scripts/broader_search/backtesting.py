import backtrader as bt
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='backtest_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Custom strategy with RSI, MACD, Bollinger Bands, and risk management
class MyStrategy(bt.Strategy):
    params = (('rsi_threshold', 35),)

    def __init__(self):
        # Indicators
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        self.macd = bt.indicators.MACD(self.data.close)
        self.bollinger = bt.indicators.BollingerBands(self.data.close)
        
        # Use CrossDown for RSI and compare MACD values in next()
        self.buy_signal = bt.indicators.CrossDown(self.rsi, self.params.rsi_threshold)

    def next(self):
        # Log the RSI and MACD values for every step
        logging.info(f"RSI: {self.rsi[0]}, MACD: {self.macd.macd[0]}, MACD Signal: {self.macd.signal[0]}")
        
        # Check if RSI is below the threshold and MACD is positive
        if self.buy_signal[0] and (self.macd.macd[0] > self.macd.signal[0]):
            self.buy()
            logging.info(f"Buy order placed at {self.data.close[0]}")
            
            # Setting Stop-Loss at 5% below the entry price and Take-Profit at 5% above
            stop_loss = self.data.close[0] * 0.95
            take_profit = self.data.close[0] * 1.05
            
            # Place stop-loss and take-profit orders
            self.sell(exectype=bt.Order.Stop, price=stop_loss)
            self.sell(exectype=bt.Order.Limit, price=take_profit)
            
            logging.info(f"Stop-Loss set at {stop_loss} and Take-Profit set at {take_profit}")

# Load historical data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
        logging.info(f"Data loaded from {file_path}")
        return bt.feeds.PandasData(dataname=data)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

# Setup backtrader
def run_backtest(data):
    if data is None:
        logging.error("Backtest could not start due to data loading error.")
        return

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)

    # Set initial cash, commission, and slippage
    cerebro.broker.set_cash(10000.0)  # Starting cash
    cerebro.broker.setcommission(commission=0.001)  # 0.1% commission per trade
    cerebro.broker.set_slippage_perc(0.001)  # 0.1% slippage

    logging.info("Backtest started")
    cerebro.run()

    # Log final portfolio value
    final_value = cerebro.broker.getvalue()
    logging.info(f"Final Portfolio Value: {final_value}")

    logging.info("Backtest completed")
    cerebro.plot()

if __name__ == "__main__":
    # Replace with your CSV file path
    file_path = '/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/BTC_USDT_1h.csv'
    
    # Load data and run backtest
    data = load_data(file_path)
    run_backtest(data)
