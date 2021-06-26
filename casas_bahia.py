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

MESSAGE_COUNT = 20


def find_device(devices, serial):
    for device in devices:
        if device.serial == serial:
            return device

    return None

def get_messages(profile):
    #name = profile['full_name'].split(' ')[0].capitalize()
    link = 'https://bit.ly/3wW0ETi'

    spintax_message1 = "O que {vc|você} acharia de ganhar um {celular|iphone} {novinho|novinho em folha} em troca de 2 {minutos|minutinhos} do seu tempo? 😱\n" \
                       "Seria {da hora|ótimo}, não {é mesmo|seria}?\n\n" \
                       "{O time Casas Bahia está|Nós do time Casas Bahia estamos} realizando uma pesquisa de satisfação.\n" \
                       "Todos {os participantes|que participarem} concorrem a 100 iPhones 📱\n\n" \
                       "Acessa esse link para participar 👇\n\n" \
                       "%s" % (link,)
    message1 = spintax.spin(spintax_message1)

    #spintax_message2 = "%s, {estamos contando|contamos} com {vc|você} 😊" % (name,)
    spintax_message2 = "{Estamos contando|Contamos} com {vc|você} 😊"
    message2 = spintax.spin(spintax_message2)

    return message1, message2

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
