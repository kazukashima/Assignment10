import random
import requests
from django.shortcuts import render
from pymongo import MongoClient

def get_mongo_collection():
    client = MongoClient("mongodb://172.31.72.54:27017")
    db = client["assignment10db"]
    return db["history"]

def continent_form(request):
    return render(request, "geoapp/continent_form.html")

def search_results(request):
    continent = request.POST.get("continent")
    countries_url = f"https://restcountries.com/v3.1/region/{continent}"
    countries_data = requests.get(countries_url).json()

    selected = random.sample(countries_data, 5)

    api_key = "76ca0d90719e4d8b211fa04ba1dfa06d"
    results = []

    for country in selected:
        country_name = country["name"]["common"]
        capital = country.get("capital", ["Unknown"])[0]

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={api_key}&units=metric"
        weather = requests.get(weather_url).json()

        temp = weather.get("main", {}).get("temp", "N/A")
        desc = weather.get("weather", [{}])[0].get("description", "N/A")

        result = {
            "country": country_name,
            "capital": capital,
            "temp": temp,
            "description": desc
        }

        results.append(result)

        collection = get_mongo_collection()
        collection.insert_one(result)

    return render(request, "geoapp/search_results.html", {"results": results, "continent": continent})

def history(request):
    collection = get_mongo_collection()
    records = list(collection.find().sort("_id", -1))
    return render(request, "geoapp/history.html", {"records": records})

