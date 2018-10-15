import requests
import json
import time
import random
from datetime import datetime,timedelta

import csv

def get_headers():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    return headers


def get_data(url):

    headers = get_headers()
    try:
        with requests.Session() as s:
            response = s.get(url, headers=headers,timeout=3)
            content = response.text
            return content

    except Exception as e:
        print(e)


# 处理数据
def parse_data(html):
    try:
        data = json.loads(html)['cmts']  # 将str转换为json
    except Exception as e:
        return None

    comments = []
    for item in data:

        comment = [item['id'],item['nickName'],item["userLevel"],item['cityName'] if 'cityName' in item else '',item['content'].replace('\n', ' '),item['score'],item['startTime']]
        comments.append(comment)
    return comments


# 存储数据
def save_to_csv():

    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间，从当前时间向前获取

    end_time = '2018-09-30 00:00:00'   # 影片的上映日期

    while start_time > end_time:  # 如果时间开始时间大于结束时间

        url = 'http://m.maoyan.com/mmdb/comments/movie/342166.json?_v_=yes&offset=0&startTime=' + start_time.replace(
            ' ', '%20')
        html = None

        try:
            html = get_data(url)

        except Exception as e:

            time.sleep(0.5)
            html = get_data(url)

        else:
            time.sleep(1)

        comments = parse_data(html)

        if comments:
            start_time = comments[14][-1]  # 获得末尾评论的时间
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(
                seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
            start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str

            print(comments)


            with open("comments.csv", "a", encoding='utf-8',newline='') as csvfile:
                writer = csv.writer(csvfile)


                writer.writerows(comments)




if __name__ == '__main__':
    save_to_csv()



