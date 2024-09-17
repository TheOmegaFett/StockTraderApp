### App Description

The app is a command-line interface (CLI) application designed to manage stock trading strategies. It allows users to achieve three main objectives: run a stock trading strategy live, backtest one or more strategies, and configure parameters for each strategy. This tool is built to facilitate both live trading and historical backtesting while offering flexibility in strategy customization and management.

### Features and Functionalities

1. **Strategy and Backtest Initialization**:
   - Instantiates a list of strategies and backtests from a `Config.json` file or loads a default state if no configuration is found.
2. **Title Screen and Main Menu**:
   - Users can navigate through the following options:
     - **Run Live**: Initiates a live session for the selected strategy.
     - **Strategies Menu**:
       - View a list of saved strategies.
       - Add a new strategy by specifying its parameters.
       - Remove an existing strategy.
       - Save changes and exit the menu.
     - **Backtest Menu**:
       - View a log of previous backtest results.
       - Perform one or multiple backtests (repeatable).
       - Save changes and exit the menu.
     - **Exit Application**: Ends the session and exits the app.

### Entities and Classes

1. **TradingApp Class**:

   - Manages the overall application workflow.
   - **Attributes**:
     - `Backtest list`: Stores instances of the `Backtest` class.
     - `Strategies dictionary`: Stores different strategies with customizable parameters.
     - `Previous Balance value`: Keeps track of the user's balance before the live trading session.
     - `Live Session Profit/Loss value`: Tracks profit or loss during the live session.

2. **Backtest Class**:

   - Represents the execution of a historical backtest for a specific strategy.
   - **Attributes**:
     - `Strategy value`: The strategy used for the backtest.
     - `Results URL value`: A URL for detailed backtest results, possibly hosted.
     - `Start Date value`: The start date for the backtest period.
     - `End Date value`: The end date for the backtest period.
     - `Starting Balance value`: The balance at the beginning of the backtest.
     - `Final Balance value`: The balance after the backtest is complete.

3. **Strategy Class**:

   - Represents a stock trading strategy with adjustable parameters.
   - **Attributes**:
     - `Time Interval Value`: Time interval for executing trades (e.g., 1-minute, 15-minute).
     - `RSI value`: Relative Strength Index value for buy/sell signals.
     - `SMA value`: Short Moving Average value for trend analysis.
     - `LMA value`: Long Moving Average value for trend analysis.
     - `Stop Loss value`: The threshold at which a position will be automatically sold to prevent further loss.
     - `Take Profit value`: The target price at which profits will be realized by selling a position.

4. **Config JSON File**:
   - Stores default or user-defined settings for strategies and backtests.
   - Acts as a source for initializing the `Backtest` and `Strategy` lists when the app starts.
