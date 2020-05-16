import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect


dbsession, md, DBase = dbconnect()


class Loginrecords(DBase):
    __table__ = Table('loginrecord', md, autoload=True)

    # 用户登录记录
    def loginrecord(self, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        loginrecord = Loginrecords(userid=session.get('userid'), logipaddr=ipaddr, createtime=now)
        dbsession.add(loginrecord)
        dbsession.commit()

# Loginrecords().loginrecord("128.0.0.1")