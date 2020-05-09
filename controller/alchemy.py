from sqlalchemy import create_engine, Column, Integer, String ,DateTime, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# engine = create_engine('mysql+mysqldb://root:123456@10.10.10.24/test',echo=False,pool_size=1000)

engine = create_engine('mysql+pymysql://root:123456@10.10.10.24/blognote',echo=True)
# echo=True  打印SQL语句
DBsession = sessionmaker(bind=engine)
dbsession = scoped_session(DBsession)  # 线程安全
Base = declarative_base()
md = MetaData(bind=engine)  # 自动加载表结构

"""
# 定义模型
class User(Base):
    __tablename__ = 'users'
    # 直接创建表结构
    userid = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(32))
    nickname = Column(String(30))
    qq = Column(String(15))
    role = Column(String(10))
    credit = Column(Integer)
User.metadata.create_all(engine) # 创建表
"""
class Users(Base):
    __table__ = Table('users', md, autoload=True)

# class Article(Base):
#     __table__ = Table('article', md, autoload=True)


if __name__ == '__main__':
    result = dbsession.query(Users).all()
    for row in result:
        print(row.userid)

    #返回元祖
    row = dbsession.query(Users.userid, Users.username).first()
    print(row)

    '''
    # 添加数据
    user = Users(username='yong5.com',password='123456!@#$%', role='user',credit=5)
    dbsession.add(user)
    dbsession.commit()
    '''
    '''
    # 删除和更新，先查询出来，在操作
    row = dbsession.query(Users).filter_by(userid='2').first()
    print(row)
    print(row.username)
    row.username = 'www.baidu.com'
    dbsession.commit()
    '''
    try:
        # 删除和更新，先查询出来，在操作
        row = dbsession.query(Users).filter_by(userid='1').first()
        print(row)
        print(row.username) # 如果没有记录会报错
        row.username = 'www.baidu.com'
        dbsession.commit()
        print('更新成功')
    except:
        print('没有记录,更新失败')

    # 删除操作
    row = dbsession.query(Users).filter_by(userid='5').delete()
    dbsession.commit()

    # 把模型对象转换为json对象
    result = dbsession.query(Users).all()
    print(result)
    list = []
    for row in result:
        dict = {}
        for k,v in row.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                dict[k] = v
            list.append(dict)
    print(list)