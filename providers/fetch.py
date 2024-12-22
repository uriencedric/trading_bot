from datetime import datetime, timedelta

import ccxt
import pandas as pd
import requests

from misc.constants import CRYPTO_DD_BASE_URL, COINGECKO_BASE_URL
from misc.utils import fetch_csv_as_dataframe


def get_provider(provider):
    """Get a registered provider

    Args:
        provider (str): binance, crypto_dd

    Returns:
        (function): our provider func with args
    """
    providers = {
        "binance": _binance,
        "crypto_dd": _crypto_dd
    }

    return providers.get(provider, None)


def _binance(timeframe="3m", symbol="BTC/USDT", since=None):
    """ Fetch data to the ohlcv format.

    Args:
        symbol (str, optional): . Defaults to "BTC/USDT".
        symbol (str, optional): . Defaults to "3m".
        since (datetime, optional): . Defaults to None.

    Returns:
        pd.DataFrame: df
    """
    exchange = ccxt.binance()
    if since is None:
        since = int(
            (datetime.now() - timedelta(days=365 * 6)).timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(
        ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def _crypto_dd(timeframe=None, symbol="BTCUSDT"):
    """
    Fetch data to the ohlcv format. (binance)

    Example :
    'timestamp', 'open', 'high', 'low', 'close', 'volume'
    2024-12-21 00:00:00,97805.44000,99540.61000,96398.39000,97291.99000,23483.54143
    2024-12-20 00:00:00,97461.86000,98233.00000,92232.54000,97805.44000,62884.13570

    Args:
        timeframe (str, optional): . Defaults to None.
        symbol (str, optional): . Defaults to "BTCUSDT".

    Returns:
       (pd.DataFrame): df
    """

    url = f"{CRYPTO_DD_BASE_URL}Binance_{symbol}_d.csv"
    new_columns = [
        "timestamp", "date", "symbol", "open", "high",
        "low", "close", "volume", "volume_btc", "trade_count"
    ]
    dataframe = fetch_csv_as_dataframe(url, new_columns)
    df = pd.DataFrame(dataframe, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.sort_values(by="timestamp")
    return df


def fetch_historical_data(symbol, vs_currency='usd', days='max'):
    """
    Fetch historical price data from CoinGecko.
    """
    url = f"{COINGECKO_BASE_URL}{symbol}/market_chart"
    params = {'vs_currency': vs_currency, 'days': days}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    else:
        print("Failed to fetch data from CoinGecko.")
        return None
