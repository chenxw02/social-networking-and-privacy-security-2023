from telethon import TelegramClient, events, sync, functions
import socks
import  asyncio
import pymysql

api_id = '23146739'
api_hash = 'afe4ee836338b640bb75a6d75f1c3d63'
session_name = 'my_session'

# 连接mysql
connection = pymysql.connect(
    host='localhost',  # 数据库主机地址
    port=3306,  # 数据库端口号
    user='root',  # 数据库用户名
    password='Cxw20140503',  # 数据库密码
    db='telegram',  # 数据库名称
    charset='utf8mb4',  # 数据库字符集
    cursorclass=pymysql.cursors.DictCursor  # 返回结果以字典形式展示
)

proxy = (socks.SOCKS5, '127.0.0.1', 1080)

# 创建 TelegramClient 对象
client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)

# 登录客户端
client.start()

# 筛选博彩频道
async def get_groups():
    print("Getting groups...")
    count = 0
    async for dialog in client.iter_dialogs():
        if dialog.name is None:
            continue
        if "博" or "博彩" in dialog.name:
            count += 1
            entity = await client.get_entity(dialog.name)
            if entity is None:
                continue
            try:
                members = await client.get_participants(entity)
                #写入数据库
                print(f"{dialog.name}: {len(members)}")
                with connection.cursor() as cursor:
                    #判断是否已经存在
                    sql = "SELECT * FROM `groups` WHERE `group_name`=%s"
                    cursor.execute(sql, dialog.name)
                    result = cursor.fetchone()
                    if result is not None:
                        continue
                    sql = "INSERT INTO `groups` (`group_name`, `member_count`) VALUES (%s, %s)"
                    cursor.execute(sql, (dialog.name, len(members)))
                    connection.commit()
            except Exception as e:
                print(e)
                print(f"{dialog.name}: 0")
                    #写入数据库
                with connection.cursor() as cursor:
                    #判断是否已经存在
                    sql = "SELECT * FROM `groups` WHERE `group_name`=%s"
                    cursor.execute(sql, dialog.name)
                    result = cursor.fetchone()
                    if result is not None:
                        continue
                    sql = "INSERT INTO `groups` (`group_name`, `member_count`) VALUES (%s, %s)"
                    cursor.execute(sql, (dialog.name, 0))
                    connection.commit()
                continue
    print(count)

# 只获取频道名字
async def get_simple_groups():
    print("Getting simple groups...")
    async for dialog in client.iter_dialogs():
        if dialog.name is None:
            continue
        if dialog.id is None:
            continue
        if '博彩' in dialog.name:
            print(f"{dialog.name}")
            with connection.cursor() as cursor:
                # 判断是否已经存在
                sql = "SELECT * FROM `simple_groups` WHERE `group_id`=%s"
                cursor.execute(sql, dialog.id)
                result = cursor.fetchone()
                if result is not None:
                    continue
                sql = "INSERT INTO `simple_groups` (`group_name`, `group_id`) VALUES (%s, %s)"
                cursor.execute(sql, (dialog.name, dialog.id))
                connection.commit()


loop = asyncio.get_event_loop()
# loop.run_until_complete(get_groups())
loop.run_until_complete(get_simple_groups())
client.disconnect()