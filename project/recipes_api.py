import requests
import os

API_KEY = "0208676f55b94fbd8840797c7f099e83"

def get_recipes_from_api(ingredients):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'apiKey': API_KEY,
        'ingredients': ingredients,
        'number': 4,  # Number of recipes to return
        'ranking': 1,
        'ignorePantry': True
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    print(f"Error: {response.status_code}")
    return None
