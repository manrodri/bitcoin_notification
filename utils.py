from requests import Request, Session, post
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


def get_bitcoin_price():
    bitcoin_symbol = 'BTC'

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '5161f97a-b40e-46d8-846d-ea3bf7838988',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return round(float(data['data'][0]['quote']['USD']['price']),2)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def post_ifttt_webhook(event_name: str, value: dict):
    '''

    :param event: itfff event name
    :param value: payload to send to itfff wehbhook url
    :return: None
    '''
    webhook_url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/pvuacfh4ZywS0t_50U0Pw7ZNyq2b1GFgigwZ1Vhl8l7'
    post(webhook_url, json=value)


get_bitcoin_price()