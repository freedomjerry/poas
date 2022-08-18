#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:59:46 2018
@author: Ming JIN
"""
#from snownlp import sentiment
#import numpy as np
from snownlp import SnowNLP
#from snownlp.sentiment import Sentiment
import matplotlib.pyplot as plt
import pymysql

def to_mysql(rates,tag,keyword):
    """
    信息写入mysql
    """
    table = 'comments_{keyword}'.format(keyword = keyword)
    db = pymysql.connect(host='localhost', user='root', password='yourpassword',  db='weibo2')
    cursor = db.cursor()
    sql = "UPDATE {table} SET sneti='{values}' WHERE id='{t}'".format(table=table, values=rates,t=tag)
    try:
        if cursor.execute(sql):
            
            #print("Successful")
            db.commit()
    except:
        #print('Failed')
        db.rollback()
    db.close()

def evaluation(keyword):
    comment = []
    pos_count = 0
    neg_count = 0
    tag=0
    for line_data in open("data_keywords_{keyword}.dat".format(keyword = keyword)):
        
        comment = line_data
        
        s = SnowNLP(comment)
        rates = s.sentiments
        to_mysql(rates,tag,keyword) 
        tag=tag+1 
        #print(rates)
        if (rates >= 0.5):
            pos_count += 1

        elif (rates < 0.5):
            neg_count += 1
        
        else :
            pass


    labels = 'Positive Side\n(eg. pray,eulogize and suggestion)', 'Negative Side\n(eg. abuse,sarcasm and indignation)'
    fracs = [pos_count,neg_count]
    explode = [0.1,0] # 0.1 凸出这部分，
    plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    #autopct ，show percet

    plt.pie(x=fracs, labels=labels, explode=explode,autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)

    plt.savefig("emotions_pie_chart_{keyword}.jpg".format(keyword = keyword),dpi = 360)
    plt.show()
    print("情感分析结束")
