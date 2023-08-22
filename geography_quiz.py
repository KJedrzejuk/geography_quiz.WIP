# -*- coding: utf-8 -*-
import random
import requests

import os
import sys
from datetime import datetime
from typing import Tuple, Optional
from more_itertools import locate
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from playsound import playsound
from PyQt5.QtGui import QPixmap, QImage


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("geography_quiz.ui", self)
        #self.StartB.clicked.connect(self.get_country_info)
        self.StartB.clicked.connect(self.start_quiz)
        self.NextB.clicked.connect(self.get_countries_list)
        self.HintB.clicked.connect(self.hints)
        self.image = QImage()
        self.score = 0
        self.round_points = 0
        self.dane_o_kraju = None
        self.indexes_list = []
        # Antarctica - wywala program

    def hints(self):
        #hint = self.HintCB.currentText()
        #print(f"HintB clicked. Current hint: {hint}")

        # text = self.send_value()
        # old_list = list(text)
        # new_list = len(old_list)
        # # letter_number = len(text)
        # Output: "Noc x i x dzień"\

        wyraz = "ala ma kota"

        # wynik = list(wyraz)
        #self.ContinentLE.setText(wyraz)
        wynik_nowy = self.find_spacebar_index(wyraz, " ")
        wynik_hint = self.transform_answer(wyraz, wynik_nowy)
        self.ContinentLE.setText(wynik_hint)

    def transform_answer(self, answer: str, index_list):
        output = len(answer) * "_"
        wynik = list(output)
        for index in index_list:
            wynik[index] = " "
        wynik = "".join(wynik)
        self.random_hint(answer, index_list, wynik)

        return wynik

    def random_hint(self, answer: str, index_list, empty_hint):
        print(index_list)
        show_index = random.randrange(len(answer))
        while show_index in index_list:
            #print(f"Podana wartość ({show_index}) już została wskazana, losuję kolejną liczbę")
            show_index = random.randrange(len(answer))
        index_list.append(show_index)
        print(index_list)
        # print(index_list)
        # print(empty_hint[show_index])
        # print(answer[show_index])
        empty_hint = list(empty_hint)
        empty_hint[show_index] = answer[show_index]
        empty_hint = "".join(empty_hint)
        print(empty_hint)
        return index_list, empty_hint
        #empty_hint[show_index] = answer[show_index]
        #print(empty_hint)
        #print(f"Losowy numer: {show_index}")

    def find_spacebar_index(self, s: str, ch: str):
        space_index = [i for i, ltr in enumerate(s) if ltr == ch]
        if not self.indexes_list:
            self.indexes_list = space_index
        return space_index

    def round_score_points(self, points: int):
        self.round_points += points
        #print(f"Dodano {points}")

    def round_score(self):
        self.score += self.round_points

    def start_quiz(self):
        if self.dane_o_kraju:
            self.round_points = 0
            continent, country, capital, latitude, longitude, area, population = self.correct_answer(self.dane_o_kraju)
            self.answer_validation(country, continent, capital, population, latitude, longitude, area)
            self.round_score()
            self.ScoreLabel.setText(f"Score: {self.score}")
            self.StartB.setDisabled(True)
        else:
            print("Pusto")

    def correct_answer(self, country_info):
        continent = country_info["continents"][0]
        country = country_info["name"]["common"]
        capital = country_info["capital"][0]
        latitude = country_info["latlng"][0]
        longitude = country_info["latlng"][1]
        area = country_info["area"]
        population = country_info["population"]
        return continent, country, capital, latitude, longitude, area, population

    def get_country_info(self):
        # countries = self.get_countries_list()
        # self.get_country_data(countries)

        # url = f"https://restcountries.com/v3.1/name/{country_name}"
        url = f"https://restcountries.com/v3.1/name/Poland"
        # data = self.get_countries_list()
        response = requests.get(url)
        country_info = self.get_countries_list()
        print(country_info)
        country_flag = country_info["flags"]["png"]
        self.image.loadFromData(requests.get(country_flag).content)
        self.FlagLabel.setPixmap(QPixmap(self.image))
        # 'flags': {'png': 'https://flagcdn.com/w320/mf.png',

        print(country_flag)
        # print(data)
        # print(data["capital"])
        # data = response.json()

        # if response.status_code == 404:
        #     print("Country not found.")
        #     return None

        # country_info = data
        # print(country_info)
        capital = country_info["capital"][0]
        continent = country_info["continents"][0]
        latitude = country_info["latlng"][0]
        longitude = country_info["latlng"][1]
        area = country_info["area"]
        population = country_info["population"]
        # print(capital, continent, latitude, longitude, area, population)
        capital_answer = self.CapitalLE.text()
        country_answer = self.CountryLE.text()
        continent_answer = self.ContinentLE.text()
        area_answer = self.AreaLE.text()
        population_answer = self.PopulationLE.text()
        latitude_answer = self.LatitudeLE.text()
        longitude_answer = self.LongitudeLE.text()
        # print(capital)
        self.capital_answer_validation(capital)
        self.population_answer_validation(population)
        self.latitude_answer_validation(latitude)
        self.longitude_answer_validation(longitude)
        self.round_score()
        self.round_points = 0
        self.ScoreLabel.setText(f"Score: {self.score}")
        # self.population_answer_validation(population)
        # if capital == capital_answer:
        #     print("Odpowiedź jest poprawna")
        # else:
        #     print("Odpowiedź nie jest poprawna")
        # return "Zakończono działanie"
        # return capital, continent, latitude, longitude, area, population

    def get_answer(self):
        capital_answer = self.CapitalLE.text()
        country_answer = self.CountryLE.text()
        continent_answer = self.ContinentLE.text()
        area_answer = self.AreaLE.text()
        population_answer = self.PopulationLE.text()
        latitude_answer = self.LatitudeLE.text()
        longitude_answer = self.LongitudeLE.text()
        return capital_answer, continent_answer, area_answer, population_answer, latitude_answer, longitude_answer

    def answer_validation(self, country: str, continent: str, capital: str, population: int, latitude: int,
                          longitude: int, area: int):
        self.country_answer_validation(country)
        self.capital_answer_validation(capital)
        self.continent_answer_validation(continent)
        self.area_answer_validation(area)
        self.population_answer_validation(population)
        self.latitude_answer_validation(latitude)
        self.longitude_answer_validation(longitude)

    def country_answer_validation(self, country: str):
        answer = self.CountryLE.text()
        if country.casefold() == answer.casefold():
            #print("country - Poprawna odpowiedź")
            self.round_score_points(10)
        else:
            #print("country - Błędna odpowiedź")
            self.round_score_points(0)

    def capital_answer_validation(self, capital: str):
        #print(f"Capital - {capital}")
        answer = self.CapitalLE.text()
        if capital.casefold() == answer.casefold():
            #print("Capital - Poprawna odpowiedź")
            self.round_score_points(10)
        else:
            #print("Capital - Błędna odpowiedź")
            self.round_score_points(0)

    def population_answer_validation(self, population: int) -> str:
        #print(f"Populatio - {population}")
        population_answer = self.PopulationLE.text()
        #print(population)
        if population_answer.isdigit():
            if (float(population) * 0.9) < float(population_answer) < (float(population) * 1.1):
                #print(f"Population - Correct answer  {population_answer}")
                self.round_score_points(10)
                return
            else:
                #print("Population - Wrong answer")
                self.round_score_points(0)
                return
        else:
            #print("Population - The value given should be a number")
            self.round_score_points(0)
            return

    def area_answer_validation(self, area: int) -> str:
        area_answer = self.AreaLE.text()
        #print(f"Area - {area}")
        if area_answer.isdigit():
            if (float(area) * 0.9) < float(area_answer) < (float(area) * 1.1):
                #print(f"Area - Correct answer  {area_answer}")
                self.round_score_points(10)
                return
            else:
                #print("Area - Wrong answer")
                self.round_score_points(0)
                return
        #print("Area - The value given should be a number")
        self.round_score_points(0)
        return

    def latitude_answer_validation(self, lattitude):
        latitude_answer = self.LatitudeLE.text()
        #print(f"LAT - {lattitude}")
        if latitude_answer.isdigit():
            if float(lattitude) - 3 < float(latitude_answer) < float(lattitude) + 3:
                #print("Lattitude - Poprawna odpowiedź")
                self.round_score_points(10)
                return
            else:
                #print("Lattitude - Błędna odpowiedź")
                self.round_score_points(0)
                return
        #print("Lattitude - podana wartośc powinna być liczbą")
        self.round_score_points(0)
        return

    def longitude_answer_validation(self, longitude):
        #print(f"Long - {longitude}")
        longitude_answer = self.LongitudeLE.text()
        if longitude_answer.isdigit():
            if float(longitude) - 3 < float(longitude_answer) < float(longitude) + 3:
                #print("Longitude - Poprawna odpowiedź")
                self.round_score_points(10)
                return
            else:
                #print("Longitude - Błedna odpowiedź")
                self.round_score_points(0)
                return
        #print("Longitude - podana wartość powinna być liczbą")
        self.round_score_points(0)
        return

    def continent_answer_validation(self, continent: str):
        #print(f"Continent - {continent}")
        continent_answer = self.ContinentLE.text()
        if continent_answer.casefold() == continent.casefold():
            #print("continent - Poprawna odpowiedź")
            self.round_score_points(10)
        else:
            #print("continent - Błędna odpowiedź")
            self.round_score_points(0)

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
        # print(type(flag))
        print(flag["png"])
        # if country_info["borders"]:
        #     neighbourhoods = country_info["borders"]
        # country_name_pl = country_info["pol"][0]
        # lat, long = coordinate_symbols(latitude, longitude)
        print(f"Capital of {country_name}: {str(capital)}")
        # capital_ask(country_name, capital)
        # print(f"Coordinates: {lat}, {long}")
        print(f"Country area: {area} km²")
        # area_ask(country_name, area)
        print(f"Population: {population}")
        # ask_population(country_name, population)
        print(continent)
        # continent_ask(country_name, continent)
        # if neighbourhoods:
        #     print(neighbourhoods)
        # print(country_name_pl)

        return capital, latitude, longitude, area

    def get_countries_list(self):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)
        if response.status_code == 200:
            countries_data = response.json()
            random_number = random.randrange(0, len(countries_data))
            random_country = countries_data[random_number]
            # country = random_country["name"]["common"]
            country_flag = random_country["flags"]["png"]
            self.image.loadFromData(requests.get(country_flag).content)
            self.FlagLabel.setPixmap(QPixmap(self.image))
            self.dane_o_kraju = random_country
            self.StartB.setEnabled(True)
            return random_country
        else:
            print("Nie udało się pobrać danych. Spróbuj ponownie później.")
            return


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(600)
widget.show()

sys.exit(app.exec())
