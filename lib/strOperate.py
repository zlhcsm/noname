from sentenceSimilarity import jaccard_similarity as SS
import time
import copy
from Class.candiword import Candiword as CD
from lib.fileOperate import readfilebyline as RF

#*************************获取两个句子的重合串***********************
def getOverlapString(fir, sec):
    if SS(fir, sec) < 0.1 or SS(fir, sec) > 0.7:
        return []
    overLapStr = []     # 保存重合串
    index1 = 0
    str = ''
    while index1 < len(fir):     # 遍历所有句子中的词
        word1 = fir[index1]
        if word1 == '|':                    # 如果是分隔符，则直接判断下一项
            index1 = index1 + 1
            continue
        if word1 not in sec:                # 如果第二句当中没有这个字，则进行下一个字的判断
            index1 = index1 + 1
            continue
        else:                # start的值是用来标记共有词到哪个位置了
            count = 1                       # 表示有几个字一样，有一样的就进行+1操作
            while index1+count < len(fir):
                if fir[index1+count] == '|':
                    str = fir[index1:index1+count]
                    break
                elif index1 + count + 1 > len(fir):      #到达短句末尾，结束
                    str = fir[index1:len(fir)]
                    break
                elif fir[index1:index1+count+1] not in sec:
                    str = fir[index1:index1+count]
                    break
                else:
                    str = fir[index1:len(fir)]
                    count = count + 1
            if len(str) > 1:
                overLapStr.append(str)
            index1 = index1 + count
    print("^^^^^^^^^^^^^^^^^^^^^^重合串^^^^^^^^^^^^^^^^^^^^^^")
    print(overLapStr)
    return overLapStr
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^
#getOverlapString方法有bug，其中存在的边界条件和具体的划分情况可能有问题
#已解决：2019-7-12
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^


#*************************获取分词词串集对象***********************
# 输入：一组分类好的句子， 断点标记|
# 输出：切分好的所有分词词串集对象
def getParticiples(groupCaluse, reg):
    participles = []
    words = []
    for item1 in groupCaluse:
        for item2 in groupCaluse:
            overLapStr = getOverlapString(item1, item2) #获得两条短句重合串集合
            if(overLapStr != []):
                print("———————————字符串集合—————————")
                for str in overLapStr:
                    firs = item1.split(str)
                    secs = item2.split(str)
                    result = firs + secs
                    print(result)
                    for item3 in result:
                        if words.count(item3) < 1:
                            words.append(item3)
                    if words.count(str) < 1:
                        words.append(str)
    prewords = []
    for word in words:
        wordlist = word.split('|')
        for item in wordlist:
            prewords.append(item)
    testwords = []
    for word in words:
        if word.find('|') == -1:
            testwords.append(word)
    words = []
    words = words + prewords
    words = set(words)
    print(words)
    for word in words:
        if (word != '') & (len(word) > 1):
            candword = CD(word, 0, 0,0)
            getParameter(groupCaluse, candword)
            participles.append(candword)

    print("****************** 产 生 的 候 选 词*****************")
    participles.sort(key=lambda x:x.c_value, reverse=True)
    for item4 in participles:
        print(item4)
    return participles
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^
#遍历的效率太低
#前提是对文本做了| 处理
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^


#***************************筛选核心关键字*************************
def selectKeyWords(groupClause, priticiples, candiWords, Locl, To):
    """
    筛选核心关键词x`
    :param groupClause: 一组分类好的短句
    :param priticiples: 该组短句的分词词串集对象
    :param candiWords: 满足阈值的一对词汇
    :param Locl: 词位阈值
    :param To: 阈值To（threeshold）
    :return: 对应短句组的核心关键词对 keyWords
    """
    # 原始核心关键词有一个，标记为描述词，属性词为空
    if len(candiWords) == 1:
        desWords = candiWords[0].word
        attWords = ""
    elif len(candiWords) == 2:
        desWords = ""                   # 初试化两个核心关键词
        attWords = ""
        fir = candiWords[0]             # 保存满足要求的两个词
        sec = candiWords[1]
        # 两词的Loc满足一个大于等于Locl，一个小于等于Locl
        if (fir.loc - Locl) * (sec.loc - Locl) <= 0:
            attWords = sec.word if (fir.loc > sec.loc) else fir.word
            desWords = fir.word if (fir.loc > sec.loc) else sec.word
        #两词的Loc同时大于Locl或同时阈值小于Locl
        elif (fir.loc - Locl) * (sec.loc - Locl) > 0:
            return
        attWords = sec.word if (fir.loc > sec.loc) else fir.word
        desWords = fir.word if (fir.loc > sec.loc) else sec.word
        keyWords = []
        keyWords.append(attWords, desWords)
        return keyWords
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^
# 这里判断属性和描述值感觉不靠谱啊
#^^^^^^^^^^^^^^^^^warning!^^^^^^^^^^^^^^^^^^^^


