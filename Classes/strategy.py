from lumibot.strategies import Strategy as BaseStrategy
import talib
import numpy as np
from lumibot.entities import Asset


class Strategy(BaseStrategy):

    def __init__(self, broker, sleeptime, maximum_shares_to_trade=500, short_ma_window=1, long_ma_window=3, rsi_window=5, maximum_percentage_to_buy=.3, minutes_before_closing=1, minutes_before_opening=60, stats_file=None, risk_free_rate=None, benchmark_asset="SPY", backtesting_start=None, backtesting_end=None, quote_asset=Asset(symbol="USD", asset_type="forex"), starting_positions=None, filled_order_callback=None, name=None, budget=None, parameters={}, buy_trading_fees=[], sell_trading_fees=[], force_start_immediately=False, discord_webhook_url=None, account_history_db_connection_str=None, db_connection_str=None, strategy_id=None, discord_account_summary_footer=None, should_backup_variables_to_database=True, should_send_summary_to_discord=True, save_logfile=False, **kwargs,):
        
        super().__init__(broker=broker)  # Call parent constructor to handle broker

        
        # Initialize values
        # self.risk_free_rate = risk_free_rate
        self.budget = budget
        self.minutes_before_closing = minutes_before_closing
        self.minutes_before_opening = minutes_before_opening
        self.sleeptime = sleeptime
        self.maximum_shares_to_trade = maximum_shares_to_trade
        self.short_ma_window = short_ma_window
        self.long_ma_window = long_ma_window
        self.rsi_window = rsi_window
        self.maximum_percentage_to_buy = maximum_percentage_to_buy
        # This specific class will only trade the following stocks:
        self.symbols = [
                    "AAPL", # Apple
                    "TSLA", # Tesla
                    "NVDA", # Nvidia
                    "AMD",  # AMD
                    "MSFT", # Microsoft
                    "GOOG", # Google
                        ]
        
        self.buy_prices = {}
        self.highest_prices = {}
    
    
    
    # Method called by lumibot to initialize the strategy, redundant due to contructor but required by lumibot.
    def initialize(self):
       pass
    
    # Method called by lumibot to execute the strategy, this will loop through the 
    # stock symbols hard coded in the __init__ method and perform the combinded strategy on them.
    def on_trading_iteration(self):
        for symbol in self.symbols:
            if symbol is None:
                print("No symbol provided for this trading iteration.")
                continue
            self.combined_strategy(symbol)
    
    # Method to sell all shares of a stock
    def sell_all(self, symbol):
        position = self.get_position(symbol)
        if position.quantity <= 0:
            return
        order = self.create_order(symbol, position.quantity, "sell")
        self.submit_order(order)
        self.buy_prices.pop(symbol, None)

    # Method to sell a percentage of the position
    def sell_percentage(self, symbol, percentage):
        position = self.get_position(symbol)
        if position is None or position.quantity <= 0:
            return
        shares_to_sell = int(position.quantity * percentage)
        if shares_to_sell < 1:
            return
        order = self.create_order(symbol, shares_to_sell, "sell")
        self.submit_order(order)
        self.buy_prices.pop(symbol, None)

    # Method to calculate the moving average based on the window size
    def get_moving_average(self, symbol, window=1):
        bars = self.get_historical_prices(symbol, window)
        if bars is None or bars.df.empty:
            return None
        close_prices = bars.df['close'].values
        return np.mean(close_prices)

    # Method to calculate the RSI
    def get_rsi(self, symbol, period=3):
        bars = self.get_historical_prices(symbol, period)
        if bars is None:
            return None
        close_prices = bars.df['close'].values
        return talib.RSI(close_prices, timeperiod=period)[-1]

    # Method to calculate the number of shares to buy based on the current price and maximum percentage of budget
    def calculate_shares_to_buy(self, current_price, max_percentage):
    
        balance = self.get_cash()
        if balance <= 0:
            return 0
        allocation =   int(balance * max_percentage) 
        if allocation <= current_price or current_price == 0:
            return 0
        num_of_shares = int(allocation / current_price)
        return min(num_of_shares, self.maximum_shares_to_trade)
    
    # Method to execute the combined strategy of moving averages and RSI with buying and selling strategies
    def combined_strategy(self, symbol):
        
        # Ensure symbol is valid before proceeding
        if not symbol:
            print("Invalid symbol passed to combined_strategy")
            return
        
        # Get the current price of the symbol and ensure it's valid
        current_price = self.get_last_price(symbol)
        if current_price is None:
            return

        # Calculate moving averages and ensure they're valid
        short_ma = self.get_moving_average(symbol, self.short_ma_window)
        long_ma = self.get_moving_average(symbol, self.long_ma_window)
        if short_ma is None or long_ma is None:
            print(f"Could not calculate moving averages for {symbol}")
            return
        
        # Calculate RSI and ensure it's valid
        rsi = self.get_rsi(symbol, self.rsi_window)
        if rsi is None:
            print(f"Could not calculate RSI for {symbol}")
            return
        
        # Get the current position for the symbol
        position = self.get_position(symbol)
        
        # Check for sell conditions
        if position is not None and symbol in self.buy_prices:
            buy_price = self.buy_prices[symbol]
            highest_price = self.highest_prices.get(symbol, buy_price)

            if current_price > buy_price + 0.04:
                self.sell_all(symbol)
                self.buy_prices.pop(symbol, None)
            if current_price > buy_price + 0.0001:
                if short_ma < long_ma or rsi > 60:
                    self.sell_all(symbol)
                    self.buy_prices.pop(symbol, None)
                    

            trailing_stop_loss = 0.1
            stop_loss_price = highest_price * (1 - trailing_stop_loss)

            if current_price < stop_loss_price:
                self.sell_all(symbol)
                self.buy_prices.pop(symbol, None)
            self.highest_prices[symbol] = max(highest_price, current_price)
        
        # Check if we should buy
        buy_condition = (position is None) and ((short_ma > long_ma) or (rsi < 30)) and not rsi > 63 
        # buy shares if the buy condition is met
        if buy_condition:
            shares_to_trade = self.calculate_shares_to_buy(current_price, self.maximum_percentage_to_buy)
            if shares_to_trade >= 1:
                buy_order = self.create_order(symbol, shares_to_trade, "buy")
                self.submit_order(buy_order)
                self.buy_prices[symbol] = current_price
                self.highest_prices[symbol] = current_price

        
            