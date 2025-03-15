import json

import loguru
import requests
from django.conf import settings
from requests import Response


class TelegramService:
    def __init__(
            self,
            bot_token: str = settings.BOT_TOKEN,
            api_url: str = settings.TELEGRAM_API_URL
    ):
        self.__bot_token = bot_token
        self.api_url = api_url
        self.__bot_api_url = f'{self.api_url}/bot{self.__bot_token}'

    def send_message(
            self,
            chat_id: int,
            text: str,
            reply_markup: dict[str, list] | None = None,
            parse_mode: str = 'HTML',
    ) -> Response:
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
        }

        if reply_markup:
            payload['reply_markup'] = json.dumps(reply_markup)

        response = requests.post(
            url=f'{self.__bot_api_url}/sendMessage',
            json=payload,
        )

        return response

    def send_file(
            self,
            chat_id: str,
            file_path: str,
            file_type: str,
            method: str,
            caption: str = ''
    ) -> Response:

        url = f'{self.__bot_api_url}/{method}'

        with open(file_path, 'rb') as file:
            files = {file_type: file}
            data = {
                'chat_id': chat_id,
                'caption': caption
            }
            response = requests.post(url, files=files, data=data)

        return response


telegram_service = TelegramService()