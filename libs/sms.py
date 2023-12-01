import requests
from django.conf import settings
# from eskiz.client import SMSClient
from environs import Env

env = Env()
env.read_env()

# client = SMSClient(**settings.MYSERVICE.get('sms_service'))


class SMSClient:
    def auth_token():
        url = env.str('SMS_URL') + "auth/login"

        payload = {
            'email': env.str('SMS_EMAIL'),
            'password': env.str('SMS_PASSWORD')
        }
        files=[]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        with open('libs/eskiz_auth_token.txt', 'w') as file:
            file.write(response.json()['data']['token'])

        return response.json()['data']['token']


    def _send_sms(phone: str, code: str):
        url = env.str('SMS_URL') + "message/sms/send"

        token = None
        
        with open('libs/eskiz_auth_token.txt', 'r') as file:
            for line in file:
                token = line

        if token is None:
            token = client.auth_token()

        files=[]
        headers = {'Authorization': 'Bearer ' + token}
        payload = {
            'mobile_phone': phone,
            'message': code,
            'from': '4546'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        if response.status_code == 401:
            client.auth_token()
            with open('libs/eskiz_auth_token.txt', 'r') as file:
                for line in file:
                    token = line
            headers = {'Authorization': 'Bearer ' + token}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

        return response.status_code


client = SMSClient

# if __name__=="__main__":
#     token = client.send_sms(phone=998900426898, code='111111')
#     print(token)