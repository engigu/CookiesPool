import json
import time
import tornado.log
import logging

from core.sqlitedb import SQLiteModel
from checker import Checker
from config import Config
from core.utils import Utils
from core.status import  TaskStatus

tornado.log.enable_pretty_logging()


class CookiesPool:

    def __init__(self):
        self.sqlite = SQLiteModel()

    def do_check(self, cookies, site):
        params = {
            'url': site.check_url,
            'method': site.method,
            'headers': site.headers,
            'cookies': cookies.cookies,
            'check_key': site.check_key,
        }
        print('*****', params)
        ckr = Checker()
        return ckr.do_check(**params)

    def deal_check_result(self, cookies, site, check_result):
        if not check_result:
            logging.info(f"cookies_id: {cookies.id} {cookies.cookies_name} has expired")
            self.sqlite.update_cookeis_status(cookies.id, TaskStatus.failed)
        else:
            logging.info(f"cookies_id: {cookies.id} {cookies.cookies_name} is ok!")
            self.sqlite.update_cookeis_status(cookies.id, TaskStatus.ok)
       
        return

    def do_a_circle(self):
        cookies_and_site = self.sqlite.get_check_cookies()
        logging.info(f"current query {len(cookies_and_site)} to check")

        for cookies, site in cookies_and_site:
            try:
                check_result = self.do_check(cookies, site)
                self.deal_check_result(cookies, site, check_result)
            except Exception as e:
                logging.exception("check error When %s" % key, e)

        logging.info(f"current check end")

    def run(self):
        while True:
            try:
                self.do_a_circle()
            except KeyboardInterrupt:
                logging.info("KeyboardInterrupt, exiting....")
            except Exception as e:
                logging.exception(e)
            logging.info(f'main loop sleep {Config.SLEEP_LOOP_TIME}s')
            time.sleep(Config.SLEEP_LOOP_TIME)


if __name__ == '__main__':
    cp = CookiesPool()
    cp.run()
