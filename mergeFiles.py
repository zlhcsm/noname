#coding=utf-8

import os
import os.path
# 用来计算完成的时间
import time
timeStart=time.time()

def MergeTxt(filepath, resultfile):
    print("合并文件开始...")
    # 创建一个目标文件
    # a+：打开一个文件用于读写。如果该文件已存在，
    # 文件指针将会放在文件的结尾。文件打开时会是追加模式。
    # 如果该文件不存在，创建新文件用于读写
    k = open(filepath + resultfile, 'a+')

    # os.walk用来遍历目录中的文件名，返回root， dirs， files
    # root：当前遍历的文件夹本身的地址
    # dirs：是一个list，内容是该文件夹所有的目录的名称
    # files：是一个list，表示所有文件
    for root, dirs, files in os.walk(filepath):
        for filepath in files:
            txtpath = os.path.join(root, filepath)
            f = open(txtpath)
            k.write(f.read())

    k.close()
    print("合并文件完成...")

if __name__ == '__main__':
    filepath = "C:/Users/Alan/py-source"
    resultfile = '/result.txt'
    MergeTxt(filepath, resultfile)
    timeEnd = time.time()
    print('合并文件总耗时：' + str(timeEnd - timeStart) + 's')

