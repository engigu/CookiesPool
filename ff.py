import hashlib
import json
import time, sys, os
from copy import deepcopy

import requests

sys.path.append(os.path.abspath('../'))
from core.schema import CookieStore
from core.mysql import session_scope
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s [%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s'
)

COOKIES_UPDATE_URL = 'https://dev.tencent.com/u/EngiGu/p/other/git/raw/master/jianxun/cook'


class COOKIES_STATUS:
    ok = 0  # 可以用
    broken = 1  # 被封需要更换
    updating = 2  # 正在更换


def send_ftqq_msg(text, desp):
    """
    :param text: 消息标题，最长为256，必填。
    :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
    :return:
    """
    server_url = 'http://notice.sooko.club:8890/notice'
    data = {'title': text, 'content': desp, 'way': 'ServerChan', 'key': 'spider_c:TFvkD9enEkvkVUyMVJUYmN'}
    return requests.post(url=server_url, data=data).content.decode()


class CookiesCheck():

    def __init__(self):
        self.cookies_url = COOKIES_UPDATE_URL
        self.business_58_url = 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29'
        self.headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,it;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; sessionid=8a9675fa-4e41-423c-bf28-96eeecbb70d3; param8616=1; param8716kop=1; id58=e87rZl0EuzCoPyC3CISqAg==; 58tj_uuid=a22f6c49-35ff-4270-bb98-d2019ec09be9; new_uv=1; utm_source=; spm=; init_refer=; jl_list_left_banner=1; als=0; wmda_uuid=b6470035d30409766e3ee91a34134b88; wmda_new_uuid=1; wmda_session_id_1731916484865=1560591154559-d9fea39d-51e4-d60a; wmda_visited_projects=%3B1731916484865; xxzl_deviceid=OaoMjiA0nALhIk8zQgyEqqC3l8WbqPO7tnnsBGKfNsq48JuDusI4uvBUV2tTaT1r; PPU="UID=63814192696597&UN=xvhjzdghyhlg&TT=7de63ccc32a8e06f75c3e53d361f507b&PBODY=RBW5dnfz1XND4QF10hm9wBOmrFc22q_0pTJ1YZOLJlFocLYgeC5QLQuPr05KE7ZzWeo58JMSzD030OzjTl62MjUvFARQi0ucSQ-Gibgnl7lWVYYSqQHG60I4BCIceOkdUZFtwP1c-hziWZ_4iJ3BqPYfu2I-T9KrpKDTC7d6qRo&VER=1"; www58com="UserID=63814192696597&UserName=xvhjzdghyhlg"; 58cooper="userid=63814192696597&username=xvhjzdghyhlg"; 58uname=xvhjzdghyhlg; new_session=0; showPTTip=1; ljrzfc=1',
            'pragma': 'no-cache',
            'referer': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-0f7d-5880-bbccd08216eb&ClickID=104',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }

    def check_cookies_is_ok(self, cookies):
        self.headers['cookie'] = cookies
        r = requests.get(url=self.business_58_url, headers=self.headers).content.decode()
        if '<title>用户登录-58同城</title>' in r:
            return False
        return True

    def __update_cookies_status(self, tag, status, cookies):
        # mysql 更新 cookies 状态
        with session_scope() as s:
            s.query(CookieStore).filter(CookieStore.tag == tag).update({'status': status, 'cookies': cookies})

    def __query_cookies_from_update_url(self):
        while True:
            try:
                return eval(requests.get(self.cookies_url).content.decode())
            except Exception as e:
                logging.error(f'trans update cookies url data error! error: {e.__context__}')
            time.sleep(3)

    def update_mysql_cookies(self, tags):
        # 阻塞状态会一直进行，直到所有的cookies正常
        _tags = deepcopy(tags)
        f = 0
        update_hash = None

        while True:
            for t in _tags:
                cookies_map = self.__query_cookies_from_update_url()
                print(cookies_map)
                # hash 处理
                hash_ = hashlib.md5(
                    json.dumps(cookies_map, sort_keys=True, ensure_ascii=False).encode('utf8')
                ).hexdigest()
                if update_hash is None:
                    update_hash = hash_  # 第一次进入这函数时候开始记录更新特征值
                else:
                    # 手动在提交过commit更新cookies文件
                    if update_hash != hash_:  # 文件变动
                        logging.info(f"detect cookie file change from url.")
                        f = 0  # 一旦开始更新cookies动作后，将推送计数置为0
                        update_hash = hash_

                cookies = cookies_map.get(t, '')
                if self.check_cookies_is_ok(cookies):  # 从cookies_url拿到的cookies是好的
                    self.__update_cookies_status(t, COOKIES_STATUS.ok, cookies)
                    _tags.remove(t)  # 成功后会移除这个tag
                    logging.info(f"tag: {t} update cookies to mysql success!")
                else:
                    logging.warning(f"tag: {t} cookies from url is bad, will try another time.")
                time.sleep(1.5)

            # _tags为空，都更新完了，跳出更新cookies阻塞状态
            if not bool(_tags):
                logging.info(f'all tags: {str(tags)} has updated to mysql, update cookies func exited...')
                send_ftqq_msg("all tags's cookies update", 'ok')
                break
            else:
                logging.info(f"{str(_tags)} still need to de update..")
                f += 1
                # 推送失败计数出现场景：
                # 1. cookies失效后，推送了失效消息，没时间去手动更新处理cookies, 达到指定次数，会不再多余提醒，
                # 还是会一直阻塞在这个函数里，循环检测
                # 2. 一旦开始处理更新cookies, 会将失败计数置为0，重新开始失败提醒（主要是处理更新的其中某个cookies不行，
                # 提醒重新更新这个cookies）
                if f < 10:  # 10次cookies更新失败后，不再推送失败消息
                    send_ftqq_msg(f"{str(_tags)} failed", f'failed--{str(_tags)}')
            print('f:', f)
            time.sleep(1 * 60)

    def run(self):
        while True:
            with session_scope() as s:
                query = s.query(CookieStore).all()
            notice = ''
            to_be_updated_tags = []

            for q in query:
                # 先检测完一轮
                if not self.check_cookies_is_ok(q.cookies):
                    notice += q.tag + ' '
                    to_be_updated_tags.append(q.tag)
                    logging.warning(f'{q.tag} is expried.')
                else:
                    logging.info(f'{q.tag} is ok.')
                time.sleep(5)

            if to_be_updated_tags:
                logging.info(f'tags {str(to_be_updated_tags)} need to be updated')
                self.update_mysql_cookies(to_be_updated_tags)  # 进入阻塞状态
            else:
                logging.info('all cookies is ok!')

            # raise SystemExit('exit')
            logging.info('main loop sleep 5min...')
            time.sleep(5 * 60)  # 正常的h话每5分钟检测一次


if __name__ == '__main__':
    c = CookiesCheck()
    c.run()