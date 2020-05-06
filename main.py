from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os

# import pymysql  # ImportError: No module named 'MySQLdb
# pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数，用于session ID

# 使用flask_sqlalchemy 集成方式连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@10.10.10.24/blognote?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 实例化db对象


# 定制404返回页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html')



# 500
@app.errorhandler(500)
def server_error(error):
    return render_template('error-500.html')

@app.context_processor
def gettype():
    type = {
        '1': 'PHP开发',
        '2': 'java开发',
        '3': 'Python开发',
        '4': 'Web前端',
        '5': '测试开发',
        '6': '数据科学',
        '7': '网络安全',
        '8': '蜗牛杂谈'
    }
    return dict(article_ytpe=type)

@app.route('/aaa')
def aaa():
    return 'gello .......'


if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)  # 把蓝图注册到app中


    app.run(debug=True)

#   flask run --host=0.0.0.0
