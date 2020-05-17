from flask import session, request
from sqlalchemy import Table
from common.database import dbconnect
import time

from common.utility import model_join_list
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

    # 根据文章编号显示评论
    def find_by_articleid(self, articleid):
        result = dbsession.query(Comment).filter_by(articleid=articleid, hidden=0, replyid=0).all()
        return result

    # 根据用户编号查询当天是否超过5条的评论的限制
    def check_limit_per_5(self):
        start = time.strftime('%Y-%m-%d 00:00:00')  # 当天开始时间
        end = time.strftime('%Y-%m-%d 23:59:59')  # 当天结束时间
        result = dbsession.query(Comment).filter(Comment.userid == session.get('userid'),
                                                 Comment.createtime.between(start, end)).all()
        if len(result) >= 5:
            return True  # 表示今天不能再发表了
        else:
            return False

    # 查询评论与用户信息，注意评论也需要分页
    # [(Comment,Users),(Comment,Users)]
    def find_limit_with_user(self, articleid, start, count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid == Comment.userid) \
            .filter(Comment.articleid == articleid, Comment.hidden == 0) \
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    # Comment().install_comment('1','这是一这是一这是一这是一','127.0.0.1')
    # Comment().check_limit_per_5()
    # Comment.find_limit_with_user('19', '1','5')

    # 添加评论回复，使用原始评论的id为新评论的replyid字段进行关联。
    def install_reply(self, articleid, commentid, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=articleid,
                          content=content, ipaddr=ipaddr, replyid=commentid, createtime=now, updatetime=now)
        dbsession.add(comment)
        dbsession.commit()

    # 查原始评论与对应的用户信息，带分页参数
    def find_comment_with_user(self, articleid, start, count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid ==
                 Comment.userid).filter(Comment.articleid == articleid,
                 Comment.hidden == 0, Comment.replyid == 0)\
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    #查询回复评论，回复评论不需要分页
    def find_reply_with_user(self, replyid):
        result = dbsession.query(Comment, Users).join(Users, Users.userid ==
                 Comment.userid).filter(Comment.replyid == replyid, Comment.hidden == 0).all()
        return result

    # 根据原始评论和回复评论生成一个关联列表
    def get_comment_user_list(self, articleid, start, count):
        result = self.find_comment_with_user(articleid,start,count)
        comment_list = model_join_list(result)  #原始评论的连接结果
        for comment in comment_list:
            # 查询原始评论的回复评论，并转换为列表保存在comment_list中
            result = self.find_reply_with_user(comment['commentid'])
            # 为comment_list 列表中的原始数据评论字典添加一个新key 叫 reply_list
            # 用于存储当前这条原始评论的所有回复评论，如果没有回复评论则列表值为空
            comment['reply_list'] = model_join_list(result)
        return comment_list  # 将新的数据结构返回给控制器接口

    # 查询某篇文章的原始评论总数量
    def get_count_by_article(self, articleid):
        count = dbsession.query(Comment).filter_by(articleid=articleid, hidden=0,replyid=0).count()
        return count











