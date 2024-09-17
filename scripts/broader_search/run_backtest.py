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

    # Plot and save as an image
    fig = cerebro.plot(style='candlestick')[0][0]
    fig.savefig('backtest_plot.png')
    plt.close(fig)
    logging.info("Plot saved as backtest_plot.png")
