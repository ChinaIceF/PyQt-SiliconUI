import random
from typing import Union

import numpy


class Color:
    @staticmethod
    def decodeColor(code: str):
        """
        解码色号为array，并且长度总是4
        :param code: 颜色色号 形如 #RRGGBB 或 #AARRGGBB
        :return: 长度为4的数组，值属于0-255
        """
        # code      STR     颜色色号 形如 #RRGGBB 或 #AARRGGBB
        code = Color.normalize(code)
        code = code.lstrip("#")
        a, r, g, b = int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16), int(code[6:8], 16)
        return numpy.array([a, r, g, b], dtype=numpy.int16)

    @staticmethod
    def encodeColor(value: Union[numpy.ndarray, list]):
        """
        将数组颜色转化为色号
        :param value: 数组类型的颜色
        :return: 色号
        """
        # value       NDARRAY 色值
        if len(value) == 3:
            r, g, b = value
            a = 255
        elif len(value) == 4:
            a, r, g, b = value
        else:
            raise ValueError(f"意外的输入值形状{value.shape}")

        return f"#{int(a):02X}{int(r):02X}{int(g):02X}{int(b):02X}"

    @staticmethod
    def mix(fore, post, weight=0.5):
        """
        将两种颜色相混合
        :param fore: 前景色
        :param post: 背景色
        :param weight: 前景色的透明度（在混合颜色中的权重）
        :return: 混合后颜色的色号
        """
        # fore      STR     前色
        # post      STR     后色
        # weight    FLOAT   前色的权重
        fore_rgb = Color.decodeColor(fore)
        post_rgb = Color.decodeColor(post)
        mixed_rgb = fore_rgb * weight + post_rgb * (1-weight)
        return Color.encodeColor(mixed_rgb)

    @staticmethod
    def transparency(code: str, transparency: float):
        """
        将颜色透明化
        :param code: 色号
        :param transparency: 透明度
        :return:
        """
        value = Color.decodeColor(code)
        value_proceed = value * numpy.array([transparency, 1, 1, 1])
        code_proceed = Color.encodeColor(value_proceed)
        return code_proceed


    @staticmethod
    def random():
        """
        返回一个随机色号
        :return: 随机色号
        """
        random_color = Color.encodeColor([255 * random.random(), 255 * random.random(), 255 * random.random()])
        return random_color

    @staticmethod
    def normalize(code):
        """
        将色号工归一化为ARGB类型
        :param code: 色号
        :return: ARGB类型色号
        """
        code_data = code.replace("#", "")
        if len(code_data) == 6:
            return f"#FF{code_data.upper()}"
        if len(code_data) == 8:
            return code.upper()
