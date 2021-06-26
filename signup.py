import logging
import sys
from ppadb.client import Client as AdbClient

from src.Bot import Bot
from src.Device import Device
from src.SMSHubService import SMSHubService

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

HOST = "127.0.0.1"
PORT = 5037


def find_device(devices, serial):
    for device in devices:
        if device.serial == serial:
            return device

    return None


if __name__ == '__main__':
    client = AdbClient(host=HOST, port=PORT)

    devices = client.devices()

    if len(devices) == 0:
        logging.error('No devices')
        quit()

    deviceAddress = sys.argv[1]
    accountName = sys.argv[2]
    password = 'xxx123xxx'
    image = sys.argv[3]
    username = sys.argv[4] if len(sys.argv) == 5 else None

    logging.debug(f'Connecting to device "{deviceAddress}"')
    adb_device = find_device(devices, deviceAddress)
    logging.info(f'Connected to {adb_device.serial}')

    device = Device(adb_device)

    sms_service = SMSHubService()
    bot = Bot(device)

    bot.signup(username, accountName, password, image, sms_service)
