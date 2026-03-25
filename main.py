import os
from flask import Flask, request, jsonify
import logging
from waitress import serve

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
sessionStorage = {}


@app.route('/', methods=['GET'])
def health_check():
    return "OK"


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Получен запрос: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Отправлен ответ: {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!"
            ],
            'animal': 'слона',
            'game_round': 1
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    user_text = req['request']['original_utterance'].lower().strip()
    animal = sessionStorage[user_id]['animal']
    if 'куплю' in user_text or 'покупаю' in user_text or any(word in user_text for word in ['ладно', 'хорошо', 'да']):
        if animal == 'слона':
            sessionStorage[user_id]['animal'] = 'кролика'
            sessionStorage[user_id]['suggests'] = [
                "Не хочу.",
                "Не буду.",
                "Отстань!"
            ]
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете! А теперь купи кролика!'
            res['response']['buttons'] = get_suggests(user_id)
        else:
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['end_session'] = True
        return
    res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи {animal}!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })
    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    serve(app, host='0.0.0.0', port=port)