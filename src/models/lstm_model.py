from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization

def build_lstm_model(input_shape):
    """
    Build the LSTM model for price prediction with improvements.
    """
    model = Sequential()
    # First LSTM layer with BatchNormalization and Dropout
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    
    # Second LSTM layer with BatchNormalization and Dropout
    model.add(LSTM(64, return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    
    # Fully connected dense layer
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    
    # Output layer
    model.add(Dense(1))  # Predict a single output: Modal_x0020_Price
    
    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    return model
