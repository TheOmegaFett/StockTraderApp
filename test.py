from lumibot.strategies import Strategy as BaseStrategy
import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.entities import Asset, TradingFee
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from config import ALPACA_CONFIG

class Strategy(BaseStrategy):
    parameters = {
        "symbol": "SPY",
        "leverage_symbol": "AAPL",
        "period_length": 17,
    }
    
    def initialize(self):
        self.sleeptime = "30S"

    def on_trading_iteration(self):
        period_length = self.parameters["period_length"]
        symbol = self.parameters["symbol"]
        leverage_symbol = self.parameters["leverage_symbol"]

        asset = Asset(symbol=symbol, asset_type="stock")
        leverage_asset = Asset(symbol=leverage_symbol, asset_type="stock")

        historical_prices = self.get_historical_prices(
            asset,
            period_length + 1,
            "day",
            quote=self.quote_asset,
        )
        df = historical_prices.df
        ema = df["close"].ewm(span=period_length).mean().iloc[-1]
        
        cur_price = self.get_last_price(asset, quote=self.quote_asset)

        if cur_price >= ema:
            # Buy leverage asset
            # Check what positions we have
            position = self.get_position(leverage_asset)
            price = self.get_last_price(leverage_asset, quote=self.quote_asset)
            quantity = self.cash // price

            if position is None or position.quantity < quantity:
                self.sell_all()
                # Buy
                if quantity > 0:
                    order = self.create_order(
                        leverage_asset,
                        quantity,
                        "buy",
                    )
                    self.submit_order(order)
        else:
            # Check what positions we have
            position = self.get_position(asset)
            price = self.get_last_price(asset, quote=self.quote_asset)
            quantity = self.cash // price

            if position is None or position.quantity < quantity:
                self.sell_all()
                # Buy
                if quantity > 0:
                    order = self.create_order(
                        asset,
                        quantity,
                        "buy",
                    )
                    self.submit_order(order)
                    
if __name__ == "__main__":
    is_live = True

    if is_live:
        trader = Trader()
        broker = Alpaca(ALPACA_CONFIG)
        strategy = Strategy(
            broker=broker,
        )

        trader.add_strategy(strategy)
        strategy_executors = trader.run_all()
    else:
        # Backtest this strategy
        backtesting_start = datetime.datetime(2011, 1, 1)
        backtesting_end = datetime.datetime(2022, 11, 10)

        # 0.01% trading/slippage fee
        trading_fee = TradingFee(percent_fee=0.0001)

        min_period_length = 17
        max_period_length = 17
        period_length = min_period_length

        while period_length <= max_period_length:
            Strategy.backtest(
                YahooDataBacktesting,
                backtesting_start,
                backtesting_end,
                benchmark_asset="SPY",
                buy_trading_fees=[trading_fee],
                sell_trading_fees=[trading_fee],
                parameters={
                    "symbol": "SPY",
                    "leverage_symbol": "UPRO",
                    "period_length": period_length,
                },
            )
            period_length += 1
