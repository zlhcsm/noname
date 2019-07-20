import jieba
import jieba.analyse
import nltk

paragraph ="杯状减少，杯状细胞减少，杯状细胞减少，杯状细胞减少，杯状细胞|减少，杯状细胞|减少，腺管杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞消失，腺上皮麟状细胞化生，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞减少，腺上皮杯状细胞|减少，杯状细胞减少|不规则，腺上皮|正常杯状细胞，腺上皮杯状细胞减少|消失，浅表腺体腺上皮杯状细胞减少，结肠粘膜腺上皮杯状细胞减少，直肠粘膜腺上皮杯状细胞减少"

# word_list = jieba.lcut(paragraph)
# print(jieba.analyse.extract_tags(paragraph, topK=5))
#
# import jieba.posseg as pseg
# words = pseg.cut(paragraph)
# for word, flag in words:
#     print('%s, %s' % (word, flag))




import lib.fileOperate as FO
content = FO.readfile('data\phraseTest1.txt')
keywords = " ".join(jieba.analyse.extract_tags(content, topK=4))
print(keywords)