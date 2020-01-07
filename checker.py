import requests


class Checker:

    def __init__(self):
        pass

    def do_check(self, url, cookies, check_key, headers=None, method='get'):
        method = method.lower()

        if method not in ['get', 'post']:
            raise Exception('method error')

        # ret_html = getattr(requests, method)()
        # TODO method的完善
        response = requests.get(url=url, headers=headers, timeout=30)
        res_html = response.content.decode()

        if not check_key in res_html:
            return True
        return False
