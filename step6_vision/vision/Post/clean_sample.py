import pandas as pd
import pymysql
from pyecharts import Pie, Map, Line,Page,Bar
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import csv
from snownlp import SnowNLP


def creat_date_sample(df,date,num):
    # 分组汇总
    date_message = df.groupby(['time'])
    date_com = date_message['time'].agg(['count'])
    date_com.reset_index(inplace=True)
    date.append([date_com.loc[date_com['count'].idxmax()].time])
    num.append([date_com.loc[date_com['count'].idxmax()]['count']])
    # 绘制走势图
    attr = date_com['time']
    v1 = date_com['count']
    line_num = Line("微博评论的时间分布", title_pos='center', title_top='18', width=700, height=400)
    line_num.add("", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,xaxis_rotate=90)
    return line_num

def creat_senti_sample(df):
    # 分组汇总
    data_com = df.groupby('time',as_index=False).mean()
    print(data_com)
    # 绘制走势图
    attr = data_com['time']
    v1 = data_com['senti']
    line_emo = Line("微博情感态势", title_pos='center', title_top='18', width=700, height=400)
    line_emo.add("情感曲线(0.5表示中性情感）", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max","min"], mark_point_symbol="pin", mark_point_symbolsize=55,mark_line=[['0.5'],["average"]],xaxis_rotate=90,is_datazoom_show = True)
    return line_emo
