from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Delhi'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=66e2f7dcb110fa2774f1c8aba666e600'
    PARAMS = {'units': 'metric'}

    API_KEY = ''  # Your OpenWeatherMap API key
    SEARCH_ENGINE_ID = ''  # Your Google Custom Search Engine ID

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()
    except Exception as e:
        messages.error(request, f"Failed to retrieve weather data for {city}: {str(e)}")
        description = 'Unknown'
        icon = '01d'
        temp = 25
        day = datetime.date.today()

    image_url = ''  # Initialize image URL as empty string
    try:
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        if search_items:  # Check if search_items is not None
            image_url = search_items[0]['link']  # Get the first image URL if available
    except Exception as e:
        messages.error(request, f"Failed to retrieve image for {city}: {str(e)}")

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'image_url': image_url
    })
