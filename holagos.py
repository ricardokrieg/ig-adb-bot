import logging
import sys
from ppadb.client import Client as AdbClient
import boto3
import spintax

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


def get_messages(profile):
    name = profile['full_name'].split(' ')[0].capitalize()

    spintax_message1 = "{Oi|Olá}, %s.\n\nPara {comemorar|celebrar} o aniversário do Hospital do Olho Lagos, " \
                       "nós estamos sorteando {vários brindes|brindes} para nossos seguidores e você pode participar dos sorteios. " \
                       "São {diversos|vários} brindes incluindo {vale-compras|consultas grátis} e até iPhones!\n\n" \
                       "Para participar, é só enviar uma mensagem para esse perfil 👇\n\n@ho.lagos.aniversario\n\nBoa Sorte! 😊" % (name,)
    message1 = spintax.spin(spintax_message1)

    return message1,


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

    bot.dm(queue, MESSAGE_COUNT, get_messages)
