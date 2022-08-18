from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from Post.clean import create_map,creat_senti,create_gender,creat_date,creat_cluster,creat_conclusion
from Post.clean_sample import creat_date_sample,creat_senti_sample
from Post.main.main import main
import pandas as pd
from Post.main.buildtabele import buildtable,tableexit
from Post.main.spider import get_message,get_user,to_mysql
from Post.main.cut_words import get_data
from Post.main.keywords_jieba import keywords
from Post.main.word_cloud import wordcloud
from Post.main.data_evaluation import evaluation,to_mysql
from Post.main.lda import run,preprocessing,DataPreProcessing,Document
import pymysql
from copyheaders import headers_raw_to_dict
from bs4 import BeautifulSoup
import requests
import time
import re
from snownlp import SnowNLP
#from snownlp.sentiment import Sentiment
import matplotlib.pyplot as plt
import logging
import logging.config
import configparser
import numpy as np
import random
import codecs
import os
import jieba
import jieba.analyse
from PIL import Image,ImageSequence
from matplotlib.font_manager import FontProperties  
from wordcloud import WordCloud,ImageColorGenerator
#import jieba
# Create your views here.
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
keyword = ""
def creat_df(keyword,K):
        conn = pymysql.connect(host='localhost', user='root', password='yourpassword',  db='weibo2', charset='utf8mb4')
        cursor = conn.cursor()
        sql = "select * from comments_{keyword}".format(keyword=keyword)
        db = pd.read_sql(sql, conn)

        # 清洗数据
        df = db['user_message'].str.split(' ', expand=True)
        #id
        #df['num']=db['id']
        # 用户名
        df['name'] = df[0]
        # 性别及地区
        df1 = df[1].str.split('/', expand=True)
        df['gender'] = df1[0]
        df['province'] = df1[1]
        # 用户ID
        df['id'] = db['user_id']
        #情感指数
        df['senti'] = db['sneti'].astype("float64")
        # 评论信息
        df['comment'] = db['comment']
        #标签
        df['label'] = db['label']
        # 点赞数
        df['praise'] = db['praise'].str.extract('(\d+)').astype("int")
        # 微博数,关注数,粉丝数
        df2 = db['weibo_message'].str.split(' ', expand=True)
        df2 = df2[df2[0] != '未知']
        df['tweeting'] = df2[0].str.extract('(\d+)').astype("int")
        df['follows'] = df2[1].str.extract('(\d+)').astype("int")
        df['followers'] = df2[2].str.extract('(\d+)').astype("int")
        # 评论时间
        df['time'] = db['date'].str.split(':', expand=True)[0]
        df['time'] = pd.Series([i+'时' for i in df['time']])
        df['day'] = df['time'].str.split(' ', expand=True)[0]
        # 去除无用信息
        df = df.iloc[:, 3:]
        df = df[df['name'] != '未知']
        df = df[df['time'].str.contains("日|今天")]
        #进行ecahrt
        return df

def index(request):
    """
    主页
    :param request:
    :return:
    """
    return render(request=request, template_name='Post/main.html')


def examlpe_virus(request):
        template = loader.get_template('Post/example_virus.html')
        # 读取数据
        prov = []
        num = []
        date = []
        comm = []
        df=creat_df("virus",'0')
        g = create_gender(df)
        m = create_map(df,prov)
        n = creat_date(df,date,num)
        s = creat_senti(df)
        p = creat_cluster(df,comm)
        c = creat_conclusion(df,'virus',prov,date,num,comm)
        #l.render("1.html") 			#生成图像实例
        context = dict(
            myechart=g.render_embed(),
            myechart2 = m.render_embed(),
            myechart3 =n.render_embed(),
            myechart4 = s.render_embed(),
            myechart5 = p.render_embed(),
            conclusion = c,  #必须要有
            host=REMOTE_HOST,	#若前端加载了对应的echarts库，可以不需要这一句和下面
            script_list=g.get_js_dependencies(),
            script_list1=m.get_js_dependencies(),
            script_list2=n.get_js_dependencies(),
            script_list3=s.get_js_dependencies(),#代码的目的是下载该图标对应的一些echarts库
        )
        return HttpResponse(template.render(context, request))

