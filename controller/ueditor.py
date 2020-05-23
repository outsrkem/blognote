import time

from flask import Blueprint, abort, render_template, request, jsonify, session

from common.utility import compress_images
from config import BASE_DIR
import os

# print(fontfile)
ueditor = Blueprint('ueditor', __name__)


@ueditor.route('/uedit', methods=['GET', 'POST'])
def uedit():
    # 根据ueditor的接口定义规则
    # http://127.0.0.1:5000/uedit?action=config
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return render_template('config.json')
    elif request.method == 'POST' and request.args.get('action') == 'uploadimage':
        f = request.files['upfile']  # 获取前端图片文件数据
        filename = f.filename
        # 为上传的文件统一命名
        suffix = filename.split('.')[-1]  # 获取文件后缀
        newname = time.strftime('%Y%m%d%H%M%S.' + suffix)  # 以时间戳和后缀为新文件名
        f.save(os.path.join(BASE_DIR, "static", "upload", newname))  # 保存图片，使用os.path.join构建路径

        # 压缩图片，覆盖原始图片
        source = dest = os.path.join(BASE_DIR, "static", "upload", newname)
        compress_images(source, dest, 800)

        result = {}  # 构造响应数据，接口定义
        result['state'] = 'SUCCESS'
        result['url'] = f"/upload/{newname}"
        result['title'] = filename
        result['original'] = filename
        return jsonify(result)  # 以json格式响应

    # 编辑页面预览服务端图片
    elif request.method == 'GET' and param == 'listimage':
        list = []
        filelist = os.listdir(os.path.join(BASE_DIR, "static", "upload"))
        # 将所有的图片构建成可以访问的URL地址并添加到列表中
        for filename in filelist:
            if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
                list.append({'url': '/upload/%s' % filename})

        # 根据listimage接口规范构建响应数据
        result = {}
        result['state'] = 'SUCCESS'
        result['list'] = list
        result['start'] = 0
        result['total'] = 50
        return jsonify(result)
