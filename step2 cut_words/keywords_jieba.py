#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:51:48 2017
@author: Ming JIN
"""
from jieba import analyse
def keywords(keyword):
    tfidf = analyse.extract_tags

    for line in open("data_full_{keyword}.dat".format(keyword = keyword),encoding='utf-8'):
        
        text = line

        keywords = tfidf(text,allowPOS=('ns','nr','nt','nz','nl','n', 'vn','vd','vg','v','vf','a','an','i'))

        result=[]

        for keyword1 in keywords:
            
            result.append(keyword1)

        #print(result)
        fo = open("data_keywords_{keyword}.dat".format(keyword = keyword), "a+")
        
        for j in result:
            
            fo.write(j)
            fo.write(' ')
        
        fo.write('\n')
        fo.close()

    print("Keywords Extraction Done!")


