from telethon import TelegramClient
import socks
import asyncio
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

async def get_dialogs():
    image_count = 0
    async for dialog in client.iter_dialogs():
        if dialog.name is None:
            continue
        if "博彩" in dialog.name:
            print(f"{dialog.id}: {dialog.name}")
            image_count += await get_channel_messages(dialog.id)
    print(f"Total image count: {image_count}")

async def get_channel_messages(channel):
    print("Getting channel messages...")
    # 获取频道消息
    image_count = 0
    async for message in client.iter_messages(channel, limit=2000):
        # 将消息存入数据库
        with connection.cursor() as cursor:
            # 判断消息是否非空
            if message.text is None:
                continue
            # 判断消息内容是否已经存在
            sql = "SELECT * FROM `messages` WHERE `message`=%s"
            cursor.execute(sql, message.text)
            result = cursor.fetchone()
            if result is not None:
                continue
            # 插入消息
            if hasattr(message, 'photo'):
                image_count += 1
            sql = "INSERT INTO `messages` (`message`, `sender_id`) VALUES (%s, %s)"
            cursor.execute(sql, (message.text, message.sender_id))
            connection.commit()
    return image_count

loop = asyncio.get_event_loop()
loop.run_until_complete(get_dialogs())
client.disconnect()