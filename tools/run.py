from matplotlib import pyplot as plt

from lib.backtesting import backtest_trend_configurations, backtest, test_on_historical_data, walk_forward_testing
from lib.indicators import calculate_indicators, calculate_volume_indicators, calculate_hybrid_trend, \
    analyze_trade_metrics, calculate_trend_indicators
from lib.ml import train_model
from lib.optimization import parallel_grid_search, refine_trend_with_volume, optimize_volume_parameters, \
    grid_search_tuning
from lib.trading import test_strategy_with_simulation, simulate_trades_with_trend, validate_strategy_on_symbols, \
    test_trend_aware_strategy, generate_volume_refined_signals, simulate_trades_with_volume, adaptive_training, \
    live_trading, adaptive_training_with_risk_controls
from lib.visualization import plot_cumulative_profit, plot_volume_indicators, evaluate_strategy, plot_trend, \
    plot_walk_forward_results
from providers import fetch
from providers.fetch import fetch_historical_data


def get_function(function):
    """Get a registered provider

    Args:
        function (str):

    Returns:
        function(args): our provider func with args

    """
    functions = {
        "back_test": back_test,
        "back_test_optimized": back_test_optimized,
        "back_test_optimized_with_grid_search": back_test_optimized_with_grid_search,
        "run_strategy_parallel_grid_search": run_strategy_parallel_grid_search,
        "adaptive_training_with_risk_controls": adaptive_training_with_risk_controls,
        "hybrid_trend_aware_strategy": hybrid_trend_aware_strategy,
        "simulation_historical_data": simulation_historical_data,
        "trend_aware_strategy_on_symbols": trend_aware_strategy_on_symbols,
        "volume_enhanced_strategy_on_symbol": volume_enhanced_strategy_on_symbol,
        "volume_enhanced_historical_strategy_on_symbols": volume_enhanced_historical_strategy_on_symbols,
        "walk_forward_live_trading": walk_forward_live_trading,
        "walk_forward_adaptative_training": walk_forward_adaptative_training,
    }

    return functions.get(function, None)


def back_test():
    symbol = 'BTCUSDT'
    timeframe = '1d'

    df = fetch.get_provider("crypto_dd")(timeframe, symbol)

    df = calculate_indicators(df)

    hmm_model, hidden_states = train_model(df)
    df, cumulative_returns = backtest(df, hidden_states, hmm_model)

    # Plotting results
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], cumulative_returns, label='Strategy Returns')
    plt.plot(df['timestamp'], (1 + df['returns']).cumprod(), label='Buy & Hold')
    plt.legend()
    plt.title(f'Backtest: {symbol}')
    plt.show()


def back_test_optimized():
    symbol = 'BTCUSDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    hmm_model, hidden_states = train_model(df)
    df, cumulative_returns = backtest(df, hidden_states, hmm_model)

    evaluate_strategy(df, cumulative_returns)


def back_test_optimized_with_grid_search():
    symbol = 'BTCUSDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    # Perform parameter tuning
    best_model, best_hidden_states, best_config = grid_search_tuning(df)

    # Evaluate and visualize the best model
    backtested_df, cumulative_returns = backtest(df, best_hidden_states, best_model, risk_per_trade=best_config['risk'])
    evaluate_strategy(backtested_df, cumulative_returns)


def run_strategy_parallel_grid_search():
    symbol = 'BTCUSDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    # Perform parallel parameter tuning
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Evaluate and visualize the best model
    evaluate_strategy(best_df, (1 + best_df['strategy_returns']).cumprod())


def adaptive_training_with_risk_controls():
    symbol = 'BTCUSDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    # Add volume indicators
    df = calculate_volume_indicators(df)

    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Test the strategy with trade simulation
    trades = test_strategy_with_simulation(symbol, timeframe, best_config)

    # Optionally, start live trading with adaptive training
    adaptive_training_with_risk_controls(symbol, timeframe, best_config)


def hybrid_trend_aware_strategy():
    symbol = 'BTC/USDT'
    timeframe = '1d'

    # Fetch and preprocess data
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)
    df = calculate_volume_indicators(df)

    # Add and optimize trend logic
    trend_configurations = [
        {"ma_short": 20, "ma_long": 50, "adx_threshold": 25, "bollinger_std_dev": 2},
        {"ma_short": 15, "ma_long": 60, "adx_threshold": 20, "bollinger_std_dev": 2.5},
    ]
    backtest_results = backtest_trend_configurations(df, trend_configurations)

    # Select best configuration
    best_config = max(backtest_results, key=lambda x: x['Sharpe Ratio'])

    print(f"Best Trend Configuration: {best_config['config']}")

    # Apply the best trend logic to the strategy
    df = calculate_hybrid_trend(df)
    trades, final_equity, cumulative_profit = simulate_trades_with_trend(
        df, signal_column='signal', trend_column='trend', atr_column='atr'
    )

    # Analyze and visualize results
    analyze_trade_metrics(trades)
    plot_cumulative_profit(trades)
    plot_volume_indicators(df)


