from telethon import TelegramClient, events, sync, functions
import socks
import  asyncio
import pymysql

api_id = '23146739'
api_hash = 'afe4ee836338b640bb75a6d75f1c3d63'
session_name = 'my_session'

proxy = (socks.SOCKS5, '127.0.0.1', 1080)

# 创建 TelegramClient 对象
client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)

# 登录客户端
client.start()

async def get_dialogs():
    count = 0
    print("Getting dialogs...")
    async for dialog in client.iter_dialogs():
        if dialog.name is None:
            continue
        if '博彩' in dialog.name:
            count += 1
    print(f"Total: {count}")

loop = asyncio.get_event_loop()
loop.run_until_complete(get_dialogs())