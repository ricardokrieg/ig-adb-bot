from lxml import etree
from dataclasses import dataclass
import time
import base64
import logging
from datetime import datetime

from XMLParser import XMLParser


IG_PREFIX = 'com.instagram.android:id'
DEFAULT_WAIT = 60


@dataclass
class Device:
    device: object

    def launch_app(self):
        self._shell(f'monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1')

    def find_node(self, query, wait=DEFAULT_WAIT):
        start = datetime.now()
        logging.debug(f'Device#find_node {query}')

        while (datetime.now() - start).total_seconds() <= wait:
            try:
                return self._xml_parser().find_node(query)
            except ValueError:
                logging.debug(f'Device#find_node sleep 1s')
                time.sleep(1)
                pass

        raise ValueError(f'Node with query "{query}" not found after {wait} seconds')

    def input_text(self, text, virtual_keyboard=False):
        # adb shell ime set com.android.adbkeyboard/.AdbIME
        # only works if: ADBKeyboard is active + Virtual Keyboard is configured to be shown in screen
        if virtual_keyboard:
            base64message = str(base64.b64encode(text.encode('utf-8')))[1:]
            self._shell("am broadcast -a ADB_INPUT_B64 --es msg %s" % base64message)
        else:
            self._shell(f'input text "{text}"')

    def tap_by_resource_id(self, resource_id, wait=DEFAULT_WAIT):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.debug(f'Device#tap {instagram_resource_id}')

        node = self.find_node(f'@resource-id="{instagram_resource_id}"', wait)
        point = XMLParser.get_point(node)

        self._tap(point)

    def tap_by_resource_id_and_text(self, resource_id, text, wait=DEFAULT_WAIT):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.debug(f'Device#tap {instagram_resource_id} and "{text}"')

        node = self.find_node(f'@resource-id="{instagram_resource_id}" and @text="{text}"', wait)
        point = XMLParser.get_point(node)

        self._tap(point)

    def tap_by_content_desc(self, content_desc):
        logging.debug(f'Device#tap {content_desc}')

        node = self.find_node(f'@content-desc="{content_desc}"')
        point = XMLParser.get_point(node)

        self._tap(point)

    def swipe_numberpicker(self, top_value, bottom_value, expected_value):
        logging.debug(f'Device#swipe_numberpicker {top_value} {bottom_value} {expected_value}')

        node1 = self.find_node(f'@text="{top_value}"')
        point1 = XMLParser.get_point(node1)

        node2 = self.find_node(f'@text="{bottom_value}"')
        point2 = XMLParser.get_point(node2)

        for _ in range(100):
            self._swipe(point1, point2)
            try:
                return self.find_node(f'@resource-id="android:id/numberpicker_input" and @text="{expected_value}"', 1)
            except ValueError:
                pass

        raise ValueError(f'Could not reach expected value: "{expected_value}"')

    def get_attr_by_resource_id(self, resource_id, attr):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.debug(f'Device#get_attr {attr} {instagram_resource_id}')

        node = self.find_node(f'@resource-id="{instagram_resource_id}"')
        return node.get(attr)

    def pick_file(self, file_name):
        node = self.find_node(f'@resource-id="android:id/title" and @text="{file_name}"')
        point = XMLParser.get_point(node)

        self._tap(point)

        try:
            allow_node = self.find_node(f'@resource-id="com.android.packageinstaller:id/permission_allow_button"', 10)
            allow_point = XMLParser.get_point(allow_node)
            logging.info('ALLOW required')

            self._tap(allow_point)
        except ValueError:
            logging.info('ALLOW not required')
            pass

    # def tap_by_resource_id(self, resource_id):
    #     point = self.find_and_get_point_by_full_resource_id(f'com.instagram.android:id/{resource_id}')
    #     self.tap(point)
    #
    # def tap_by_resource_id_and_text(self, resource_id, text):
    #     point = self.find_and_get_point_by_full_resource_id_and_text(f'com.instagram.android:id/{resource_id}', text)
    #     self.tap(point)
    #
    # def swipe_numberpicker(self, resource_id, top_value, bottom_value, expected_value):
    #     point1 = self.find_and_get_point(f'@text="{top_value}"')
    #     point2 = self.find_and_get_point(f'@text="{bottom_value}"')
    #
    #     for _ in range(100):
    #         self.swipe(point1, point2)
    #         try:
    #             self.find_node(f'@resource-id="{resource_id}" and @text="{expected_value}"')
    #             return
    #         except ValueError:
    #             pass
    #
    #     raise ValueError(f'Could not reach expected value: "{expected_value}"')
    #
    #
    #
    # def find_and_get_point_by_full_resource_id(self, resource_id):
    #     return self.find_and_get_point(f'@resource-id="{resource_id}"')
    #
    # def find_and_get_point_by_full_resource_id_and_text(self, resource_id, text):
    #     return self.find_and_get_point(f'@resource-id="{resource_id}" and @text="{text}"')
    #
    # def find_and_get_point(self, query):
    #     node = self.find_node(query)
    #     return self.get_point_for_node(node)

    def debug(self):
        logging.info(etree.tostring(self._dump()))

    def _xml_parser(self):
        return XMLParser(self._dump())

    def _tap(self, point):
        logging.debug(f'Device#tap {point}')

        self._shell(f'input tap {point.x} {point.y}')

    def _swipe(self, point1, point2):
        logging.debug(f'Device#swipe {point1} {point2}')

        self._shell(f'input touchscreen swipe {point1.x} {point1.y} {point2.x} {point2.y}')

    def _dump(self):
        self._shell(f'uiautomator dump /tmp/view.xml')
        xml_view = self._shell(f'cat /tmp/view.xml')

        return etree.XML(xml_view.encode('utf8'))

    def _shell(self, cmd):
        return self.device.shell(cmd)
