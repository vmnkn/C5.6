import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Failed to process currency: {quote}')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Failed to process currency: {base}')

        if quote_ticker == base_ticker:
            raise APIException('Unable to convert identical currencies')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process quantity: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        final = round(total_base * float(amount), 3)

        return final