#***************************求解两个候选词当中较小的值*************************
def minlocate(candi1, candi2):
    """
    选择候选词当中词位较小的
    :param candi1: 候选词一
    :param candi2: 候选词二
    :return: 当中词位较小的词
    """
    if (candi1 is None) | candi2 is None:
        return


# ***************************计算候选词的参数*************************
# 输入：一个短句簇， 一个候选词
# 输出：一个候选词的各项参数
def getParameter(groupClause, candiword):
    startTime = time.time()
    average = 0
    count = 0
    wc = 0  # wordCount即单词出现的次数
    fc = 0  # frequenceCount即单词出现的句子数目
    for phrase in groupClause:
        if phrase == candiword.word:
            continue
        else:
            wc = wc + phrase.count(candiword.word)
            sum = average * count
            count = count + 1
            loc = (phrase.find(candiword.word) + 1) / len(phrase)
            average = (sum + loc) / count
            if phrase.find(candiword.word) != -1:
                fc = fc + 1
    candiword.loc = round(average, 4)
    candiword.c_value = round(wc, 4)
    candiword.f_value = round(fc / len(groupClause), 4)
    endTime = time.time()
    # print("计算一个候选词的参数时间为：", str(endTime - startTime) + "S")
    return candiword


# ***************************调整候选词*************************
def adjustCandiWords(groupClause, participles, candiWords, leng, Tc, To, Tf, Cc, Tocal, libD, libA):
    """

    :param groupClause:分类好的一组短句
    :param participles:该组短句的分词词串集对象
    :param candiWords:满足阈值Tf和Cc的词汇组
    :param leng:满足阈值Tf和Cc的词汇个数len
    :param Tc:判断词串包含关系的阈值，和To保持一致
    :param To:判断部分重合关系的阈值，值为0.2
    :param Tf:词频的阈值
    :param Cc:词数的阈值
    :param Tocal:词位的阈值
    :param libD:描述词基准词库
    :param libA:属性词基准词库
    :return:
    """
    count1 = 0
    if leng > 2:
        for i in range(leng):
            for j in range(i, leng):
                candi1 = candiWords[i]
                candi2 = candiWords[j]
                if (candi1.word == candi2.word) | (candi1.word == '') | (candi2.word == ''):
                    continue
                print("-------------------- ")
                print(candi1.word, candi2.word)
                # 如果两个词串满足规则一，保存组合词
                if ruleFirst(groupClause, candi1,candi2, 0.15):
                    print("以上信息满足条件一")
                    # 在分词词串集合中获取组合词的词串对象
                    combine = combineStr(candi1.word, candi2.word)
                    candiWords[j] = getSelected(participles, combine)
                    candiWords[i].word = ''
                    for item in candiWords:
                        print(item)
                   # adjustCandiWords(groupClause, participles, candiWords, Tc, To, Tf, Tocal=0.2, libD='', libA='')
                    break
                # 如果连个词串满足规则而，保留长词，否则保留短词
                elif ruleSec(candi1, candi2, Tc) != None:
                    print("以上信息满足条件二")
                    resuleRes = copy.deepcopy(ruleSec(candi1, candi2, Tc))
                    candiWords[j] = resuleRes
                    candiWords[i].word = ''
                    for item in candiWords:
                        print(item)
                    break
                # 如果两个词串满足规则三或四，保留合并词在靠后位置
                elif ruleThir(candi1, candi2, libD, libA) != None:
                    print("以上信息满足条件三或者四")
                    candi_combine = ruleThir(candi1, candi2, libD, libA)
                    if candi_combine == None:
                        continue
                    candiWords[j] = getParameter(groupClause, candi_combine)
                    candiWords[i].word = ''
                    for item in candiWords:
                        print(item)
                    return
        midWords = list(candiWords)
        for item4 in candiWords:
            if item4.word == '':
                midWords.remove(item4)
        candiWords = midWords
        for item in candiWords:
            print(item)
        if len(candiWords) < 3:
            keywords = selectKeyWords(groupClause, participles, candiWords, Locl=0.6, To=0.2)
            print('关键字是：')
            print(keywords)
            return keywords
    elif leng == 0:
        # 对阈值下调，重新获取满足阈值要求的候选词串
        Tf = Tf - 0.1
        Cc = Cc - 5
        candiWords = getCandidateWords(groupClause, participles, Tf, Cc)
        if leng == 1 | leng == 2:
            keyWords = selectKeyWords(groupClause, participles, candiWords, Locl=0.2, To=0.2)
            return keyWords
        if leng == 0:
            return None
        if leng >= 2:
            adjustCandiWords(groupClause, participles, candiWords, Tc, To, Tf, Tocal, libD, libA)


