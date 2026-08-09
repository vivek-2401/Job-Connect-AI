import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

URL = "https://jsearch.p.rapidapi.com/search-v2"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def search_jobs(query):

    params = {
        "query": query,
        "num_pages": "1",
        "country": "in",
        "date_posted": "all"
    }

    try:

        print("\n==============================")
        print("JSearch Query:", query)
        print("Country: India")
        print("==============================")

        response = requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=30
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        jobs = data.get("data", {}).get("jobs", [])

        print("Jobs Received:", len(jobs))

        return jobs

    except requests.exceptions.Timeout:

        print("❌ JSearch API Timeout")
        return []

    except requests.exceptions.RequestException as e:

        print("❌ JSearch API Error:", e)
        return []

    except Exception as e:

        print("❌ Unexpected Error:", e)
        return []