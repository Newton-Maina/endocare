import os
import requests

def fetch_diet_plan(calories, diet_type):
    diet_api_id = os.getenv('DIET_API_ID')
    diet_api_key = os.getenv('DIET_API_KEY')

    if not diet_api_id or not diet_api_key:
        print("DIET_API_ID or DIET_API_KEY is not set or loaded incorrectly")
        return {"error": "DIET_API_ID or DIET_API_KEY is not set in environment variables"}

    url = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'type': 'public',
        'q': '',  # Empty query to get general meal plans
        'app_id': diet_api_id,
        'app_key': diet_api_key,
        'calories': f'lt{calories}',  # Less than or equal to the specified calories
        'diet': diet_type,  # Diet type like 'balanced', 'high-protein', 'low-carb'
        'fields': 'hits.recipe.label,hits.recipe.calories,hits.recipe.ingredients,hits.recipe.image',
        'random': 'true'  # Randomize the result
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        meals = []

        # Process the response to match the template requirements
        for hit in data.get('hits', []):
            recipe = hit.get('recipe', {})
            meals.append({
                'name': recipe.get('label', 'No Name'),
                'calories': recipe.get('calories', 'No Calories'),
                'ingredients': [ingredient.get('text', 'No Ingredients') for ingredient in
                                recipe.get('ingredients', [])],
                'image': recipe.get('image', '')
            })

        return {'meals': meals}
    else:
        # Log full error response for better debugging
        error_info = response.json() if response.content else response.text
        return {"error": error_info}


def fetch_exercise_recommendations(period_day, heaviness, muscle_group=None, equipment=None, category=None, limit=10):
    exercise_api_key = os.getenv('EXERCISE_API_KEY')
    if not exercise_api_key:
        print("EXERCISE_API_KEY is not set or loaded incorrectly")
        return {"error": "EXERCISE_API_KEY is not set in environment variables"}

    url = 'https://wger.de/api/v2/exercise/'
    params = {
        'period_day': period_day,
        'heaviness': heaviness,
        'apikey': exercise_api_key,
        'limit': limit
    }

    if muscle_group:
        params['muscle'] = muscle_group
    if equipment:
        params['equipment'] = equipment
    if category:
        params['category'] = category

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
