# Import the requests library for making HTTP API calls
import requests

# API Key for authenticating with the AviationStack API
API_KEY = "3b45028f8868d5d7ea9ec808d9410a7b"


def fetch_flight_data():
    """
    Fetches real-time flight data from the AviationStack API.
    
    Returns:
        list: A list of flight data dictionaries, or an empty list if the request fails
              or no data is available.
    """
    # Construct the API endpoint URL with the access key (using f-string for string interpolation)
    URL = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}"
    
    # Make an HTTP GET request to the API
    response = requests.get(URL)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print("Error fetching data from the API")
        return []
    
    # Parse the JSON response from the API
    data = response.json()
    
    # Verify that the response contains the expected "data" field
    if "data" not in data:
        print("No flight data found in the response")
        return []
    
    # Return the list of flight records from the API response
    return data["data"]

    
