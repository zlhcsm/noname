#encoding=utf-8

from jieba import analyse
import jieba
import nltk
import numpy as np

# 导入自己写入的函数
import os
import lib.fileOperate as FO
import constant as CONS

# 去除停用词的两个函数
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

# 对句子去除停用词
def movestopwords(sentence):
    stopwords = stopwordslist(CONS.FILEPATH + 'breakpoint.txt')   # 这里加载停用词的路径
    outstr = ''                                               # 输出的字符串
    for word in sentence:

        if word not in stopwords:
            if word != '\t' and '\n':
                outstr += word
    return outstr

corpus_path = CONS.FILEPATH + 'rake/'     # 未分词分类语料库路径
seg_path = CONS.FILEPATH + 'rake1/'               # 分词后分类语料库路径

catelist= os.listdir(corpus_path)               # 获取未分词目录下所有子目录
for mydir in catelist:
    class_path = corpus_path + mydir + '/'             # 拼出分类子目录的路径
    seg_dir = seg_path + mydir + '/'            # 拼出分词后语料分类目录
    if not os.path.exists(seg_path):            # 是否存在，不存在则创建
        os.makedirs(seg_dir)

    file_list = os.listdir(class_path)
    for file_path in file_list:
        fullname = class_path + file_path   # 路径 + 文件名
        print("当前处理的文件是：", fullname)

        content = FO.readfile(fullname).strip()
        content = content.replace("\n", "").strip()
        content_seg = jieba.cut(content)
        print("jieba分词后：", content_seg)
        listcontent = ''
        for i in content_seg:
            listcontent += i
            listcontent += " "
        print(listcontent)

        listcontent = movestopwords(listcontent)
        print("去除停用词后：", listcontent[0:])
        listcontent = listcontent.replace("  ", "").replace("  ", " ")
        FO.savefile(seg_path + file_path, "".join(listcontent))


