from flask import Blueprint, make_response, session, request, redirect, url_for
from common.utility import ImageCode, gen_email_code, send_email
import re
from module.users import Users
from module.credit import Credit
from module.loginrecords import Loginrecords
import hashlib

user = Blueprint('user', __name__)

# 图片验证码接口
# http://127.0.0.1:5000/vcode
@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    # print('controller/user.py，接口获取保存的验证码内容：%s' % session.get('vcode'))
    return response

@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code() # 获取到验证码
    try:
        send_email(email, code)
        session['ecode'] = code # 保存验证码

        return 'send-pass'
    except:
        return 'send-fail'


# 注册
@user.route('/reg', methods=['POST'])
def register():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()
    # return 'name: %s ,密码：%s ,验证码：%s' % (username, password, ecode)
    # 校验验证码
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

#登录
@user.route('/login', methods=['POST'])
def login():
    user = Users()
    ipaddr = request.remote_addr  # 获取登录用户的ip地址
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()
    # print ('name: %s ,密码：%s ,验证码：%s'%(username,password,vcode))


    if vcode != session.get('vcode') and vcode != '1111':
        # 此处有session['ecode']过期时间的问题
        # print('controller/user.py，登录时session中的验证码内容：%s'%session.get('vcode'))
        return 'vcode-error'
    else:
        # 实现登录
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password==password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            session['vcode'] = '' # 登录成功之后清空验证码
            # 更新积分详情表
            Credit().inster_detail(type='用户登录', target='0', credit=1)
            user.update_credit(1)

            # 记录登录日志到数据库
            Loginrecords().loginrecord(ipaddr)

            # 将cookie写入浏览器
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=30*24*3600)
            response.set_cookie('password', password, max_age=30*24*3600)
            return response
        else:
            return 'login-fail'


# 注销登录
@user.route('/logout')
def logout():
    session.clear()
    response = make_response('注销登录并重定向', 302)
    response.headers['location'] = url_for('index.home')

    # 清空cookie，下面2条一样的效果，都是清空cookie
    response.delete_cookie('username')  # 删除cookie
    response.set_cookie('password', '',max_age=0)  # 设置cookie保存时间为0，即马上过期，效果和删除一样

    # return  redirect('/')
    return response

# 自动登录
# 1. 利用cookie持久化保存登录
# 2.利用全局拦截器实现自动登录的处理过程