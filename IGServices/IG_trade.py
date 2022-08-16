import logging
import requests
from rest import IGService
import sys
from config.trade_ig_config import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# if you need to cache to DB your requests
from datetime import timedelta

sys.path.append('/...IGServices/config')



class IGtrade():
    def __init__(self,username,password,api_key,acc_type,acc_number):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.acc_type = acc_type
        self.acc_number = acc_number

    def create_session(self):
        ig_service = IGService(self.username, self.password, self.api_key, self.acc_type,
                               acc_id=self.acc_number)
        self.ig_service = ig_service

        try:
            session = ig_service.create_session()
            print(session)
        except:
            raise Exception('There has been an error in the system')

        return session

    def get_epic(self,symbol):
        ig_service = self.ig_service
        epic = ig_service.get_epic(symbol)

        return epic


    def open_position_market(self,currency_code,direction,epic,size):
        ig_service = self.ig_service
        op = ig_service.create_open_position(currency_code= currency_code, direction= direction, epic= epic,
                                             expiry='-', force_open='True', guaranteed_stop='False',
                                             level='', limit_distance=None, limit_level=None,
                                             order_type='MARKET', quote_id=None, size= size, stop_distance=None,
                                             stop_level=None)

        print(op)
        print(op['reason'])
        print(op['dealId'])

        return op

    def open_position_limit(self,currency_code,direction,epic,size,level_price):
        ig_service = self.ig_service
        op = ig_service.create_open_position(currency_code= currency_code, direction= direction, epic= epic,
                                             expiry='-', force_open='True', guaranteed_stop='False',
                                             level= level_price, limit_distance=None, limit_level=None,
                                             order_type='LIMIT', quote_id=None, size=size, stop_distance=None,
                                             stop_level=None)

        print(op)
        print(op['reason'])
        print(op['dealId'])

        return op


    def close_position(self,dealid,direction,size,order_type):
        ig_service = self.ig_service
        cp = ig_service.close_open_position(deal_id = dealid, direction= direction, epic=None, expiry='-',
                                            level='', order_type = order_type, quote_id=None, size = size)

        return cp


