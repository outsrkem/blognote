# 页码函数
import os


def pagination(page, total):
    # 传递2个参数，page为当前页，total为总页数
    page_range = [x for x in range(int(page) - 2, int(page) + 3) if 0 < x <= total]
    # 加上省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if total - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页,total 为总页数，在数据库获取
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != total:
        page_range.append(total)
    # 返回处理好的页码，总50页，当前30页，格式如下
    # [1, '...', 28, 29, 30, 31, 32, '...', 50]
    return page_range


def loginfo():
    DB_USERNAME = 'blognote'
    DB_PASSWORD = '123456'
    try:
        DB_HOSTIP = os.environ['DB_HOSTIP']
    except Exception:
        DB_HOSTIP = '10.10.10.24'
    DB_PORT = '3306'
    DB_DATABASE = 'blognote'
    return DB_USERNAME, DB_PASSWORD, DB_HOSTIP, DB_PORT, DB_DATABASE
print('数据库连接信息--->{用户名：%s,密码：%s,数据库IP：%s,数据库端口：%s,数据库名称：%s}'%loginfo())

