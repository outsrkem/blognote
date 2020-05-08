from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql  # ImportError: No module named 'MySQLdb
from common.function import loginfo

pymysql.install_as_MySQLdb()
app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数，用于session ID

# 使用flask_sqlalchemy 集成方式连接数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blognote:123456@10.10.10.24/blognote?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % loginfo()
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

# 自定义truncate过滤器
def mytruncate(s, length, end='...'):
    # 中文定义为1个字符，英文为0.5个字符
    # 遍历整个字符串，获取ASCII码，大于 128或256，则为英文
    #否则是中文
    count = 0
    new = ''
    for c in s:
        new += c # 没循环一次，将一个字符串添加到new后面
        if ord(c) <= 128:
            count +=0.5
        else:
            count +=1
        if count > length:
            break

    return new + end
app.jinja_env.filters.update(truncate=mytruncate)


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



from controller.index import * # 一定要在db后面

if __name__ == '__main__':
    app.register_blueprint(index)  # 把蓝图注册到app中

    app.run(debug=True, host='0.0.0.0')

#   flask run --host=0.0.0.0
