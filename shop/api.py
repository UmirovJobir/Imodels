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