def simulation_historical_data():
    """
    Analyze Simulated Trades:
    Visualize Volume Indicators:
    Run the simulation on multiple symbols or timeframes.
    :return:
    """

    symbol = 'BTC/USDT'
    timeframe = '1d'

    # Fetch and process data
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)
    df = calculate_volume_indicators(df)
    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Simulate trades
    trades = test_strategy_with_simulation(symbol, timeframe, best_config)

    # Analyze and plot trade results
    metrics = analyze_trade_metrics(trades)
    plot_cumulative_profit(trades)

    # Plot volume indicators
    plot_volume_indicators(df)

    # Validate across symbols and timeframes
    symbols = ['BTC/USDT', 'ETH/USDT']
    timeframes = ['1d', '4h']
    validate_results = validate_strategy_on_symbols(symbols, timeframes, best_config)

    # Fetch data from CoinGecko and identify trends
    coingecko_data = fetch_historical_data('bitcoin')
    coingecko_data = calculate_trend_indicators(coingecko_data)
    plot_trend(coingecko_data)


def trend_aware_strategy_on_symbols():
    symbol = 'BTC/USDT'
    timeframe = '1d'

    # Perform parameter optimization
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Test trend-aware strategy
    metrics = test_trend_aware_strategy(symbol, timeframe, best_config)

    # Validate on multiple symbols and timeframes
    symbols = ['BTC/USDT', 'ETH/USDT']
    timeframes = ['1d', '4h']
    validate_results = validate_strategy_on_symbols(symbols, timeframes, best_config)


def volume_enhanced_strategy_on_symbol():
    symbol = 'BTC/USDT'
    timeframe = '1d'

    # Fetch and preprocess data
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)
    df = calculate_volume_indicators(df)
    df = calculate_trend_indicators(df)
    df = calculate_hybrid_trend(df)
    df = refine_trend_with_volume(df)

    # Train HMM and generate signals
    hmm_model, hidden_states = train_model(df, n_states=3)
    df = generate_volume_refined_signals(df, hidden_states)

    # Simulate trades with refined signals
    trades, final_equity, cumulative_profit = simulate_trades_with_volume(
        df, signal_column='signal', volume_trend_column='volume_trend', atr_column='atr'
    )

    # Analyze results
    analyze_trade_metrics(trades)
    plot_cumulative_profit(trades)
    plot_volume_indicators(df)


def walk_forward_live_trading():
    symbol = 'BTC/USDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Perform walk-forward testing
    walk_forward_results, summary_metrics = walk_forward_testing(
        df,
        train_window_size=365,
        test_window_size=30,
        step_size=30,
        best_config=best_config,
    )

    print(f"Walk-Forward Summary Metrics: {summary_metrics}")

    # Visualize walk-forward results
    plot_walk_forward_results(walk_forward_results)

    live_trading(symbol, timeframe, best_model, best_config)
    # Start live trading


def walk_forward_adaptative_training():
    symbol = 'BTC/USDT'
    timeframe = '1d'
    df = fetch.get_provider("crypto_dd")(timeframe, symbol)
    df = calculate_indicators(df)

    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Test on historical data
    walk_forward_results, summary_metrics = test_on_historical_data(
        symbol, timeframe, train_window_size=365, test_window_size=30, step_size=30, best_config=best_config
    )

    # Visualize results and refine parameters if needed
    plot_walk_forward_results(walk_forward_results)

    # Start live trading with adaptive training
    adaptive_training(symbol, timeframe, best_config)


def volume_enhanced_historical_strategy_on_symbols():
    symbol = 'BTC/USDT'
    timeframe = '1d'

    symbols = ['bitcoin', 'ethereum', 'binancecoin', 'solana']
    results_by_symbol = {}
    df = None
    for symbol in symbols:
        df = fetch_historical_data(symbol, "usd", "max")
        df = calculate_indicators(df)
        df = calculate_volume_indicators(df)
        df = calculate_trend_indicators(df)
        df = calculate_hybrid_trend(df)
        df = refine_trend_with_volume(df)

        parameter_grid = [
            {"short_window": 14, "long_window": 28},
            {"short_window": 20, "long_window": 40},
        ]
        results = optimize_volume_parameters(df, parameter_grid)
        results_by_symbol[symbol] = results

    # Display top results for each symbol
    for symbol, results in results_by_symbol.items():
        print(f"Best Results for {symbol}:")
        print(results[0])
        plot_volume_indicators(df)
