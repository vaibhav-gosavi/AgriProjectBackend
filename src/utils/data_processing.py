import pandas as pd

# Path to the data file
FILE_PATH = "data/agriculture_data.csv"

# Load the dataset
def load_data():
    # Read the CSV file
    df = pd.read_csv(FILE_PATH)
    
    # Clean column names
    df.rename(columns={
        "Min_x0020_Price": "Min_Price",
        "Max_x0020_Price": "Max_Price",
        "Modal_x0020_Price": "Modal_Price",
        "Arrival_Date": "Date"
    }, inplace=True)
    
    # Convert columns to appropriate types
    df["Date"] = pd.to_datetime(df["Date"],format="%d/%m/%Y")
    df["Min_Price"] = pd.to_numeric(df["Min_Price"], errors="coerce")
    df["Max_Price"] = pd.to_numeric(df["Max_Price"], errors="coerce")
    df["Modal_Price"] = pd.to_numeric(df["Modal_Price"], errors="coerce")
    
    # Drop rows with missing price data
    df.dropna(subset=["Modal_Price"], inplace=True)
    return df

# Analysis functions
def top_commodities_by_price(df):
    commodity_prices = df.groupby("Commodity")["Modal_Price"].mean().sort_values()
    return {
        "cheapest": commodity_prices.head(5).to_dict(),
        "expensive": commodity_prices.tail(5).to_dict()
    }

def top_states_by_price(df):
    state_prices = df.groupby("State")["Modal_Price"].mean().sort_values(ascending=False)
    return state_prices.head(5).to_dict()

def top_states_by_profit(df):
    state_profits = (df.groupby("State")["Max_Price"].mean() - df.groupby("State")["Min_Price"].mean()).sort_values(ascending=False)
    return state_profits.head(5).to_dict()

def seasonal_trends(df):
    df["Month"] = df["Date"].dt.month
    monthly_avg_price = df.groupby("Month")["Modal_Price"].mean()
    return monthly_avg_price.to_dict()

def monthly_avg_price_for_commodity(df, commodity):
    df_commodity = df[df["Commodity"] == commodity]
    monthly_avg = df_commodity.groupby(df_commodity["Date"].dt.month)["Modal_Price"].mean()
    return monthly_avg.to_dict()

def most_frequent_commodities(df):
    freq_commodities = df["Commodity"].value_counts().head(5)
    return freq_commodities.to_dict()

def state_with_most_commodities(df):
    state_commodities = df.groupby("State")["Commodity"].nunique().sort_values(ascending=False)
    return state_commodities.head(5).to_dict()

def price_trends_for_commodity(df, commodity):
    df_commodity = df[df["Commodity"] == commodity]
    trends = df_commodity[["Date", "Modal_Price"]].sort_values("Date").to_dict("records")
    return trends

def price_correlations(df):
    numeric_df = df[["Min_Price", "Max_Price", "Modal_Price"]]
    correlation_matrix = numeric_df.corr().to_dict()
    return correlation_matrix

def markets_with_highest_and_lowest_prices(df):
    market_prices = df.groupby("Market")["Modal_Price"].mean().sort_values()
    return {
        "lowest": market_prices.head(5).to_dict(),
        "highest": market_prices.tail(5).to_dict()
    }
