#-*- coding:utf-8 -*-

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

def main(keyword,url):
    tableexit(keyword)
    buildtable(keyword)
    print("建表完成...")
    get_message(url , keyword)
    print("爬虫完毕，原始数据已录入...")
    get_data(keyword)
    print("分词完毕...")
    keywords(keyword)
    print("关键词提取完毕")
    evaluation(keyword)
    print("情感分析完成，已录入数据库...")
    run(keyword)
    print("LDA话题聚类完毕，结果和标签已保存...")
    wordcloud(keyword)
    print("可视化完成,Done!")