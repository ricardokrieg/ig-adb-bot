from dataclasses import dataclass
import time
import logging
import json

from src.Device import Device

MAX_ERROR = 2


@dataclass
class Bot:
    device: Device

    def signup(self, name, password, sms_service):
        logging.info('Launching app')
        self.device.launch_app()
        time.sleep(15)

        logging.info('Clicking in Sign Up button')
        self.device.tap_by_resource_id('sign_up_with_email_or_phone')

        logging.info('Selecting country: Russia')
        self.device.tap_by_resource_id('country_code_picker')
        self.device.input_text('+7')
        time.sleep(2)
        self.device.tap_by_resource_id_and_text('row_simple_text_textview', 'Russia (+7)')

        # phone_number = input('Phone Number: ')
        sms_service.get_balance()
        logging.info('Getting phone number...')
        phone_number = sms_service.get_number()
        self.device.input_text(phone_number.number[1:])
        time.sleep(len(phone_number.number))

        self.device.tap_by_resource_id('button_text')
        sms_service.set_status_ready(phone_number)

        # code = input('Code: ')
        logging.info(f'Waiting for code for {phone_number.number}')
        code = sms_service.wait_for_code(phone_number)

        if code is None:
            sms_service.set_status_cancel(phone_number)
            raise Exception(f'Failed to get SMS Code for {phone_number.number}')

        sms_service.set_status_done(phone_number)

        self.device.input_text(code)
        time.sleep(len(code))

        logging.info('Clicking in Next')
        self.device.tap_by_resource_id('button_text')

        logging.info('Filling Name and Password')
        logging.info(f'Name: {name}')
        logging.info(f'Password: {password}')
        self.device.tap_by_resource_id('full_name')
        self.device.input_text(name)
        time.sleep(len(name))
        self.device.tap_by_resource_id('password')
        self.device.input_text(password)
        time.sleep(len(password))
        self.device.tap_by_resource_id('continue_without_ci')

        year = 2000
        logging.info('Setting Year')
        logging.info(f'Year: {year}')
        self.device.swipe_numberpicker(2019, 2020, year)
        self.device.tap_by_resource_id('button_text')

        try:
            username = self.device.get_attr_by_resource_id('field_title_second_line', 'text', 10)
        except ValueError:
            username = self.device.get_attr_by_resource_id('field_title', 'text', 10)
            username = username.split("\n")[1].replace('?', '')
        logging.info(f'Username: {username}')

        logging.info('Clicking in Next')
        self.device.tap_by_resource_id('button_text')

        logging.info('Skipping Facebook friends')
        self.device.tap_by_resource_id('skip_button')
        self.device.tap_by_resource_id('negative_button')

        logging.info('Picking photo')
        self.device.tap_by_resource_id('button_text')
        self.device.tap_by_resource_id_and_text('row_simple_text_textview', 'Choose From Library')
        self.device.pick_file('ig_image.jpeg')
        self.device.tap_by_resource_id('save')
        self.device.tap_by_resource_id('button_text')

        logging.info('Following 3 recommended profiles')
        for _ in range(3):
            self.device.tap_by_resource_id_and_text('row_recommended_user_follow_button', 'Follow')
            time.sleep(3)
        self.device.tap_by_resource_id('action_bar_button_action')

        self.device.swipe_refresh()
        time.sleep(30)
        logging.info('Done')

    def dm(self, queue, message_count, get_messages):
        logging.info(f'Will DM {message_count} users')

        logging.info('Launching app')
        self.device.launch_app()
        time.sleep(10)

        self.device.swipe_refresh()
        time.sleep(10)

        try:
            self.device.tap_by_resource_id('action_bar_inbox_button', 5)
        except ValueError:
            pass

        n_error = 0
        try:
            for i in range(message_count):
                sqs_message = Bot._get_message(queue)

                profile = json.loads(sqs_message.body)
                username = profile['username']

                logging.info(f'#{i} Sending DM to: @{username}')
                self.device.swipe_refresh()
                time.sleep(5)

                self.device.tap_by_resource_id('search_edit_text')
                self.device.input_text(username)
                time.sleep(len(username) / 10)

                try:
                    self.device.tap_by_resource_id_and_text('row_inbox_digest', username, 30)
                except ValueError:
                    try:
                        self.device.tap_by_resource_id_and_text('row_inbox_username', username, 5)
                    except ValueError:
                        logging.error(f'User {username} not found. Removing message')
                        sqs_message.delete()

                        n_error += 1
                        logging.info(f'{MAX_ERROR - n_error} errors left')

                        if MAX_ERROR - n_error <= 0:
                            logging.info('Exiting')
                            raise ValueError(f'Failed {n_error} when trying to find users')

                        logging.info(f'Going to next message')
                        continue

                for message in get_messages(profile):
                    self.device.tap_by_resource_id('row_thread_composer_edittext')

                    logging.info(f'Message: {message}')

                    self.device.input_text(message, True)
                    time.sleep(len(message) / 20)
                    self.device.tap_by_resource_id('row_thread_composer_button_send')

                    time.sleep(5)
                self.device.tap_by_resource_id('action_bar_button_back')

                sqs_message.delete()

                i += 1

            return True
        except ValueError as err:
            self.device.debug()

            raise err

    def follow(self, username):
        logging.info(f'Will follow {username}')

        logging.info(f'Going to Search')
        self.device.tap_by_content_desc('Search and Explore')
        self.device.tap_by_resource_id('action_bar_search_edit_text')

        self.device.input_text(username)
        time.sleep(len(username) / 10)

        try:
            self.device.tap_by_resource_id_and_text('row_search_user_username', username, 30)
        except ValueError:
            self.device.tap_by_resource_id_and_text('row_search_digest', username, 30)

        self.device.tap_by_text('Follow')
        time.sleep(5)

    @staticmethod
    def _get_message(queue):
        logging.info(f'Getting message from SQS')
        tries = 3

        while tries > 0:
            messages = queue.receive_messages(MaxNumberOfMessages=1)

            if len(messages) > 0:
                logging.info(f'Got message: {messages[0]}')
                return messages[0]

            tries -= 1

        return None
