import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# def load_and_preprocess_data(input_data):
#     """
#     Load and preprocess the data for LSTM training.
#     If input_data is a string, it is treated as a file path. Otherwise, it is treated as a DataFrame.
#     """
#     # Check if input_data is a file path or DataFrame
#     if isinstance(input_data, str):
#         df = pd.read_csv(input_data)
#     else:
#         df = input_data.copy()

#     # Ensure required columns exist
#     required_columns = ["Arrival_Date", "Min_x0020_Price", "Max_x0020_Price", "Modal_x0020_Price"]
#     for col in required_columns:
#         if col not in df.columns:
#             raise ValueError(f"Column '{col}' not found in the dataset.")

#     # Process data
#     df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], dayfirst=True)
#     df.sort_values("Arrival_Date", inplace=True)
#     df = df.ffill()

#     # Select relevant features
#     features = ["Min_x0020_Price", "Max_x0020_Price", "Modal_x0020_Price"]
#     df_features = df[features]

#     # Scale prices
#     scaler = MinMaxScaler()
#     scaled_data = scaler.fit_transform(df_features)

#     return df, scaled_data, scaler



# def prepare_data(scaled_data, look_back=30):
#     """
#     Prepare the dataset for LSTM training.
#     """
#     X, y = [], []
#     for i in range(len(scaled_data) - look_back):
#         X.append(scaled_data[i : i + look_back])
#         y.append(scaled_data[i + look_back, 2])  # Predicting Modal_x0020_Price
#     return np.array(X), np.array(y)



def load_and_preprocess_data(input_data):
    """
    Load and preprocess the data for LSTM training.
    If input_data is a string, it is treated as a file path. Otherwise, it is treated as a DataFrame.
    """
    # Check if input_data is a file path or DataFrame
    if isinstance(input_data, str):
        df = pd.read_csv(input_data)
    else:
        df = input_data.copy()

    # Ensure required columns exist
    required_columns = ["Arrival_Date", "Min_x0020_Price", "Max_x0020_Price", "Modal_x0020_Price"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the dataset.")

    # Process data
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], dayfirst=True)
    df.sort_values("Arrival_Date", inplace=True)
    df = df.ffill()

    # Select relevant features
    features = ["Min_x0020_Price", "Max_x0020_Price", "Modal_x0020_Price"]
    df_features = df[features]

    # Scale prices
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_features)

    return df, scaled_data, scaler

def prepare_data(scaled_data, look_back=30):
    """
    Prepare the dataset for LSTM training.
    """
    X, y = [], []
    for i in range(len(scaled_data) - look_back):
        X.append(scaled_data[i : i + look_back])
        y.append(scaled_data[i + look_back, 2])  # Predicting Modal_x0020_Price
    return np.array(X), np.array(y)