from sqlalchemy import Table, func
from common.database import dbconnect
from module.users import Users
dbsession, md, DBase = dbconnect()


class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    # 查询所有文章
    def fine_all(self):
        result = dbsession.query(Article).all()

    # 按id查询
    def find_by_id(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        return row

    #
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).\
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1).\
            order_by(Article.articleid.asc()).limit(count).offset(start).all()
        return result
    # filter(Article.hidden==0, Article.drafted==0, Article.checked==1) 过滤不显示的文章

    # 统计当前文章总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).count()
        return count

    # 根据文章类别获取文章
    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid)\
            .filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.type==type)\
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result
    # 根据文章类别获取文章总数量
    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hidden==0,
                                                Article.drafted==0,
                                                Article.checked==1,
                                                Article.type==type).count()

        return count

    # 根据文章标题进行模糊搜索
    def fine_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid)\
            .filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.headline.like('%' + headline + '%'))\
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result
    # 统计分页数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hidden==0,
                                                Article.drafted==0,
                                                Article.checked==1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

# 右侧栏数据
    # 最新文章
    def find_list_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1).\
            order_by(Article.articleid.desc()).limit(9).all()
        return result
    # 最多阅读
    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1).\
            order_by(Article.readcount.desc()).limit(9).all()
        return result
    # 特别推荐,如果超过9篇， 可以考虑order by rand() 随机显示
    # SELECT * FROM article ORDER BY RAND() LIMIT 10;
    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1,Article.recmmended==1).\
            order_by(func.rand()).limit(9).all()
        return result
    # 一次性返回3个数据
    def find_last_most_recommended(self):
        last = self.find_list_9()
        most = self.find_most_9()
        recommended = self.find_recommended_9()
        return last, most, recommended








