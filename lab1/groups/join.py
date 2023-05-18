from telethon import TelegramClient, functions
import socks
import  asyncio

api_id = '23146739'
api_hash = 'afe4ee836338b640bb75a6d75f1c3d63'
session_name = 'my_session'

proxy = (socks.SOCKS5, '127.0.0.1', 1080)

# 创建 TelegramClient 对象
client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)

# 登录客户端
client.start()

# 读取line，加入群组
async def join_group():
    print("Joining groups...")
    with open('./urls4.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        print(line)
        try:
            await client(functions.channels.JoinChannelRequest(
                channel=line
            ))
            print("Joined!")
        except Exception as e:
            print(e)
            if "wait" in str(e):
                print("Waiting...")
                await asyncio.sleep(60)
                continue
            else:
                continue

loop = asyncio.get_event_loop()
loop.run_until_complete(join_group())
client.disconnect()
