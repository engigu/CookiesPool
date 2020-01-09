import base64
import redis
import json

from config import Config


class SameOriginSingleton(type):
    """
    同样的连接uri只有一个实例
    """
    _instances = {}

    @staticmethod
    def calc_params_identify(params):
        return base64.b64encode(str(params).encode())

    def __call__(cls, *args, **kwargs):
        params_ident = cls.calc_params_identify(args)
        if params_ident not in cls._instances:
            cls._instances[params_ident] = super(
                SameOriginSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[params_ident]


class Redis(metaclass=SameOriginSingleton):
    def __init__(self, uri):
        self.redis_client = self.init_redis(uri)

    def init_redis(self, uri):
        return redis.StrictRedis(
            connection_pool=redis.ConnectionPool.from_url(uri),
            decode_responses=True
        )

    # def lpush(self, key: object, value: object):
    #     return self.redis_client.lpush(key, value)
    #
    # def llen(self, key):
    #     return self.redis_client.llen(key)
    #
    # def rpop(self, key):
    #     return self.redis_client.rpop(key)
    #
    # def incr(self, key):
    #     return self.redis_client.incr(key)


class CookiesPoolRedis(Redis):
    # store format string

    cookies_key_format = Config.COOKIES_KEY_FORMAT

    def query_all_cookies_keys(self):
        # 获取所有存储的cookies key
        all_keys = self.redis_client.keys(
            '*:%s:*' % self.cookies_key_format.split(':')[1])
        for key in all_keys:
            if isinstance(key, bytes):
                key = key.decode()
            yield key

    def add_one_cookies(self, site: str, value: str) -> str:
        #  key样式  ['58:cookies:0']
        # site = '58'
        no = self.calc_missing_no(site)
        cookies_key = self.cookies_key_format % dict(site=site, no=no)
        return self.redis_client.set(cookies_key, value)

    def get_sorted_list(self,  raw_list):
        all_key = [i.decode() if isinstance(i, bytes) else i for i in raw_list]
        return sorted(all_key, key=lambda x: x.split(":")[-1])

    def calc_missing_no(self, site):
        # 计算出缺失的序号
        all_key = self.redis_client.keys(
            '%s:%s:*' % (site, self.cookies_key_format.split(':')[1]))
        all_key = [i.decode() if isinstance(i, bytes) else i for i in all_key]
        all_no = [int(x.split(':')[-1]) for x in all_key]
        all_no_sort = sorted(all_no, key=lambda x: x)

        if not bool(all_no):
            return 0

        last_no = all_no_sort[-1] if bool(all_no_sort) else 0
        missing_set = set(range(last_no)) - set(all_no)

        if not missing_set:
            # 沒有缺失的序号，序号直接加1
            return last_no + 1
        # 直接返回缺失的第一个序号
        return list(sorted(missing_set))[0]

    def delete_one_cookies(self, key):
        return self.redis_client.delete(key)

    def update_one_cookies(self, key, value):
        return self.redis_client.set(key, value)

    def get_one_cookies(self, key):
        cookies = self.redis_client.get(key)
        return json.loads(cookies.decode()) if cookies else {}

    def query_all_cookies(self, page=1, size=20):
        # 获取所有存储的cookies key
        page =  page if page else 1
        size =  size if size else 20
        all_keys = self.redis_client.keys( '*:%s:*' % self.cookies_key_format.split(':')[1])
        all_keys = self.get_sorted_list(all_keys)
        to_query = all_keys[(page-1)*size:page*size]

        return [
            dict({'key': k}, **self.get_one_cookies(key=k))
            for k in to_query
        ], len(all_keys)
