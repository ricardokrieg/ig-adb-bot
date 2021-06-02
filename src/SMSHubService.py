import requests
import logging
import re
from dataclasses import dataclass
import time


@dataclass
class PhoneNumber:
    id: str
    number: str


class SMSHubService:
    def __init__(self):
        self.api_key = '52283U8c6238866021a16f14ac13f7da8ec3d9'

    def get_balance(self):
        url = f'https://smshub.org/stubs/handler_api.php?api_key={self.api_key}&action=getBalance'
        response = requests.get(url)

        logging.debug(response.text)

        match = re.match(r'ACCESS_BALANCE:(.*)', response.text)

        return float(match.groups()[0])

    def get_number(self):
        url = f'https://smshub.org/stubs/handler_api.php?api_key={self.api_key}&action=getNumber&service=ig&country=russia'
        response = requests.get(url)

        logging.debug(response.text)

        match = re.match(r'ACCESS_NUMBER:(\d+):(\d+)', response.text)

        return PhoneNumber(id=match.groups()[0], number=match.groups()[1])

    def get_status(self, phone_number):
        url = f'https://smshub.org/stubs/handler_api.php?api_key={self.api_key}&action=getStatus&id={phone_number.id}'
        response = requests.get(url)

        logging.debug(response.text)

        return response.text

    def wait_for_code(self, phone_number):
        tries = 10
        while tries > 0:
            status = self.get_status(phone_number)
            logging.debug(status)

            match = re.match(r'STATUS_OK:(\d+)', status)

            if match:
                return match.groups()[0]

            time.sleep(30)
            tries -= 1

        return None

    def set_status(self, phone_number, status):
        url = f'https://smshub.org/stubs/handler_api.php?api_key={self.api_key}&action=setStatus&status={status}&id={phone_number.id}'
        response = requests.get(url)

        logging.debug(response.text)

        return response.text

    def set_status_ready(self, phone_number):
        return self.set_status(phone_number, '1')

    def set_status_done(self, phone_number):
        return self.set_status(phone_number, '6')

    def set_status_cancel(self, phone_number):
        return self.set_status(phone_number, '8')