# ***************************获取元素集合中的一部分*************************
def getSelected(participles, combine):
    for candi in participles:
        if candi.word == combine:
            return candi


# ***************************调整候选词：规则一*************************
def ruleFirst(groupClause, candi1, candi2, To):
    if getOverlap(candi1.word, candi2.word) == '':
        return False
    else:
        overlap = getOverlap(candi1.word, candi2.word)
        if (overlap == candi1.word) | (overlap == candi2.word) | (overlap == ''):
            return False
        s12 = 0
        for sentence in groupClause:
            s12 = s12 + sentence.count(overlap)
        minCount =  min(candi1.c_value, candi2.c_value)
        if (minCount - s12) / s12 < To:
            return True
    return False


# ***************************调整候选词：规则二*************************
def ruleSec(candi1, candi2, Tc=0.2):
    """
    第二规则定义：词串包含关系，假设较长字串包含较短词串，则保留词频相对较大的词串
    计算公式：( Count(S2) - Count(S1)) / Count(S2) < Tc
    :param candi1: 候选词1
    :param candi2:  候选词2
    :param Tc:  包含关系的阈值
    :return:    结果串
    """
    if candi2.word == '':
        return candi2
    elif candi1.word == '':
        return candi1
    c1word = candi1.word
    c2word = candi2.word
    if len(c1word) > len(c2word):
        resultmax = candi1
        maxlen = c1word
        maxscore = candi1.c_value
        resultmin = candi2
        minLen = c2word
        minscore = candi2.c_value
    else:
        resultmax = candi2
        maxlen = c2word
        maxscore = candi2.c_value
        resultmin = candi1
        minLen = c1word
        minscore = candi1.c_value
    if (maxlen.find(minLen) != -1):
        if (minscore - maxscore) / minscore < Tc:
            return resultmax
        else:
            return resultmin


# ***************************调整候选词：规则三*************************
def ruleThir(candi1, candi2, libD, libA):
    com_str1 = candi1.word + candi2.word
    com_str2 = candi2.word + candi1.word
    if libA.count(com_str1) > 0 | libD.count(com_str1) > 0:
        return com_str1
    elif libA.count(com_str2) > 0 | libD.count(com_str2) > 0:
        return com_str2


# ***************************求解公共串*************************
def getOverlap(s1, s2):
    m = min(len(s1), len(s2))
    for i in range(m, 0, -1):
        if s1[-i:] == s2[:i]:
            return(s2[:i])
        elif s2[-i:] == s1[:i]:
            return (s1[:i])
    return ''


# ***************************求解连接串*************************
def combineStr(s1, s2):
    """
    把两个有公共前缀或者后缀的词连接起来
    :param s1:  句子一
    :param s2:  句子二
    :return:    合并后的句子
    """
    m = min(len(s1), len(s2))
    for i in range(m, 0, -1):
        if s1[-i:] == s2[:i]:
            return s1 + s2[i:]
        elif s2[-i:] == s1[:i]:
            return s2 + s1[i:]


# ***************************选择候选词串*************************
def getCandidateWords(groupClause, participles, Tf, Cc):
    midCluster = list(participles)
    for item in participles:
        if (item.f_value < Tf) | (item.c_value < Cc):
            midCluster.remove(item)
    participles = midCluster
    print("_________________________选择候选词_______________________")
    for item in participles:
        print(item)
    return participles


list1 = []

list1 = RF('..\data\phraseTest.txt')
# print(list1)


listTest = [1, 2, 3, 4, 5, 6]
listResult = list(listTest)


#————————————————流程————————————————
candiwordslist =  getParticiples(list1, '')
gcw = getCandidateWords('',candiwordslist , Tf=0.6, Cc=5)
aa = adjustCandiWords(groupClause=list1, participles=candiwordslist, candiWords=gcw,
    leng=len(gcw), Tc=0.2, To=0.2, Tf=0.6, Cc=5, Tocal=0.6, libD='', libA='')
# bb = selectKeyWords(groupClause=list1, priticiples=candiwordsList,
#     candiWords=gcw, Locl=0.6, To=0.2)
print('|++++++++++++++++++++++++|++++++++++++++++++++++++')
print(aa)
#————————————————流程————————————————

# for item in listTest:
#     if item < 4:
#         listResult.remove(item)
#
# listTest = listResult
# print(listTest)

# for index1, value1 in enumerate(listTest):
#     for index2, value2 in enumerate(listTest, index1):
#         print(value1, value2)
for i in range(5):
    for j in range(i,5):
        if(i==j):
            break
        print(i,j)



