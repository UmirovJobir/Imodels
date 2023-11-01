import requests
from django.conf import settings


class TeleBotClient:
    PASE_MODE = "html"
    SEND_MESSAGE = "/sendMessage"
    
    TYPE_ORDERS = "chat_id_orders"
    TYPE_WARNINGS = "chat_id_warnings"
    

    def __init__(self, base_url: str, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.base_url = base_url
        self.main_url = f'{self.base_url}{self.token}'


    def send_message(self, text: str, type: str) -> dict:
        if type == self.TYPE_ORDERS:
            chat_id: str = self.chat_id.get(self.TYPE_ORDERS)
            
        if type == self.TYPE_WARNINGS:
            chat_id: str = self.chat_id.get(self.TYPE_WARNINGS)
        
        params = {
            'text': text,
            'chat_id': chat_id,
            'parse_mode': self.PASE_MODE
        }
        
        return requests.post(f'{self.main_url}{self.SEND_MESSAGE}', params)


telebot = TeleBotClient(
    **settings.MYSERVICE.get('telebot')
)


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