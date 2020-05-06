from flask import Blueprint, render_template, abort
from module.article import Article
import math
index = Blueprint("index", __name__)

def pagination(page, total):
    # 传递2个参数，page为当前页，total为总页数
    page_range = [x for x in range(int(page) - 2, int(page) + 3) if 0 < x <= total]
    # 加上省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if total - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页,total 为总页数，在数据库获取
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != total:
        page_range.append(total)
    # 返回处理好的页码，总50页，当前30页，格式如下
    # [1, '...', 28, 29, 30, 31, 32, '...', 50]
    return page_range

@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0, 3)
    total = math.ceil(article.get_total_count() / 3)   # 总页数
    # 首页页码直接为1 即可
    page = 1
    # 页码列表
    page_range = pagination(page, total)
    last, most, recommended = article.find_last_most_recommended()
    return render_template('index.html', result=result, page=page, page_range=page_range, total=total, last=last, most=most, recommended=recommended)


# 分页接口
@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 3
    article = Article()
    result = article.find_limit_with_users(start, 3)
    total = math.ceil(article.get_total_count() / 3)   # 获取总页数
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
