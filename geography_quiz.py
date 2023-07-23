# -*- coding: utf-8 -*-
import random

import requests


def get_country_data(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 404:
        print("Kraj nie został znaleziony.")
        return None

    country_info = data[0]
    # print(country_info)
    capital = country_info["capital"]
    latitude = country_info["latlng"][0]
    longitude = country_info["latlng"][1]
    area = country_info["area"]
    population = country_info["population"]
    continent = country_info["continents"]
    # if country_info["borders"]:
    #     neighbourhoods = country_info["borders"]
    # country_name_pl = country_info["pol"][0]
    lat, long = coordinate_symbols(latitude, longitude)
    print(f"Stolica kraju {country_name}: {str(capital)}")
    # capital_ask(country_name, capital)
    print(f"Współrzędne geograficzne stolicy: {lat}, {long}")
    print(f"Powierzchnia państwa: {area} km²")
    print(f"Populacja wynosi: {population}")
    print(continent)
    # if neighbourhoods:
    #     print(neighbourhoods)
    # print(country_name_pl)

    return capital, latitude, longitude, area


def coordinate_symbols(lat: int, long: int) -> str:
    latittude = ""
    longitude = ""
    if lat > 0:
        latittude = str(lat) + " N"
    if lat < 0:
        latittude = str(lat * -1) + " S"
    if long > 0:
        longitude = str(long) + " E"
    if long < 0:
        longitude = str(long * -1) + " W"
    return latittude, longitude


def get_countries_list():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)

    if response.status_code == 200:
        countries_data = response.json()
        all_countries = [country["name"]["common"] for country in countries_data]

        random_countries = random.sample(all_countries, 10)
        return random_countries
    else:
        print("Nie udało się pobrać danych. Spróbuj ponownie później.")
        return []


def start():
    countries = get_countries_list()
    country_number = 1
    if countries:
        for country in countries:
            print(f"Numer kraju: {country_number}")
            country_number += 1
            get_country_data(country)


def capital_ask(country: str, capital: str):
    capital_answear = input(f"Podaj nazwę stolicy państwa {country}: ")
    capital = str(capital)
    if capital.lower() == capital_answear.lower():
        print("Odpowiedź poprawna! ")
    else:
        print(f"Podano błędną odpowiedź. Poprawna odpowiedź to: {capital}")


start()
