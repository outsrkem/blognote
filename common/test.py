import random, string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class ImageCode:
    # 验证码颜色，值下字暗
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(32, 255)
        blue = random.randint(32, 128)
        return red, green, blue

    # 生成4位随机字符串
    def gen_text(self):
        list = random.sample(string.ascii_letters+string.digits,4)
        return ''.join(list)

    # 绘制干扰线
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2,height)
            draw.line(((x1,y1),(x2,y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width,height = 120, 50  #图片大小
        # im = Image.new('RGB', (width, height), 'black')  # 黑背景
        im = Image.new('RGB', (width, height),(137,169,163))   # 无背景
        # im.show()  # 临时调试，打开图片
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 3, width, height)
        im.show()

# ImageCode().draw_verify_code()

#!D:\linux\Python\flask\Scripts\python.exe
from sqlalchemy import create_engine, Column, Integer, String ,DateTime, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# engine = create_engine('mysql+mysqldb://root:123456@10.10.10.24/test',echo=False,pool_size=1000)

engine = create_engine('mysql+pymysql://blognote:123456@10.10.10.24/blognote',echo=True)
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
    '''
    result = dbsession.query(Users).all()
    for row in result:
        pass
        # print(row.userid)
    '''
    '''
    #返回元祖
    row = dbsession.query(Users.userid, Users.username).first()
    # print(row)
    '''
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
    '''
    '''

    # 删除操作
    row = dbsession.query(Users).filter_by(userid='5').delete()
    dbsession.commit()
    '''
    '''
    result = dbsession.query(Users).all
    # print(result)
    list = []
    for row in result:
        dict = {}
        for k,v in __dict__.items():
            if not k.startswith('_sa_instance_state'):
                dict[k] = v
        list.append(dict)
    print(list)
    '''