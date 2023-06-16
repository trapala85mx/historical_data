import requests as r
import pytz
from datetime import datetime
from binance import AsyncClient, Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance.enums import KLINE_INTERVAL_15MINUTE
from typing import List


def get_today_timestamp():
    actual= datetime.now(pytz.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    actual_timestamp = actual.timestamp() * 1_000
    return int(actual_timestamp)


def get_last_data_updateable(minute_multiple:int=15):
    now = datetime.now(pytz.utc)
    rounded_minute = (now.minute // minute_multiple) * minute_multiple
    rounded_time = now.replace(minute=rounded_minute, second=0, microsecond=0)
    timestamp = rounded_time.timestamp() * 1000  # Convert to milliseconds
    return int(timestamp)


def get_exchange_info() -> dict:
    base = "https://fapi.binance.com"
    uri = "/fapi/v1/exchangeInfo"
    url = base + uri
    
    try:
        response = r.get(url)
        if response.status_code in (200,300):
            return (response.json())
        else:
            raise ValueError(f"No se pudo extraer la información: Error {response.status_code}")
    except ValueError as ve:
        print(ve)


def get_on_board_timestamp(asset:str, exchange_info:dict):
    try:
        for symbol in exchange_info["symbols"]:
                ticker = symbol["symbol"]
                if ticker.lower() == asset:
                    on_board = symbol["onboardDate"]
                    return on_board
        raise ValueError(f"No se pudo obtener la fecha de 'on_board' para {asset.upper()}.")
    except ValueError as ve:
        print(ve)


def get_historical_data(asset:str, timeframe:str, exchange_info:dict) -> List[list]:
    symbol = asset.upper()
    intervals = {
        "15m": KLINE_INTERVAL_15MINUTE
    }
    interval = intervals[timeframe]
    start_str = get_on_board_timestamp(asset.lower(), exchange_info)
    end_str = get_last_data_updateable()
    client = Client()
    data = client.futures_historical_klines(symbol=symbol, interval=interval,
                                     start_str= start_str, end_str=str(end_str))
    return data

def update_historical_data(asset:str, timeframe:str, start:int, end:int):
    symbol = asset.upper()
    intervals = {
        "15m": KLINE_INTERVAL_15MINUTE
    }
    interval = intervals[timeframe]
    client = Client()
    data = client.futures_historical_klines(symbol=symbol, interval=interval,
                                     start_str= start, end_str=str(end))
    return data