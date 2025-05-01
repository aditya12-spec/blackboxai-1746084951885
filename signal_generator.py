import pandas as pd
from technical_analysis import calculate_macd, calculate_rsi, calculate_moving_averages, detect_candlestick_patterns

def generate_signals(data: pd.DataFrame, predictions: pd.Series):
    """
    Generate buy/sell signals based on technical indicators and model predictions.
    """
    signals = pd.DataFrame(index=data.index)
    macd, macd_signal, _ = calculate_macd(data)
    rsi = calculate_rsi(data)
    short_ma, long_ma = calculate_moving_averages(data)

    signals['macd'] = macd
    signals['macd_signal'] = macd_signal
    signals['rsi'] = rsi
    signals['short_ma'] = short_ma
    signals['long_ma'] = long_ma
    signals['prediction'] = predictions

    signals['signal'] = 0  # Default no signal

    # MACD crossover signal
    signals.loc[(signals['macd'] > signals['macd_signal']), 'signal'] = 1  # Buy
    signals.loc[(signals['macd'] < signals['macd_signal']), 'signal'] = -1  # Sell

    # RSI overbought/oversold signal
    signals.loc[(signals['rsi'] > 70), 'signal'] = -1  # Sell
    signals.loc[(signals['rsi'] < 30), 'signal'] = 1   # Buy

    # Moving average crossover
    signals.loc[(signals['short_ma'] > signals['long_ma']), 'signal'] = 1  # Buy
    signals.loc[(signals['short_ma'] < signals['long_ma']), 'signal'] = -1  # Sell

    # Combine with model prediction trend
    signals.loc[(signals['prediction'].diff() > 0), 'signal'] = 1
    signals.loc[(signals['prediction'].diff() < 0), 'signal'] = -1

    # Detect candlestick patterns for additional signals
    candle_patterns = detect_candlestick_patterns(data)
    # For simplicity, if any pattern detected, adjust signal
    signals.loc[candle_patterns.any(axis=1), 'signal'] = 1  # Buy signal on pattern detection

    return signals
