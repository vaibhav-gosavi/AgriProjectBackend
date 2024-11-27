import requests
import pandas as pd
from io import StringIO
from fastapi import HTTPException

def fetch_real_time_prices(api_url):
    """
    Fetch real-time prices from the given API URL and parse CSV data.
    """
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch real-time prices"
            )
        
        # Handle CSV response
        csv_data = response.content.decode("utf-8")
        df = pd.read_csv(StringIO(csv_data))
        return df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")
