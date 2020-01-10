import json
import time
import tornado.log
import logging

from core.db import CookiesPoolRedis
from checker import Checker
from config import Config
from core.utils import Utils
from core.status import  TaskStatus

tornado.log.enable_pretty_logging()


class RedisPool:

    def __init__(self, redis_uri):
        self.redis = CookiesPoolRedis(uri=redis_uri)

    def do_check(self, cookies_dict):
        params = {
            'url': cookies_dict['check_url'],
            'method': cookies_dict['method'],
            'headers': cookies_dict['headers'],
            'cookies': cookies_dict['cookies'],
            'check_key': cookies_dict['check_key'],
        }

        ckr = Checker()
        return ckr.do_check(**params)

    def deal_check_result(self, key,cookies_dict, check_result):
        print('key, check_result::::', key, check_result)
        if not  check_result:
            logging.info(f"key: {key} has expired")
            cookies_dict['modified_at']  =  Utils.now
            cookies_dict['status']  =  TaskStatus.failed
            self.redis.update_one_cookies(key, json.dumps(cookies_dict, ensure_ascii=False))
        return

    def do_a_circle(self):
        for key in self.redis.query_all_cookies_keys():
            print('keys:', key)
            # setattr(self, key, False)
            cookies_dict = self.redis.get_one_cookies(key)
            print('cookies_dict:', cookies_dict)

            try:
                check_result = self.do_check(cookies_dict)
                self.deal_check_result(key=key, cookies_dict=cookies_dict,check_result=check_result)
            except Exception as e:
                logging.exception("check error When %s" % key, e)

    def run(self):
        while True:
            try:
                self.do_a_circle()
            except KeyboardInterrupt:
                logging.info("KeyboardInterrupt, exiting....")
            except Exception as e:
                logging.exception(e)
            logging.info(f'main loop sleep {Config.SLEEP_LOOP_TIME}s')
            break
            time.sleep(Config.SLEEP_LOOP_TIME)


if __name__ == '__main__':
    rp = RedisPool(redis_uri=Config.REDIS_URI)
    rp.run()
