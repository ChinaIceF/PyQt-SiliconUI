import abstract
import numpy


class SiExpAnimation(abstract.ABCAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.factor = 1 / 2
        self.bias = 1

    def setFactor(self, factor: float):
        """
        Set the factor of the animation.
        :param factor: number between 0 to 1
        :return: None
        """
        self.factor = factor

    def setBias(self, bias: float):
        """
        Set the factor of the animation.
        :param bias: positive float number
        :return: None
        """
        if bias <= 0:
            raise ValueError(f"Bias is expected to be positive but met {bias}")
        self.bias = bias

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = abs(dis) * self.factor + self.bias                     # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)     # 确定动画方向
        arr = arr * (1 - cut) + dis * cut                            # 对于差距小于偏置的项，直接返回差距
        return arr
