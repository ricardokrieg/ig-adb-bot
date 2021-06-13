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
    name = profile['full_name']
    tagger_name = profile['tagger_name']
    link = profile['link']

    spintax_message1 = "{Hi|Hey}, %s. How are you?\n%s tagged you in one of our giveaways and {you won|you just won} " \
                       "{a brand new iphone|an iphone}! What a luck!" %(name, tagger_name)
    message1 = spintax.spin(spintax_message1)

    spintax_message2 = "{Now you need to access this site and claim|Access this site to claim} your prize.\nHurry, " \
                       "because if you don't claim it in the next hours we will give it to another participant\n"
    message2 = spintax.spin(spintax_message2)

    message3 = link

    return message1, message2, message3

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
