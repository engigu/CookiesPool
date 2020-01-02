import time
import tornado.log
import logging

from core.db import CookiesPoolRedis
from config import Config

tornado.log.enable_pretty_logging()


class RedisPool:

    def __init__(self, redis_uri):
        self.redis = CookiesPoolRedis(uri=redis_uri)

    def _run_(self):
        for key in self.redis.query_all_cookies_keys():
            print('keys:', key)

    def run(self):
        while True:
            self._run_()
            logging.info(f'main loop sleep {Config.SLEEP_LOOP_TIME}s')
            time.sleep(Config.SLEEP_LOOP_TIME)


if __name__ == '__main__':
    rp = RedisPool(redis_uri=Config.REDIS_URI)
    rp.run()
