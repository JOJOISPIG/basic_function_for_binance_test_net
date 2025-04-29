#!/usr/bin/env python
import logging
import time
from binance.um_futures import UMFutures
from binance.error import ClientError
import pandas as pd
from config import load_client
from position import get_position_info

# setting logging type
logging.basicConfig(level=logging.INFO)


# load Futures Client
client = load_client()

# parameter setting
symbol = "BTCUSDT"
quantity_ratio = 0.5  
short_ma_period = 20
long_ma_period = 60
take_profit_ratio = 1.005   # TP：0.05%
stop_loss_ratio = 0.995     # SL：-0.05%



def get_balance():
    account_info = client.balance()
    for asset in account_info:
        if asset["asset"] == "USDT":
            return float(asset["balance"])
    return 0.0



def get_latest_price(symbol):
    price_info = client.ticker_price(symbol=symbol)
    return float(price_info["price"])




def get_ma_signal(symbol):
    
        kline = client.klines(symbol=symbol, interval="1m", limit=long_ma_period+1)
        df = pd.DataFrame(kline, columns=["timestamp","open","high","low","close","volume",
                                      "close_time","quote_asset_volume","number_of_trades",
                                      "taker_buy_base_asset_volume","taker_buy_quote_asset_volume","ignore"])
        df["close"] = df["close"].astype(float)
        df["short_ma"] = df["close"].rolling(window=short_ma_period).mean()
        df["long_ma"] = df["close"].rolling(window=long_ma_period).mean()

        if df["short_ma"].iloc[-2] < df["long_ma"].iloc[-2] and df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]:
            return "BUY"  # Golden Cross : long
        elif df["short_ma"].iloc[-2] > df["long_ma"].iloc[-2] and df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]:
            return "SELL"  # Death Cross : short
        else:
            return "HOLD"





def place_order(side, quantity, entry_price):
    position_side = "LONG" if side == "BUY" else "SHORT"
    close_side = "SELL" if side == "BUY" else "BUY"

    # place main order
    order = client.new_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity,
        positionSide=position_side,
    )
    logging.info(f"ORDER PLACED: {order}")

    # calcuate TP/SL
    take_profit_price = entry_price * take_profit_ratio if side == "BUY" else entry_price * stop_loss_ratio
    stop_loss_price = entry_price * stop_loss_ratio if side == "BUY" else entry_price * take_profit_ratio

    # place TP order
    client.new_order(
        symbol=symbol,
        side=close_side,
        type="TAKE_PROFIT_MARKET",
        stopPrice=round(take_profit_price, 2),
        closePosition=True,
        positionSide=position_side,
        workingType="CONTRACT_PRICE",
    )

    # place SL order
    client.new_order(
        symbol=symbol,
        side=close_side,
        type="STOP_MARKET",
        stopPrice=round(stop_loss_price, 2),
        closePosition=True,
        positionSide=position_side,
        workingType="CONTRACT_PRICE",
    )

    logging.info(f"TP: {round(take_profit_price, 2)}, SL: {round(stop_loss_price, 2)}")





def calculate_profit(symbol):
    positions = client.position_information(symbol=symbol)
    for pos in positions:
        if float(pos["positionAmt"]) != 0:
            entry_price = float(pos["entryPrice"])
            mark_price = float(pos["markPrice"])
            side = "LONG" if float(pos["positionAmt"]) > 0 else "SHORT"
            quantity = abs(float(pos["positionAmt"]))
            pnl = float(pos["unRealizedProfit"])
            logging.info(f"SIDE: {side} ENTRY_PRICE: {entry_price} MARK_PRICE: {mark_price} PNL: {pnl}")
            return pnl, mark_price
    return 0, 0





def main():
    while True:
        try:
            signal = get_ma_signal(symbol)
            logging.info(f"SIGNAL: {signal}")
            # get BTCUSDT mark price
            get_mark_price = client.mark_price("BTCUSDT")            

            if signal in ["BUY", "SELL"]:
                usdt_balance = get_balance()
                mark_price = round(float(get_mark_price["markPrice"]),2)
                quantity = round((usdt_balance * quantity_ratio) / mark_price, 3)

                # place order
                place_order(signal, quantity, mark_price)

                # waiting for order execution
                time.sleep(10)

                get_position_info(client, symbol)

                time.sleep(50)

                break  # 單次跑完退出（可以改成持續跑）
            else:
                logging.info("Waiting for signal...")
            time.sleep(10)

        except ClientError as e:
            logging.error(f"API Error: {e}")
            time.sleep(5)
        except Exception as ex:
            logging.error(f"Unexpected Error: {ex}")
            time.sleep(5)

if __name__ == "__main__":
    main()

