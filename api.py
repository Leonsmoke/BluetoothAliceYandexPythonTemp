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
        'влажность в комнате',
        'какая влажность в комнате',
        'скажи влажность в комнате',
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
        res['response']['text'] = 'В вашей комнате сейчас '+ str(vlazh) + ' процентов влажности.'
        return

    if req['request']['original_utterance'].lower() in [
        'заряд у датчиков',
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
        'полный отчёт',
        'состояние комнаты',
        'микроклимат',
    ]:
        # Пользователь согласился, прощаемся .
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

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'А Костя всё равно негодяй!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
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