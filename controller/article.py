import math

from flask import Blueprint, abort, render_template, request, session

from common.utility import parse_image_url, generate_thumb
from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.favorite import Favorite
from module.users import Users

article = Blueprint('article', __name__)


# 阅读文章
@article.route('/type/article/<int:articleid>')
@article.route('/search/<int:articleid>')
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
    print()

    # ，如果没有消耗过积分显示一半文章
    payed = Credit().check_payed_article(articleid)
    position = 0
    if not payed and dict['credit'] !=0: # 此处有问题，需要先判断是否消耗积分(已修复)，但是去过只有结尾有才有 </p>标签会报错。
        content = dict['content']
        # print(content)
        temp = content[0:int(len(content) / 2)]
        # print(temp)
        position = temp.rindex('</p>') + 4  # 获取文章</p>标签的位置
        dict['content'] = temp[0:position]
        # print(dict['content'])
    Article().update_read_count(articleid)  # 阅读次数加1
    is_favorite = Favorite().check_favorite(articleid)  # 检测文章是否被收藏
    # print('检测文章是否被收藏 %s'%is_favorite)
    # 获取当前文章的上一篇和下一篇
    prev_next = Article().find_prev_next_by_id(articleid)

    # 显示当前文章对应的评论
    # comment_user = Comment().find_limit_with_user(articleid,0,50) # 此条没有回复评论
    comment_list = Comment().get_comment_user_list(articleid, 0, 4)
    # for i in comment_list:
    #     print(i)
    count = Comment().get_count_by_article(articleid)
    total = math.ceil(count / 4)

    return render_template('article-user.html', article=dict, position=position, payed=payed,
                           is_favorite=is_favorite, prev_next=prev_next, comment_list=comment_list, total=total)


'''
评论和回复评论的数据结构
[
    {'content': '这是www@baidu.com 的评论','reply_list': 
        [
            {
                'content': '这是回复文章id为1的回复--4444'    
            }
            {
                'content': '这是回复文章id为1的回复--4444'    
            }
        ]
    }
]
'''


# 消耗积分的文章展示文章剩余内容，虽然这个接口不显示，但是还要处理，已防绕开前端界面被直接调用
@article.route('/article/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[position:]  # 获取文章</p>标签的位置后面胡内容

    # 如果已经消耗积分，则不再扣除
    payed = Credit().check_payed_article(articleid)  # 查询是否已经消耗积分
    if not payed:
        # 添加积分明细
        Credit().inster_detail(type='阅读文章', target=articleid, credit=-1 * result[0].credit)
        # 减少用户表胡剩余积分
        Users().update_credit(credit=-1 * result[0].credit)
    return content



# 发布文章界面
@article.route('/prepost')
def add_prepost():
    return render_template('post-user.html')

# 发布文章接口
@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type = int(request.form.get('type'))
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    if session.get('userid') is None:
        print(session.get('userid'))
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'editor':  # 编辑者可编辑
            url_list = parse_image_url(content)
            if len(url_list) > 0:
                thumbnail = generate_thumb(url_list)
            else:  # 如果文章中没有图片，则随机指定一张
                # thumbname = '%d.png' % type
                thumbnail = '1.png'
            try:
                id = Article().instert_article(type=type, headline=headline, content=content, thumbnail=thumbnail,
                                               credit=credit, drafted=drafted, checked=checked)
                return str(id)
            except Exception as e:
                return 'post-fail'
            # 如果角色不是作者，则只能投稿
        elif checked == 1:
            return 'perm-denied1'
        else:
            return 'perm-denied2'
