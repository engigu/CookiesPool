import json

from config import Config
from core.sqlitedb import SQLiteModel
from core.utils import Utils


class AddCookies:
    def __init__(self, redis_uri):
        self.sql = SQLiteModel()

    def add_to_redis(self, to_add_cookies: list):
        site = '58'

        site_dict = {
                'site': site,
                'check_url': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29',
                'check_key': '<title>用户登录-58同城</title>',
                'method': 'get',
                'headers': '{}',
                'status': 0
            }

        self.sql.add_one_site(site_dict)

        for i in to_add_cookies:
            now = Utils.now()
            cookies_dict = {
                'site': site,
                'cookies': i,
                'status': 0

            }
            self.sql.add_one_cookies(cookies_dict)
        #     self.redis.add_one_cookies(site, json.dumps(cookies_dict, ensure_ascii=False))

    def test(self):
        # for i in range(1000):
        self.redis.add_one_cookies('58', '888')
        # self.redis.query_all_cookies_keys()


if __name__ == '__main__':
    to_add_cookies = [
        '111111'
    ]

    ac = AddCookies(redis_uri=Config.REDIS_URI)
    ac.add_to_redis(to_add_cookies)
    # ac.test()
