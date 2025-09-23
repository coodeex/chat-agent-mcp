import requests

def get_cat_fact():
    """
    Retrieves a random cat fact from the Cat Facts API.
    """
    api_url = "https://catfact.ninja/fact"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return {"fact": data.get("fact")}
    else:
        return {"error": "Failed to retrieve data from API"}