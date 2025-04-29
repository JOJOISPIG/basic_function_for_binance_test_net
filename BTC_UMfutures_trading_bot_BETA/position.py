import logging
from binance.error import ClientError

def get_position_info(client, symbol):
    try:
        position = client.get_position_risk(recvWindow=6000)
        
        if position:
            # only get BTCUSDT info
            position_info = next((p for p in position if p['symbol'] == 'BTCUSDT'), None)
            
            if position_info:
                position_side = position_info['positionSide']
                position_amt = float(position_info['positionAmt'])
                entry_price = float(position_info['entryPrice'])
                unrealized_profit = float(position_info['unRealizedProfit'])
                mark_price = float(position_info['markPrice'])
                logging.info(f"\nPOSITION INFO：\n- position side: {position_side}\n- position amt: {position_amt} BTC\n- entry price: {entry_price} USDT\n- mark price: {round(mark_price,2)} USDT\n- unrealized profit: {unrealized_profit} USDT")
                return position_info
            else:
                logging.info("No info of BTCUSDT 。")
                return None
        else:
            logging.error("Failed to get position info。")
            return None
    except ClientError as error:
        logging.error("API Error: status: {}, error code: {}, error message: {}".format(error.status_code, error.error_code, error.error_message))
        return None
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return None