from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
import pandas as pd
import os

router = APIRouter()

DATA_FILE = "data/agriculture_data.csv"
EXPORT_DIR = "exports"

# Load the data
def load_data():
    return pd.read_csv(DATA_FILE)

@router.get("/filter-data")
def filter_data(
    state: str = Query(None, description="Filter by state"),
    export: bool = Query(False, description="Export filtered data to CSV"),
):
    """
    Filter data based on state and optionally export as CSV.
    """
    df = load_data()

    # Normalize strings for filtering
    df["State"] = df["State"].str.strip().str.lower()

    # Parse Arrival_Date for future extensibility
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Arrival_Date"])  # Drop rows with invalid dates

    # Debug dataset after preprocessing
    print(df.head())
    print(f"Initial dataset size: {len(df)} rows")

    # Filter by state
    if state:
        state = state.strip().lower()
        df = df[df["State"] == state]
        print(f"Filtered by state ({state}): {len(df)} rows")

    # If export is True, save the filtered data to a CSV file
    if export:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        file_path = os.path.join(EXPORT_DIR, f"{state}_data.csv")
        df.to_csv(file_path, index=False)
        return FileResponse(file_path, filename=f"{state}_data.csv")

    # Return filtered data as JSON
    return df.to_dict(orient="records")
