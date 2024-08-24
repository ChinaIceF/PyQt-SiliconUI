import numpy

from .abstract import ABCSiAnimation, Curve


class SiExpAnimation(ABCSiAnimation):
    """ 级数动画类，每次动画的进行步长都与当前进度有关 """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.factor = 1/2
        self.bias = 1

    def setFactor(self, factor: float):
        """
        Set the factor of the animation.
        :param factor: number between 0 and 1
        """
        self.factor = factor

    def setBias(self, bias: float):
        """
        Set the factor of the animation.
        :param bias: positive float number
        """
        if bias <= 0:
            raise ValueError(f"Bias is expected to be positive but met {bias}")
        self.bias = bias

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = abs(dis) * self.factor + self.bias  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr

    def isCompleted(self):
        """ To check whether we meet the point that the animation should stop """
        return (self._distance() == 0).all()

    def _process(self):
        # 如果已经到达既定位置，终止计时器，并发射停止信号
        if self.isCompleted():
            self.stop()
            self.finished.emit(self.target_)
            return

        step_length = self._step_length()

        # 更新数值
        self.setCurrent(self.current_ + step_length)

        # 发射信号
        self.ticked.emit(self.current_)


class SiExpAccelerateAnimation(SiExpAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.accelerate_function = lambda x: x ** 1.6
        self.step_length_bound = 0
        self.frame_counter = 0

    def setAccelerateFunction(self, function):
        self.accelerate_function = function

    def setStepLengthBound(self, bound):
        self.step_length_bound = bound

    def refreshStepLengthBound(self):
        self.setStepLengthBound(min(self.accelerate_function(self.frame_counter), 10000))  # prevent getting too large

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = numpy.clip(abs(dis) * self.factor + self.bias, 0, self.step_length_bound)  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr

    def _process(self):
        self.frame_counter += 1
        self.refreshStepLengthBound()
        super()._process()

    def stop(self, delay=None):
        super().stop(delay)
        self.frame_counter = 0
        self.refreshStepLengthBound()


class SiSqrExpAnimation(ABCSiAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mean_rate = 0.5
        self.base = 1/2
        self.peak = 10
        self.bias = 1
        raise NotImplementedError()

    def setMeanRate(self, mean_rate):
        self.mean_rate = mean_rate

    def setBase(self, base):
        self.base = base

    def setPeak(self, peak):
        self.peak = peak

    def setBias(self, bias):
        self.bias = bias

    def _step_length(self):
        dis = self._distance()
        if (abs(dis) <= self.bias).all() is True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype="int8")
        arr = abs(dis) * self.factor + self.bias  # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut  # 对于差距小于偏置的项，直接返回差距
        return arr

    def isCompleted(self):
        return (self._distance() == 0).all()


class SiCounterAnimation(ABCSiAnimation):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.duration = 1000  # 动画总时长，单位毫秒
        self.reversed = False  # 是否倒序运行动画
        self.counter_addend = self._get_addend()
        self.curve = Curve.LINEAR

    def setReversed(self, reversed_):
        """
        Set whether the animation is reversed
        :param reversed_:
        :return:
        """
        self.reversed = reversed_

    def setDuration(self, duration):
        """
        Set the duration of the animation.
        :param duration: ms
        :return:
        """
        self.duration = duration
        self.counter_addend = self._get_addend()

    def setInterval(self, interval: int):
        super().setInterval(interval)
        self.counter_addend = self._get_addend()

    def _get_addend(self):
        """
        Get the addend for the counter
        :return:
        """
        duration = self.duration
        interval = self.timer.spacing()  # 两个值全是 毫秒 ms
        return interval / duration

    def setCurve(self, curve_func):
        """
        Set the animation curve.
        :param curve_func: a function which expect an input between 0 and 1, return a float number
        :return:
        """
        self.curve = curve_func

    def isCompleted(self):
        """
        To check whether we meet the point that the animation should stop
        :return: bool
        """
        self.counter = max(min(1, self.counter), 0)  # 规范计数器数值，防止超出范围
        return (self.reversed is False and self.counter == 1) or (self.reversed and self.counter == 0)

    def _process(self):
        # 如果已经到达既定位置，终止计时器，并发射停止信号
        if self.isCompleted():
            self.stop()
            self.finished.emit(self.target_)
            return

        # 计数器更新
        self.counter = self.counter + (-1 if self.reversed else 1) * self.counter_addend

        # 更新数值
        self.setCurrent(self.curve(self.counter))

        # 发射信号
        self.ticked.emit(self.current_)
