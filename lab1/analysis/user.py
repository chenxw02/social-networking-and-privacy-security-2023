import pymysql
from collections import Counter

connection = pymysql.connect(
    host='localhost',  # 数据库主机地址
    port=3306,  # 数据库端口号
    user='root',  # 数据库用户名
    password='Cxw20140503',  # 数据库密码
    db='telegram',  # 数据库名称
    charset='utf8mb4',  # 数据库字符集
)

# 读取数据库
with connection.cursor() as cursor:
    sql = "SELECT sender_id FROM messages"
    cursor.execute(sql)
    sender_ids = cursor.fetchall()

def extract_id(id):
    if id is not None:
        if id[0] == '-':
            return id[1:]
        return id
    return None

ids=[]
print('counting senders...')
for sender_id in sender_ids:
    ids += [extract_id(sender_id[0])]
sender_count = Counter(ids)
print(sender_count.most_common(10))

# 去除重复id
ids = list(set(ids))
print('counting unique senders...')
print(len(ids))