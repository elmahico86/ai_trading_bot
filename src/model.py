# model.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Dropout, LayerNormalization, MultiHeadAttention
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

class TradingModel:
    def __init__(self, model_path='models/trading_model.keras', scaler_path='models/scaler.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = self.build_model()
        self.configure_gpu()

    def configure_gpu(self):
        # Configura TensorFlow per utilizzare l'85% della GPU
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                    tf.config.experimental.set_virtual_device_configuration(
                        gpu,
                        [tf.config.experimental.VirtualDeviceConfiguration(
                            memory_limit=(tf.config.experimental.get_device_details(gpu)['device_memory_size'] * 0.85)
                        )]
                    )
            except RuntimeError as e:
                print(e)

    def build_model(self):
        # Costruzione del modello Transformer
        input_layer = Input(shape=(None, input_dim))
        x = MultiHeadAttention(num_heads=4, key_dim=64)(input_layer, input_layer)
        x = LayerNormalization(epsilon=1e-6)(x)
        x = Dropout(0.1)(x)
        x = Dense(64, activation='relu')(x)
        output_layer = Dense(1, activation='linear')(x)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model

    def train(self, X_train, y_train, X_val, y_val):
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=5, verbose=1),
            ModelCheckpoint(self.model_path, save_best_only=True, monitor='val_loss', mode='min')
        ]
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=100,
            batch_size=64,
            callbacks=callbacks
        )
        return history

    def predict(self, data):
        # Previsione
        predictions = self.model.predict(data)
        return predictions
