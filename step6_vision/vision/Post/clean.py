import pandas as pd
import pymysql
from pyecharts import Pie, Map, Line,Page,Bar
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import csv
from snownlp import SnowNLP

def create_gender(df):
    # 全部用户
    # df = df.drop_duplicates('id')
    # 包含关键字用户
    #df = df[df['name'].str.contains("坤|蔡|葵|kun")].drop_duplicates('id')
    # 分组汇总
    gender_message = df.groupby(['gender'])
    gender_com = gender_message['gender'].agg(['count'])
    gender_com.reset_index(inplace=True)

    # 生成饼图
    attr = gender_com['gender']
    v1 = gender_com['count']
    # pie = Pie("微博评论用户的性别情况", title_pos='center', title_top=0)
    # pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True, legend_orient="vertical", legend_pos="left", legend_top="%10")
    # pie.render("微博评论用户的性别情况.html")
    pie = Pie("微博评论用户的性别情况", title_pos='center', title_top=0,width=600,height=400)
    pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True, legend_orient="vertical", legend_pos="left", legend_top="%10")
    return pie
   

def create_map(df,prov):
    # 全部用户
    df = df.drop_duplicates('id')
    # 分组汇总
    loc_message = df.groupby(['province'])
    loc_com = loc_message['province'].agg(['count'])
    loc_com.reset_index(inplace=True)
    prov.append([loc_com.loc[loc_com['count'].idxmax()].province])
    # 绘制地图
    value = [i for i in loc_com['count']]
    attr = [i for i in loc_com['province']]
    map = Map("微博评论用户的地区分布图", title_text_size=24,title_top=20,title_pos="center", width=800,height=400)
    map.add("", attr, value, maptype="china", is_visualmap=True, visual_text_color="#000", is_map_symbol_show=False, visual_range=[0, 400])
    return map

def creat_date(df,date,num):
    # 分组汇总
    date_message = df.groupby(['day'])
    date_com = date_message['day'].agg(['count'])
    date_com.reset_index(inplace=True)
    date.append([date_com.loc[date_com['count'].idxmax()].day])
    num.append([date_com.loc[date_com['count'].idxmax()]['count']])
    # 绘制走势图
    attr = date_com['day']
    v1 = date_com['count']
    line_num = Line("微博评论的时间分布", title_pos='center', title_top='18', width=700, height=400)
    line_num.add("", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,xaxis_rotate=90)
    return line_num

def creat_senti(df):
    # 分组汇总
    data_com = df.groupby('day',as_index=False).mean()
    print(data_com)
    # 绘制走势图
    attr = data_com['day']
    v1 = data_com['senti']
    line_emo = Line("微博情感态势", title_pos='center', title_top='18', width=700, height=400)
    line_emo.add("情感曲线(0.6表示中性情感）", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max","min"], mark_point_symbol="pin", mark_point_symbolsize=55,mark_line=[['0.5'],["average"]],xaxis_rotate=90,is_datazoom_show = True)
    return line_emo

def creat_cluster(df,comm):
    # 分组汇总
    date_message = df.groupby(df['label'],as_index=False)['id'].agg(['count'])
    date_com = pd.DataFrame(date_message)
    date_com['comment']= None
    date_com.reset_index(inplace=True)
    
    print(date_com)
    for x in range(0,10):
        data_sample = df[df["label"]==x]
        str1 = data_sample.sample(1).comment.values
        date_com['comment'].iloc[x] = str1
       # date_com.iloc[x,2] = data_sample.comment

        #print(date_com.comments)
    # 绘制走势图
    str2 = date_com.loc[date_com['count'].idxmax()].comment
    comm.append(str2)
    attr = date_com['comment']
    v1 = date_com['count']
    bar = Bar("微博主要评论", title_pos='center', title_top='18', width=700, height=450)
    bar.add("", attr,v1,visual_range=[0, 10000], is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True,area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,xaxis_rotate=90,is_convert=True)
    #line.render("1.html")
    return bar

def creat_conclusion(df,keyword,prov,date,num,comm):
    comment = []
    pos_count = 0
    neg_count = 0
    for line_data in open("C:/Users/Administrator/Desktop/毕设/程序/data_keywords_{keyword}.dat".format(keyword=keyword)):
        comment = line_data
        s = SnowNLP(comment)
        rates = s.sentiments
        #print(rates)
        if (rates >= 0.6):
            pos_count += 1

        elif (rates < 0.6):
            neg_count += 1
        else :
            pass
    percent = pos_count/(pos_count+neg_count)
    percent = format(percent,'.2%')
    if(neg_count*2.9013>pos_count):
        conclusion = "对于{keyword}事件，{province}地区的群众最为关注，{date}产生了最多的{count}话题量，大家最主要的观点是{comment} ，积极情感占比{percent} ,消极情感占比较多，应注意舆情引导，并对事件进行进一步的分析".format(keyword=keyword,province=prov[0],date=date[0],count=num[0],comment=comm[0],percent=percent)
    else:
        conclusion = "对于{keyword}事件，{province}地区的群众最为关注，{date}产生了最多的{count}话题量，大家最主要的观点是{comment} ，积极情感占比{percent} ,群众观点较为积极乐观，请保持事件跟踪，追踪舆论走向".format(keyword=keyword,province=prov[0],date=date[0],count=num[0],comment=comm[0],percent=percent)
    return conclusion