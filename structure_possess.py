# 文本结构化处理算法

def strucData(record, libA, libD):
    for index, clasue in enumerate(record):
        print(index, clause)
        # 分别获取属性词和描述词的全切分结果
        setA = set(getAllSegWords(clause, libA))
        setD = set(getAllSegWords(clause, libD))
        # 分别获取属性词和描述词的最大匹配结果
        maxA = maxMatch(Ci, setA)
        maxD = maxMatch(Ci, setD)

        # 将最大匹配结果按照在短句中出现的顺序排序
        wordsList = sortWordsObj(Ci, maxA, maxD)

        # 获取产生歧义的部分，保存无歧义词串对象
        wordsWrong = getWordsObj(Ci, wordsList)
        wordsRight = wordsList - wordsWrong

        # 如果分词存在交集的结果，则按照负责处理
        if len(wordsWrong)  > 0:
            for item1, item2 in wordsWrong:
                if libA.





list = ['a', 'b', 'c']
strucData(list, None, None)

