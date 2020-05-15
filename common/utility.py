import random, string, os
from io import BytesIO
from main import STATIC_DIRS
from PIL import Image, ImageFont, ImageDraw

# 获取字体路径，用于验证码图片生成
fontfile = os.path.join(STATIC_DIRS, "font", "arial.ttf")
# print(fontfile)

class ImageCode:
    # 验证码颜色，值下字暗
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(32, 255)
        blue = random.randint(32, 128)
        return red, green, blue

    # 生成4位随机字符串
    def gen_text(self):
        list = random.sample(string.ascii_letters+string.digits,4)
        return ''.join(list)

    # 绘制干扰线
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2,height)
            draw.line(((x1,y1),(x2,y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width,height = 120, 50  #图片大小
        # im = Image.new('RGB', (width, height), 'black')  # 黑背景
        # im = Image.new('RGB', (width, height),(137,169,163))   # 自定义背景
        im = Image.new('RGB', (width, height), 'white')   # 白背景
        # im.show()  # 临时调试，打开图片
        font = ImageFont.truetype(font=fontfile, size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 3, width, height)
        return im, code
        # im.show()
# 调试
# ImageCode().gen_text()
# ImageCode().draw_verify_code()
    #     生成图片验证码并返回控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring
# ImageCode().get_code()

# 邮件验证码：
# 1. 需要有支持邮件发送或接受的模块。
# 2. 需要一台支持邮件发送的邮箱服务器，（使用QQ邮箱）：收件人，发件人，服务器地址，端口，账号
# 3.校验。
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def send_email(receiver, ecode):
    sender = 'Yonge <xhdascnf@126.com>'
    # receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = f"<br/>欢迎注册博客，验证码为：" \
        f"<span style='color: red; font-size: 20px;'>{ecode}</span><br/> "\
        f"请复制到注册窗口完成注册，感谢您的支持。<br/>"
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('博客验证码', 'utf-8')
    message['From'] = sender  # 发送者
    message['To'] = receiver# 接收者

    subject = 'Python SMTP 邮件测试'



    smtpObj = SMTP_SSL('smtp.126.com')
    smtpObj.login(user='xhdascnf@126.com', password='HKFKVIQTMAWGGBVD')
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()

# 生成6位随机邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    # str = 'asdasd'
    return ''.join(str)

# code = gen_email_code()
# print(code)
# send_email('981789763@qq.com', code)