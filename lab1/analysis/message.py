import pymysql
import jieba
import re
from collections import Counter

def remove_punctuations(text):
    # 剔除所有的标点符号
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '', text)

def extract_domain(url):
    if 'com' not in url:
        return None
    pattern = r'(?<=//)(.*?)(?=[/.])'
    match = re.search(pattern, url)
    if match:
        if 'www' not in match.group(0):
            return match.group(0)+'.com'
        return None
    
def extract_id(id):
    if id is not None:
        if id[0] == '-':
            return id[1:]
        return id
    return None

# 连接mysql
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
    # 选择需要读取的表
    sql = "SELECT message FROM messages"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有结果
    results = cursor.fetchall()

    sql = "SELECT sender_id FROM messages"

    cursor.execute(sql)

    sender_ids = cursor.fetchall()

categories = ['游戏', '电竞', '棋牌', '体育', '彩票']
sports = ['CBA', 'NBA', '英雄联盟', '英超', '西甲', '法甲', '西乙']
benefits = ['送', '礼金', '优惠', '红包', '免费', '活动', '佣金']

split_pattern = re.compile('[，、。？！. \, \n]')
url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
mention_pattern = re.compile('@(\w+)')
VS_pattern = re.compile(r'([\u4e00-\u9fa5]+)\s*VS\s*([\u4e00-\u9fa5]+)')
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

words = []
words_ignored = []
cash = []
urls = []
mentions = []
teams = []
emojis = []
for result in results:
    content = remove_punctuations(result[0])
    words += jieba.cut(content)
    words_ignored += list(filter(lambda x: len(x) > 1, jieba.cut(content)))
    urls += re.findall(url_pattern, result[0])
    mentions += re.findall(mention_pattern, result[0])
    emojis += re.findall(emoji_pattern, result[0])
    sentences = re.split(split_pattern, result[0])
    for sentence in sentences:
        if '送' in sentence:
            match = re.search('送(\d+)', sentence)
            if match:
                cash += [int(match.group(1))]
        if 'VS' in sentence:
            match = re.search(VS_pattern, sentence)
            if match:
                teams += [match.group(1)]
                teams += [match.group(2)]
    

word_counts = Counter(words_ignored)
top_10_words = word_counts.most_common(25)
print(top_10_words)

print('counting categories...')
for category in categories:
    print(category, ":", words.count(category))

print('counting sports...')
for sport in sports:
    print(sport, ":", words.count(sport))

print('counting benefits...')
for benefit in benefits:
    print(benefit, ":", words.count(benefit))

print('counting cash...')
cash_count = Counter(cash)
print(cash_count.most_common(10))

domains = []
print('counting urls...')
for url in urls:
    if extract_domain(url) is not None:
        domains += ([extract_domain(url)])
domain_count = Counter(domains)
print(domain_count.most_common(10))

vaild_mentions = []
print('counting mentions...')
for mention in mentions:
    if len(mention) > 3:
        vaild_mentions += [mention]
mention_count = Counter(vaild_mentions)
print(mention_count.most_common(10))

print('counting emojis...')
emoji_count = Counter(emojis)
print(emoji_count.most_common(10))

print('counting teams...')
team_count = Counter(teams)
print(team_count.most_common(10))

ids = []
print('counting senders...')
for sender_id in sender_ids:
    ids += [extract_id(sender_id[0])]
sender_count = Counter(ids)
print(sender_count.most_common(10))