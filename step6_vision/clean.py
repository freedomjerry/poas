import pandas as pd
import pymysql
from pyecharts import Pie, Map, Line,Page,Bar
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import csv
from snownlp import SnowNLP

# 设置列名与数据对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 显示10列
pd.set_option('display.max_columns', 10)
# 显示10行
pd.set_option('display.max_rows', 10)
# 设置显示宽度为500,这样就不会在IDE中换行了
pd.set_option('display.width', 2000)

# 读取数据
conn = pymysql.connect(host='localhost', user='root', password='yourpassword',  db='weibo2', charset='utf8mb4')
cursor = conn.cursor()
sql = "select * from comments_xian"
db = pd.read_sql(sql, conn)
# 清洗数据

df = db['user_message'].str.split(' ', expand=True)
id
df['num']=db['id']
#用户名
df['name'] = df[0]
#性别及地区
df1 = df[1].str.split('/', expand=True)
df['gender'] = df1[0]
df['province'] = df1[1]
#用户ID
df['id'] = db['user_id']
#情感指数
df['senti'] = db['sneti'].astype("float64")
# 评论信息
df['comment'] = db['comment']
#标签
df['label'] = db['label']
#点赞数
df['praise'] = db['praise'].str.extract('(\d+)').astype("int")
#微博数,关注数,粉丝数
df2 = db['weibo_message'].str.split(' ', expand=True)
df2 = df2[df2[0] != '未知']
df['tweeting'] = df2[0].str.extract('(\d+)').astype("int")
df['follows'] = df2[1].str.extract('(\d+)').astype("int")
df['followers'] = df2[2].str.extract('(\d+)').astype("int")
#评论时间
df['time'] = db['date'].str.split(':', expand=True)[0]
df['time'] = pd.Series([i+'时' for i in df['time']])
print(df['comment'],df['senti'])
df['day'] = df['time'].str.split(' ', expand=True)[0]
print(df)
# 去除无用信息
df = df.iloc[:, 3:]
#df = df[df['name'] != '未知']
#df = df[df['time'].str.contains("日")]
# 随机输出10行数据
page=Page()
prov = []
num = []
date = []
comm = []
def create_gender(df,page):
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
    pie = Pie("微博评论用户的性别情况", title_pos='center', title_top=0,width=500,height=300)
    pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True, legend_orient="vertical", legend_pos="left", legend_top="%10")
    page.add_chart(pie)
   

def create_map(df,page,prov):
    # 全部用户
    df = df.drop_duplicates('id')
    # 分组汇总
    loc_message = df.groupby(['province'])
    loc_com = loc_message['province'].agg(['count'])
    loc_com.reset_index(inplace=True)
    print(loc_com)
    #print(loc_com['count'].idxmax())
    prov.append([loc_com.loc[loc_com['count'].idxmax()].province])
    #print(prov)
    # 绘制地图
    value = [i for i in loc_com['count']]
    attr = [i for i in loc_com['province']]
    map = Map("微博评论用户的地区分布图", title_text_size=24,title_top=20,title_pos="center", width=1200,height=400)
    map.add("", attr, value, maptype="china", is_visualmap=True, visual_text_color="#000", is_map_symbol_show=False, visual_range=[0, 400])
    page.add_chart(map)

def creat_date(df,page,date,num):
    # 分组汇总
    date_message = df.groupby(['day'])
    date_com = date_message['day'].agg(['count'])
    date_com.reset_index(inplace=True)
    date.append([date_com.loc[date_com['count'].idxmax()].day])
    num.append([date_com.loc[date_com['count'].idxmax()]['count']])
    #print(date)
    #print(num)
    # 绘制走势图
    attr = date_com['day']
    v1 = date_com['count']
    line = Line("微博评论的时间分布", title_pos='center', title_top='18', width=1200, height=400)
    line.add("", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,xaxis_rotate=90)
    page.add_chart(line)

def creat_senti(df,page):
    # 分组汇总
    data_com = df.groupby('day',as_index=False).mean()
    #print(data_com)
    # 绘制走势图
    attr = data_com['day']
    v1 = data_com['senti']
    line = Line("微博情感态势", title_pos='center', title_top='18', width=1200, height=400)
    line.add("情感曲线(0.6表示中性情感）", attr, v1, is_smooth=True, is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True, xaxis_min="dataMin", area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,mark_line=[['0.5'],["average"]],xaxis_rotate=90,is_datazoom_show = True)
    #line.render("1.html")
    page.add_chart(line)
def creat_cluster(df,page,comm):
    # 分组汇总
    date_message = df.groupby(df['label'],as_index=False)['id'].agg(['count'])
    date_com = pd.DataFrame(date_message)
    date_com['comment']= None
    date_com.reset_index(inplace=True)
    
    #print(date_com)
    for x in range(0,10):
        data_sample = df[df["label"]==x]
        str1 = data_sample.sample(1).comment.values
        date_com['comment'].iloc[x] = str1
       # date_com.iloc[x,2] = data_sample.comment

        #print(date_com.comments)
    # 绘制走势图
    #print(date_com)
    str2 = date_com.loc[date_com['count'].idxmax()].comment
    comm.append(str2)
    #print(comm)
    attr = date_com['comment']
    v1 = date_com['count']
    bar = Bar("微博主要评论", title_pos='center', title_top='18', width=1200, height=400)
    bar.add("", attr,v1,visual_range=[0, 10000], is_fill=True, area_color="#000", xaxis_interval=1, is_xaxislabel_align=True,area_opacity=0.3, mark_point=["max"], mark_point_symbol="pin", mark_point_symbolsize=55,xaxis_rotate=90,is_convert=True)
    #line.render("1.html")
    
    page.add_chart(bar)
def creat_conclusion(df,keyword,prov,date,num,comm):
    comment = []
    pos_count = 0
    neg_count = 0
    for line_data in open("C:/Users/Administrator/Desktop/毕设/程序/data_keywords_{keyword}.dat".format(keyword=keyword)):
        comment = line_data
        s = SnowNLP(comment)
        rates = s.sentiments
        #print(rates)
        if (rates >= 0.5):
            pos_count += 1

        elif (rates < 0.5):
            neg_count += 1
        else :
            pass
    percent = pos_count/(pos_count+neg_count)
    percent = format(percent,'.2%')
    if(neg_count*3>pos_count):
        conclusion = "对于{keyword}事件，{province}地区的群众最为关注，{date}产生了最多的{count}话题量，大家最主要的观点是{comment} ，积极情感占比{percent} ,消极情感占比较多，应注意舆情引导，并对事件进行进一步的分析".format(keyword=keyword,province=prov[0],date=date[0],count=num[0],comment=comm[0],percent=percent)
    else:
        conclusion = "对于{keyword}事件，{province}地区的群众最为关注，{date}产生了最多的{count}话题量，大家最主要的观点是{comment} ，积极情感占比{percent} ,群众观点较为积极乐观，请保持事件跟踪，追踪舆论走向".format(keyword=keyword,province=prov[0],date=date[0],count=num[0],comment=comm[0],percent=percent)
    print(conclusion)
#creat_senti(df,page)
#create_gender(df,page)
#create_map(df,page,prov)
#creat_date(df,page,date,num)
#creat_cluster(df,page,comm)
#page.render("fire.html")
#creat_conclusion(df,'fire',prov,date,num,comm)