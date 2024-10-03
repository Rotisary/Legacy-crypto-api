import requests


def get_currency_price(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'X-CMC_PRO_API_KEY': '1a6662b6-b353-4e4c-8ee7-5e0f4070b27f'
    }
    query_params = {
        'symbol': symbol,
        'convert': 'USD'  # Convert the price to USD
    }
    price_response = requests.get(url, params=query_params, headers=headers)
    if price_response.status_code != 200:
        return price_response.text
    else:
        coin_name = price_response.json()['data'][symbol]['name']
        coin_symbol = price_response.json()['data'][symbol]['symbol']
        coin_price = price_response.json()['data'][symbol]['quote']['USD']['price']
        return coin_name, coin_symbol, coin_price