from flask import Blueprint, abort, render_template
from module.article import Article

article = Blueprint('article', __name__)



@article.route('/type/article/<int:articleid>')
@article.route('/article/<int:articleid>')
def read(articleid):
    try:
        result = Article().find_by_id(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)
    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    print(dict)
    dict['nickname'] = result.nickname

    # 显示一半文章
    content = dict['content']
    temp = content[0:int(len(content)/4)]
    position = temp.rindex('</p>') + 4
    dict[content]=temp[0:position]

    Article().update_read_count(articleid)
    return render_template('article-user.html', article=dict)
