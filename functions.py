import requests
SERP_API_KEY = "efb7ab91a902926c12b290ef01a5c2b66f8cc08e5270d0f60079866313bec533"


def get_address(location: str):
    url = 'https://serpapi.com/search?engine=google_maps'

    params = {
        "engine": "google_maps",
        "type": "search",
        "google_domain": "google.com",
        "q": "berekeley student gym",
        "ll": "@40.7455096,-74.0083012,14z",
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    try:
        # Send GET request
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Convert response to JSON format

            print(data)
        else:
            print(
                f"Request failed with status code {response.status_code} {response.json()}"
            )

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    # search = GoogleSearch(params)
    # results = search.get_dict()