import os
from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from strategy import Strategy
from backtest import Backtest


class StockTrader():



    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def main_menu():
        StockTrader.clear_screen()

        print(" ___________________________________________________________")
        print("|----------------------- Main Menu -------------------------|")
        print("| 1. Trade Live on Alpaca Brokerage                         |#")
        print("| 2. Backtest Trading Strategy on Historical Data           |#")
        print("| 3. Edit Trading Strategy Parameters                       |#")
        print("| 4. Exit                                                   |#")
        print("|___________________________________________________________|#")
        print("   ###########################################################")
        print()

    @staticmethod
    def run():                    
            print("""
                    
        \033[33m
  /$$$$$$  /$$                      /$$             /$$$$$$$$                    /$$                  
 /$$__  $$| $$                     | $$            |__  $$__/                   | $$                  
| $$  \\__/$$$$$$   /$$$$$$  /$$$$$$| $$   /$$         | $$ /$$$$$$ /$$$$$$  /$$$$$$$ /$$$$$$  /$$$$$$ 
|  $$$$$|_  $$_/  /$$__  $$/$$_____| $$  /$$/         | $$/$$__  $|____  $$/$$__  $$/$$__  $$/$$__  $$
 \\____  $$| $$   | $$  \\ $| $$     | $$$$$$/          | $| $$  \\__//$$$$$$| $$  | $| $$$$$$$| $$  \\__/
 /$$  \\ $$| $$ /$| $$  | $| $$     | $$_  $$          | $| $$     /$$__  $| $$  | $| $$_____| $$      
|  $$$$$$/|  $$$$|  $$$$$$|  $$$$$$| $$ \\  $$         | $| $$    |  $$$$$$|  $$$$$$|  $$$$$$| $$      
 \\______/  \\___/  \\______/ \\_______|__/  \\__/         |__|__/     \\_______/\\_______/\\_______|__/                                                                                                     
        \033[0m                                                                                                      
                    
                    """)
                    
            print("\033[32m\n\nPress any key to continue...\033[0m\n\n")
            input()
        
        
            user_input = None
            while user_input != '4':
                StockTrader.main_menu()
                user_input = input("Enter your selection then press enter: ")
                match user_input:
                    case '1':
                        print("Conduct live trading - This is a Point of No Return, where you will have to exit the application to stop live trading.")
                        user_input = input("Are you sure you would like to continue? [Y/N]: ")
                        if user_input.upper() == "Y":
                            broker = Alpaca(ALPACA_CONFIG)
                            trader = Trader()
                            strategy = Strategy(broker=broker, sleeptime="30S", maximum_shares_to_trade=500, short_ma_window = 1, long_ma_window = 7, maximum_percentage_to_buy = .3)
                            trader.add_strategy(strategy)
                            trader.run_all()
                        else:
                            continue
                    case '2':
                        
                    
                        while True:
                            user_input = input("Enter the starting date after the 30th of July 2010 and at least 14 days in the past (DD/MM/YYYY): ")
                            try:
                                start_date = datetime.strptime(user_input, "%d/%m/%Y")
                                if start_date > datetime.now()-timedelta(days=14):
                                    print("Start date cannot be in the future or within the last 14 days to generate a sufficient amount of data.")
                                    continue
                                if start_date < datetime(2010, 7, 30):
                                    print("Start date cannot be before 30th of July 2010.")
                                    continue
                            except ValueError:
                                print("Invalid date format. Please use DD/MM/YYYY.")
                                continue
                            break
                        
                        
                        while True:
                            user_input = input("Enter the end date (DD/MM/YYYY): ")
                            try:
                                end_date = datetime.strptime(user_input, "%d/%m/%Y")
                                if end_date < start_date:
                                    print("End date cannot be before the start date.")
                                    continue
                                if end_date > datetime.now()-timedelta(days=5):
                                    print("End date cannot be in the future or within the last 5 days.")
                                    continue
                            except ValueError:
                                print("Invalid date format. Please use DD/MM/YYYY.")
                                continue
                            break
                    
                       
                        budget = 5000
                        broker = Alpaca(ALPACA_CONFIG)
                        
                        strategy = Strategy(broker=broker, sleeptime="30M", maximum_shares_to_trade=500, short_ma_window = 10, long_ma_window = 20, maximum_percentage_to_buy = .3)
                        
                        new_backtest = Backtest(strategy, start_date, end_date, budget)
            
                        new_backtest.run_backtest()

                        print("Backtest has completed.")
                        print("\033[32m\n\nPress Enter to continue...\033[0m\n\n")
                        input()
                            
                    case '3':
                        print("Edit Trading Strategy Parameters")
                        print("\033[32m\n\nPress Enter to continue...\033[0m\n\n")
                        input()
                    case '4':
                        print("Exiting...")
                        exit()
                    case _:
                        print("Invalid input. Please enter a valid selection.")
                        user_input = input("Type your selection then press enter: ")




if __name__ == "__main__":
    StockTrader.run()                
                
        