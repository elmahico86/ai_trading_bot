# model.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Dropout, LayerNormalization, MultiHeadAttention
from tensorflow.keras.optimizers import Adam
import os

class TradingModel:
    def __init__(self, model_path='models/trading_model.keras'):
        self.model_path = model_path
        self.model = self.load_or_build_model()
        self.configure_gpu()

    def configure_gpu(self):
        # Configura TensorFlow per utilizzare l'85% della GPU
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_virtual_device_configuration(
                        gpu,
                        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=int(0.85 * tf.config.experimental.get_device_details(gpu)['device_memory_size']))]
                    )
            except RuntimeError as e:
                print(e)

    def load_or_build_model(self):
        if os.path.exists(self.model_path):
            model = load_model(self.model_path)
            print("Modello caricato correttamente.")
        else:
            model = self.build_model()
            print("Modello creato ex novo.")
        return model

    def build_model(self):
        # Costruzione del modello Transformer
        input_dim = 12  # Numero di caratteristiche dopo l'elaborazione
        input_layer = Input(shape=(input_dim,))
        x = Dense(64, activation='relu')(input_layer)
        x = Dense(32, activation='relu')(x)
        output_layer = Dense(1, activation='tanh')(x)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model

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
