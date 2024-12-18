import pandas as pd

from misc.constants import CRYPTO_DD_BASE_URL
from misc.utils import fetch_csv_as_dataframe


def fetch_data(provider="Binance", symbol="BTCUSDT"):
    """
    Fetch data to the ohlcv format. Binance data is limited to 4y
    :param provider: i.e. Binance
    :param str symbol: i.e. BTCUSDT
    :return : A dataframe representing ohlcv data

    """

    url = f"{CRYPTO_DD_BASE_URL}{provider}_{symbol}_d.csv"
    new_columns = [
        "timestamp", "date", "symbol", "open", "high",
        "low", "close", "volume_usdt", "volume_btc", "trade_count"
    ]
    dataframe = fetch_csv_as_dataframe(url, new_columns)
    df = pd.DataFrame(dataframe, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume_usdt'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


