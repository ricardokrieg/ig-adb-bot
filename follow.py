import logging
import sys
from ppadb.client import Client as AdbClient

from src.Bot import Bot
from src.Device import Device
from src.Dizu import Dizu, TaskRequest


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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

    logging.debug(f'Connecting to device "{deviceAddress}"')
    adb_device = find_device(devices, deviceAddress)
    logging.info(f'Connected to {adb_device.serial}')

    device = Device(adb_device)
    bot = Bot(device)

    account_id = '48117313086'
    dizu = Dizu()

    for i in range(10):
        logging.info(f'Follow #{i + 1}')
        task_request = TaskRequest(account_id=account_id, state='RJ')

        logging.info(f'Getting Dizu task {task_request}')
        task = None
        while not task:
            try:
                task = dizu.get_task(TaskRequest(account_id=account_id, state='SP'))
                break
            except ValueError as err:
                logging.info(err)
        logging.info(task)

        bot.follow(task.username)

        logging.info(f'Submitting Dizu task {task}')
        dizu.submit_task(task)
