import requests
import time
from datetime import datetime

from utils import get_bitcoin_price, post_ifttt_webhook

BITCOIN_PRICE_THRESHOLD = 50000

def format_bitcoin_history(bitcoin_data: list):
    '''

    :param bitcoin_data:
    :return: a dictionary with the format the itff is expecting data passed as argument
    '''

    email_values = {}
    email_values['EventName'] = 'bitcoin_price_update'
    email_values['OccurredAt'] = datetime.now().strftime('%d.%m.%Y %H:%M')

    for count, value in enumerate(bitcoin_data):
        price = value['price']
        var_name = f"Value{count +1 }"
        email_values[var_name] = price
    return email_values


def main():
    bitcoin_history = []
    while True:
        price = get_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # send notification
        if price > BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', {'Value1': price})

        # Send email with updates
        # Once we have 5 items in our bitcoin_history sed and update

        if len(bitcoin_history) == 3:
            post_ifttt_webhook(
                'bitcoin_price_update',
                format_bitcoin_history(bitcoin_history)
            )

        # we don't want to make too many requests to the webhook
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()