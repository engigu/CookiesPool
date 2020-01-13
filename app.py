import datetime
import json
from flask import Flask, render_template, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuthreid

from core.sqlitedb import SQLiteModel
from core.model import init_sqlite
from core.utils import Utils
from config import Config
from api import API

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
@app.route('/cookies_api', methods=['GET'])
# @auth.login_required
def cookies_api():
    return jsonify(API)


# 查询所有的sites
@app.route('/cookies_all_sites', methods=['GET'])
# @auth.login_required
def cookies_all_sites():
    sites = SQL_MODEL.query_all_sites()
    sites = [s.site for s in sites]
    return jsonify({"total": len(sites), "sites":  sites})

# 查询指定的site
@app.route('/cookies_this_site', methods=['GET'])
# @auth.login_required
def cookies_this_site():
    site = request.args.get('site', None)
    if not site:
        return error(msg='site error')
    site = SQL_MODEL.get_one_site(site=site)
    return jsonify({"site": Utils.row2dict(site)})

# 查询指定的site
@app.route('/cookies_this_site', methods=['POST'])
# @auth.login_required
def cookies_this_site_post():
    site = request.form.get('site', None)
    if not site:
        return error(msg='site error')
    site_dict = dict(request.form)
    site = SQL_MODEL.add_one_site(site_dict=site_dict)
    return ok()


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

# 查询指定的site
@app.route('/cookies', methods=['GET'])
# @auth.login_required
def cookies_get():
    site = request.args.get('site', None)
    strategy = request.args.get('strategy', None)
    if not site:
        return error(msg='site error')
    if strategy:
        if strategy not in ['random', 'order']:
            return error(msg='strategy error')
    else:
        strategy = 'random'
    cookies = SQL_MODEL.get_one_cookies(site=site, strategy=strategy)
    return jsonify({"cookies": Utils.row2dict(cookies) if cookies else {}})


# 添加一条新的cookies
@app.route('/cookies', methods=['POST'])
# @auth.login_required
def cookies_post():
    site = request.form.get('site', None)
    cookies = request.form.get('cookies', None)
    cookies_name = request.form.get('cookies_name', None)
    if not all([site,  cookies]):
        return error(msg='site or cookies is empty!')
    cookies_dict = {
        'site': site,
        'cookies': cookies,
        'cookies_name': cookies_name,
    }
    SQL_MODEL.add_one_cookies(cookies_dict)
    return ok()

# 更新一条cookies
@app.route('/cookies', methods=['PUT'])
# @auth.login_required
def cookies_put():
    cookies_id = request.form.get('cookies_id', None)
    cookies = request.form.get('cookies', None)
    cookies_name = request.form.get('cookies_name', None)
    if not all([cookies_id,  cookies]):
        return error(msg='cookies_id or cookies is empty!')
    cookies_dict = {
        'cookies': cookies,
        'cookies_name': cookies_name
    }
    SQL_MODEL.update_one_cookies(cookies_id, cookies_dict)
    return ok()

# 删除一条cookies
@app.route('/cookies', methods=['DELETE'])
# @auth.login_required
def cookies_delete():
    cookies_id = request.args.get('cookies_id', None)
    if not cookies_id:
        return error(msg='cookies_id  is empty!')
    SQL_MODEL.delete_one_cookies(cookies_id=cookies_id)
    return ok()


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
