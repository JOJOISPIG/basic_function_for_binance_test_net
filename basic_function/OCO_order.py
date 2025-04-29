#!/usr/bin/env python

import logging
from binance.um_futures import UMFutures
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv(dotenv_path="API.env")


api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# 建立 client，指向 testnet
client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")

# 設定 logging
logging.basicConfig(level=logging.INFO)

symbol = "BTCUSDT"
quantity = 0.002
entry_side = "BUY"
position_side = "LONG"
entry_price = None  # 市價單，不設定價格

# 你自己設定的止盈和止損價格
take_profit_price = 95000   # 止盈目標價
stop_loss_price = 89000    # 止損價格

try:
    # 1. 建立市價開倉單
    entry_order = client.new_order(
        symbol=symbol,
        side=entry_side,
        type="MARKET",
        quantity=quantity,
        positionSide=position_side,
    )
    logging.info(f"開倉單送出: {entry_order}")

    # 2. 建立止損單
    sl_order = client.new_order(
        symbol=symbol,
        side="SELL",
        type="STOP_MARKET",
        stopPrice=stop_loss_price,
        closePosition=True,
        positionSide=position_side,
        workingType="CONTRACT_PRICE",
    )
    logging.info(f"止損單送出: {sl_order}")

    # 3. 建立止盈單
    tp_order = client.new_order(
        symbol=symbol,
        side="SELL",
        type="TAKE_PROFIT_MARKET",
        stopPrice=take_profit_price,
        closePosition=True,
        positionSide=position_side,
        workingType="CONTRACT_PRICE",
    )
    logging.info(f"止盈單送出: {tp_order}")


except Exception as e:
    logging.error(f"下單失敗: {e}")





