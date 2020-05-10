from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time, random

dbsession, md ,DBase = dbconnect()

class Users(DBase):
    __table__ = Table('users', md , autoload=True)

    def find_by_username(self, username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result

    def do_register(self, username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]  #取昵称
        avatar = str(random.randint(1, 9)) # 从9张头像中取得一张
        user = Users(username=username, password=password, role='user', credit=50,
                     nickname=nickname, avatar=avatar + '.png', createtime=now, updatetime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    # credit可正可负
    def update_credit(self, credit):
        user = dbsession.query(Users).filter_by(userid=session.get('userid')).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()














