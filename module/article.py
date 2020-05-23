from flask import session
from sqlalchemy import Table, func
from common.database import dbconnect
from module.users import Users
import time

dbsession, md, DBase = dbconnect()


class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    # 查询所有文章
    def fine_all(self):
        result = dbsession.query(Article).all()

    # 按id查询文章
    def find_by_id(self, articleid):
        row = dbsession.query(Article, Users.nickname).join(Users,
                                                            Users.userid == Article.userid).filter(
            Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
            Article.articleid == articleid).first()
        return row

    #
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1). \
            order_by(Article.articleid.asc()).limit(count).offset(start).all()
        return result

    # filter(Article.hidden==0, Article.drafted==0, Article.checked==1) 过滤不显示的文章

    # 统计当前文章总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1).count()
        return count

    # 根据文章类别获取文章
    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type == type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类别获取文章总数量
    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.type == type).count()

        return count

    # 根据文章标题进行模糊搜索
    def fine_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                    Article.headline.like('%' + headline + '%')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 统计分页数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

    # 右侧栏数据
    # 最新文章
    # [(id, headline),(id, headline)] ,这样的结果可以直接被jsonify处理
    def find_list_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1). \
            order_by(Article.articleid.desc()).limit(9).all()
        return result

    # 最多阅读
    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1). \
            order_by(Article.readcount.desc()).limit(9).all()
        return result

    # 特别推荐,如果超过9篇， 可以考虑order by rand() 随机显示
    # SELECT * FROM article ORDER BY RAND() LIMIT 10;
    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.recmmended == 1). \
            order_by(func.rand()).limit(9).all()
        return result

    # 一次性返回3个数据
    def find_last_most_recommended(self):
        last = self.find_list_9()
        most = self.find_most_9()
        recommended = self.find_recommended_9()
        return last, most, recommended

    # 没阅读一次，阅读数加一
    def update_read_count(self, articleid):
        article = dbsession.query(Article).filter_by(articleid=articleid).first()
        article.readcount += 1
        dbsession.commit()

    # 用于显示上一篇和一下篇
    # 根据文章编号查询文章标题
    def find_headline_by_id(self, articleid):
        row = dbsession.query(Article.headline).filter_by(articleid=articleid).first()
        return row.headline

    # 获取当前文章的上一篇肯下一篇
    def find_prev_next_by_id(self, articleid):
        dict = {}
        # 查询比当前编号小的最大的一个(即上一篇)
        row = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                              Article.articleid < articleid).order_by(Article.articleid.desc()).limit(
            1).first()
        # 如果已经是第一篇，则上一篇也是当前文章
        if row is None:
            prev_id = articleid
        else:
            prev_id = row.articleid

        dict['prev_id'] = prev_id
        dict['prev_headline'] = self.find_headline_by_id(prev_id)

        # 查询比当前编号大的最小的一个（即下一篇）
        row = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                              Article.articleid > articleid).order_by(Article.articleid).limit(
            1).first()
        # 如果已经是最后一篇，则下一篇也是当前文章
        if row is None:
            next_id = articleid
        else:
            next_id = row.articleid
        dict['next_id'] = next_id
        dict['next_headline'] = self.find_headline_by_id(next_id)

        return dict

    # 增加回复次数
    def update_replycount(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        row.replycount += 1
        dbsession.commit()

    # 插入一篇新的文章
    def instert_article(self, type, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')
        print(type, headline, content, thumbnail, credit, drafted, checked)
        article = Article(userid=userid, type=type, headline=headline, content=content,
                          thumbnail=thumbnail, credit=credit, drafted=drafted,
                          checked=checked, createtime=now, updatetime=now)
        dbsession.add(article)
        dbsession.commit()
        return article.articleid  # 返回新文章的id，便于跳转
