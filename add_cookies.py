from config import Config
from core.db import CookiesPoolRedis


class AddCookies:
    def __init__(self, redis_uri):
        self.redis = CookiesPoolRedis(uri=redis_uri)

    # def format_json(self, fa):

    def add_to_redis(self, to_add_cookies: list):
        site = '58'

        same_site_cookies = [
            i for i in self.redis.query_all_cookies_keys()
            if i.startswith(site)
        ]

        same_site_cookies_num = len(same_site_cookies)

        for index, c in enumerate(to_add_cookies):
            no = same_site_cookies_num + index


        key = Config.COOKIES_KEY_FORMAT % dict(
            site=site, no=0
        )

        self.redis.add_one_cookies()


    def test(self):
        self.redis.add_one_cookies('58:cookies:0', '555')
        # self.redis.query_all_cookies_keys()

if __name__ == '__main__':
    to_add_cookies = [
        '111111'
    ]

    ac = AddCookies(redis_uri=Config.REDIS_URI)
    # ac.add_to_redis(to_add_cookies)
    ac.test()
