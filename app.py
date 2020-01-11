import datetime
import json
from flask import Flask, render_template, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuthreid

from core.sqlitedb import SQLiteModel
from core.model import init_sqlite
from core.utils import Utils
from config import Config

SQL_MODEL = SQLiteModel()
app = Flask(__name__)
# auth = HTTPBasicAuth()

init_sqlite()

# @auth.verify_password
# def verify_password(username, password):
#     if username in users:
#         return check_password_hash(users.get(username), password)
#     return False


def error(code=-1,  msg='inter error'):
    return jsonify({'code': code, 'msg': msg})


def ok(code=0,  msg='ok!'):
    return jsonify({'code': code, 'msg': msg})


@app.route('/')
# @auth.login_required
def index():
    return 'WELCOME TO WORLD!<br />'


# 查询所有的sites
@app.route('/cookies_all_sites', methods=['GET'])
# @auth.login_required
def cookies_all_sites():
    sites = SQL_MODEL.query_all_sites()
    sites = [s.site for s in sites]
    return jsonify({"total": len(sites), "sites":  sites})

# 查询指定site对应所有的cookies
@app.route('/cookies_all', methods=['GET'])
# @auth.login_required
def cookies_all():
    site = request.args.get('site', None)
    if not site:
        return error(msg='site error')
    total, cookies = SQL_MODEL.query_site_cookies(site)
    cookies = [Utils.row2dict(c) for c in cookies]
    return jsonify({"total": total, "cookies": cookies})


# # 查询指定的cookies
# @app.route('/cookies', methods=['GET'])
# # @auth.login_required
# def cookies_get():
#     key = request.args.get('key',  None)
#     if not key:
#         return error(msg='key error')
#     cookies = REDIS_MODEL.get_one_cookies(key=key)
#     cookies = json.loads(cookies) if cookies else {}
#     return jsonify(cookies)


# # 添加一条新的cookies
# @app.route('/cookies', methods=['POST'])
# # @auth.login_required
# def cookies_post():
#     site = request.form.get('site', None)
#     cookies = request.form.get('cookies', None)
#     if not all([site,  cookies]):
#         return error(msg='site or cookies is empty!')
#     REDIS_MODEL.add_one_cookies(site=site,  value=cookies)
#     return ok()

# # 更新一条cookies
# @app.route('/cookies', methods=['PUT'])
# # @auth.login_required
# def cookies_put():
#     key = request.form.get('key', None)
#     cookies = request.form.get('cookies', None)
#     if not all([key,  cookies]):
#         return error(msg='key or cookies is empty!')
#     REDIS_MODEL.update_one_cookies(key=key,  value=cookies)
#     return ok()

# # 删除一条cookies
# @app.route('/cookies', methods=['DELETE'])
# # @auth.login_required
# def cookies_delete():
#     key = request.form.get('key', None)
#     if not key:
#         return error(msg='key  is empty!')
#     REDIS_MODEL.delete_one_cookies(key=key)
#     return ok()


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
