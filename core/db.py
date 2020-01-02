import base64
import redis

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
            cls._instances[params_ident] = super(SameOriginSingleton, cls).__call__(*args, **kwargs)
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
    #   hash
    #     key:         value:
    #               --- {cookies_0:
    # cookies_pool |-- cookies_1
    #               --- cookies_0
    #
    #
    #
    #

    cookies_key_format = Config.COOKIES_KEY_FORMAT

    def query_all_cookies_keys(self):
        # 获取所有存储的cookies key
        return self.redis_client.keys('*:%s:*' % self.cookies_key_format.split(':')[1])

        # return self.redis_client.hkeys(self.store_key)

    def query_store_cookies(self, key):
        return self.redis_client.hget(self.store_key, key)

    def _add_one_cookies(self, key, value):
        return self.redis_client.hset(self.store_key, key, value)

    def add_one_cookies(self, key, value):
        # print(self.redis_client.keys('58:*:0'))
        site = '58'
        cookies_key = self.cookies_key_format % dict(site=site, no=0)
        c_len = self.redis_client.keys(
            '%s:%s:*' % (site, self.cookies_key_format.split(':')[1])
        )
        
        print(c_len, self.redis_client.keys('*'))
        # return self.redis_client.set(cookies_key, '6666')
