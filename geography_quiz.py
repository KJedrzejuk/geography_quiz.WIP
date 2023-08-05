# -*- coding: utf-8 -*-
import random
import requests

import os
import sys
from datetime import datetime
from typing import Tuple, Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from playsound import playsound
from PyQt5.QtGui import QPixmap


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("geography_quiz.ui", self)
        self.StartB.clicked.connect(self.get_country_info)
        self.score = 0
        self.round_points = 0

    def round_score_points(self, points: int):
        self.round_points += points
        print(f"Dodano {points}")

    def round_score(self):
        self.score += self.round_points



    def get_country_info(self):
        #countries = self.get_countries_list()
        #self.get_country_data(countries)

       # url = f"https://restcountries.com/v3.1/name/{country_name}"
        url = f"https://restcountries.com/v3.1/name/Poland"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 404:
            print("Country not found.")
            return None

        country_info = data[0]
        capital = country_info["capital"][0]
        continent = country_info["continents"][0]
        latitude = country_info["latlng"][0]
        longitude = country_info["latlng"][1]
        area = country_info["area"]
        population = country_info["population"]
        #print(capital, continent, latitude, longitude, area, population)
        capital_answer = self.CapitalLE.text()
        country_answer = self.CountryLE.text()
        continent_answer = self.ContinentLE.text()
        area_answer = self.AreaLE.text()
        population_answer = self.PopulationLE.text()
        latitude_answer = self.LatitudeLE.text()
        longitude_answer = self.LongitudeLE.text()
        # print(capital)
        self.capital_answer_validation(capital)
        print("Capital answer")
        self.population_answer_validation(population)
        print("population answer")
        self.latitude_answer_validation(latitude)
        print("lat answer")
        self.longitude_answer_validation(longitude)
        print("long answer")
        self.round_score()
        print("round score")
        self.round_points = 0
        self.ScoreLabel.setText(f"Wynik wynosi: {self.score}")
        #self.population_answer_validation(population)
        # if capital == capital_answer:
        #     print("Odpowiedź jest poprawna")
        # else:
        #     print("Odpowiedź nie jest poprawna")
        # return "Zakończono działanie"
        #return capital, continent, latitude, longitude, area, population

    def get_answer(self):
        capital_answer = self.CapitalLE.text()
        country_answer = self.CountryLE.text()
        continent_answer = self.ContinentLE.text()
        area_answer = self.AreaLE.text()
        population_answer = self.PopulationLE.text()
        latitude_answer = self.LatitudeLE.text()
        longitude_answer = self.LongitudeLE.text()
        return capital_answer, continent_answer, area_answer, population_answer, latitude_answer, longitude_answer

    def answer_validation(self, capital: str, population: int, latitude: int, longitude: int, area: int, continent: str):
        self.capital_answer_validation(capital)
        self.continent_answer_validation(continent)
        self.area_answer_validation(area)
        self.population_answer_validation(population)
        self.latitude_answer_validation(latitude)
        self.longitude_answer_validation(longitude)



    def capital_answer_validation(self, capital: str):
        answer = self.CapitalLE.text()
        if capital.casefold() == answer.casefold():
            print("Capital - Poprawna odpowiedź")
            self.round_score_points(10)
        else:
            print("Capital - Błędna odpowiedź")
            self.round_score_points(0)


    def population_answer_validation(self, population: int) -> str:
        population_answer = self.PopulationLE.text()
        if population_answer.isdigit():
            if (float(population) * 0.9) < float(population_answer) < (float(population) * 1.1):
                print(f"Population - Correct answer  {population_answer}")
                self.round_score_points(10)
                return
            else:
                print("Population - Wrong answer")
                self.round_score_points(0)
                return
        else:
            print("Population - The value given should be a number")
            self.round_score_points(0)
            return

    def area_answer_validation(self, area: int) -> str:
        area_answer = self.PopulationLE.text()
        if area_answer.isdigit():
            if (float(area) * 0.9) < float(area_answer) < (float(area) * 1.1):
                print(f"Area - Correct answer  {area_answer}")
                self.round_score_points(10)
                return
            else:
                print("Area - Wrong answer")
                self.round_score_points(0)
                return
        else:
            print("Area - The value given should be a number")
            self.round_score_points(0)
            return

    def latitude_answer_validation(self, lattitude):
        latitude_answer = self.LatitudeLE.text()
        if latitude_answer.isdigit():
            if float(lattitude) - 3 < float(latitude_answer) < float(lattitude) + 3:
                print("Lattitude - Poprawna odpowiedź")
                self.round_score_points(0)
                return
            else:
                print("Lattitude - Błędna odpowiedź")
                self.round_score_points(0)
                return
        print("Lattitude - podana wartośc powinna być liczbą")
        self.round_score_points(0)
        return

    def longitude_answer_validation(self, longitude):
        longitude_answer = self.LongitudeLE.text()
        if longitude_answer.isdigit():
            if float(longitude) - 3 < float(longitude_answer) < float(longitude) + 3:
                print("Longitude - Poprawna odpowiedź")
                self.round_score_points(10)
                return
            else:
                print("Longitude - Błedna odpowiedź")
                self.round_score_points(0)
                return
        print("Longitude - podana wartość powinna być liczbą")
        self.round_score_points(0)
        return

    def continent_answer_validation(self, continent: str):
        continent_answer = self.ContinentLE.text()
        if continent_answer.casefold() == continent.casefold():
            print("continent - Poprawna odpowiedź")
            self.round_score_points(10)
        else:
            print("continent - Błędna odpowiedź")
            self.round_score_points(0)

        # if (float(population) * 0.9) < float(population_answer) < (float(population) * 1.1):
        #     print("Odpowiedź zaliczona! ")
        #     print(f"Poprawna odpowiedź to: {population}")
        # else:
        #     print("Odpowiedź błędna")
        #     print(f"Poprawna odpowiedź to: {population}")
        # flag = country_info["flags"]
        # print(flag["png"])
        # image_url = "https://flagcdn.com/w320/pl.png"
        #image = QImage()
        #image.loadFromData(requests.get(image_url).content)

        #self.FlagLabel.setPixmap(QPixmap(image))
        # pixmap = QPixmap(image_url)
        # self.FlagLabel.setPixmap(pixmap)
        # self.resize(pixmap.width(40), pixmap.height(10))

        # self.CountrylLabel.setText(country_name)
        # self.CapitalLabel.setText(capital[0])
        # print(capital[0])
        # latitude = country_info["latlng"][0]
        # longitude = country_info["latlng"][1]
        # area = country_info["area"]
        # # self.AreaLabel.setText(area)
        # population = country_info["population"]
        # continent = country_info["continents"][0]
        # self.ContinentLabel.setText(continent)


    def get_answer(self):
        capital_answer = self.CapitalLE.text()
        country_answer = self.CountryLE.text()
        continent_answer = self.ContinentLE.text()
        area_answer = self.AreaLE.text()
        population_answer = self.PopulationLE.text()
        latitude_answer = self.LatitudeLE.text()
        longitude_answer = self.LongitudeLE.text()
        # return capital_answer, country_answer, continent_answer, area_answer, population_answer, \
        #        latitude_answer, longitude_answer
        part1 = "part1"
        part2 = "part2"
        return capital_answer

    # def set_value(self, capital, country, continent, area, population, lattitude, longitude):
    def set_value(self, zmienna1):
        self.CapitalLE.setText(zmienna1)
        # self.CapitalLabel.setText(capital)
        # self.CountryLE.text(country)
        # self.ContinentLE.text(continent)
        # self.AreaLE.text(area)
        # self.PopulationLE.text(population)
        # self.LatitudeLE.text(lattitude)
        # self.LongitudeLE.text(longitude)

    def count(self):
        #capital, country, continent, area, population, lattitude, longitude = self.get_answer()
        p1 = self.get_answer()
        #self.set_value(capital, country, continent, area, population, lattitude, longitude)
        self.set_value(p1)
        #print(capital, country, continent, population, area, lattitude, longitude)



    def get_country_data(self, country_name):
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 404:
            print("Country not found.")
            return None

        country_info = data[0]
        # print(country_info)
        self.CountrylLabel.setText(country_name)
        capital = country_info["capital"]
        self.CapitalLabel.setText(capital)
        latitude = country_info["latlng"][0]
        longitude = country_info["latlng"][1]
        area = country_info["area"]
        self.AreaLabel.setText(area)
        population = country_info["population"]
        continent = country_info["continents"][0]
        self.ContinentLabel.setText(continent)
        flag = country_info["flags"]
        #print(type(flag))
        print(flag["png"])
        # if country_info["borders"]:
        #     neighbourhoods = country_info["borders"]
        # country_name_pl = country_info["pol"][0]
        lat, long = coordinate_symbols(latitude, longitude)
        print(f"Capital of {country_name}: {str(capital)}")
        # capital_ask(country_name, capital)
        print(f"Coordinates: {lat}, {long}")
        print(f"Country area: {area} km²")
        #area_ask(country_name, area)
        print(f"Population: {population}")
        #ask_population(country_name, population)
        print(continent)
        #continent_ask(country_name, continent)
            # if neighbourhoods:
        #     print(neighbourhoods)
        # print(country_name_pl)

        return capital, latitude, longitude, area
    #
    #
    # def coordinate_symbols(self, lat: int, long: int) -> str:
    #     latittude = ""
    #     longitude = ""
    #     if lat > 0:
    #         latittude = str(lat) + " N"
    #     if lat < 0:
    #         latittude = str(lat * -1) + " S"
    #     if long > 0:
    #         longitude = str(long) + " E"
    #     if long < 0:
    #         longitude = str(long * -1) + " W"
    #     return latittude, longitude
    #
    # def answers_message(correctness: bool, coreect_answer):
    #     if correctness is True:
    #         print("answer is correct!")
    #     else:
    #         print(f"Your answer was wrong. Correct answer is {coreect_answer}")
    #
    #
    # def ask_population(self, country: str, population: int) -> str:
    #     population_answer = input(f"Give population of {country}: ")
    #     if (float(population) * 0.9) < float(population_answer) < (float(population) * 1.1):
    #         print("Odpowiedź zaliczona! ")
    #         print(f"Poprawna odpowiedź to: {population}")
    #     else:
    #         print("Odpowiedź błędna")
    #         print(f"Poprawna odpowiedź to: {population}")
    #
    #
    # def capital_ask(self, country: str, capital: str):
    #     capital_answer = input(f"Podaj nazwę stolicy państwa {country}: ")
    #     capital = str(capital)
    #     if capital.lower() == capital_answer.lower():
    #         print("Odpowiedź poprawna! ")
    #     else:
    #         print(f"Podano błędną odpowiedź. Poprawna odpowiedź to: {capital}")
    #
    #
    # def area_ask(self, country: str, area: int):
    #     area_answer = input(f"Podaj ludność państwa {country}: ")
    #     if (float(area) * 0.9) < float(area_answer) < (float(area) * 1.1):
    #         print("Odpowiedź zaliczona!")
    #         print(f"Poprawna odpowiedź: {area}")
    #     else:
    #         print("Błędna odpowiedź")
    #         print(f"Poprawna odpowiedź to: {area}")
    #
    #
    # def continent_ask(self, country: str, continent: str):
    #     continent_answer = input(f"Podaj kontynent do którego należy {country}: ")
    #     #print(continent[0])
    #     print(continent_answer)
    #     if str(continent).lower() == str(continent_answer).lower():
    #         print("Odpowiedź zaliczona!")
    #         print(f"Poprawna odpowiedź: {continent}")
    #     else:
    #         print("Podana odpowiedź jest błędna")
    #         print(f"Poprawna odpowiedź to: {continent}")
    #
    def get_countries_list(self):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)
        if response.status_code == 200:
            countries_data = response.json()
            all_countries = [country["name"]["common"] for country in countries_data]
            # random_countries = random.sample(all_countries, 10)
            random_countries = random.sample(all_countries, 1)
            return random_countries
        else:
            print("Nie udało się pobrać danych. Spróbuj ponownie później.")
            return []
    #
    #
    # def start(self):
    #     print("funkcja start")
    #     countries = self.get_countries_list()
    #     self.get_country_data(countries)
        # country_number = 1
        # if countries:
        #     for country in countries:
        #         print(f"Numer kraju: {country_number}")
        #         country_number += 1
        #         get_country_data(country)
    #
    #
    # #start()

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(600)
widget.show()

sys.exit(app.exec())
