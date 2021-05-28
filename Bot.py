from dataclasses import dataclass
import time
import spintax
import logging

from Device import Device


@dataclass
class Bot:
    device: Device

    def signup(self, name, password):
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

        phone_number = input('Phone Number: ')
        self.device.input_text(phone_number)
        time.sleep(len(phone_number))

        self.device.tap_by_resource_id('button_text')

        code = input('Code: ')
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

        username = self.device.get_attr_by_resource_id('field_title_second_line', 'text')
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

        logging.info('Done')

    def dm(self, usernames, spintax_message):
        logging.info(f'Will DM {len(usernames)} users:')
        logging.info(usernames)

        try:
            self.device.tap_by_resource_id('action_bar_inbox_button', 5)
        except ValueError:
            pass

        try:
            i = 1
            for username in usernames:
                logging.info(f'#{i} Sending DM to: @{username}')

                self.device.tap_by_resource_id('search_edit_text')
                self.device.input_text(username)
                time.sleep(len(username))

                try:
                    self.device.tap_by_resource_id_and_text('row_inbox_username', username, 30)
                except ValueError:
                    self.device.tap_by_resource_id_and_text('row_inbox_digest', username, 5)

                self.device.tap_by_resource_id('row_thread_composer_edittext')
                message = spintax.spin(spintax_message)
                logging.info(f'Message: {message}')
                self.device.input_text(message, True)
                time.sleep(len(message) / 10)
                self.device.tap_by_resource_id('row_thread_composer_button_send')

                time.sleep(5)
                self.device.tap_by_resource_id('action_bar_button_back')

                i += 1
        except ValueError as err:
            self.device.debug()

            raise err
