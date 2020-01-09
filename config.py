import os


class Config:
    PROJECT_NAME = 'cookies_pool'

    COOKIES_KEY_FORMAT = '%(site)s:cookies:%(no)s'

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    # REDIS_URI = 'redis://192.168.244.128:6379/2'
    REDIS_URI = 'redis://127.0.0.1:6352/2'

    SLEEP_LOOP_TIME = 5 * 60
