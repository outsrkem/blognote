import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(host='10.10.10.24',port=3306,user='root',password='123456',
                     charset='utf8', database='test',autocommit=False)
print(conn.get_server_info()) # 输出版本，则连接成功

cursor = conn.cursor(DictCursor)
sql = "select * from userinfo"
cursor.execute(sql)
result = cursor.fetchall()

print(result[9]['email'])
cursor.close()
conn.close()