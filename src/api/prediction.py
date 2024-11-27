from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from src.utils.data_preparation import load_and_preprocess_data, prepare_data

router = APIRouter()

# File paths
MODEL_FILE = "data/best_lstm_model.keras"
DATA_FILE = "data/agriculture_data.csv"

@router.post("/predict")
def predict_prices(commodity: str = Query(..., description="Name of the commodity")):
    """
    Predict future prices for a specific commodity using the LSTM model.
    """
    try:
        # Load dataset
        df = pd.read_csv(DATA_FILE)

        # Filter for the specified commodity
        if commodity not in df["Commodity"].unique():
            raise HTTPException(status_code=404, detail=f"Commodity '{commodity}' not found in the dataset.")
        
        df_filtered = df[df["Commodity"] == commodity]

        # Preprocess filtered data
        df_filtered, scaled_data, scaler = load_and_preprocess_data(df_filtered)

        # Prepare data for prediction
        look_back = 30
        X, _ = prepare_data(scaled_data, look_back)

        # Load the trained model
        model = load_model(MODEL_FILE)
        model.compile(optimizer="adam", loss="mean_squared_error")

        # Predict next 30 days
        predictions = []
        input_sequence = X[-1]
        for _ in range(30):
            prediction = model.predict(np.expand_dims(input_sequence, axis=0))[0, 0]
            predictions.append(prediction)
            input_sequence = np.vstack([input_sequence[1:], [0, 0, prediction]])

        # Prepare predictions for inverse transformation
        predictions_array = np.zeros((len(predictions), 3))  # Create a (30, 3) array
        predictions_array[:, 2] = predictions  # Assign predictions to the "Modal_x0020_Price" column

        # Inverse scale predictions
        predictions = scaler.inverse_transform(predictions_array)[:, 2]  # Extract the "Modal_x0020_Price"

        return {
            "commodity": commodity,
            "predictions": predictions.tolist()
        }

    except Exception as e:
        import traceback
        print("Error Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
