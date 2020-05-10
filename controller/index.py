from flask import Blueprint, render_template, abort, jsonify, session, request
from module.article import Article
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



