import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# import matplotlib.pyplot as plt
from src.utils.data_preparation import load_and_preprocess_data, prepare_data
from src.models.lstm_model import build_lstm_model

# File paths
DATA_FILE = "data/agriculture_data.csv"
MODEL_FILE = "data/lstm_model.h5"
BEST_MODEL_FILE = "data/best_lstm_model.keras"

# Load and preprocess data
df, scaled_data, scaler = load_and_preprocess_data(DATA_FILE)

# Prepare the dataset for LSTM
look_back = 30  # Number of past days to use for prediction
X, y = prepare_data(scaled_data, look_back)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the LSTM model
model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))

# Callbacks for training
early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
checkpoint = ModelCheckpoint(filepath=BEST_MODEL_FILE, save_best_only=True, monitor="val_loss", verbose=1)

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=100,  # Increased epochs for better convergence
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping, checkpoint],
    verbose=1
)

# Save the trained model
os.makedirs("data", exist_ok=True)
model.save(MODEL_FILE)
print(f"Final model saved to {MODEL_FILE}")

# Evaluate the best saved model
model.load_weights(BEST_MODEL_FILE)
train_loss, train_mae = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)

# Calculate RMSE
train_rmse = np.sqrt(train_loss)
test_rmse = np.sqrt(test_loss)

# Predict on test data
y_pred = model.predict(X_test)
y_test_inverse = scaler.inverse_transform(np.concatenate([np.zeros((len(y_test), 2)), y_test.reshape(-1, 1)], axis=1))[:, 2]
y_pred_inverse = scaler.inverse_transform(np.concatenate([np.zeros((len(y_pred), 2)), y_pred], axis=1))[:, 2]

# Metrics
rmse = np.sqrt(mean_squared_error(y_test_inverse, y_pred_inverse))
mae = mean_absolute_error(y_test_inverse, y_pred_inverse)
print(f"Train RMSE: {train_rmse}, Test RMSE: {test_rmse}")
print(f"Test MAE: {mae}")

# Save metrics to a file
metrics_file = "data/metrics.txt"
with open(metrics_file, "w") as f:
    f.write(f"Train RMSE: {train_rmse}\n")
    f.write(f"Test RMSE: {test_rmse}\n")
    f.write(f"Test MAE: {mae}\n")
print(f"Metrics saved to {metrics_file}")