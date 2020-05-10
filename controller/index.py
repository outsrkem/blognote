from flask import Blueprint, render_template, abort, jsonify, session, request
from module.article import Article
from module.credit import Credit
from module.users import Users
import math, re
import hashlib
from common.function import pagination #引用页码函数
index = Blueprint("index", __name__)

@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0, 10)
    total = math.ceil(article.get_total_count() / 10)   # 总页数
    # 首页页码直接为1 即可
    page = 1
    # 页码列表
    page_range = pagination(page, total)
    last, most, recommended = article.find_last_most_recommended()
    return render_template('index.html', result=result, page=page, page_range=page_range, total=total, last=last, most=most, recommended=recommended)


# 分页接口
@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_limit_with_users(start, 10)
    total = math.ceil(article.get_total_count() / 10)   # 获取总页数
    page_range = pagination(page, total)
    return render_template('index.html', result=result, page=page, total=total, page_range=page_range)

# 文章类别接口
@index.route('/type/<int:type>-<int:page>')
def classify(type, page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.get_count_by_type(type) / 10)

    return render_template('type.html',result=result, page=page, total=total, type=type)

# 搜索
@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 10:
        abort(404)
    start = (page - 1) * 10
    article = Article()
    result = article.fine_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)
    return render_template('search.html', result=result, page=page, total=total, keyword=keyword)

# 定义边侧栏数据接口，返回json格式
@index.route('/recommended')
def recommended():
    article = Article()
    # last, most, recommended ： 这是一个数据对象
    last, most, recommended = article.find_last_most_recommended()
    return jsonify(last, most, recommended)




@index.route('/user/reg', methods=['POST'])
def register():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()

    # 校验验证码
    print(ecode)
    if ecode != session.get('ecode'):
        return 'ecode-error'
    # 用户名和密码校验
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'
    # 校验用户名重复
    # elif len(user.find_by_username(username)) > 0:
    #     return 'user-repeated'
    else:
        # 注册
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_register(username, password)
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role
        # 跟新积分详情表
        Credit().inster_detail(type='用户注册', target='0', credit=50)
        return 'reg-pass'

