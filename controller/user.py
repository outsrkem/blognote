from flask import Blueprint, make_response, session
from common.utility import ImageCode
user = Blueprint('user', __name__)

# 图片验证码接口
# http://127.0.0.1:5000/vcode
@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response
    # return ('asdad')