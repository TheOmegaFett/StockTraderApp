# Trading Strategy Backtest Project

## Overview

This project performs algorithmic trading backtests using a custom strategy implemented in Python. The core components include:

### Files Overview

- **main.py**: This is the entry point of the application. It initializes and coordinates the backtesting process, calling the necessary methods and modules from other files. Contains StockTrader class and handles user interactions and manages the overall application flow.

- **strategy.py**: This file defines the custom trading strategy. It includes the logic for entering and exiting trades based on technical indicators, such as moving averages or relative strength index (RSI).

- **backtest.py**: This file contains the logic to run backtests on various trading strategies. It uses historical market data to evaluate the performance of strategies over time.

## Installation

### Prerequisites

- **Python**: Ensure you have Python 3.8+ installed. You can download it [here](https://www.python.org/downloads/).
- **pip**: Python's package installer.

### Python Packages:

The following Python packages are required to run this project. Each package’s license is provided along with a brief description of how it is used:

1. **`numpy`**

   - **License**: [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)
   - **Description**: A fundamental package for numerical computations in Python. Used for matrix operations, calculations, and managing large arrays of market data.
   - **Ethical Consideration**: The permissive BSD license allows for commercial and non-commercial use of `numpy` with minimal restrictions.

2. **`ta-lib`**

   - **License**: [MIT License](https://opensource.org/licenses/MIT)
   - **Description**: A technical analysis library used for calculating indicators like moving averages, RSI, MACD, and more. Essential for defining the strategy logic.
   - **Ethical Consideration**: The MIT License is very permissive, allowing for easy integration into both open-source and commercial projects.

3. **`alpaca-trade-api`**

   - **License**: [MIT License](https://opensource.org/licenses/MIT)
   - **Description**: A Python client for the Alpaca trading platform. This library facilitates interaction with Alpaca's API to retrieve market data and place simulated or live trades.
   - **Ethical Consideration**: Users should ensure they comply with Alpaca's terms of service and any applicable financial regulations in their jurisdiction.

4. **`lumibot`**

   - **License**: [MIT License](https://opensource.org/licenses/MIT)
   - **Description**: A Python-based algorithmic trading framework that simplifies the process of creating and testing strategies using real-time data and backtesting capabilities.
   - **Ethical Consideration**: As a part of the MIT License, this package allows modification and distribution, making it ideal for custom trading strategies while maintaining openness and flexibility.

5. **`datetime`** (Standard Python Library)

   - **License**: Python Software Foundation License (PSFL)
   - **Description**: Handles date and time objects in Python, used to manage timestamps and time-based calculations.

6. **`os`** (Standard Python Library)
   - **License**: Python Software Foundation License (PSFL)
   - **Description**: Provides a way to interact with the operating system for tasks like reading environment variables, file paths, etc.

## License and Ethical Considerations

### License:

This project is licensed under the **MIT License**. This is a permissive license that allows the following:

- **Usage**: You are free to use, modify, and distribute this software in personal, educational, or commercial projects.
- **Conditions**: You must retain the original copyright notice and permission notice in all copies or substantial portions of the software.

**Key Points** of the MIT License:

- The project is provided "as is", without any warranty.
- You are free to make derivative works, but proper attribution must be maintained.

For more details, see the full MIT License [here](https://opensource.org/licenses/MIT).

### Ethical Considerations:

1. **Use of Open-source Libraries**: This project heavily relies on open-source libraries like `numpy` and `TA-Lib`. These libraries are widely adopted in both academia and industry, ensuring transparency, collaboration, and the ability to build upon each other's work. Ethical usage of these libraries involves adhering to their licenses, which are permissive, but it's important to ensure that their authors are credited appropriately.

2. **Data Privacy**: If you are using live trading APIs, such as Alpaca, to gather market data, you should ensure that any sensitive data, such as API keys or user information, is stored securely and in compliance with privacy laws like GDPR.

3. **Algorithmic Trading Risks**: While algorithmic trading can offer significant benefits, it’s crucial to understand and mitigate risks such as market manipulation, regulatory compliance, and fairness in financial markets. Ensure your strategy abides by local financial regulations and avoid unethical practices like spoofing or high-frequency trading that can manipulate market prices.

### Setup Instructions

1. **Clone the Repository:**
   Open your terminal and clone the repository using Git:

   ```bash
   git clone https://github.com/TheOmegaFett/StockTraderApp.git
   cd your-repo
   ```

2. **Create a Virtual Environment (Optional):**
   It's recommended to create a virtual environment to isolate project dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   Execute the main script to start the application:
   ```bash
   python main.py
   ```
