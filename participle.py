# 用来实现分词
import jieba
filepath = 'C:/Users/Alan/py-source/phrasingResult.txt'
paragraph = open(filepath).read()

# seg_list = jieba.lcut(paragraph, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# seg_list = jieba.cut(paragraph, cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

# seg_list = jieba.cut(paragraph)  # 默认是精确模式
# print(", ".join(seg_list))
#
seg_list = jieba.cut_for_search(paragraph)  # 搜索引擎模式
print(", ".join(seg_list))