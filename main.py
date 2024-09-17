import datetime
import os
from config import ALPACA_CONFIG
import multiprocessing
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from strategy import Strategy
import multiprocessing
import signal
import threading

def run_backtest(params):
    start, end, budget = params
    broker = Alpaca(ALPACA_CONFIG)
    backtest = Strategy(broker=broker)
    backtest.backtest(YahooDataBacktesting, start, end, budget=budget)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    clear_screen()

    print(" ___________________________________________________________")
    print("|----------------------- Main Menu -------------------------|")
    print("| 1. Trade Live on Alpaca Brokerage                         |#")
    print("| 2. Backtest Trading Strategy on Historical Data           |#")
    print("| 3. Edit Trading Strategy Parameters                       |#")
    print("| 4. Exit                                                   |#")
    print("|___________________________________________________________|#")
    print("   ###########################################################")
    print()

if __name__ == "__main__":
            
            
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
            
    print("""   
            
          \033[31m        © 2024 Shane W Miller
          \033[31m        All rights reserved.

          \033[31m        This software is provided for personal use only.
          \033[31m        Modification, distribution, or commercial use is
          \033[31m        prohibited without prior written permission from 
          \033[31m        the copyright holder.
          \033[0m 
              """)

    print("\033[32m\n\nPress any key to continue...\033[0m\n\n")
    input()

    user_input = None
    while user_input != '4':
        main_menu()
        user_input = input("Enter your selection then press enter: ")
        match user_input:
            case '1':
                print("Conduct live trading - This is a Point of No Return, where you will have to exit the application to stop live trading.")
                user_input = input("Are you sure you would like to continue? [Y/N]: ")
                if user_input.upper() == "Y":
                    broker = Alpaca(ALPACA_CONFIG)
                    trader = Trader()
                    strategy = Strategy(broker=broker)
                    trader.add_strategy(strategy)
                    trader.run_all()
                else:
                    continue
            case '2':
                start1 = datetime(2024, 2, 1)
                end1 = datetime(2024, 2, 7)
                start2 = datetime(2023, 2, 1)
                end2 = datetime(2023, 2, 7)

                backtest_params = [
                    (start1, end1, 350),
                    (start2, end2, 350)
                    ]

                with multiprocessing.Pool() as pool:
                    pool.map(run_backtest, backtest_params)

                print("Both backtests have completed.")
                print("\033[32m\n\nPress any key to continue...\033[0m\n\n")
                input()
                    
            case '3':
                print("Edit Trading Strategy Parameters")
                print("\033[32m\n\nPress any key to continue...\033[0m\n\n")
                input()
            case '4':
                print("Exiting...")
                print("\033[32m\n\nPress any key to continue...\033[0m\n\n")
                input()
                exit()
            case _:
                print("Invalid input. Please enter a valid selection.")
                user_input = input("Enter your selection then press enter: ")

