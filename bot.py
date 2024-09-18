# Copyright 2024 Matvii Jarosh
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import mysql.connector
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from datetime import datetime, timedelta
import logging
import sys

logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)

TOKEN = ''

schedule = [
    # 7 а класс
    {"lesson": "Алгебра", "room": "29", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Біологія", "room": "14", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Біологія", "room": "14", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},
{"lesson": "ІК історія та грю.освю", "room": "не знаю", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "7а"},

{"lesson": "Фізика", "room": "26", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Геометрія", "room": "29", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Англіська мова", "room": "44/21", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Географія", "room": "24", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Технології", "room": "4/7", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},
{"lesson": "Українська література", "room": "30", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "7а"},

{"lesson": "Алгебра", "room": "29", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},
{"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},
{"lesson": "ІК Здоров'я, безпека та добробут", "room": "4", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},
{"lesson": "Англіська мова", "room": "33/21", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},
{"lesson": "Фізика", "room": "26", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},
{"lesson": "Плавання", "room": "басейн", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "7а"},

{"lesson": "Алгебра", "room": "29", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "Муз. мист./Образотв мист", "room": "48/34", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "ІК історія та гр.осв", "room": "20", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "ІК історія та гр.осв", "room": "20", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "Геометрія", "room": "32", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},
{"lesson": "Англіська мова", "room": "21", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "7а"},

{"lesson": "Хімія", "room": "14", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},
{"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},
{"lesson": "Англіська мова", "room": "22/21", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},
{"lesson": "Географія", "room": "24", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},
{"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},
{"lesson": "Українська література", "room": "3", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "7а"},




    # 8 а класс
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8а"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8а"},
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8а"},
    {"lesson": "Алгебра", "room": "30", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8а"},
    {"lesson": "Плавання", "room": "басейн", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8а"},

    {"lesson": "Українська література", "room": "30", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},
    {"lesson": "Англіська мова", "room": "17/44", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},
    {"lesson": "Історія", "room": "31", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},
    {"lesson": "Історія", "room": "31", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8а"},

    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Труди", "room": "4/1", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Мистецство", "room": "34", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},
    {"lesson": "Англіська мова", "room": "17/33", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8а"},

    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Українська література", "room": "30", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},
    {"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8а"},

    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Основи здоровья", "room": "31", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Історія", "room": "31", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},
    {"lesson": "Англіська мова", "room": "17/22", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8а"},

    # 8 б класс
    {"lesson": "Алгебра", "room": "23", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Геометрія", "room": "23", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Англіська мова/Інформатика", "room": "21/7", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Історія", "room": "32", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},
    {"lesson": "Історія", "room": "33", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8б"},

    {"lesson": "Історія", "room": "31", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Плавання", "room": "басейн", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Українська література", "room": "30", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Мистецтво", "room": "34", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},
    {"lesson": "Інформатика/Англіська мова", "room": "21", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8б"},

    {"lesson": "Алгебра", "room": "23", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},
    {"lesson": "Географія", "room": "20", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},
    {"lesson": "Труди", "room": "4/1", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},
    {"lesson": "Англіська мова", "room": "21", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8б"},

    {"lesson": "Англіська мова", "room": "21", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Українська література", "room": "30", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Англіська мова/Інформатика", "room": "21/7", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},
    {"lesson": "Геометрія", "room": "29", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8б"},

    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},
    {"lesson": "Основи здоровья", "room": "31", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},
    {"lesson": "Інформатика/Англіська мова", "room": "7/21", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8б"},

    # 8 В класс
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},
    {"lesson": "Алгебра", "room": "23", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},
    {"lesson": "Геометрія", "room": "23", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},
    {"lesson": "Історія", "room": "33", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "8в"},

    {"lesson": "Англіська мова", "room": "21/44", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Біологія", "room": "30", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Історія", "room": "12", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Історія", "room": "31", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "8в"},

    {"lesson": "Англіська мова", "room": "21/33", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8в"},
    {"lesson": "Плавання", "room": "басейн", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8в"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8в"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8в"},
    {"lesson": "Труди", "room": "20", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "8в"},

    {"lesson": "Українська лытература", "room": "30", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Мистецтво", "room": "34", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Геометрія", "room": "29", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},
    {"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "8в"},

    {"lesson": "Основи здоров'я", "room": "31", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Українська мова", "room": "30", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Інформатика", "room": "3/7", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Алгебра", "room": "29", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Англіська мова", "room": "21", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "8в"},

    # 9 А класс
    {"lesson": "Англіська мова", "room": "25а", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Алгебра", "room": "23", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Основи здоров'я", "room": "33", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Зарібіжна література", "room": "22", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Українська мова", "room": "33", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},
    {"lesson": "Англіська мова", "room": "25а", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "9а"},

    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Англіська мова/Інформатикка", "room": "25а/3", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Інформатикка/Англіська мова", "room": "3/25а", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Історія", "room": "27", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Геометрія", "room": "23", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Плавання", "room": "басейн", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},
    {"lesson": "Труди", "room": "4/1", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "9а"},

    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Біологія", "room": "12", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Географія", "room": "22", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Географія/Історія", "room": "22/27", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "9а"},

    {"lesson": "Українська мова", "room": "33", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Українська література", "room": "33", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Англіська мова/Інформатикка", "room": "25а/3", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Інформатикка/Англіська мова", "room": "3/25а", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Алгебра", "room": "23", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Історія", "room": "27", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},
    {"lesson": "Зарібіжна література", "room": "22", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "9а"},

    {"lesson": "Геометрія", "room": "23", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "9а"},
    {"lesson": "Правознаство", "room": "27", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "9а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "9а"},
    {"lesson": "Українська література", "room": "33", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "9а"},
    {"lesson": "Мистецство", "room": "34", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "9а"},

    # 10 А класс
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Громад освіта", "room": "27", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Громад освіта", "room": "27", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Українська мова", "room": "31", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Істрорія", "room": "25", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},
    {"lesson": "Істрорія", "room": "25", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10а"},

    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Фізика/Фізкультура", "room": "26/спорт зал", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Зарубіжна література", "room": "20", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},
    {"lesson": "Біологія", "room": "14", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10а"},

    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Англіська мова/Інфрматика", "room": "17/6", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Англіська мова/Інфрматика", "room": "17/6", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Інформатика/Англіська мова", "room": "6/17", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Українська література", "room": "31", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},
    {"lesson": "Технології", "room": "4/1", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10а"},

    {"lesson": "Біологія", "room": "14", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Українська мова", "room": "31", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Українська література", "room": "31", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Фізіка", "room": "26", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Інформатика/Англіська мова", "room": "6/17", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10а"},

    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},
    {"lesson": "Фізкультура", "room": "спорт зал", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},
    {"lesson": "Алгебра", "room": "15", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},
    {"lesson": "Геометрія", "room": "15", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10а"},

    # 10 Б класс
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Громад освіта", "room": "27", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Громад освіта", "room": "27", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Фізкультура", "room": "", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Інформатика/Англіська мова", "room": "7/21", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("15:00", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 0, "class": "10б"},

    {"lesson": "Українська мова", "room": "32", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Українська мова", "room": "32", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Історія Українськааїни", "room": "25", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Математика", "room": "15", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Математика", "room": "15", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Технології", "room": "4/1", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},
    {"lesson": "Фізкультура", "room": "", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 1, "class": "10б"},

    {"lesson": "Українська література", "room": "32", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Українська література", "room": "32", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Інформатика/Англіська мова", "room": "7/21", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Фізкультура", "room": "", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Математика", "room": "15", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Зарубіжна літератураіжна література", "room": "20", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Хімія", "room": "14", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 2, "class": "10б"},

    {"lesson": "Англіська мова", "room": "17", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("08:25", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Англіська мова", "room": "17", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Інформатика", "room": "7", "time": (datetime.strptime("09:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Біологія", "room": "14", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Біологія", "room": "14", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 3, "class": "10б"},

    {"lesson": "Географія", "room": "24", "time": (datetime.strptime("10:10", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
    {"lesson": "Історія", "room": "25", "time": (datetime.strptime("11:05", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
    {"lesson": "Фізика", "room": "26", "time": (datetime.strptime("11:50", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
    {"lesson": "Фізкультура", "room": "", "time": (datetime.strptime("12:35", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
    {"lesson": "Математика", "room": "15", "time": (datetime.strptime("13:30", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
    {"lesson": "Математика", "room": "15", "time": (datetime.strptime("14:15", "%H:%M") - timedelta(hours=3)).strftime("%H:%M"), "day": 4, "class": "10б"},
]

db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

cursor = db.cursor()

last_sent = {}

async def send_scheduled_messages(bot) -> None:
    while True:
        try:
            now = datetime.now()
            current_day = now.weekday()

            cursor.execute("SELECT user_id, user_name, class FROM users")
            users = cursor.fetchall()

            user_data = {user_name: (user_id, user_class) for user_id, user_name, user_class in users}

            for item in schedule:
                if "time" not in item:
                    print(f"Отсутствует ключ 'time' в элементе: {item}")

                if item["day"] != current_day:
                    continue

                lesson_time = datetime.strptime(item["time"], "%H:%M").time()
                lesson_datetime = datetime.combine(now.date(), lesson_time)

                if lesson_datetime < now:
                    lesson_datetime += timedelta(days=1)

                if lesson_datetime - now < timedelta(minutes=1):
                    message = f"Следующий урок {item['lesson']}\nВ кабинете {item['room']}"
                    for user_name, (user_id, user_class) in user_data.items():
                        last_time = last_sent.get(user_name, None)
                        if last_time is None or now - last_time > timedelta(minutes=1):
                            if user_class == item["class"]:
                                try:
                                    await bot.send_message(chat_id=user_id, text=message)
                                    last_sent[user_name] = now
                                except Exception as e:
                                    if 'Forbidden: bot was blocked by the user' in str(e):
                                        # Удаляем пользователя из базы данных, если он заблокировал бота
                                        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                                        db.commit()  # Фиксируем изменения
                                        print(f"Пользователь {user_name} заблокировал бота. Пользователь удален из базы данных.")
                                    else:
                                        print(f"Ошибка при отправке сообщения пользователю {user_name} класса {user_class}: {e}")

            await asyncio.sleep(10)
        except Exception as e:
            print(f"Ошибка при отправке сообщений: {e}")
            sys.exit(1)


async def get_user_class(user_name):
    try:
        cursor.execute("SELECT class FROM users WHERE user_name = %s", (user_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
    except Exception as e:
        print(f"Ошибка при получении класса пользователя: {e}")
    return None

async def get_user_id(user_name):
    try:
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
    except Exception as e:
        print(f"Ошибка при получении ID пользователя: {e}")
    return None

async def start(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username or str(user_id)
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, class) VALUES (%s, %s, %s)", (user_id, user_name, '10а'))
        db.commit()
        await context.bot.send_message(chat_id=user_id, text="Привет! Я буду напоминать вам о следующих уроках.\nПосмотреть команды можно используя /help\n Настоятельно рекомендуем почитать инструкцию через /instruction перед использыванием, тут вам ракажут ваши дальнейшие действия и что не надо делать")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

async def stop(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username or str(user_id)
        cursor.execute("DELETE FROM users WHERE user_name = %s", (user_name,))
        db.commit()
        await context.bot.send_message(chat_id=user_id, text="Вы больше не будете получать сообщения.")
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")

async def current(update: Update, context: CallbackContext) -> None:
    try:
        user_name = update.message.from_user.username or str(update.message.from_user.id)
        user_class = await get_user_class(user_name)
        now = datetime.now()
        current_day = now.weekday()

        current_lesson = None
        for item in schedule:
            if item["class"] == user_class:
                lesson_time = datetime.strptime(item["time"], "%H:%M").time()
                lesson_datetime = datetime.combine(now.date(), lesson_time)

                if item["day"] == current_day and lesson_datetime <= now:
                    current_lesson = item

        if current_lesson:
            message = f"Текущий урок: {current_lesson['lesson']}\nКабинет: {current_lesson['room']}"
        else:
            message = "Сейчас нет активного урока."

        user_id = await get_user_id(user_name)
        if user_id:
            await context.bot.send_message(chat_id=user_id, text=message)
        else:
            print(f"Ошибка: Не удалось найти ID для пользователя {user_name}")
    except Exception as e:
        print(f"Ошибка при отправке текущего урока: {e}")

async def next_lesson(update: Update, context: CallbackContext) -> None:
    try:
        user_name = update.message.from_user.username or str(update.message.from_user.id)
        user_class = await get_user_class(user_name)
        now = datetime.now()
        current_day = now.weekday()

        next_lesson = None
        for item in schedule:
            if item["class"] == user_class:
                lesson_time = datetime.strptime(item["time"], "%H:%M").time()
                lesson_datetime = datetime.combine(now.date(), lesson_time)

                if item["day"] == current_day and lesson_datetime > now:
                    next_lesson = item
                    break

        if next_lesson:
            message = f"Следующий урок: {next_lesson['lesson']}\nКабинет: {next_lesson['room']}"
        else:
            message = "Сегодня больше уроков нет."

        user_id = await get_user_id(user_name)
        if user_id:
            await context.bot.send_message(chat_id=user_id, text=message)
        else:
            print(f"Ошибка: Не удалось найти ID для пользователя {user_name}")
    except Exception as e:
        print(f"Ошибка при отправке следующего урока: {e}")

async def set_class(update: Update, context: CallbackContext) -> None:
    try:
        user_name = update.message.from_user.username or str(update.message.from_user.id)
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, укажите новый класс. Пример: /setclass 11б")
            return

        new_class = ' '.join(context.args)

        cursor.execute("UPDATE users SET class = %s WHERE user_name = %s", (new_class, user_name))
        db.commit()

        if cursor.rowcount == 0:
            await context.bot.send_message(chat_id=update.message.chat_id, text="Не удалось найти вашего пользователя в базе данных.")
        else:
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Ваш класс был обновлён на {new_class}.")
    except Exception as e:
        print(f"Ошибка при обновлении класса: {e}")

async def t_help(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        # Получаем аргументы команды
        args = context.args

        if len(args) == 0:
            # Общий случай: выводим список команд
            message = (
                "Команды:\n"
                "Включение и выключение:\n"
                "/start: включить уведомление об уроках\n"
                "/stop: выключить уведомление об уроках\n"
                "Вспомогательные:\n"
                "/current: выводит текущий урок\n"
                "/next: выводит следующий урок\n"
                "/setclass [CLASS_NAME]: меняет ваше расписание\n"
                "Помощь и новости:\n"
                "/help: получить это сообщение\n"
                "/help [COMMAND]: подробно расскажет, что делает та или иная команда\n"
                "/bug: раскажет как получить помощь и сообщить об ошибке\n"
                "/about: получить информацию о приложении\n"
                "/instruction: выведет инструкцию к боту\n"
                "/licenses: выведет лицензию, под которой распространяется бот\n"
                "/news: выведет последнюю новость о боте или предупреждение об отключении\n"
                "Технические:\n"
                "/donnate: усли вы хотите задонатить то вам сюда\n" +
                "/git: выводит ссылку на репозиторий проекта"
            )
        elif len(args) == 1:
            # Специфический случай: выводим информацию о конкретной команде
            command = args[0]
            help_text = {
                "start": "/start: включить уведомление об уроках. Вас добавять в базу данных пользывателей где будут хранитсья ваши user_id и user_name. Что бы перкратить действие команды напишите /stop",
                "stop": "/stop: выключить уведомление об уроках. Вас удлят из базы данных пользывателей где хранились ваши user_id и user_name. Что бы пснова получать уведомления напишите /start",
                "current": "/current: выводит текущий урок. От вас возьмётсья ваш user_name и по нему найдётсья ваш класс и выведитсья текущий урок если он есть, если уроков не было вам об этом сообщитсья что нет текущего урока",
                "next": "/next: выводит следующий урок. От вас возьмётсья ваш user_name и по нему найдётсья ваш класс и выведитсья следуйщий урок если он есть, если урока не будет вам об этом сообщитсья что нет слудуйщего урока",
                "setclass": "/setclass [CLASS_NAME]: меняет ваше расписание. Класс должен быть написан рускими буква, как пример \"10б\", постарайтесь тут не совершать ошибок.Также возможно получение ошибки, елси это так то попробуйте написать /start а после и/stop, если ничего не получилось то напишите /bug и вам напишут дальнейшие действия",
                "bug": "/bug: раскажет как получить помощь и сообщить об ошибке. Вы напишите сообщение главному разработчику и он вам всё обяснит\n",
                "about": "/about: получить информацию о приложении. Выведет под какой лицензией приложение, кто главный програмист, и цель програмы",
                "instruction": "/instruction: выведет инструкцию к боту, также тут написано как справлятсья с неполадками и что не надо делать",
                "licenses": "/licenses: выведет лицензию, под которой распространяется бот",
                "news": "/news: выведет последнюю новость о боте или предупреждение об отключении. Рекомендуем проверять новости что бы быть в курсе о проблемах или достижениях",
                "dannate": "/donnate: усли вы хотите задонатить то вам сюда",
                "git": "/git: выводит ссылку на репозиторий проекта",
            }
            message = help_text.get(command, "Неизвестная команда. Используйте /help для получения списка доступных команд.")
        else:
            # Если аргументов больше одного, выдаем ошибку
            message = "Используйте /help или /help [COMMAND] для получения справки."

        await context.bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке команды помощи: {e}")

async def bug(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text=("Если вы обнаружили ошибку или у вас что то не получаетсья то напишите @MatviiJarosh"))
    except Exception as e:
        print(f"Ошибка при отправке дейтсивй при ошибке: {e}")

async def about(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text=("Лицензия: GNU GPL v3\n" +
            "Главный разработчик: Matvii Jarosh\n" +
            "Это приложение создано чтобы помочь правильно и вовремя приходить на уроки"))
    except Exception as e:
        print(f"Ошибка при отправке информации о лицензии: {e}")

async def instruction(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text=("Начнём с предупреждения, ЕСЛИ ВАМ НЕ НУЖЕН БОТ НЕ НАДО ЕГО БЛОКИРЫВАТЬ, напишите /stop а после блокируйте\n" +
            "Что бы начать работу надо написать /start, а после написать /setclass [ВАШ КЛАСС], по типу /setclass 10а, изначально стоит 10а класс по исторической причине\n" +
            "Если у вас вышла какето ошибка то скорее всего она исправляетсья при написании /stop, а после /start \n" +
            "Если вам бот не ответил на сообщение то вы продублируйте его"))
    except Exception as e:
        print(f"Ошибка при отправке инструкции: {e}")

async def licenses(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        license_text = (
            "GNU GENERAL PUBLIC LICENSE\n"
            "Version 3, 29 June 2007\n\n"
            "Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org>\n"
            "Everyone is permitted to copy and distribute verbatim copies\n"
            "of this license document, but changing it is not allowed.\n\n"
            "Preamble\n\n"
            "The GNU General Public License is a free, copyleft license for\n"
            "software and other kinds of works. The licenses for most software\n"
            "and other practical works are designed to take away your freedom to\n"
            "share and change the works. By contrast, the GNU General Public\n"
            "License is intended to guarantee your freedom to share and change\n"
            "all versions of a program--to make sure it remains free software for\n"
            "all its users.\n\n"
            "When we speak of free software, we are referring to freedom, not\n"
            "price. Our General Public Licenses are designed to make sure that you\n"
            "have the freedom to distribute copies of free software (and charge for\n"
            "this service if you wish), that you receive source code or can get it\n"
            "if you want it, that you can change the software or use pieces of it\n"
            "in new free programs, and that you know you can do these things.\n\n"
            "To protect your rights, we need to make restrictions that forbid anyone\n"
            "to deny you these rights or to ask you to surrender the rights. These\n"
            "restrictions translate to certain responsibilities for you if you\n"
            "distribute copies of the software, or if you modify it.\n\n"
            "For example, if you distribute copies of such a program, whether gratis\n"
            "or for a fee, you must pass on the same freedoms to the recipients that\n"
            "you received. You must make sure that everyone else also gets the source\n"
            "code or can get it if they want it. And you must show them these terms\n"
            "so they know their rights.\n\n"
            "You may not impose any further restrictions on the recipients' exercise\n"
            "of the rights granted herein. You may not use the program's name for\n"
            "promotion or any other purpose without permission.\n\n"
            "To learn more about GNU licenses, visit https://www.gnu.org/licenses/gpl-3.0.html\n"
        )
        await context.bot.send_message(chat_id=user_id, text=license_text)
    except Exception as e:
        print(f"Ошибка при отправке лицензии: {e}")

async def news(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text=("Был обновлено количество команд и улучшено взаимодействие с пользывателем"))
    except Exception as e:
        print(f"Ошибка при отправке новостей: {e}")

async def donnate(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text=("Это бесплатное приложение которые без реклам ыи с открытым исходынм кодом, если у вас доброе сердце и вы хотите что то пожертвывать то напишите @MatviiJarosh и он вам всё сообщит"))
    except Exception as e:
        print(f"Ошибка при отправке информации о том как задонатить: {e}")

async def t_git(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.from_user.id
        await context.bot.send_message(chat_id=user_id, text="https://github.com/Matvii-Jarosh/lessons_tg-bot")
    except Exception as e:
        print(f"Ошибка при отправке сылки на git: {e}")

def main() -> None:
    try:
        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("stop", stop))

        application.add_handler(CommandHandler("current", current))
        application.add_handler(CommandHandler("next", next_lesson))
        application.add_handler(CommandHandler("setclass", set_class))

        application.add_handler(CommandHandler("help", t_help))
        application.add_handler(CommandHandler("bug", bug))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("instruction", instruction))
        application.add_handler(CommandHandler("licenses", licenses))
        application.add_handler(CommandHandler("news", news))

        application.add_handler(CommandHandler("git", t_git));
        application.add_handler(CommandHandler("donnate", donnate));

        loop = asyncio.get_event_loop()
        loop.create_task(send_scheduled_messages(application.bot))

        application.run_polling()
    except Exception as e:
        print(f"Фатальная ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
