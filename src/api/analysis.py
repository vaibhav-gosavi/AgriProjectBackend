from fastapi import APIRouter
from src.utils.data_processing import (
    load_data,
    top_commodities_by_price,
    top_states_by_price,
    top_states_by_profit,
    seasonal_trends,
    monthly_avg_price_for_commodity,
    most_frequent_commodities,
    state_with_most_commodities,
    price_trends_for_commodity,
    price_correlations,
    markets_with_highest_and_lowest_prices
)

router = APIRouter()

@router.get("/analysis/commodities")
def analyze_commodities():
    df = load_data()
    return top_commodities_by_price(df)

@router.get("/analysis/states")
def analyze_states():
    df = load_data()
    return {
        "top_states_by_price": top_states_by_price(df),
        "top_states_by_profit": top_states_by_profit(df),
    }

@router.get("/analysis/seasonal")
def analyze_seasonal():
    df = load_data()
    return seasonal_trends(df)

@router.get("/analysis/commodity/{commodity}/monthly")
def analyze_monthly_avg_price(commodity: str):
    df = load_data()
    return monthly_avg_price_for_commodity(df, commodity)

@router.get("/analysis/frequent-commodities")
def analyze_frequent_commodities():
    df = load_data()
    return most_frequent_commodities(df)

@router.get("/analysis/state-commodities")
def analyze_state_with_most_commodities():
    df = load_data()
    return state_with_most_commodities(df)

@router.get("/analysis/commodity/{commodity}/trends")
def analyze_price_trends(commodity: str):
    df = load_data()
    return price_trends_for_commodity(df, commodity)

@router.get("/analysis/correlations")
def analyze_price_correlations():
    df = load_data()
    return price_correlations(df)

@router.get("/analysis/markets")
def analyze_market_prices():
    df = load_data()
    return markets_with_highest_and_lowest_prices(df)
