from lxml import etree
from dataclasses import dataclass
import time
import base64
import logging
from datetime import datetime

from src.XMLParser import XMLParser, Point

IG_PREFIX = 'com.instagram.android:id'
DEFAULT_WAIT = 60


@dataclass
class Device:
    device: object

    def launch_app(self):
        self._shell(f'monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1')

    def find_node(self, query, wait=DEFAULT_WAIT):
        start = datetime.now()
        logging.info(f'Device#find_node {query}')

        while (datetime.now() - start).total_seconds() <= wait:
            try:
                return self._xml_parser().find_node(query)
            except ValueError:
                logging.debug(f'Device#find_node sleep 1s')
                time.sleep(1)
                pass

        raise ValueError(f'Node with query "{query}" not found after {wait} seconds')

    def input_text(self, text, virtual_keyboard=False):
        logging.info(f'Input text: {text}')

        # adb shell ime set com.android.adbkeyboard/.AdbIME
        # only works if: ADBKeyboard is active + Virtual Keyboard is configured to be shown in screen
        if virtual_keyboard:
            base64message = str(base64.b64encode(text.encode('utf-8')))[1:]
            self._shell("am broadcast -a ADB_INPUT_B64 --es msg %s" % base64message)
        else:
            self._shell(f'input text "{text}"')

    def tap_by_resource_id(self, resource_id, wait=DEFAULT_WAIT):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.info(f'Device#tap {instagram_resource_id}')

        node = self.find_node(f'@resource-id="{instagram_resource_id}"', wait)
        point = XMLParser.get_point(node)

        self._tap(point)

    def tap_by_resource_id_and_text(self, resource_id, text, wait=DEFAULT_WAIT):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.info(f'Device#tap {instagram_resource_id} and "{text}"')

        node = self.find_node(f'@resource-id="{instagram_resource_id}" and @text="{text}"', wait)
        point = XMLParser.get_point(node)

        self._tap(point)

    def tap_by_text(self, text, wait=DEFAULT_WAIT):
        logging.info(f'Device#tap "{text}"')

        node = self.find_node(f'@text="{text}"', wait)
        point = XMLParser.get_point(node)

        self._tap(point)

    def tap_by_content_desc(self, content_desc):
        logging.info(f'Device#tap {content_desc}')

        node = self.find_node(f'@content-desc="{content_desc}"')
        point = XMLParser.get_point(node)

        self._tap(point)

    def clear_input(self):
        self._shell(f'input keyevent KEYCODE_MOVE_END')
        self._shell(f'input keyevent --longpress {"KEYCODE_DEL " * 250}')

    def swipe_numberpicker(self, top_value, bottom_value, expected_value):
        logging.info(f'Device#swipe_numberpicker {top_value} {bottom_value} {expected_value}')

        node1 = self.find_node(f'@text="{top_value}"')
        point1 = XMLParser.get_point(node1)

        node2 = self.find_node(f'@text="{bottom_value}"')
        point2 = XMLParser.get_point(node2)

        for _ in range(100):
            self._swipe(point1, point2, 100)
            try:
                date_of_birth = self.get_attr_by_resource_id('date_of_birth', 'text', 10)
                logging.info(f'Device#swipe_numberpicker date_of_birth={date_of_birth}')
                year = int(date_of_birth.split(' ')[-1])
                
                if year <= expected_value: return
            except ValueError:
                pass

        raise ValueError(f'Could not reach expected value: "{expected_value}"')

    def swipe_refresh(self):
        logging.info(f'Device#swipe_refresh')

        point1 = Point(300, 100)
        point2 = Point(300, 200)

        self._swipe(point1, point2, 500)

    def get_attr_by_resource_id(self, resource_id, attr, wait=DEFAULT_WAIT):
        instagram_resource_id = f'{IG_PREFIX}/{resource_id}'

        logging.info(f'Device#get_attr {attr} {instagram_resource_id}')

        node = self.find_node(f'@resource-id="{instagram_resource_id}"', wait)
        return node.get(attr)

    def pick_file(self, file_name):
        self.go_to_downloads()

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

    def go_to_downloads(self):
        # class="android.widget.ImageButton" package="com.android.documentsui" content-desc="Show roots" bounds="[8,24][64,88]"
        # text="Downloads" resource-id="android:id/title" class="android.widget.TextView" package="com.android.documentsui" bounds="[80,327][240,346]"
        node1 = self.find_node(f'@content-desc="Show roots"')
        point1 = XMLParser.get_point(node1)
        self._tap(point1)
        time.sleep(5)

        node2 = self.find_node(f'@resource-id="android:id/title" and @text="Downloads"')
        point2 = XMLParser.get_point(node2)
        self._tap(point2)
        time.sleep(5)
        
    def close_intent_filter(self):
        node = self.find_node(f'@resource-id="android:id/aerr_close"')
        point = XMLParser.get_point(node)
        self._tap(point)
        time.sleep(5)

    def debug(self):
        logging.info(etree.tostring(self._dump()))
        
    def screenshot_debug(self):
        timestamp = str(time.time() * 1000).split('.')[0]
        
        image = f'{timestamp}.png'
        logging.info(f'Saving screenshot to {image}')
        self._shell(f'screencap -p /tmp/{image}')
        self.device.pull(f'/tmp/{image}', image)
        
        dump = f'{timestamp}.xml'
        logging.info(f'Saving dump to {dump}')
        self._shell(f'uiautomator dump /tmp/{dump}')
        self.device.pull(f'/tmp/{dump}', dump)

    def _xml_parser(self):
        return XMLParser(self._dump())

    def _tap(self, point):
        logging.info(f'Device#tap {point}')

        self._shell(f'input tap {point.x} {point.y}')

    def _swipe(self, point1, point2, time=0):
        logging.info(f'Device#swipe {point1} {point2}')

        self._shell(f'input touchscreen swipe {point1.x} {point1.y} {point2.x} {point2.y} {time}')

    def _dump(self):
        self._shell(f'uiautomator dump /tmp/view.xml')
        xml_view = self._shell(f'cat /tmp/view.xml')

        return etree.XML(xml_view.encode('utf8'))

    def _shell(self, cmd):
        return self.device.shell(cmd)
