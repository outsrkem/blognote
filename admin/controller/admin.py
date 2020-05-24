from datetime import datetime

from flask import Blueprint, abort, render_template, request, session, jsonify
from module.article import Article
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/admin')
def mydmin():
    return render_template('admin/admin.html')

# 获取个人文章
@admin.route('/myarticle')
def Myarticle():
    result = Article().get_my_article()
    print(result)
    return jsonify(result)
# 删除一篇文章
@admin.route('/deltet',methods=['POST'])
def Delete_article():
    articleid = request.form.get('articleid')
    result = Article().delete_my_article(articleid)
    return result