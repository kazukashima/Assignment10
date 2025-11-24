import random
import requests
from django.shortcuts import render
from pymongo import MongoClient

# Connect to MongoDB on the MongoDB-EC2 instance
def get_mongo_collection():
    client = MongoClient("mongodb://172.31.72.54:27017")
    db = client["assignment10db"]
    return db["history"]

# Show the continent selection form
def continent_form(request):
    return render(request, "geoapp/continent_form.html")

# Handle the search action after selecting a continent
def search_results(request):
    # Read selected continent from the form
    continent = request.POST.get("continent")

    # Call REST Countries API to get countries in that continent
    countries_url = f"https://restcountries.com/v3.1/region/{continent}"
    countries_data = requests.get(countries_url).json()

    # Randomly pick 5 countries
    selected = random.sample(countries_data, 5)

    # Your OpenWeatherMap API key
    api_key = "76ca0d90719e4d8b211fa04ba1dfa06d"

    results = []

    # Loop through 5 selected countries and get weather for each capital
    for country in selected:
        country_name = country["name"]["common"]
        capital = country.get("capital", ["Unknown"])[0]

        # Call OpenWeatherMap API for weather
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={capital}&appid={api_key}&units=metric"
        )
        weather = requests.get(weather_url).json()

        # Extract temperature and description safely
        temp = weather.get("main", {}).get("temp", "N/A")
        desc = weather.get("weather", [{}])[0].get("description", "N/A")

        # Build result record
        result = {
            "country": country_name,
            "capital": capital,
            "temp": temp,
            "description": desc,
        }

        results.append(result)

        # Save to MongoDB
        collection = get_mongo_collection()
        collection.insert_one(result)

    # Render the results page
    return render(
        request,
        "geoapp/search_results.html",
        {"results": results, "continent": continent},
    )

# Display saved history from MongoDB
def history(request):
    collection = get_mongo_collection()
    records = list(collection.find().sort("_id", -1))
    return render(request, "geoapp/history.html", {"records": records})

