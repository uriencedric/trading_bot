from data.fetch import *
from lib.calculations import calculate_indicators
from lib.ml import train_model
from lib.tools import backtest, evaluate_strategy


def main():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
    df = calculate_indicators(df)

    model, hidden_states = train_model(df)
    df, cumulative_returns = backtest(df, hidden_states, model)

    evaluate_strategy(df, cumulative_returns)


if __name__ == "__main__":
    main()
