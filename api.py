# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import pymysql

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "температуру",
                "влажность",
                "полный отчёт",
            ]
        }

        res['response']['text'] = 'Здравствуй! Что тебе назвать?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'температуру',
        'температура',
        'какая температура',
        'температуру в комнате',
        'какая температура в комнате',
        'температура в комнате',
    ]:
        # Пользователь согласился, прощаемся.
        con = pymysql.connect('f0469046.xsph.ru', 'f0469046_temp',
                              '2234562', 'f0469046_data')
        cur = con.cursor()
        cur.execute("SELECT * FROM data ORDER BY date DESC")
        rows = cur.fetchall()
        latest = rows[0]
        temp = latest[1]
        vlazh = latest[2]
        battery = latest[3]
        res['response']['text'] = 'В вашей комнате сейчас '+ str(temp) + ' градусов'
        return

    if req['request']['original_utterance'].lower() in [
        'влажность',
        'какая влажность',
        'влажность в комнате',
        'какая влажность в комнате',
        'скажи влажность в комнате',
    ]:
        con = pymysql.connect('f0469046.xsph.ru', 'f0469046_temp',
                              '2234562', 'f0469046_data')
        cur = con.cursor()
        cur.execute("SELECT * FROM data ORDER BY date DESC")
        rows = cur.fetchall()
        latest = rows[0]
        temp = latest[1]
        vlazh = latest[2]
        battery = latest[3]
        res['response']['text'] = 'В вашей комнате сейчас '+ str(vlazh) + ' процентов влажности.'
        return

    if req['request']['original_utterance'].lower() in [
        'заряд у датчиков',
        'зарядка датчиков',
        'зарядка у датчиков',
        'заряд датчиков',
        'заряд батареи',
        'остаток батареи',
    ]:
        # Пользователь согласился, прощаемся.
        con = pymysql.connect('f0469046.xsph.ru', 'f0469046_temp',
                              '2234562', 'f0469046_data')
        cur = con.cursor()
        cur.execute("SELECT * FROM data ORDER BY date DESC")
        rows = cur.fetchall()
        latest = rows[0]
        temp = latest[1]
        vlazh = latest[2]
        battery = latest[3]
        res['response']['text'] = 'У датчика '+ str(battery) + ' процентов заряда баттареи. '
        return

    if req['request']['original_utterance'].lower() in [
        'скажи всё',
        'расскажи всё',
        'покажи всё',
        'дай полный отчёт',
        'давай полный отчёт',
        'полный отчёт',
        'состояние комнаты',
        'микроклимат',
        'микро климат',
    ]:
        con = pymysql.connect('f0469046.xsph.ru', 'f0469046_temp',
                              '2234562', 'f0469046_data')
        cur = con.cursor()
        cur.execute("SELECT * FROM data ORDER BY date DESC")
        rows = cur.fetchall()
        latest = rows[0]
        temp = latest[1]
        vlazh = latest[2]
        battery = latest[3]
        res['response']['text'] = 'У вас в комнате '+ temp + ' градусов и ' + vlazh + ' процентов влажности. Заряд батареи ' + battery + ' процентов.'
        return

    if req['request']['original_utterance'].lower() in [
        'это нормально?',
        'это нормальное состояние?',
        'это нормальное состояние комнаты?',
        'как должно быть?',
        'а как должно быть?',
        'это комфортно?',
        'а как комфортно?',
        'мне будет нормально?',
        'это хорошо для меня?',
    ]:
        con = pymysql.connect('f0469046.xsph.ru', 'f0469046_temp',
                              '2234562', 'f0469046_data')
        cur = con.cursor()
        cur.execute("SELECT * FROM data ORDER BY date DESC")
        rows = cur.fetchall()
        latest = rows[0]
        temp = latest[1]
        vlazh = latest[2]
        battery = latest[3]
        if temp < 22:
            res['response']['text'] = 'В данный момент у вас в комнате '+ temp + ' градусов. Это низкая температура, вы можете замерзнуть. Закройте окно и укройтесь одеялом. Можете выпить горячего чая.'
        if temp > 27:
            res['response']['text'] = 'В данный момент у вас в комнате '+ temp + ' градусов. Это высокая температура. Откройте окно, выпейте водички или выйдите прогуляться.'
        if temp >= 22 & temp <= 27:
            res['response']['text'] = 'В данный момент у вас в комнате '+ temp + ' градусов. Это идеальная температура. Вы можете спокойно заниматься своими делами.'
        if vlazh < 35:
            res['response']['text'] = 'В данный момент у вас в комнате '+ vlazh + ' процентов влажности. Это очень низкая влажность. Пролей водичку на подоконник.'
        if temp > 70:
            res['response']['text'] = 'В данный момент у вас в комнате '+ vlazh + ' процентов влажности. Это высокая влажность. Наверное за окном дождь, если нет, то высуши свою комнату.'
        if temp >= 35 & temp <= 70:
            res['response']['text'] = 'В данный момент у вас в комнате '+ vlazh + ' процентов влажности. Это нормальная влажность. Вы можете спокойно заниматься своими делами.'
        return

    res['response']['text'] = 'Что-то я не расслышала'
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:3]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests