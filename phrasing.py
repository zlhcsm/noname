import  jieba
import re

# 读取一个txt文件，分成句子，可使用split函数来实现
paragraph = open("C:/Users/Alan/py-source/result.txt").read()

pattern1 = '，|。|！|\!|\,|\.|？|\?|；'
sentences = re.split(pattern1, paragraph)


# 把句子的list写入txt文件
writeFilePath = 'C:/Users/Alan/py-source/phrasing.txt'
writeFile = open(writeFilePath, 'a+')
for phrasingData in sentences:
    writeFile.write(phrasingData + '\n')
writeFile.close()

paragraph1 = open(writeFilePath).read()
words_list = jieba.lcut(paragraph1)
# print(words_list)
# for item in words_list:
#     print(item)

import nltk
import numpy as np

# 统计词频
# nltk.FreqDist返回一个词典，key是不同的词，value是词出现的频率

# freq_dist = nltk.FreqDist(words_list)
# freq_list = []
# num_words = len(freq_dist.values())
# for i in range(num_words):
#     freq_list.append([list(freq_dist.keys())[i], list(freq_dist.values()[i])])
# freqArr = np.array(freq_list)
# print(freq_list)
# print(freq_dist)
# print(freqArr)

