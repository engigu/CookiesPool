import time
import tornado.log
import logging

from core.db import CookiesPoolRedis
from config import Config

tornado.log.enable_pretty_logging()


class RedisPool:

    def __init__(self, redis_uri):
        self.redis = CookiesPoolRedis(uri=redis_uri)

    def do_check(self, cookies_dict):

        return True

    def deal_check_result(self, key, check_result):
        return

    def _run_(self):
        for key in self.redis.query_all_cookies_keys():
            print('keys:', key)
            cookies_dict = self.redis.get_one_cookies(key)
            print('cookies_dict:', cookies_dict)

            check_result = self.do_check(cookies_dict)
            self.deal_check_result(key=key, check_result=check_result)

    def run(self):
        while True:
            self._run_()
            logging.info(f'main loop sleep {Config.SLEEP_LOOP_TIME}s')
            time.sleep(Config.SLEEP_LOOP_TIME)


if __name__ == '__main__':
    rp = RedisPool(redis_uri=Config.REDIS_URI)
    rp.run()
