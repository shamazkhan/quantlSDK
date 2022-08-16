import logging
import requests
from IGServices.rest import IGService
import sys
from IGServices.config.trade_ig_config import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# if you need to cache to DB your requests
from datetime import timedelta
import requests_cache

sys.path.append('/...IGServices/config')



ig_service = IGService(config.username, config.password, config.api_key, config.acc_type, acc_id=config.acc_number)
# if you want to globally cache queries
# ig_service = IGService(config.username, config.password, config.api_key, config.acc_type, session)
ig_service.create_session()
# ig_stream_service.create_session(version='3')
#accounts = ig_service.fetch_accounts()
#print("accounts:\n%s" % accounts)

'''op = ig_service.create_open_position(currency_code='GBP', direction='BUY', epic='CS.D.GBPINR.CFD.IP',
                                expiry='-', force_open='True', guaranteed_stop='False',
                                level='', limit_distance=None, limit_level=None,
                                order_type='MARKET', quote_id=None, size='2',stop_distance=None,
                                stop_level=None)
print(op)
print(op['reason'])
print(op['dealId'])'''
