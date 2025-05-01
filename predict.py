import numpy as np
import pandas as pd
from data_loader import fetch_stock_data
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from signal_generator import generate_signals

def prepare_data(data, feature='Close', look_back=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[[feature]])

    x_test = []
    for i in range(look_back, len(scaled_data)):
        x_test.append(scaled_data[i-look_back:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    return x_test, scaler

def predict(ticker='AAPL'):
    data = fetch_stock_data(ticker)
    model = load_model(f"{ticker}_lstm_model.h5")

    x_test, scaler = prepare_data(data)
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # Align predictions with original data index
    pred_series = pd.Series(predictions.flatten(), index=data.index[-len(predictions):])

    # Generate buy/sell signals
    signals = generate_signals(data.loc[pred_series.index], pred_series)

    return pred_series, signals

if __name__ == "__main__":
    predictions, signals = predict()
    print("Predictions and signals generated.")
    print(signals.tail())
