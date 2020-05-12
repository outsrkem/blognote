from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()


class Credit(DBase):
    __table__ = Table('credit', md, autoload=True)

    def inster_detail(self, type, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'), category=type, target=target, credit=credit, createtime=now,
                        updatetime=now)
        print(session.get('userid'))
        dbsession.add(credit)
        dbsession.commit()

    # 判断用户是否已经消耗积分
    def check_payed_article(self, articleid):
        result = dbsession.query(Credit).filter_by(userid=session.get('userid'), target=articleid).all() #返回的是一个列表
        print(result)
        if len(result) > 0:
            return True
        else:
            return False


# if __name__ == '__main__':
#     Credit().inster_detail(type='用户注册', target='0', credit=50)
