import numpy as np
import pandas as pd
from data_loader import fetch_stock_data
from model import create_lstm_model
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def prepare_data(data, feature='Close', look_back=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[[feature]])

    x_train = []
    y_train = []

    for i in range(look_back, len(scaled_data)):
        x_train.append(scaled_data[i-look_back:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    return x_train, y_train, scaler

def train_model(ticker='AAPL', epochs=10, batch_size=32):
    data = fetch_stock_data(ticker)
    x_train, y_train, scaler = prepare_data(data)

    model = create_lstm_model((x_train.shape[1], 1))
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    model.save(f"{ticker}_lstm_model.h5")
    return model, scaler

if __name__ == "__main__":
    model, scaler = train_model()
    print("Model training completed and saved.")
