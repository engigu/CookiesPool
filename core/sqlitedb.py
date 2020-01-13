from sqlalchemy import func
from  sqlalchemy.sql.expression import func as expression_func


from core.model import Site, StoreCookies, session_scope
from core.status import TaskStatus, ReturnStatus
from core.utils import Utils
from core.exceptions import *


class SQLiteModel:

    def query_all_sites(self):
        with session_scope() as s:
            sites = s.query(Site).filter(Site.status == TaskStatus.ok).all()
            return sites

    # 查询site指定的cookies
    def query_site_cookies(self, site, page=1, size=20):
        page = page if page else 1
        size = size if size else 20
        with session_scope() as s:
            query = s.query(StoreCookies).join(
                Site,
                Site.id == StoreCookies.site_id
            ).filter(
                Site.site == site
            ).order_by(
                StoreCookies.id.asc()
            )

            total = s.execute(
                query.with_labels().statement.with_only_columns(
                    [func.count(1)])
            ).scalar()
            cookies = query.offset(page*(page-1)).limit(size).all()
            return total, cookies

    def get_one_site(self, site):
        with session_scope() as s:
            site = s.query(Site).filter(Site.site == site).first()
            return site

    # 添加或者更更新一个site信息
    def add_one_site(self, site_dict):
        with session_scope() as s:
            old_record = s.query(Site).filter(Site.site == site_dict['site'])
            if not old_record.first():
                site = Site(
                    **site_dict
                )
                s.add(site)
            else:
                site_dict['modified'] = Utils.now(return_datetime=True)
                old_record.update(site_dict)

    def add_one_cookies(self, cookies_dict):
        site = cookies_dict['site']
        with session_scope() as s:
            old_record = s.query(Site).filter(
                Site.site == site
            ).first()

            if not old_record:
                raise SQLDataNULL(f'has no site record: {site}')
            cookies_dict.pop('site')
            c = StoreCookies(**cookies_dict)
            s.add(c)
            # c.cookies_name = ''
            c.site_id = old_record.id
            s.flush()
            if not cookies_dict.get('cookies_name', None):
                c.cookies_name = f'{site}:cookies:{c.id}'

    def update_one_cookies(self, cookies_id,  cookies: dict):
        with session_scope() as s:
            query = s.query(StoreCookies).filter(StoreCookies.id == cookies_id)
            if not query.first():
                raise SQLDataNULL('cookies do not exists!')
            cookies['modified'] = Utils.now(return_datetime=True)
            query.update(cookies)

    def delete_one_cookies(self,  cookies_id):
        with session_scope() as s:
            s.query(StoreCookies).filter(
                StoreCookies.id == cookies_id
            ).delete()

    def  get_one_cookies(self, site,  strategy='random'):
        # 返回一条cookies
        with session_scope() as s:
            if strategy=='random':
                cookies = s.query(StoreCookies).filter(
                    StoreCookies.status == TaskStatus.ok
                ).order_by(
                    expression_func.random()
                ).limit(1).first()
            else:
                cookies_query = s.query(StoreCookies).filter(
                    StoreCookies.status == TaskStatus.ok,
                ).order_by(StoreCookies.id.asc())
                
                cookies = cookies_query.filter(StoreCookies.return_order == ReturnStatus.not_return).first()

                if not bool(cookies):
                    # 全部已经返回了一遍
                    s.query(StoreCookies).filter(
                        StoreCookies.status == TaskStatus.ok,
                    ).update(
                        {'return_order': ReturnStatus.not_return}
                    )
                    s.flush()
                    cookies = cookies_query.filter(StoreCookies.return_order == ReturnStatus.not_return).first()
                else:
                    # 有这一轮还未返回过的cookies，返回并更改为返回过
                      s.query(StoreCookies).filter(
                          StoreCookies.id == cookies.id
                      ).update(
                          {'return_order': ReturnStatus.has_return}
                      )
                      s.flush()    
            return cookies

