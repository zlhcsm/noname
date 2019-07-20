# coding=utf-8
import numpy as np
from math import sqrt
import time
# 用来计算两个短句之间的相似度
from sentenceSimilarity import jaccard_similarity as JSI

from constant import FILEPATH as FP

# 定义一个簇单元
class ClusterUnit:
    def __init__(self):
        self.node_list = []         # 该簇存在的节点列表
        self.node_num = 0           # 该簇节点数
        self.centroid = ''          # 该簇的质心（也就是第一句话）

    def add_node(self, node, sent, flag):
        """
        为本簇添加指定节点，并更新簇心
         sent:该节点的字符串
         node:节点
         flag:1表示存在簇类，0表示新建的簇类
         return:null
        """
        self.node_list.append(sent)
        if(flag == 0):                                  # 如果原来不存在类，则添加
            self.centroid = sent
        self.node_num += 1                              # 节点数加1


class OnePassCluster:
    def __init__(self, t, sens_list):
        # t:一趟聚类的阈值
        self.threshold = t                      # 一趟聚类的阈值
        self.sents = sens_list                  # 数据列表
        self.cluster_list = []                  # 聚类后簇的列表

        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)       # 聚类完成后 簇的个数
        self.spend_time = t2 - t1                       # 聚类花费的时间

    def clustering(self):
        self.cluster_list.append(ClusterUnit())                     # 初始新建一个簇
        self.cluster_list[0].add_node(0, self.sents[0], 0)          # 将读入的第一个节点归于该簇
        for index in range(len(self.sents))[1:]:                    # 从第二个句子来开始分类，index为列表的下标
            max_similarity = JSI(self.sents[index], self.sents[0])    # 与簇的质心的最小距离
            max_sililarity_cluster_index = 0                          # 最大相似度的簇的索引
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # enumerate会将数组或列表组成一个索引序列
                # 寻找相似度最大的簇，记录相似度和对应的簇的索引
                similarity = JSI(self.sents[index], cluster.node_list[0])

                if similarity > max_similarity:
                    max_similarity = similarity
                    max_sililarity_cluster_index = cluster_index + 1
            if max_similarity > self.threshold:                       # 最大相似度大于阈值，则归于该簇
                self.cluster_list[max_sililarity_cluster_index].add_node(index, self.sents[index], 1)
            else:                                                   # 最大相似度小于阈值，则新建一个簇
                new_cluster = ClusterUnit()
                new_cluster.add_node(index, self.sents[index], 0)
                self.cluster_list.append(new_cluster)
                del new_cluster

    def print_result(self):
        # 打印出聚类结果
        # label_dict:节点对应的标签字典
        print("***********  single-pass的聚类结果展示  ***********")
        for index, cluster in enumerate(self.cluster_list):
            # 把生成的聚类文件写入txt
            filename = FP + "/cluster/cluster" + str(index + 1) + '.txt'
            f = open(filename, 'a+')
            for node in  cluster.node_list:
                f.write(node + '\n')
            f.close()

            print("cluster:%s" % index)         # 簇的序号
            print(cluster.node_list)            # 该簇的节点列表
            print("node num: %s" % cluster.node_num)
            print( "-------------")
        print( "所有节点的个数为： %s" % len(self.sents))
        print("簇类的个数为：%s" % self.cluster_num)
        print("花费的时间为： %.9fs" % (self.spend_time / 1000))



# 读取测试集
f = open(FP + 'phrasingResult.txt', 'r')
lines = f.read().splitlines()
# print(lines)
f.close()

# 构建一趟聚类器
clustering = OnePassCluster(sens_list=lines, t=0.2)
clustering.print_result()

