import telebot

from django.urls import reverse
from django.conf import settings

from telebot.util import quick_markup

from libs.sms import client

bot = telebot.TeleBot(settings.MYSERVICE.get('telebot').get('token'))


def return_markup(id, request):
    admin_url = reverse('admin:index')
    full_admin_url = request.build_absolute_uri(admin_url)
    return quick_markup({
        f'Buyurtma: #{id}': {'url': f'{full_admin_url}shop/order/{id}/change/'},
    })

#💳 Метод оплата: Наличными при получении
#📅 Дата: {order.created_at.strftime("%d.%m.%Y, %H:%M")}

#settings.MYSERVICE.get('telebot').get('chat_id').get('chat_id_orders')


def send_message(type=None, **kwargs):
    if type == "order":
        order = kwargs.get('order')
        request = kwargs.get('request')

        basket = ""
        pk = 1

        for product in order.order_products.all():
            if len(product.product_name) > 20:
                name = product.product_name[:20] + "..."
            else:
                name = product.product_name
            basket += f"{pk}. {name} ✖️ {product.quantity}dona\n💵{product.subtotal:,.2f}\n"
            pk += 1

        if order.status == "Kutish":
            order_status = "🟡 " + order.status
        elif order.status == "To'langan":
            order_status = "🟢 " + order.status
        elif order.status == "Rad etilgan":
            order_status = "🔴 " + order.status

        telegram_message = f"""
📩 Yangi buyurtma❗️\n
📄 ID: #{order.pk}
💸 Status: {order_status}
-----------------------
👤 Mijoz:  {order.customer.first_name} {order.customer.last_name}
📞 Raqam: <code>+{order.customer.phone}</code>
-----------------------
{basket}-----------------------
💰 Jami: {order.total_price:,.2f} UZS
"""
        
        sms_message = f"""📄 Buyurtma: #{order.pk}
💸 Status:\n{order_status}
-----------------------
{basket}-----------------------
💰 Jami: {order.total_price:,.2f} UZS"""
        
        chat_id = settings.MYSERVICE.get('telebot').get('chat_id').get('chat_id_orders')

        try:
            bot.send_message(chat_id=chat_id, text=telegram_message, reply_markup=return_markup(id=order.pk, request=request), parse_mode="HTML")
            if settings.DEBUG==False:
                client._send_sms(
                    phone_number=order.customer.phone,
                    message=sms_message)
        except:
            pass
    
    elif type == "auth":
        try:
            bot.send_message(chat_id=chat_id, text=kwargs.get('text'), parse_mode="HTML")
        except:
            pass
    
    elif type == "contact":
        obj = kwargs.get('obj')
        
        telegram_message = f"""
📩 Yangi murojaat❗️\n
👤 Mijoz:  {obj.name}
📧 Email: {obj.email}
📞 Raqam: <code>+{obj.phone}</code>
📄 Xabar:  <code>{obj.message}</code>
"""
        chat_id = settings.MYSERVICE.get('telebot').get('chat_id').get('chat_id_warnings')

        try:
            bot.send_message(chat_id=chat_id, text=telegram_message, parse_mode="HTML")
        except:
            pass









# class TeleBotClient:
#     PASE_MODE = "html"
#     SEND_MESSAGE = "/sendMessage"
    
#     TYPE_ORDERS = "chat_id_orders"
#     TYPE_WARNINGS = "chat_id_warnings"
    

#     def __init__(self, base_url: str, token: str, chat_id: str) -> None:
#         self.token = token
#         self.chat_id = chat_id
#         self.base_url = base_url
#         self.main_url = f'{self.base_url}{self.token}'


#     def send_message(self, text: str, type: str) -> dict:
#         if type == self.TYPE_ORDERS:
#             chat_id: str = self.chat_id.get(self.TYPE_ORDERS)
            
#         if type == self.TYPE_WARNINGS:
#             chat_id: str = self.chat_id.get(self.TYPE_WARNINGS)
        
#         params = {
#             'text': text,
#             'chat_id': chat_id,
#             'parse_mode': self.PASE_MODE
#         }
        
#         return requests.post(f'{self.main_url}{self.SEND_MESSAGE}', params)
    
#     def send_order_message(self, order):
        
#         basket = ""

#         for product in order.order_products.all():
#             if len(product.product_name) > 37:
#                 name = product.product_name[:37] + "..."
#             else:
#                 name = product.product_name
            
#             basket += f"{name} ✖️ {product.quantity}\n"

#         text = f"""
# 📄 Заказ: #{order.pk}
# 📅 Дата: {order.created_at}
# 💳 Метод оплата: Наличными при получении
# 💸 Финансовый статус: {order.status}
# 🚛 Тип доставка: Deliver
# -----------------------
# 👤 Клиент: Jobir
# 📞 Номер телефона: 998900426898
# -----------------------
# {basket}
# -----------------------
# Итого: {order.total_price} som
# """
#         print(text)

#         params = {
#             'text': text,
#             'chat_id': self.chat_id.get(self.TYPE_ORDERS),
#             'parse_mode': self.PASE_MODE
#         }
        
#         return requests.post(f'{self.main_url}{self.SEND_MESSAGE}', params)


# telebot = TeleBotClient(
#     **settings.MYSERVICE.get('telebot')
# )


# import requests

# class TelegramBot:
#     def __init__(self, token):
#         self.token = token
#         self.base_url = f"https://api.telegram.org/bot{token}"

#     def send_message(self, chat_id, text):
#         method = "sendMessage"
#         url = f"{self.base_url}/{method}"
#         data = {
#             "chat_id": chat_id,
#             "text": text,
#         }

#         try:
#             response = requests.post(url, json=data)
#             if response.status_code == 200:
#                 print("Message sent successfully.")
#             else:
#                 print("Failed to send message.")
#         except Exception as e:
#             print(f"Error sending message: {e}")

# if __name__ == "__main__":
#     # Replace 'YOUR_BOT_TOKEN' with your actual bot token
#     bot = TelegramBot('6346162578:AAE347B4sBORRiErxrPxqHRWDHEyxERsDSI')

#     # Replace 'CHAT_ID' with the chat ID of the user or group you want to send the message to
#     chat_id = '5738824208'

#     message_text = "Hello, this is your Telegram bot!"

#     bot.send_message(chat_id, message_text)