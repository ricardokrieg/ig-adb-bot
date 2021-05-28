from ppadb.client import Client as AdbClient
import logging
import sys

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

    adb_device = find_device(devices, '192.168.56.105:5555')
    print(f'Connected to {adb_device.serial}')

    device = Device(adb_device)

    # device.debug()
    # print(device.find_node('@resource-id="com.instagram.android:id/username"'))
    # print(device.tap_by_resource_id('username'))
    # print(device.tap_by_resource_id_and_text('username', 'cristiano'))
    # print(device.tap_by_content_desc('Search and Explore'))
    # print(device.input_text('Test'))
    # print(device.get_attr_by_resource_id('username', 'text'))

    # TODO pending test
    # print(device.swipe_numberpicker(2019, 2020, 2000))
    # print(device.pick_file('ig_image.jpeg'))
