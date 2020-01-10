import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_, distinct, TIMESTAMP, text, String
from contextlib import contextmanager

import sys
import os

sys.path.insert(0, os.path.abspath('../'))
from config import Config

Base = declarative_base()


#   {'cookies': '111111',
#  'check_url': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29',
# 'check_key': '<title>用户登录-58同城</title>', 'method': 'get', 'headers': {},
# 'modified_at': '2020-01-09 16:14:37', 'created_at': '2020-01-09 16:14:37', 'status': 0}


class Site(Base):
    __tablename__ = "site"
    id = Column(Integer, primary_key=True, autoincrement=True)  
    site = Column(String(64), server_default=text("''"))
    headers = Column(String(4096), server_default=text("''"))
    check_key = Column(String(2048), server_default=text("''"))
    check_url = Column(String(2048), server_default=text("''"))
    method = Column(String(128), server_default=text("''"))

    status = Column(Integer, server_default=text("0"))
    created = Column(TIMESTAMP,  server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class StoreCookies(Base):
    __tablename__ = "cookies"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    site_id = Column(Integer, nullable=False)
    cookies_name = Column(String(256), server_default=text("''"))
    cookies = Column(String(64), server_default=text("''"))

    status = Column(Integer, server_default=text("0"))
    created = Column(TIMESTAMP,  server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


engine = create_engine(Config.SQLITE_URI, echo=True)
session = sessionmaker(bind=engine)
SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def GetSession():
    return SessionType()


@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    pass
