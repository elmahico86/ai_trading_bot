import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
import os

class TradingModel:
    def __init__(self, model_path='models/trading_model.h5'):
        self.model_path = model_path
        self.model = None  # Il modello verrà costruito dopo la feature selection
        self.configure_gpu()

    def configure_gpu(self):
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)

    def build_model(self, input_dim):
        # Costruzione del modello LSTM con input_dim basato sul numero di feature selezionate
        input_layer = Input(shape=(1, input_dim))
        x = LSTM(64, return_sequences=True)(input_layer)
        x = Dropout(0.2)(x)
        x = LSTM(32)(x)
        x = Dropout(0.2)(x)
        output_layer = Dense(1, activation='tanh')(x)
        self.model = Model(inputs=input_layer, outputs=output_layer)
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return self.model

    def train(self, X_train, y_train, X_val, y_val):
        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5),
            tf.keras.callbacks.ModelCheckpoint(self.model_path, save_best_only=True, monitor='val_loss')
        ]
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=64,
            callbacks=callbacks
        )
        return history

    def predict(self, data):
        predictions = self.model.predict(data)
        return predictions
