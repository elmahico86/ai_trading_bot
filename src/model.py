# src/model.py

import tensorflow as tf
from config import MODEL_PATH, TIME_STEPS, N_FEATURES
from tensorflow.keras import layers
from tqdm.keras import TqdmCallback

class TradingModel:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        inputs = tf.keras.Input(shape=(TIME_STEPS, N_FEATURES))
        x = layers.LayerNormalization()(inputs)
        x = layers.MultiHeadAttention(num_heads=4, key_dim=64)(x, x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(64, activation='relu')(x)
        outputs = layers.Dense(1, activation='linear')(x)

        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train(self, X_train, y_train):
        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5),
            tf.keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor='val_loss', save_best_only=True),
            TqdmCallback(verbose=1)
        ]
        self.model.fit(
            X_train, y_train,
            validation_split=0.2,
            epochs=100,
            batch_size=64,
            callbacks=callbacks
        )

    def load(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def predict(self, X):
        return self.model.predict(X)
