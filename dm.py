import logging
import sys
from ppadb.client import Client as AdbClient
import boto3

from src.Bot import Bot
from src.Device import Device


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
sqs = boto3.resource(
    'sqs',
    aws_access_key_id='AKIAS3T76JZKRWI5XQX3',
    aws_secret_access_key='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',
    region_name='us-east-1',
)

HOST = "127.0.0.1"
PORT = 5037

MESSAGE_COUNT = 15


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
    queue = sqs.get_queue_by_name(QueueName=sys.argv[2])

    logging.debug(f'Connecting to device "{deviceAddress}"')
    adb_device = find_device(devices, deviceAddress)
    logging.info(f'Connected to {adb_device.serial}')

    device = Device(adb_device)

    bot = Bot(device)

    spintax_message = '{Oi|Oii|Oie}. Tem {várias fotos|um monte de fotos} de gatinhas nesse perfil @lindasbrasileiras20. {E de vez em quando a gente posta nudes nos stories|A gente posta nudes nos stories de vez {em quando|em quando também}| A gente também posta nudes nos stories} {🍑|🔞|🔥}. {Segue a gente lá|Segue a gente|Vai lá dar uma olhada} {😘|💋|😗|😙|😚}'

    bot.dm(queue, MESSAGE_COUNT, spintax_message)
