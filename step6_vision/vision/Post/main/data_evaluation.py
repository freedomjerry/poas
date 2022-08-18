#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    for line_data in open("C:\\Users\\Administrator\\Desktop\\毕设\\程序\\data_keywords_{keyword}.dat".format(keyword = keyword)):
        
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
