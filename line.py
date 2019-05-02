"""LINEへのアクセス関数群."""
import logging

import requests


def notify(token, message):
    """LINE Notifyでメッセージを送る."""
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.post('https://notify-api.line.me/api/notify',
                        data=payload, headers=headers)
    logging.info('LINE Notify response status code: %d', res.status_code)
    logging.info('LINE Notify response: %s', res.text)
