from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# Direct API link
API_URL = "https://newsdata.io/api/1/news?apikey=pub_602448946c9883dbee4f1d4e1888450cb5c94&q=Agriculture&country=in&language=en,hi&category=food,health"

@router.get("/news")
def fetch_agriculture_news():
    """
    Fetch agricultural news using the provided API link.
    """
    try:
        # Make the API request
        response = requests.get(API_URL)

        # Handle non-200 status codes
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Failed to fetch news."
            )

        # Parse the response
        data = response.json()

        # Extract relevant fields
        articles = [
            {
                "title": article.get("title"),
                "link": article.get("link"),
                "pubDate": article.get("pubDate"),
                "description": article.get("description"),
            }
            for article in data.get("results", [])
        ]

        return {"articles": articles}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
