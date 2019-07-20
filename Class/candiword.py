import sys

class Candiword:
    """定义了一个公用的候选词类

    """
    def __init__(self, word, c_value, f_value, loc):
        """
        :param word: 字符串类型，用来表示候选词的内容
        :param c_value: int类型，用来表示词数信息
        :param f_value:float类型，用来表示词频信息
        :param loc:float类型：用来表示词位信息
        """
        self.word = word
        self.c_value = c_value
        self.f_value = f_value
        self.loc = loc
    def __str__(self):
        return " ".join(str(item) for item in (self.word, self.c_value, self.f_value, self.loc))


