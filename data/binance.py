from datetime import datetime, timedelta

import ccxt
import pandas as pd


def fetch_data(symbol, timeframe, since=None):
    """
    Fetch data to the OHLCV format. Binance data is limited to 4y
    :param str symbol: ie BTC/USDT
    :param str timeframe: i.e. id, 7d, 1m, 3m
    :param datetime since:
    :return pd.DataFrame :
    """
    exchange = ccxt.binance()
    if since is None:
        since = int((datetime.now() - timedelta(days=365 * 6)).timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
