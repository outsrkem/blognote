from flask import Blueprint, make_response, session, request
from common.utility import ImageCode, gen_email_code, send_email
import re


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

@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    print(email)
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code() # 获取到验证码
    try:
        send_email(email, code)
        session['ecode'] = code # 保存验证码
        print(code)
        return 'send-pass'
    except:
        return 'send-fail'
