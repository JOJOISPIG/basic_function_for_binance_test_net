# Binance UMFutures BTC Trading Bot (base on MA Crossover)
Project Overview
This project is a Python-based automated trading bot that connects to the Binance Futures API.
It implements a simple Moving Average (MA) Crossover Strategy to detect potential buy (long) or sell (short) signals, and automatically executes trades via market orders.

The bot calculates the trade amount as 0.1% of the available USDT balance for each trade, and sets both take-profit and stop-loss orders based on the entry price.

Key Features
Supports Binance USDT-margined perpetual futures.

Fetches real-time price and historical candlestick (Kline) data.

Detects trading signals based on short-term/long-term MA crossover.

Dynamically calculates:

Entry price

Take Profit price (+0.5%)

Stop Loss price (-0.5%)

Trades using 0.1% of account balance per position.

Auto-closes positions and outputs real-time profit/loss per trade.

Secure API authentication via environment variables.

Tech Stack
Python 3.10+

Requests (HTTP API client)

Pandas (data handling and indicator calculation)

python-dotenv (environment variable management)

Project Structure

BTC_UMfutures_trading_bot_BETA/
│
├── main.py           # Main script (core trading logic)
├── config
├── position
├── API.env              # Environment variables (API keys) - DO NOT upload to GitHub
├── README.md         # Project documentation
![image](https://github.com/user-attachments/assets/79220004-001b-4f74-b6b3-0bec654cafb0)
How to Use
1. Install Dependencies

pip install binance-futures-connector

2. Setup .env File
Create a .env file in the project root directory with the following content:


BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

Tip: Only enable the "Futures Trading" permission for your API keys. Never enable withdrawal permissions for security reasons.

3. Run the Bot
Start the trading bot:


BTC_trading_bot_BETA.ipynb
The bot will continuously monitor the market based on the selected MA strategy and execute trades automatically every minute.

Strategy Details
Short-term Moving Average (20MA) vs Long-term Moving Average (60MA).

Entry Rules:

Short MA crosses above Long MA ➔ Open Long (BUY)

Short MA crosses below Long MA ➔ Open Short (SELL)

Exit Rules:

Auto-close when either Take Profit or Stop Loss target is hit.

Important Notes
Always test thoroughly on Binance Futures Testnet before trading with real funds.

Current version is basic and does not include:

Advanced error handling (recommended for production)

Multi-symbol monitoring

Dynamic risk management

For live deployment, it's recommended to host the bot on a reliable cloud server (e.g., AWS EC2, GCP) to ensure 24/7 uptime.

⚠️  Disclaimer
This project is intended for educational and personal research purposes only.
Cryptocurrency trading is highly volatile and risky. The developer is not responsible for any financial losses incurred from using this program. Please use at your own discretion.


