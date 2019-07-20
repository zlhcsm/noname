
filepath = 'C:/Users/Alan/py-source/phrasing.txt'
primevalfile = open(filepath, 'r')
result = list()

# #readline的效率比readlines的低
# #方法一
# for line in open(filepath):
#     line = primevalfile.readline()
#     print(line)
#     result.append(line)

# 方法二
for line in primevalfile.readlines():
    line = line.strip()                     #去掉每行头尾空白
    if not len(line) or line.startswith('#'):
        continue
    if len(line) <= 15:
        result.append(line)

# print(result)
open('C:/Users/Alan/py-source/phrasingResult.txt', 'a+').write('%s' % '\n'.join(result))
primevalfile.close()
