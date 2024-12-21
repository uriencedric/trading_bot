from data.fetch import *
from lib.backtesting import *
from lib.indicators import *
from lib.optimization import *
from lib.signals import *
from lib.trading import *
from lib.visualization import plot_volume_indicators, plot_trend, evaluate_strategy


def run_with_adaptative_training():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
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

    # Visualize results and refine parameters if needed
    plot_walk_forward_results(walk_forward_results)

    # Start live trading with adaptive training
    adaptive_training(symbol, timeframe, best_config)


def run_volume_indicator_visualization():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
    df = calculate_indicators(df)

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


def run_strategy_on_symbols():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
    df = calculate_indicators(df)

    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Test trend-aware strategy
    metrics = test_trend_aware_strategy(symbol, timeframe, best_config)

    print(metrics)

    # Validate on multiple symbols and timeframes
    symbols = ['BTC/USDT', 'ETH/USDT']
    timeframes = ['1d', '4h']
    validate_results = validate_strategy_on_symbols(symbols, timeframes, best_config)

    print(validate_results)


def run_simulation_with_trends_historical():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
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


def run_with_risk_controls():
    symbol = 'BTC/USDT'
    timeframe = '3m'
    provider = get_provider("binance")
    df = provider(timeframe, symbol)
    df = calculate_indicators(df)
    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

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

    # Add volume indicators
    df = calculate_volume_indicators(df)

    # Perform parameter optimization
    best_model, best_hidden_states, best_metrics, best_df, best_config = parallel_grid_search(df)

    # Test the strategy with trade simulation
    trades = test_strategy_with_simulation(symbol, timeframe, best_config)

    # Optionally, start live trading with adaptive training
    adaptive_training_with_risk_controls(symbol, timeframe, best_config)


def run_eval_strategy():
    symbol = 'BTC/USDT'
    timeframe = '1d'
    df = fetch.get_provider("binance")(timeframe, symbol)
    df = calculate_indicators(df)

    hmm_model, hidden_states = train_model(df)
    df, cumulative_returns = backtest(df, hidden_states, hmm_model)

    evaluate_strategy(df, cumulative_returns)


def run_volume():
    symbol = 'BTC/USDT'
    timeframe = '1d'

    # Fetch and preprocess data
    df = fetch.get_provider("binance")(timeframe, symbol)
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


def main_volume_multiple_symbol():
    symbols = ['bitcoin', 'ethereum', 'binancecoin', 'solana']
    results_by_symbol = {}

    for symbol in symbols:
        df = fetch_historical_data(symbol, "1d", "2020-01-01", "2023-12-01")
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
