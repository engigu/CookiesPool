import time, datetime
import os

class Utils:

    @staticmethod
    def now(return_datetime=False):
        if not datetime:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return datetime.datetime.now()

    @staticmethod
    def run_in_docker():
        return bool(os.environ.get('RUN_IN_DOCKER'))
    
if __name__ == '__main__':
    pass
