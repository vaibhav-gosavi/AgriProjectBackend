from fastapi import APIRouter, Query
from src.utils.data_processing import load_data
import pandas as pd
from typing import Optional


router = APIRouter()

@router.get("/visualization/historical")
def get_historical_data(
    commodity: str = Query(None, description="Filter by commodity"),
    state: str = Query(None, description="Filter by state"),
    market: str = Query(None, description="Filter by market"),
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format")
):
    """
    Get historical data for visualization.
    Filters:
    - Commodity
    - State
    - Market
    - Date Range
    """
    df = load_data()

    # Apply filters
    if commodity:
        df = df[df["Commodity"] == commodity]
    if state:
        df = df[df["State"] == state]
    if market:
        df = df[df["Market"] == market]
    if start_date:
        df = df[df["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Date"] <= pd.to_datetime(end_date)]

    # Group by date and calculate average modal price
    grouped_data = df.groupby("Date")["Modal_Price"].mean().reset_index()

    # Convert to JSON for frontend
    return grouped_data.to_dict(orient="records")

@router.get("/visualization/market-trends")
def get_market_trends(commodity: Optional[str] = Query(None)):
    """
    Get price trends for a commodity across all markets.
    """
    df = load_data()
    df = df[df["Commodity"] == commodity]
    grouped_data = df.groupby(["Date", "Market"])["Modal_Price"].mean().reset_index()
    return grouped_data.to_dict(orient="records")


@router.get("/visualization/state-prices")
def get_state_prices_over_time(commodity: Optional[str] = Query(None)):
    """
    Get average prices of a commodity across states over time.
    """
    df = load_data()

    # Print column names for debugging
    print("Original columns in dataset:", df.columns.tolist())

    # Rename specific columns to standardize their names
    df.rename(
        columns={
            "Arrival_Date": "Arrival Date",
            "Modal_x0020_Price": "Modal Price",
        },
        inplace=True,
    )

    # Print column names after renaming
    print("Columns after renaming:", df.columns.tolist())

    # Check for required columns
    required_columns = ["Date", "Modal_Price"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return {"error": f"Missing required columns: {', '.join(missing_columns)}"}

    # Convert 'Arrival Date' to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with invalid dates
    df = df[df["Date"].notnull()]

    # Filter by commodity if provided
    if commodity:
        df = df[df["Commodity"] == commodity]

    # Check if filtered data is empty
    if df.empty:
        return {"message": "No data available for the selected commodity."}

    # Group data by 'Arrival Date' and 'State'
    grouped_data = (
        df.groupby(["Date", "State"])["Modal_Price"]
        .mean()
        .reset_index()
    )
    grouped_data.rename(columns={"Modal_Price": "Average_Price"}, inplace=True)

    return grouped_data.to_dict(orient="records")



@router.get("/visualization/monthly-averages")
def get_monthly_averages(commodity: Optional[str] = Query(None)):
    """
    Get monthly average prices for a commodity.
    """
    df = load_data()
    df = df[df["Commodity"] == commodity]
    df["Month"] = df["Date"].dt.to_period("M")
    grouped_data = df.groupby("Month")["Modal_Price"].mean().reset_index()
    grouped_data["Month"] = grouped_data["Month"].astype(str)  # Convert to string for JSON
    return grouped_data.to_dict(orient="records")
