from flask import Flask, render_template, abort, send_from_directory, request, session, Blueprint
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

# 定义全局拦截器，实现自动登录
@app.before_request
def before():
    url = request.path
    pass_list = ['/reg', '/login', '/vcode', '/session']
    if url in pass_list or url.endswith('js') or url.endswith('.css') or \
            url.endswith('.png') or url.endswith('.jpg') or url.endswith('.ico'):
        pass
    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            user = Users()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password==password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role


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
    # return 'gello .......'

    return render_template('article-user.html', result=8)

# 添加文件下载功能
@app.route("/download/<filename>")
def download(filename):
    directory = os.getcwd()
    return send_from_directory(r"download", filename=filename, as_attachment=True)


# 接口测试
@app.after_request
def foot_log(environ):
    print("访问接口--->",request.path)
    return environ


 # 一定要在db后面
# from controller.user import *

if __name__ == '__main__':
    from controller.index import *
    from controller.user import *
    from controller.article import *
    from controller.favorite import *
    from controller.comment import *

    app.register_blueprint(index)  # 把蓝图注册到app中
    # app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(favorite)
    app.register_blueprint(commnet)


    app.run(debug=True)

#   flask run --host=0.0.0.0
