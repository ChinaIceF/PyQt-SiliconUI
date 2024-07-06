import time

class TokenizedDatabase:
    def __init__(self, name):
        self.name = name
        self.item_tokens = []
        self.item_values = []

    def register(self, token, value):
        """
        注册一个新项
        :param token: 项名
        :param value: 项值
        :return:
        """
        # 如果项已经存在，直接覆写
        if token in self.item_tokens:
            index = self.item_tokens.index(token)
            self.item_values[index] = value
            return

        self.item_tokens.append(token)
        self.item_values.append(value)

    def fromToken(self, token):
        """
        根据提供的 token 获取对应的项值
        :param token: token
        :return: 项值
        """
        if (token in self.item_tokens) is False:
            raise ValueError(f"未在此数据库（{self.name}）内找到名为 {token} 的项")

        index = self.item_tokens.index(token)
        return self.item_values[index]

    def tree(self, level=0):
        """
        打印结构树
        :param level: 层级
        :return:
        """
        stem = "│"
        branch = "├"
        branch_end = "└"
        node_value = "◇"
        node_subtree = "◆"

        if level == 0:
            print(self)

        for token, value in zip(self.item_tokens, self.item_values):
            is_end = token != self.item_tokens[-1]
            is_subtree = isinstance(value, TokenizedDatabase)
            print(stem * level +
                  (branch if is_end else branch_end) +
                  (node_subtree if is_subtree else node_value) +
                  " " + token + " = " + str(value))

            if is_subtree:
                value.tree(level = level + 1)
