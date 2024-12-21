# **Cryptocurrency Trading Bot using AI and Indicators-Based Refinements**

## **Overview**

This project is a Python-based cryptocurrency trading bot designed for long-term trading (weekly/monthly timeframes). The bot leverages:
- **Machine Learning Models** for market state prediction.
- **Volume Indicators** for trend refinement.
- Backtesting, walk-forward optimization, and advanced metrics analysis for robust strategy development.

The bot integrates technical and statistical indicators to enhance entry/exit signals and supports trend-based risk management strategies.

---

## **Features**

### **Core Functionalities**
1. **Market State Prediction**:
   - ML to classify market states (e.g., bullish, bearish, neutral).
   - Adaptive training for periodic model updates.

2. **Volume Indicators**:
   - **On-Balance Volume (OBV)**: Measures cumulative buying/selling pressure.
   - **Volume Moving Averages (VMA)**: Tracks short- and long-term volume trends.
   - **Volume Oscillator (VO)**: Analyzes relative changes in volume.

3. **Trend Refinement**:
   - Refines price-based trends using volume indicators.
   - Confirms or filters entry/exit signals based on volume trends.

4. **Risk Controls**:
   - Stop-loss, take-profit, and position-sizing strategies.
   - Adaptive exit signals based on volume reversals.

5. **Backtesting and Simulation**:
   - Historical testing with detailed performance metrics.
   - Simulates trades, calculates cumulative profit, win rate, Sharpe ratio, and maximum drawdown.

6. **Walk-Forward Optimization**:
   - Sliding-window approach for parameter optimization.
   - Ensures strategy robustness across unseen data.

7. **Multi-Symbol Validation**:
   - Tests strategy on multiple cryptocurrencies.
   - Analyzes performance consistency across different markets.

8. **Visualization**:
   - Plots trends, volume indicators, cumulative profits, and trade outcomes for analysis.

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- Required Python libraries:
  - `numpy`
  - `pandas`
  - `hmmlearn`
  - `matplotlib`
  - `requests`

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/crypto-trading-bot.git
   cd crypto-trading-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**


### **Run main.py by providing Preexisting functions**
Run the main.py by providing a prexisting function:
```python
   #_back_test"
   #_back_test_optimized"
   #_adaptive_training_with_risk_controls"
   #_hybrid_trend_aware_strategy"
   #_run_strategy_parallel_grid_search"
   #_simulation_historical_data"
   #_trend_aware_strategy_on_symbols"
   #_volume_enhanced_strategy_on_symbol"
   #_volume_enhanced_historical_strategy_on_symbols"
   #_walk_forward_live_trading"
   #_walk_forward_adaptative_training"

main.py --funcname=func
```

---

## **Project Structure**
```
crypto-trading-bot/
├── data/                      # data providers
├── misc/                      # Utility methods
├── lib/
   ├── indicators.py          # Indicator calculation functions
   ├── backtesting.py         # Backtesting and simulation logic
   ├── optimization.py        # Parameter optimization functions
   ├── visualization.py       # Plotting and analysis tools# Sample data (optional)
   ├── ml.py                  # ML functions
   ├── trading.py             # Live Trading functions
├── tools/                     # Tools to exec trades and refine strategies
├── main.py                    # Main script
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
```

---

## **Examples**

### **Backtesting on Bitcoin**
Run a backtest on Bitcoin using a predefined configuration:
```python
main.py --funcname=_backtest
```

### **Multi-Symbol Testing**
Test a trend aware  strategy across multiple cryptocurrencies:
```python
main.py --funcname=_trend_aware_strategy_on_symbols
```
---

## **Performance Metrics**

The bot evaluates strategy performance using:
- **Win Rate**: Percentage of profitable trades.
- **Sharpe Ratio**: Risk-adjusted returns.
- **Maximum Drawdown**: Largest equity drop from peak.
- **Profit Factor**: Ratio of gross profit to gross loss.

---

## **Planned Features**

1. **Real-Time Trading**:
   - Integrate with exchanges like Binance for live trading.
   - WebSocket support for real-time data.

2. **Sentiment Analysis**:
   - Incorporate social media sentiment to refine signals.

3. **Advanced Machine Learning**:
   - Experiment with LSTMs or transformers for predictive modeling.

4. **Portfolio Management**:
   - Optimize allocation across multiple cryptocurrencies.

---

## **Disclaimer**

This project is under development. Also, cryptocurrency trading involves significant risk. This bot does not guarantee winning trades.