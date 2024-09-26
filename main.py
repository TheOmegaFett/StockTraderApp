import os
from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from Classes.strategy import Strategy
from Classes.backtest import Backtest


class StockTrader():

    sleeptime="30M"
    maximum_shares_to_trade=500
    short_ma_window = 10
    long_ma_window = 20
    maximum_percentage_to_buy = .3


    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def any_key():
        print("\033[32m\n\nPress Enter to continue...\033[0m\n\n")
        input()

    @staticmethod
    def main_menu():
        StockTrader.clear_screen()

        print(" ___________________________________________________________")
        print("|----------------------- Main Menu -------------------------|")
        print("| \033[42m\033[30m1. Trade Live on Alpaca Brokerage                         \033[0m|#")
        print("| \033[42m\033[30m2. Backtest Trading Strategy on Historical Data           \033[0m|#")
        print("| \033[42m\033[30m3. Edit Trading Strategy Parameters                       \033[0m|#")
        print("| \033[42m\033[30m4. Exit                                                   \033[0m|#")
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
                        print("Conduct live trading - This is a \033[31mPoint of No Return\033[0m, where you will have to exit the application to stop live trading.")
                        user_input = input("Are you sure you would like to continue? [Y/N]: ")
                        if user_input.upper() == "Y":
                            broker = Alpaca(ALPACA_CONFIG)
                            trader = Trader()
                            strategy = Strategy(broker=broker, sleeptime="30S", maximum_shares_to_trade=500, short_ma_window = 1, long_ma_window = 7, maximum_percentage_to_buy = .3)
                            trader.add_strategy(strategy)
                            trader.run_all()
                        elif user_input.upper() == "N":
                            print("Returning to main menu.")
                            StockTrader.any_key()
                        else:
                            print("invalid input, try again.")
                            StockTrader.any_key()
                            continue
                    case '2': 
                        # Get start date from user
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
                            except Exception as e:
                                print(f"An error has occurred: {e}")
                                continue
                            break
                        
                        # Get end date from user
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
                    
                        while True:
                            user_input = input("Enter the budget (e.g. 5000): ")
                            try:
                                budget = int(user_input)
                                if budget < 500:
                                    print("Budget cannot be less than 500.")
                                    continue
                            except ValueError:
                                print("Invalid budget. Please enter a valid integer.")
                                continue
                            break
                       
                        
                        broker = Alpaca(ALPACA_CONFIG)
                        
                        strategy = Strategy(broker=broker, sleeptime="30M", maximum_shares_to_trade=500, short_ma_window = 10, long_ma_window = 20, maximum_percentage_to_buy = .3)
                        
                        new_backtest = Backtest(strategy, start_date, end_date, budget)
            
                        new_backtest.run_backtest()

                        print("Backtest has completed.")
                        StockTrader.any_key()                 
                    case '3':
                        while True:
                            print("Trading Strategy Parameters")
                            print()
                            print("Which parameter would you like to change?")
                            print("1. Sleeptime")
                            print("2. Maximum shares to trade")
                            print("3. Moving Average Short Window")
                            print("4. Moving Average Long Window")       
                            print("5. Maximum percentage to buy")
                            print("6. Exit")
                            print()
                            user_input = input("Type your selection then press enter: ")
                            match user_input:
                                case '1':
                                    while True:
                                        user_input = input("Enter the sleeptime (e.g. 30M): ")
                                        if user_input not in ['30S','1M', '5M', '15M', '30M', '1H', '2H', '4H', '1D']:
                                            print("Invalid sleeptime. Please enter a valid sleeptime.")
                                            print("Valid sleeptimes are: 30S, 1M, 5M, 15M, 30M, 1H, 2H, 4H, 1D")
                                            StockTrader.any_key()
                                            break
                                        else:
                                            StockTrader.sleeptime = user_input
                                            print("Sleeptime changed to: " + user_input)
                                            StockTrader.any_key()
                                            break
                                case '2':
                                    while True:
                                        user_input = input("Enter the maximum shares to trade (e.g. 500): ")
                                        try:
                                            maximum_shares_to_trade = int(user_input)
                                            if maximum_shares_to_trade < 500:
                                                print("Maximum shares to trade cannot be less than 500.")
                                                StockTrader.any_key()
                                                break
                                        except ValueError:
                                            print("Invalid maximum shares to trade. Please enter a valid integer.")
                                            StockTrader.any_key()
                                            break
                                        StockTrader.maximum_shares_to_trade = maximum_shares_to_trade
                                        print("Maximum shares to trade changed to: " + user_input)
                                        StockTrader.any_key()
                                        break
                                case '3':
                                    while True:
                                        user_input = input("Enter the moving average short window (e.g. 10): ")
                                        try:
                                            short_ma_window = int(user_input)
                                            if short_ma_window < 1:
                                                print("Moving average short window cannot be less than 1.")
                                                StockTrader.any_key()
                                                break
                                        except ValueError:
                                            print("Invalid moving average short window. Please enter a valid integer.")
                                            StockTrader.any_key()
                                            continue
                                        StockTrader.short_ma_window = short_ma_window
                                        print("Moving average short window changed to: " + user_input)
                                        break
                                case '4':
                                    while True:
                                        user_input = input("Enter the moving average long window (e.g. 20): ")
                                        try:
                                            long_ma_window = int(user_input)
                                            if long_ma_window < 1:
                                                print("Moving average long window cannot be less than 1.")
                                                StockTrader.any_key()
                                                break
                                        except ValueError:
                                            print("Invalid moving average long window. Please enter a valid integer.")
                                            StockTrader.any_key()
                                            break
                                        StockTrader.long_ma_window = long_ma_window
                                        print("Moving average long window changed to: " + user_input)
                                        StockTrader.any_key()
                                        break
                                case '5':
                                    while True:
                                        user_input = input("Enter the maximum percentage to buy (e.g. 0.3): ")
                                        try:
                                            maximum_percentage_to_buy = float(user_input)
                                            if maximum_percentage_to_buy < 0.1:
                                                print("Maximum percentage to buy cannot be less than 0.1")
                                                StockTrader.any_key()
                                                break
                                        except ValueError:
                                            print("Invalid maximum percentage to buy. Please enter a valid float.")
                                            StockTrader.any_key()
                                            break
                                        StockTrader.maximum_percentage_to_buy = maximum_percentage_to_buy
                                        print("Maximum percentage to buy changed to: " + user_input)
                                        StockTrader.any_key()
                                        break
                                case '6':
                                    print("Exiting to main menu...")
                                    StockTrader.any_key()
                                    break
                                case _:
                                    print("Invalid input. Please enter a valid selection.")
                                    StockTrader.any_key()
                                    continue
                    case '4':
                        print("Exiting...")
                        exit()
                    case _:
                        print("Invalid input. Please enter a valid selection.")
                        StockTrader.any_key()
                        continue




if __name__ == "__main__":
    StockTrader.run()                
                
        