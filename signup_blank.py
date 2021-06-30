import logging
import sys
from ppadb.client import Client as AdbClient
import boto3
import random
from datetime import date

from src.Bot import Bot
from src.Device import Device
from src.SMSHubService import SMSHubService

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAS3T76JZKRWI5XQX3',
    aws_secret_access_key='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',
    region_name='us-east-1',
)

HOST = "127.0.0.1"
PORT = 5037


def find_device(devices, serial):
    for device in devices:
        if device.serial == serial:
            return device

    return None
    
def callback(username, password, phone_number, email, email_password, name):
    logging.info(f'Account Summary')
    logging.info(f'username: {username}')
    logging.info(f'password: {password}')
    logging.info(f'phone_number: {phone_number}')
    logging.info(f'email: {email}')
    logging.info(f'email_password: {email_password}')
    logging.info(f'name: {name}')
    
    table = dynamodb.Table('ACCOUNTS')
    return table.put_item(
       Item={
            'username': username,
            'password': password,
            'phone_number': phone_number,
            'email': email,
            'email_password': email_password,
            'name': name,
            'registered_at': date.today().strftime("%Y-%m-%d"),
        }
    )

def get_account_name():
    adjs = [
        "autumn", "hidden", "bitter", "misty", "silent", "empty", "dry", "dark",
        "summer", "icy", "delicate", "quiet", "white", "cool", "spring", "winter",
        "patient", "twilight", "dawn", "crimson", "wispy", "weathered", "blue",
        "billowing", "broken", "cold", "damp", "falling", "frosty", "green",
        "long", "late", "lingering", "bold", "little", "morning", "muddy", "old",
        "red", "rough", "still", "small", "sparkling", "throbbing", "shy",
        "wandering", "withered", "wild", "black", "young", "holy", "solitary",
        "fragrant", "aged", "snowy", "proud", "floral", "restless", "divine",
        "polished", "ancient", "purple", "lively", "nameless"
    ]
    nouns = [
        "waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning",
        "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter",
        "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook",
        "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly",
        "feather", "grass", "haze", "mountain", "night", "pond", "darkness",
        "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder",
        "violet", "water", "wildflower", "wave", "water", "resonance", "sun",
        "wood", "dream", "cherry", "tree", "fog", "frost", "voice", "paper",
        "frog", "smoke", "star"
    ]
    
    sample_adjs = random.sample(adjs, 2)
    sample_noun = random.choice(nouns).capitalize()
    
    return ' '.join([sample_adjs[0].capitalize(), sample_adjs[1].capitalize(), sample_noun])


if __name__ == '__main__':
    client = AdbClient(host=HOST, port=PORT)

    devices = client.devices()

    if len(devices) == 0:
        logging.error('No devices')
        quit()

    deviceAddress = sys.argv[1]
    accountName = get_account_name()

    logging.debug(f'Connecting to device "{deviceAddress}"')
    adb_device = find_device(devices, deviceAddress)
    logging.info(f'Connected to {adb_device.serial}')

    device = Device(adb_device)

    sms_service = SMSHubService()
    bot = Bot(device)
    
    try:
        bot.signup(None, get_account_name, None, None, None, sms_service, callback)
    except ValueError as error:
        bot.device.screenshot_debug()
        raise error
