# 保存文件的函数
def savefile(savefile, content):
    fp = open(savefile, 'w')
    fp.write(content)
    fp.close()

# 读取文件的函数
def readfile(path):
    fp = open(path, 'r')
    content = fp.read()
    fp.close()
    return content

# 返回list的函数
def readfilebyline(path):
    f = open(path, 'r')
    result = list()
    for line in f.read().splitlines():
        result.append(line)
    f.close()
    return result

# print(len(readfilebyline('..\data\phraseTest.txt')))

