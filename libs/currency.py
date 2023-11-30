import json
import requests
from decimal import Decimal
from datetime import datetime

# def get_usd_currency():
#     url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
#     response = requests.get(url)
#     res = response.json()   
#     USD = [item['Rate'] for item in res if item['Ccy']=='USD']
#     EUR = [item['Rate'] for item in res if item['Ccy']=='EUR']

#     USD = Decimal(USD[0].replace(',','.'))
#     EUR = Decimal(EUR[0].replace(',','.'))

#     return {
#         'usd': USD,
#         'eur': EUR
#     }


# def get_eur_currency():
#     url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
#     response = requests.get(url)
#     res = response.json()   
#     EUR = [item['Rate'] for item in res if item['Ccy']=='EUR']

#     EUR = Decimal(EUR[0].replace(',','.'))
    
#     return EUR 


def get_currency(obj_price):
    # usd_kurs = get_usd_currency()
    # eur_kurs = get_eur_currency()

    # usd_kurs = curreny['usd']
    # eur_kurs = curreny['eur']

        with open('libs/curency.json') as f:
                data = json.load(f)
                total_seconds = int((datetime.now() - datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")).total_seconds())
                if total_seconds <= 86400:
                        USD = Decimal(data['usd'].replace(',','.'))
                        EUR = Decimal(data['usd'].replace(',','.'))
                else:
                        url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
                        response = requests.get(url)
                        res = response.json()   

                        USD = [item['Rate'] for item in res if item['Ccy']=='USD']
                        EUR = [item['Rate'] for item in res if item['Ccy']=='EUR']

                        USD = Decimal(USD[0].replace(',','.'))
                        EUR = Decimal(EUR[0].replace(',','.'))

        
                        with open('libs/curency.json', 'w', encoding='utf-8') as f:
                                json.dump({
                                        "usd": str(USD),
                                        "eur": str(EUR),
                                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }, f, ensure_ascii=False, indent=4)
        
        price = {}
        price['usd'] = obj_price
        price['uzs'] = round(obj_price * USD, -3)
        price['eur'] = round(obj_price * USD / EUR, 2)

        return price
