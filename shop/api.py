import requests
from decimal import Decimal

def get_usd_currency():
    url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
    response = requests.get(url)
    res = response.json()   
    USD = [item['Rate'] for item in res if item['Ccy']=='USD']

    USD = Decimal(USD[0].replace(',','.'))
    return USD 

def get_eur_currency():
    url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
    response = requests.get(url)
    res = response.json()   
    EUR = [item['Rate'] for item in res if item['Ccy']=='EUR']

    EUR = Decimal(EUR[0].replace(',','.'))
    
    return EUR 


def get_currency(currency, obj_price):
    if currency=='uzs':
        kurs = get_usd_currency()
        price = round(obj_price * kurs, 2)
    elif currency=='eur':
        usd = get_usd_currency()
        eur = get_eur_currency()
        price = round(obj_price * usd / eur, 2)
    elif currency=='usd':
        price = obj_price
    return price
