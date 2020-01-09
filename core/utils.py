import time
import os

class Utils:

    @staticmethod
    def now():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


    @staticmethod
    def run_in_docker():
        return bool(os.environ.get('RUN_IN_DOCKER'))
    
if __name__ == '__main__':
    pass
