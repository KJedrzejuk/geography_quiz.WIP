# -*- coding: utf-8 -*-
import random
import requests

import os
import sys
from datetime import datetime
from typing import Tuple, Optional, Dict
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
        self.StartB.clicked.connect(self.start_quiz)
        self.NextB.clicked.connect(self.get_countries_list)
        self.HintB.clicked.connect(self.get_hint)
        self.image = QImage()
        self.score = 0
        self.round_points = 0
        self.country_informations = None
        self.indexes_list = []
        self.clear_show_correct_answer_flag = False

    def minus_rmove(self, answer: str):
        if answer[0] == "-":
            return answer[1:]
        else:
            return answer


    def get_hint(self) -> Optional[str]:
        widget = self.check_hint_type()
        answer = widget.text()
        correct_answer = str(self.hint_correct_answer())
        correct_answer = self.minus_rmove(correct_answer)
        if not answer:
            spacebar_index = self.find_spacebar_index(correct_answer, " ")
            empty_hint = self.transform_answer(correct_answer, spacebar_index)
            widget.setText(empty_hint)
            self.correct_message_hint_test()
            return empty_hint
        else:
            if answer == correct_answer:
                self.correct_message_hint()
            else:
                answer = self.hint_lenght_compare(correct_answer, answer)
                correct_char_indexes = self.hints_compare(correct_answer, answer)
                new_char_index = self.random_hint_char(correct_answer, correct_char_indexes)
                self.put_new_hint_char(widget, new_char_index, answer)
                self.correct_message_hint_test()

    def random_hint_char(self, correct_answer: str, correct_char_indexes: list[int]) -> Dict[str, int]:
        hint_index = random.randrange(len(correct_answer))
        while hint_index in correct_char_indexes:
            hint_index = random.randrange(len(correct_answer))
        new_char_index = {correct_answer[hint_index]: hint_index}
        return new_char_index

    def put_new_hint_char(self, widget, new_char_index: Dict[str, int], current_answer: str):
        hint_value = list(new_char_index.values())[0]
        hint_key = list(new_char_index.keys())[0]
        hint = current_answer[:int(hint_value)] + str(hint_key) + current_answer[int(hint_value)+1:]
        widget.setText(hint)

    def random_hint(self, answer: str, index_list: list[int], empty_hint: str) -> tuple[list[int], str]:
        show_index = random.randrange(len(answer))
        while show_index in index_list:
            show_index = random.randrange(len(answer))
        index_list.append(show_index)
        empty_hint = list(empty_hint)
        empty_hint[show_index] = answer[show_index]
        empty_hint = "".join(empty_hint)
        return index_list, empty_hint

    def hints_compare(self, correct_answer: str, answer: str) -> int:
        indexes = []
        for index, (element1, element2) in enumerate(zip(list(correct_answer), list(answer))):
            if element1 == element2:
                indexes.append(index)
        return indexes

    def hint_lenght_compare(self, correct_answer: str, answer: str) -> str:
        if len(answer) < len(correct_answer):
            answer += "_" * (len(correct_answer) - len(answer))
            return answer
        else:
            answer = answer[:len(correct_answer)]
            return answer

    def transform_answer(self, answer: str, index_list: list[int]) -> str:
        output = len(answer) * "_"
        wynik = list(output)
        for index in index_list:
            wynik[index] = " "
        wynik = "".join(wynik)
        self.random_hint(answer, index_list, wynik)
        return wynik

    def find_spacebar_index(self, s: str, ch: str) -> list[int]:
        space_index = [i for i, ltr in enumerate(s) if ltr == ch]
        if not self.indexes_list:
            self.indexes_list = space_index
        return space_index

    def check_hint_type(self) -> str:
        text = self.HintCB.currentText()
        widget_item = self.go_hint(text)
        return widget_item

    def go_hint(self, value: str):
        if value == "Country":
            widget_item = self.CountryLE
        if value == "Capital":
            widget_item = self.CapitalLE
        if value == "Continent":
            widget_item = self.ContinentLE
        if value == "Longitude":
            widget_item = self.LongitudeLE
        if value == "Latitude":
            widget_item = self.LatitudeLE
        if value == "Area":
            widget_item = self.AreaLE
        if value == "Population":
            widget_item = self.PopulationLE
        return widget_item

    def hint_correct_answer(self) -> str:
        continent, country, capital, latitude, longitude, area, population = self.correct_answer(self.country_informations)
        value = self.HintCB.currentText()
        if value == "Country":
            return country
        if value == "Capital":
            return capital
        if value == "Continent":
            return continent
        if value == "Longitude":
            return longitude
        if value == "Latitude":
            return latitude
        if value == "Area":
            return area
        if value == "Population":
            return population

    def round_score_points(self, points: int):
        self.round_points += points

    def round_score(self):
        self.score += self.round_points

    def start_quiz(self):
        self.correct_message_hint_test()
        if self.country_informations:
            try:
                self.round_points = 0
                continent, country, capital, latitude, longitude, area, population = self.correct_answer(self.country_informations)
                self.answer_validation(country, continent, capital, population, latitude, longitude, area)
                self.round_score()
                self.ScoreLabel.setText(f"Score: {self.score}")
                self.set_show_answer()
            except:
                self.get_countries_list()
                self.start_quiz()
        else:
            print("Empty")

    def correct_answer(self, country_info) -> tuple[str, str, str, float, float, float, int]:
        continent = country_info["continents"][0]
        country = country_info["name"]["common"]
        capital = country_info["capital"][0]
        latitude = int(country_info["latlng"][0])
        longitude = int(country_info["latlng"][1])
        area = int(country_info["area"])
        population = country_info["population"]
        return continent, country, capital, latitude, longitude, area, population

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
            self.round_score_points(10)
        else:
            self.round_score_points(0)

    def capital_answer_validation(self, capital: str):
        answer = self.CapitalLE.text()
        if capital.casefold() == answer.casefold():
            self.round_score_points(10)
        else:
            self.round_score_points(0)

    def population_answer_validation(self, population: int):
        population_answer = self.PopulationLE.text()
        if population_answer.isdigit():
            if (float(population) * 0.9) < float(population_answer) < (float(population) * 1.1):
                self.round_score_points(10)
                return
            else:
                self.round_score_points(0)
                return
        else:
            self.round_score_points(0)
            return

    def area_answer_validation(self, area: int):
        area_answer = self.AreaLE.text()
        if area_answer.isdigit():
            if (float(area) * 0.9) < float(area_answer) < (float(area) * 1.1):
                self.round_score_points(10)
                return
            else:
                self.round_score_points(0)
                return
        self.round_score_points(0)
        return

    def latitude_hemisphere(self, latitude: float):
        if str(self.ltitudeCB.currentText()) == "S" and latitude != 0:
            return float(latitude) * (-1)
        else:
            return float(latitude)

    def longitude_hemisphere(self, longitude: float):
        if str(self.longitudeCB.currentText()) == "W" and longitude != 0:
            return float(longitude) * (-1)
        else:
            return float(longitude)

    def latitude_answer_validation(self, lattitude: float):
        latitude_answer = self.LatitudeLE.text()
        lattitude = self.latitude_hemisphere(lattitude)
        if latitude_answer.isdigit():
            if float(lattitude) - 3 < float(latitude_answer) < float(lattitude) + 3:
                self.round_score_points(10)
                return
            else:
                self.round_score_points(0)
                return
        self.round_score_points(0)
        return

    def longitude_answer_validation(self, longitude: float):
        longitude_answer = self.LongitudeLE.text()
        longitude = self.longitude_hemisphere(longitude)
        if longitude_answer.isdigit():
            if float(longitude) - 3 < float(longitude_answer) < float(longitude) + 3:
                self.round_score_points(10)
                return
            else:
                self.round_score_points(0)
                return
        self.round_score_points(0)
        return

    def continent_answer_validation(self, continent: str):
        continent_answer = self.ContinentLE.text()
        if continent_answer.casefold() == continent.casefold():
            self.round_score_points(10)
        else:
            self.round_score_points(0)

    def correct_message_hint(self):
        self.correctAnsweLabel.setText("Answer is correct")
        self.correctAnsweLabel.setStyleSheet("background-color: green; color: white;")

    def correct_message_hint_disabled(self):
        self.correctAnsweLabel.setText("")
        self.correctAnsweLabel.setStyleSheet("")

    def correct_message_hint_test(self):
        if self.correctAnsweLabel.text():
            self.correct_message_hint_disabled()

    def get_countries_list(self):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)
        if response.status_code == 200:
            if self.clear_show_correct_answer_flag:
                self.set_start_quiz()
            self.clear()
            countries_data = response.json()
            random_number = random.randrange(0, len(countries_data))
            random_country = countries_data[random_number]
            country_flag = random_country["flags"]["png"]
            self.image.loadFromData(requests.get(country_flag).content)
            self.FlagLabel.setPixmap(QPixmap(self.image))
            self.country_informations = random_country
            self.StartB.setEnabled(True)
            self.HintB.setEnabled(True)
            self.HintCB.setEnabled(True)
            return random_country
        else:
            print("Data acquisition failed.")
            return

    def clear(self):
        self.CountryLE.setText("")
        self.ContinentLE.setText("")
        self.CapitalLE.setText("")
        self.LongitudeLE.setText("")
        self.LatitudeLE.setText("")
        self.AreaLE.setText("")
        self.PopulationLE.setText("")
        self.correct_message_hint_test()


    def set_show_answer(self):
        self.StartB.clicked.disconnect(self.start_quiz)
        self.StartB.setText("Show correct answers")
        self.StartB.clicked.connect(self.show_correct_answers)
        self.clear_show_correct_answer_flag = True

    def show_correct_answers(self):
        continent, country, capital, lat, long, area, population = self.correct_answer(self.country_informations)
        lat = self.minus_rmove(str(lat))
        long = self.minus_rmove(str(long))
        self.CountryLE.setText(str(country))
        self.ContinentLE.setText(str(continent))
        self.CapitalLE.setText(str(capital))
        self.LongitudeLE.setText(str(long))
        self.LatitudeLE.setText(str(lat))
        self.AreaLE.setText(str(area))
        self.PopulationLE.setText(str(population))
        self.StartB.setDisabled(True)
        self.set_start_quiz()

    def set_start_quiz(self):
        self.StartB.setText("Start")
        self.StartB.clicked.disconnect(self.show_correct_answers)
        self.StartB.clicked.connect(self.start_quiz)
        self.clear_show_correct_answer_flag = False


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(600)
widget.show()

sys.exit(app.exec())
