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


def get_currency(obj_price):
    usd_kurs = get_usd_currency()
    eur_kurs = get_eur_currency()

    price = {}
    price['usd'] = obj_price
    price['uzs'] = round(obj_price * usd_kurs, -3)
    price['eur'] = round(obj_price * usd_kurs / eur_kurs, 2)

    return price


# from PIL import Image, ImageDraw

# def image():
#     original_image = Image.open('static/img/imodels.jpg')

#     # Create a circular mask
#     mask = Image.new('L', original_image.size, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((0, 0, original_image.width, original_image.height), fill=255)

#     # Apply the circular mask to the image
#     round_image = Image.new('RGBA', original_image.size)
#     round_image.paste(original_image, mask=mask)

#     # Save the round image
#     round_image.save('static/img/imodels.png')



# if __name__=="__main__":
    