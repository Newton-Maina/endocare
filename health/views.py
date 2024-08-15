# health/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .utils import fetch_diet_plan, fetch_exercise_recommendations

def health_profile_view(request):
    diet_plan = None
    exercise_recommendations = None

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        period_day = request.POST.get('period_day')
        heaviness = request.POST.get('heaviness', 'light')  # Default to 'light' if not provided

        # Fetch data from APIs
        diet_plan = fetch_diet_plan(period_day, heaviness)
        exercise_recommendations = fetch_exercise_recommendations(period_day, heaviness)

        return render(request, 'health_profile_results.html', {
            'diet_plan': diet_plan,
            'exercise_recommendations': exercise_recommendations,
        })

    return render(request, 'health_profile.html')

