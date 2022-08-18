#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:51:48 2017
@author: Ming JIN
"""
import jieba
#import string
#import sys
#import os
import pymysql






def get_data(keyword):
    jieba.load_userdict("step2 cut_words/SogouLabDic.txt")
    jieba.load_userdict("step2 cut_words/dict_baidu_utf8.txt")
    jieba.load_userdict("step2 cut_words/dict_pangu.txt")
    jieba.load_userdict("step2 cut_words/dict_sougou_utf8.txt")
    jieba.load_userdict("step2 cut_words/dict_tencent_utf8.txt")
    jieba.load_userdict("step2 cut_words/my_dict.txt")
    stopwords = {}.fromkeys([ line.rstrip() for line in open('step2 cut_words/Stopword.txt',encoding='utf-8') ])
    print("连接MySql数据库...")
    
    db = pymysql.connect(host='localhost', user='root', password='yourpassword',  db='weibo2', charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor = db.cursor()

    sql_1 = "select count(*) from comments_{keyword}".format(keyword = keyword)
    cursor.execute(sql_1)
    index = cursor.fetchone()
    index=int(index['count(*)'])
    print(index)
    
    print("正在解析数据...")
    
    for n in range(1,index):
        
        result = []
   
        sql_2 = "select comment from comments_{keyword} limit ".format(keyword = keyword) + str(n-1)+",1"
        cursor.execute(sql_2)
        result_mtest2dle_1 = cursor.fetchall()
        #print(result_mtest2dle_1)
        result_mtest2dle = result_mtest2dle_1[0]['comment']
        #print(result_mtest2dle)
   
        seg = jieba.cut(result_mtest2dle)

        for i in seg:
            
            if i not in stopwords:  
              
                result.append(i)

        fo = open("data_full_{keyword}.dat".format(keyword = keyword), "a+",encoding='utf-8')
        #fo = open("/Users/kimmeen/Downloads/P_Weibo/%s"%user_test2, "w")

        for j in result:
          
           fo.write(j)
           fo.write(' ')
     
        fo.write('\n')
        fo.close()
        n += 1
    
    db.close()
    print("解析完成!")

if __name__ == '__main__':
    
    total_news = 11
    print("进程开始...")
        
    get_data('earthquake')
        
    print("Done!")






