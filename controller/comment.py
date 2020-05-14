from flask import Blueprint, request

from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.users import Users

commnet = Blueprint('comment',__name__)

@commnet.route('/comment',methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr

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