def examlpe_sample(request):
        template = loader.get_template('Post/example_sample.html')
        print(keyword+".....")
        prov = []
        num = []
        date = []
        comm = []
        # 读取数据
        df=creat_df(keyword,'1')
        print(df)
        g = create_gender(df)
        m = create_map(df,prov)
        n = creat_date_sample(df,date,num)
        s = creat_senti_sample(df)
        p = creat_cluster(df,comm)
        c = creat_conclusion(df,keyword,prov,date,num,comm)
        #l.render("1.html") 			#生成图像实例
        context = dict(
            myechart=g.render_embed(),
            myechart2 = m.render_embed(),
            myechart3 =n.render_embed(),
            myechart4 = s.render_embed(),
            myechart5 = p.render_embed(),
            conclusion = c,  #必须要有
            host=REMOTE_HOST,	#若前端加载了对应的echarts库，可以不需要这一句和下面
            script_list=g.get_js_dependencies(),
            script_list1=m.get_js_dependencies(),
            script_list2=n.get_js_dependencies(),
            script_list3=s.get_js_dependencies(),#代码的目的是下载该图标对应的一些echarts库
        )
        return HttpResponse(template.render(context, request))
def examlpe_earthquake(request):
        template = loader.get_template('Post/example_earthquake.html')
        prov = []
        num = []
        date = []
        comm = []
        # 读取数据
        df=creat_df("earthquake",'0')
        g = create_gender(df)
        m = create_map(df,prov)
        n = creat_date(df,date,num)
        s = creat_senti(df)
        p = creat_cluster(df,comm)
        c = creat_conclusion(df,'earthquake',prov,date,num,comm)
        #l.render("1.html") 			#生成图像实例
        context = dict(
            myechart=g.render_embed(),
            myechart2 = m.render_embed(),
            myechart3 =n.render_embed(),
            myechart4 = s.render_embed(),
            myechart5 = p.render_embed(),
            conclusion = c,  #必须要有
            host=REMOTE_HOST,	#若前端加载了对应的echarts库，可以不需要这一句和下面
            script_list=g.get_js_dependencies(),
            script_list1=m.get_js_dependencies(),
            script_list2=n.get_js_dependencies(),
            script_list3=s.get_js_dependencies(),#代码的目的是下载该图标对应的一些echarts库
        )
        return HttpResponse(template.render(context, request))
def examlpe_fire(request):
        template = loader.get_template('Post/example_fire.html')
        prov = []
        num = []
        date = []
        comm = []
        # 读取数据
        df=creat_df("fire",'0')
        g = create_gender(df)
        m = create_map(df,prov)
        n = creat_date(df,date,num)
        s = creat_senti(df)
        p = creat_cluster(df,comm)
        c = creat_conclusion(df,'fire',prov,date,num,comm)
        #l.render("1.html") 			#生成图像实例
        context = dict(
            myechart=g.render_embed(),
            myechart2 = m.render_embed(),
            myechart3 =n.render_embed(),
            myechart4 = s.render_embed(),
            myechart5 = p.render_embed(),
            conclusion = c,  #必须要有
            host=REMOTE_HOST,	#若前端加载了对应的echarts库，可以不需要这一句和下面
            script_list=g.get_js_dependencies(),
            script_list1=m.get_js_dependencies(),
            script_list2=n.get_js_dependencies(),
            script_list3=s.get_js_dependencies(),#代码的目的是下载该图标对应的一些echarts库
        )
        return HttpResponse(template.render(context, request))

def receive_data(request):
    if request.POST: 
        print("YES")# 如果数据提交
        url = request.POST.get('url_user',None)
        global keyword
        keyword = request.POST.get('keyword_user',None)
        str(keyword)
        print(keyword)
        main(keyword,url)
        return render(request=request, template_name='Post/main.html')
    else:
        print("NO")
        return render(request=request, template_name=None)