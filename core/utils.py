import time


class Utils:

    @staticmethod
    def now():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


if __name__ == '__main__':
    pass
