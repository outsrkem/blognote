from flask import session, request
from sqlalchemy import Table
from common.database import dbconnect
import time

from module.users import Users

dbsession, md, DBase = dbconnect()


class Comment(DBase):
    __table__ = Table("comment", md, autoload=True)

    # 新增一条评论
    def install_comment(self, articleid, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid,
                          content=content, ipaddr=ipaddr, createtime=now, updatetime=now)
        dbsession.add(comment)
        dbsession.commit()

    # 新增回复

    #根据文章编号显示评论
    def find_by_articleid(self, articleid):
        result = dbsession.query(Comment).filter_by(articleid=articleid, hidden=0, replyid=0).all()
        return result

    # 根据用户编号查询当天是否超过5条的评论的限制
    def check_limit_per_5(self):
        start = time.strftime('%Y-%m-%d 00:00:00') # 当天开始时间
        end = time.strftime('%Y-%m-%d 23:59:59')  #当天结束时间
        result = dbsession.query(Comment).filter(Comment.userid==session.get('userid'),
                    Comment.createtime.between(start,end)).all()
        if len(result) >= 5:
            return True  # 表示今天不能再发表了
        else:
            return False

    # 查询评论与用户信息，注意评论也需要分页
    # [(Comment,Users),(Comment,Users)]
    def find_limit_with_user(self,articleid,start,count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
            .filter(Comment.articleid == articleid, Comment.hidden == 0) \
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

# Comment().install_comment('1','这是一这是一这是一这是一','127.0.0.1')
# Comment().check_limit_per_5()
# Comment.find_limit_with_user('19', '1','5')













