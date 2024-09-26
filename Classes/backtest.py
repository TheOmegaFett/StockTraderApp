from lumibot.backtesting import YahooDataBacktesting

class Backtest:
    
    def __init__(self, strategy, start_date, end_date, budget):
        
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
    
  
    def run_backtest(self):
        self.strategy.backtest(YahooDataBacktesting, self.start_date, self.end_date, budget=self.budget)
        
       