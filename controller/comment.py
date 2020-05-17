from flask import Blueprint, request, session, jsonify

from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.users import Users

commnet = Blueprint('comment', __name__)


# 定义模块拦截器，修复没有登录也能调用接口的问题
@commnet.before_request
def before_commnet():
    if session.get('islogin') is None or session.get('islogin') != 'true':
        return 'not-login'


@commnet.route('/comment', methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    content = request.form.get('content').strip()
    if request.headers.getlist("X-Forwarded-For"):
        ipaddr = request.headers.getlist("X-Forwarded-For")[0]  # 获取请求头部的IP ，用于nginx代理后获取用户的源ip
    else:
        ipaddr = request.remote_addr  # 获取请求ip地址

    comment = Comment()
    '''
    # 简单检验文章评论
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    
    if not comment.check_limit_per_5():
        try:
            comment.install_comment(articleid, content, ipaddr)
            Credit().inster_detail(type='添加评论', target=articleid, credit=2)
            Users().update_credit(2)  # 给用户添加积分2分
            Article().update_replycount(articleid)  # 对文章评论数加一
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        return 'add-limit'
    '''
    # 简单检验文章评论
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    if not comment.check_limit_per_5():
        try:
            comment.install_comment(articleid, content, ipaddr)
            Credit().inster_detail(type='添加评论', target=articleid, credit=2)
            Users().update_credit(2)  # 给用户添加积分2分
            Article().update_replycount(articleid)  # 对文章评论数加一
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        try:
            comment.install_comment(articleid, content, ipaddr)
            Credit().inster_detail(type='添加评论', target=articleid, credit=2)
            # Users().update_credit(2)  # 如果已经超过5天评论 ，不给用户添加积分
            Article().update_replycount(articleid)  # 对文章评论数加一
            return 'add-pass'
        except:
            return 'add-fail'


@commnet.route('/reply', methods=['POST'])
def reply():
    articleid = request.form.get('articleid')
    commentid = request.form.get('commentid')
    content = request.form.get('content').strip()
    if request.headers.getlist("X-Forwarded-For"):
        ipaddr = request.headers.getlist("X-Forwarded-For")[0]  # 获取请求头部的IP ，用于nginx代理后获取用户的源ip
    else:
        ipaddr = request.remote_addr  # 获取请求ip地址

    # 简单检验文章评论
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment = Comment()
    if not comment.check_limit_per_5():
        try:
            comment.install_reply(articleid, commentid, content, ipaddr)
            Credit().inster_detail(type='回复评论', target=articleid, credit=2)
            Users().update_credit(2)  # 给用户添加积分2分
            Article().update_replycount(articleid)  # 对文章评论数加一
            return 'reply-pass'
        except:
            return 'reply-fail'
    else:
        try:
            comment.install_reply(articleid, commentid, content, ipaddr)
            Credit().inster_detail(type='回复评论', target=articleid, credit=2)
            # Users().update_credit(2)  # 如果已经超过5天评论 ，不给用户添加积分
            Article().update_replycount(articleid)  # 对文章评论数加一
            return 'reply-pass'
        except:
            return 'reply-fail'


@commnet.route('/comment/<int:articleid>-<int:page>')
def comment_page(articleid, page):
    start = (page - 1) * 4
    comment = Comment()
    list = comment.get_comment_user_list(articleid, start, 4)
    return jsonify(list)
