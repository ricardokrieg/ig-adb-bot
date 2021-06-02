import logging
import sys

from src.SMSHubService import SMSHubService, PhoneNumber

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if __name__ == '__main__':
    service = SMSHubService()

    logging.debug(f'Balance = {service.get_balance()}')
    # service.wait_for_code(PhoneNumber(id='115537415', number='79089839873'))
    # service.set_status_cancel(PhoneNumber(id='115537415', number='79089839873'))
