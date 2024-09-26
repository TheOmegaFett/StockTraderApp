from lumibot.strategies import Strategy as BaseStrategy
import talib
import numpy as np

class Strategy(BaseStrategy):

        
    def initialize(self,sleeptime="30S", maximum_shares_to_trade=500, short_ma_window = 10, long_ma_window = 20, maximum_percentage_to_buy = .3):
        self.sleeptime = sleeptime   
        self.symbols = [
                    "AAPL", # Apple
                    "TSLA", # Tesla
                    "NVDA", # Nvidia
                    "AMD",  # AMD
                    "MSFT", # Microsoft
                    "GOOG", # Google
                        ]
        self.maximum_shares_to_trade = maximum_shares_to_trade
        self.highest_prices = {}    # A dictionary to store the highest price for each symbol
        self.buy_prices = {}    # A dictionary to store the buy price for each symbol
        self.short_ma_window = short_ma_window
        self.long_ma_window = long_ma_window
        self.maximum_percentage_to_buy = maximum_percentage_to_buy
        
    def on_trading_iteration(self):
        for symbol in self.symbols:
            if symbol is None:
                print("No symbol provided for this trading iteration.")
                return
            self.combined_strategy(symbol)
            
   
          
   
    def sell_all(self, symbol):
        position = self.get_position(symbol)
        if position.quantity <= 0:
            return
        order = self.create_order(symbol, position.quantity, "sell")
        self.submit_order(order)
        self.buy_prices.pop(symbol, None)

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

    def get_moving_average(self, symbol, window=1):
        bars = self.get_historical_prices(symbol, window)
        if bars is None or bars.df.empty:
            return None
        close_prices = bars.df['close'].values
        return np.mean(close_prices)

    def get_rsi(self, symbol, period=3):
        bars = self.get_historical_prices(symbol, period)
        if bars is None:
            return None
        close_prices = bars.df['close'].values
        return talib.RSI(close_prices, timeperiod=period)[-1]

    def calculate_shares_to_buy(self, current_price, max_percentage):
    
        balance = self.get_cash()
        if balance <= 0:
            return 0
        allocation =   int(balance * max_percentage) 
        if allocation <= current_price or current_price == 0:
            return 0
        num_of_shares = int(allocation / current_price)
        return min(num_of_shares, self.maximum_shares_to_trade)
    
    def combined_strategy(self, symbol):
        
        # Ensure symbol is valid before proceeding
        if not symbol:
            print("Invalid symbol passed to combined_strategy")
            return
        
        current_price = self.get_last_price(symbol)
        if current_price is None:
            return

        short_ma = self.get_moving_average(symbol, self.short_ma_window)
        long_ma = self.get_moving_average(symbol, self.long_ma_window)
        
        if short_ma is None or long_ma is None:
            print(f"Could not calculate moving averages for {symbol}")
            return
        
        rsi = self.get_rsi(symbol, 3)

        if None in (short_ma, long_ma, rsi):
            return

        
        position = self.get_position(symbol)
        
        
        buy_condition = (position is None) and ((short_ma > long_ma) or (rsi < 30)) and not rsi >63 

        if buy_condition:
            shares_to_trade = self.calculate_shares_to_buy(current_price, self.maximum_percentage_to_buy)
            if shares_to_trade >= 1:
                buy_order = self.create_order(symbol, shares_to_trade, "buy")
                self.submit_order(buy_order)
                self.buy_prices[symbol] = current_price
                self.highest_prices[symbol] = current_price

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
                    

            trailing_stop_loss = 0.001
            stop_loss_price = highest_price * (1 - trailing_stop_loss)

            if current_price < stop_loss_price:
                self.sell_all(symbol)
                self.buy_prices.pop(symbol, None)
            self.highest_prices[symbol] = max(highest_price, current_price)
            