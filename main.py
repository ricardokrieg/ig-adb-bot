import logging
import sys
from ppadb.client import Client as AdbClient

from Bot import Bot
from Device import Device

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
        print('No devices')
        quit()

    adb_device = find_device(devices, '192.168.56.108:5555')
    print(f'Connected to {adb_device.serial}')

    device = Device(adb_device)

    bot = Bot(device)
    # bot.signup('Gabriela Manoela', 'xxx123xxx')
    # quit()

    spintax_message = '{Oi|Oii|Oie}. Tem {várias fotos|um monte de fotos} de gatinhas nesse perfil @lindasbrasileiras20. {E de vez em quando a gente posta nudes nos stories|A gente posta nudes nos stories de vez {em quando|em quando também}| A gente também posta nudes nos stories} {🍑|🔞|🔥}. {Segue a gente lá|Segue a gente|Vai lá dar uma olhada} {😘|💋|😗|😙|😚}'
    # spintax_message = '{Oi|Oii|Oie}. Tem {varias fotos|um monte de fotos} de gatinhas nesse perfil @lindasbrasileiras20. {E de vez em quando a gente posta nudes nos stories|A gente posta nudes nos stories de vez {em quando|em quando tambem}| A gente tambem posta nudes nos stories}. {Segue a gente la|Segue a gente|Vai la dar uma olhada}'
    usernames = [
        'ewertonmayco',
        'pathernom3',
        'elielsonchavessil',
        'enriquecoutinho_',
        'belaweed',
        'prof.valadaresalan',
        'moreira7180',
        'tativasconcelos30',
        'gibson_pereira',
        'cesartutb',
        'riick.c89',
        'malluboneca',
        'debora12oliveira',
        'diogodjgospel',
        'kellytonalan07',
        'eujuniorferreira_',
        'dafson_silva_psc',
        'tayaquinoo',
        'michaelsilva313924',
        'rysa_ribeiro',
        'marciiohenriqu23',
        'elielsonchavessilva',
        'armandocostapsc',
        'oficialclasseapa',
        'deise_pompeu',
        'cleycecruzz',
        'kevisontor',
        'kevison4848',
        'shoe_belem',
        '02jepe',
        'fernandosouza104',
        'naldinho_pantoja',
    ]
    bot.dm(usernames[:15], spintax_message)
