import numpy as np
import matplotlib.pyplot as plt
import math
def f_testset_word_count(testset):                                     #测试集的词数统计
    return (len(testset.split()))
 
 
def graph_draw(topic,perplexity):             #做主题数与困惑度的折线图
    x=topic
    y=perplexity
    plt.plot(x,y,marker="*",color="red",linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()
 
 
phi = np.fromfile('step5_LDA\data\tmp\model_phi.dat')
word_topic = {}
f = open('step5_LDA\data\tmp\model_tassign.dat')
patterns = f.read().split()
f = open('step5_LDA\data\tmp\model_tassign.dat')
testset_word_count = f_testset_word_count(f.read())
 
# 用作循环
_topic=[]
perplexity_list=[]
 
_topic.append(10)
for pattern in patterns:
    word = int(pattern.split(':')[0])
    topic = int(pattern.split(':')[1])
    pattern = pattern.replace(':','_')
    if not pattern in word_topic:
        word_topic[pattern] = phi[topic][word]
 
duishu = 0.0
for frequency in word_topic.values():
    duishu += -math.log(frequency)
kuohaoli = duishu/testset_word_count
perplexity = math.exp(kuohaoli)
perplexity_list.append(perplexity)
 
graph_draw(_topic,perplexity_list)
