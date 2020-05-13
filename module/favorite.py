from flask import session
from sqlalchemy import Table, func
from common.database import dbconnect
from module.users import Users
import time, random

dbsession, md, DBase = dbconnect()


class Favorite(DBase):
    __table__ = Table('favorite', md, autoload=True)

    # 插入文章收藏数据
    def install_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is not None: # 如果有这条记录，表示收藏过
            row.canceled = 0  # 0 表示收藏
        else: # 如果没有收藏过，直接收藏
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=articleid, userid=session.get('userid'),canceled=0,createtime=now,updatetime=now)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消收藏
    def cancel_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        row.canceled = 1
        dbsession.commit()

    # 判断是否已经被收藏
    def check_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return Favorite
        else:
            return True




















