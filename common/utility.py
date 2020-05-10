import random, string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


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
        print(''.join(list))
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
        im = Image.new('RGB', (width, height),'white')   # 无背景
        # im.show()  # 临时调试，打开图片
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 6, width, height)
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