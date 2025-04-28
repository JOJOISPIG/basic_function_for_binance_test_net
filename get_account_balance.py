#!/usr/bin/env python

import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from dotenv import load_dotenv
import os

# 設定 logging 等級
logging.basicConfig(level=logging.INFO)

# 載入 .env 檔案中的環境變數
load_dotenv(dotenv_path="API.env")

# 從環境變數中讀取 API Key 和 Secret
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

if not api_key or not api_secret:
    logging.error("API Key and Secret must setup in .env file")
    exit(1)

# 建立 client，記得設定 base_url 指向 Testnet
client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")


# 查詢帳戶資金
try:
    response = client.account(recvWindow=6000)
    
    # 過濾出 USDT 的資產
    usdt_data = next((asset for asset in response['assets'] if asset['asset'] == 'USDT'), None)
    
    if usdt_data:
        logging.info(f"USDT details: {usdt_data}")
    else:
        logging.info("you dont have USDT")
        
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )






