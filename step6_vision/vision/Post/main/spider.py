from copyheaders import headers_raw_to_dict
from bs4 import BeautifulSoup
import requests
import pymysql
import time
import re

headers = b"""
accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding:gzip, deflate, br
accept-language:zh-CN,zh;q=0.9
cache-control:max-age=0
cookie:ALF=1589365573; SCF=AniXL6rCS6W9V3VSynmE0C26Qw1bEc44O9aCyDCwc1UtXvTdcZ611b80KGZSNb5U-gfwkwkb6MFljSRHpit7Xr8.; SUB=_2A25zkE4BDeRhGeBL61sY-SbNzDqIHXVRe1JJrDV6PUJbktANLUXckW1NR1s4WgQj4RpRzW-KmzOyMEgRc6HOEnLV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFzOfv4gNBIfNcZvJzmvn6e5JpX5K-hUgL.Foqfeh.41KnpS0q2dJLoI7DJMJHLIsHoIcHE; SUHB=0XDlNsipllnIy_; SSOLoginState=1586773585; _T_WM=33499474818; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
"""

# 将请求头字符串转化为字典
headers = headers_raw_to_dict(headers)


def to_mysql(data,keyword):
    """
    信息写入mysql
    """
    table = 'comments_{keyword}'.format(keyword = keyword)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    db = pymysql.connect(host='localhost', user='root', password='yourpassword',  db='weibo2')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            #print("Successful")
            db.commit()
    except:
        #print('Failed')
        db.rollback()
    db.close()


def get_user(user_id):
    """
    获取用户信息
    """
    try:
        url_user = 'https://weibo.cn' + str(user_id)
        response_user = requests.get(url=url_user, headers=headers)
        soup_user = BeautifulSoup(response_user.text, 'html.parser')
        # 用户信息
        re_1 = soup_user.find_all(class_='ut')
        user_message = re_1[0].find(class_='ctt').get_text()
        # 微博信息
        re_2 = soup_user.find_all(class_='tip2')
        weibo_message = re_2[0].get_text()
        return (user_message, weibo_message)
    except:
        return ('未知', '未知')


def get_message(linkurl,keyword):
    # 第一页有热门评论,拿取信息较麻烦,这里偷个懒~
    for i in range(2, 20):
        time.sleep(3)
        data = {}
        #print('第------------' + str(i) + '------------页')
        # 请求网址
        url = '{linkurl}'.format(linkurl=linkurl) + str(i)
        response = requests.get(url=url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # 评论信息
        comments = soup.find_all(class_='ctt')
        # 点赞数
        praises = soup.find_all(class_='cc')
        # 评论时间
        date = soup.find_all(class_='ct')
        # 获取用户名
        name = re.findall('id="C_.*?href="/.*?">(.*?)</a>', html)
        # 获取用户ID
        user_ids = re.findall('id="C_.*?href="(.*?)">(.*?)</a>', html)

        for j in range(len(name)):
            # 用户ID
            user_id = user_ids[j][0]
            (user_message, weibo_message) = get_user(user_id)
            data['user_id'] = " ".join(user_id.split())
            data['user_message'] = " ".join(user_message.split())
            data['weibo_message'] = " ".join(weibo_message.split())
            data['comment'] = " ".join(comments[j].get_text().split())
            data['praise'] = " ".join(praises[j * 2].get_text().split())
            data['date'] = " ".join(date[j].get_text().split())
            #print(data)
            # 写入数据库中
            to_mysql(data,keyword)