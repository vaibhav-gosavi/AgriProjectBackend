import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from src.api.analysis import router as analysis_router
from src.api.visualization import router as visualization_router
from src.api.filter_export import router as filter_export_router
from src.api.news import router as news_router
from src.api.prediction import router as prediction_router
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://agri-project-frontend-9hftotri4-vaibhav-gosavis-projects.vercel.app","http://localhost:5173","https://agri-project-frontend-l9qapyk3u-vaibhav-gosavis-projects.vercel.app/"],  # Adjust based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
API_URL = os.getenv("AGMARKNET_API_URL")
CSV_FILE_PATH = "data/agriculture_data.csv"  # Save data here

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/fetch-data")
def fetch_and_save_data():
    """
    Fetch data from the API (CSV format) and save it to a CSV file.
    """
    try:
        # Fetch data from the API
        print(f"Fetching data from: {API_URL}")
        response = requests.get(API_URL)
        
        # Check response status
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch data from API"
            )
        
        # Read CSV content
        print(f"Response Content (first 500 chars): {response.text[:500]}")
        csv_data = response.content.decode("utf-8")  # Decode CSV content to a string

        # Load into Pandas DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))

        # Save DataFrame to a CSV file
        os.makedirs("data", exist_ok=True)  # Create directory if it doesn't exist
        df.to_csv(CSV_FILE_PATH, index=False)

        print(f"Data saved to: {CSV_FILE_PATH}")
        return {"message": "Data fetched and saved successfully", "file_path": CSV_FILE_PATH}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


app.include_router(analysis_router, prefix="/api")
app.include_router(visualization_router, prefix="/api")
app.include_router(filter_export_router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
