from typing import Any

import numpy
from PyQt5.QtCore import (
    QAbstractAnimation,
    QObject,
    QPoint,
    QPointF,
    QRect,
    QRectF,
    QSize,
    QSizeF,
    QTimer,
    pyqtSignal,
)
from PyQt5.QtGui import QColor

global_fps = 60


class Curve:
    @staticmethod
    def LINEAR(x):
        return x


class ABCSiAnimation(QObject):
    ticked = pyqtSignal(object)     # 动画进行一刻的信号
    finished = pyqtSignal(object)   # 动画完成的信号，回传目标值

    def __init__(self, parent=None):
        super().__init__(parent)

        self.enabled = True
        self.target_ = numpy.array(0)         # 目标值
        self.current_ = numpy.array(0)        # 当前值
        self.counter = 0                     # 计数器

        # 构建计时器
        self.timer = QTimer()
        self.timer.setInterval(int(1000/global_fps))
        self.timer.timeout.connect(self._process)  # 每经历 interval 时间，传入函数就被触发一次
        # self.timer.setTimerType(Qt.PreciseTimer)

        # 构建行为计时器
        self.action_timer = QTimer()
        self.action_timer.setSingleShot(True)
        # self.action_timer.setTimerType(Qt.PreciseTimer)

    def setEnable(self, on):
        self.enabled = on
        if on is False:
            self.stop()

    def isEnabled(self):
        return self.enabled

    def setFPS(self, fps: int):
        """
        set fps of the animation.
        """
        self.timer.setInterval(int(1000 / fps))

    def setTarget(self, target):
        """
        Set the target of the animation.
        :param target: Anything can be involved in calculations.
        :return:
        """
        self.target_ = numpy.array(target)

    def setCurrent(self, current):
        """
        Set the current value of the animation.
        :param current: Anything can be involved in calculations.
        :return:
        """
        self.current_ = numpy.array(current)

    def current(self):
        """
        返回动画计数器的当前值
        :return: 当前值
        """
        return self.current_

    def target(self):
        """
        返回动画计数器的目标值
        :return: 目标值
        """
        return self.target_

    def _distance(self):
        """
        Get the D-value between current and target.
        :return: D-value
        """
        return self.target_ - self.current_

    def _step_length(self):
        raise NotImplementedError()

    def _process(self):
        raise NotImplementedError()

    def isCompleted(self):
        """
        To check whether we meet the point that the animation should stop
        :return: bool
        """
        raise NotImplementedError()

    def isActive(self):
        """
        To check whether the timer of this animation is activated
        :return: bool
        """
        return self.timer.isActive()

    def stop(self, delay=None):
        """
        Stop the animation
        :param delay: msec, time delay before this action works
        """
        if delay is None:
            self.timer.stop()
        else:
            self.action_timer.singleShot(delay, self.timer.stop)

    def start(self, delay=None):
        """
        Start the animation
        :param delay: msec, time delay before this action works
        """
        if self.isEnabled() is False:
            return

        if delay is None:
            self.timer.start()
        else:
            self.action_timer.singleShot(delay, self.timer.start)

    def setInterval(self, interval: int):
        """
        Set the time interval of the timer
        :param interval: Time interval (ms)
        :return:
        """
        self.timer.setInterval(interval)

    def try_to_start(self, delay=None):
        """
        Start the animation but check whether the animation is active first
        :return: whether this attempt is succeeded.
        """
        if not self.isActive():
            self.start(delay=delay)
        return not self.isActive()


class SiExpAnimation(ABCSiAnimation):
    """ 级数动画类，每次动画的进行步长都与当前进度有关 """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.factor = 1/2
        self.bias = 1

    def init(self, factor: float, bias: float, current: Any, target: Any, fps: int = 60):
        self.setFactor(factor)
        self.setBias(bias)
        self.setCurrent(current)
        self.setTarget(target)
        self.setFPS(fps)

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
        interval = self.timer.interval()  # 两个值全是 毫秒 ms
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


class SiAnimationGroup:
    """
    动画组，为多个动画的管理提供支持，允许使用token访问动画对象
    """
    def __init__(self):
        self.animations = []
        self.tokens = []

    def addMember(self, ani, token: str):
        if token in self.tokens:
            raise ValueError(f"代号已经存在：{token}")
        self.animations.append(ani)
        self.tokens.append(token)

    def fromToken(self, aim_token: str) -> ABCSiAnimation:
        for ani, token in zip(self.animations, self.tokens):
            if token == aim_token:
                return ani
        raise ValueError(f"未在代号组中找到传入的代号：{aim_token}")


class TypeConversionFuncs:
    functions = {
        QPoint.__name__: [
            lambda x: numpy.array((x.x(), x.y()), dtype="float64"),
            lambda x: QPoint(int(x[0]), int(x[1]))
        ],
        QPointF.__name__: [
            lambda x: numpy.array((x.x(), x.y()), dtype="float64"),
            lambda x: QPointF(float(x[0]), float(x[1])),
        ],
        QSize.__name__: [
            lambda x: numpy.array((x.width(), x.height()), dtype="float64"),
            lambda x: QSize(int(x[0]), int(x[1])),
        ],
        QSizeF.__name__: [
            lambda x: numpy.array((x.width(), x.height()), dtype="float64"),
            lambda x: QSizeF(float(x[0]), float(x[1])),
        ],
        QRect.__name__: [
            lambda x: numpy.array((x.x(), x.y(), x.width(), x.height()), dtype="float64"),
            lambda x: QRect(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
        ],
        QRectF.__name__: [
            lambda x: numpy.array((x.x(), x.y(), x.width(), x.height()), dtype="float64"),
            lambda x: QRectF(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
        ],
        QColor.__name__: [
            lambda x: numpy.array(x.getRgb(), dtype="float64"),
            lambda x: QColor(int(x[0]), int(x[1]), int(x[2]), int(x[3]))
        ]
    }


class SiExpAnimationRefactor(QAbstractAnimation):
    valueChanged = pyqtSignal(object)

    def __init__(self, target: QObject, property_name=None, parent=None) -> None:
        super().__init__(parent)
        self.start_after_timer = QTimer(self)

        self._target = target
        self._property_name = None
        self._property_type = None
        self._in_func = None
        self._out_func = None
        self._end_value = None
        self._current_value = None
        self.factor = 1/4
        self.bias = 0.5

        self._velocity_inertia = 0.0  # value between 0 and 1, higher value causes animation harder to accelerate.
        self._velocity = 0

        if property_name is not None:
            self.setPropertyName(property_name)

    def init(self, factor: float, bias: float, current_value, end_value) -> None:
        self.factor = factor
        self.bias = bias
        self.setCurrentValue(current_value)
        self.setEndValue(end_value)
        self.resetVelocity()

    def setFactor(self, factor: float):
        self.factor = factor

    def setBias(self, bias: float):
        self.bias = bias

    def target(self) -> QObject:
        return self._target

    def propertyName(self) -> str:
        return self._property_name

    def endValue(self, raw=False) -> Any:
        if raw is True:
            return self._end_value
        else:
            return self._out_func(self._end_value)

    def currentValue(self, raw=False) -> Any:
        if raw is True:
            return self._current_value
        else:
            return self._out_func(self._current_value)

    def distance(self) -> numpy.array:
        return self._end_value - self._current_value

    def duration(self) -> int:
        return -1

    def start(self, *args, **kwargs):
        if self.state() != QAbstractAnimation.State.Running:
            super().start(*args, **kwargs)

    def startAfter(self, msec: int):
        self.start_after_timer.singleShot(msec, self.start)

    def fromProperty(self):
        """ load value from target's property """
        self.setCurrentValue(self._target.property(self._property_name))

    def toProperty(self):
        """ set target's property to animation value """
        self._target.setProperty(self._property_name, self._out_func(self._current_value))

    def setPropertyName(self, name: str) -> None:
        self._property_name = name
        self._property_type = type(self._target.property(name))
        self._loadConversionFuncs()
        self._end_value = self._in_func(self._target.property(name))
        self._current_value = self._in_func(self._target.property(name))

    def setEndValue(self, value: Any) -> None:
        if isinstance(value, self._property_type):
            self._end_value = self._in_func(value)
        else:
            self._end_value = numpy.array(value)

    def setCurrentValue(self, value: Any) -> None:
        if isinstance(value, self._property_type):
            self._current_value = self._in_func(value)
        else:
            self._current_value = numpy.array(value)
        self.valueChanged.emit(self._current_value)

    def resetVelocity(self):
        self._velocity = 0 * self._current_value

    def setVelocityInertia(self, n: float):
        self._velocity_inertia = n

    def updateCurrentTime(self, _) -> None:
        # print(self.distance())
        if (self.distance() == 0).all():
            self.stop()
            return

        distance = self._end_value - self._current_value
        flag = numpy.array(abs(distance) <= self.bias, dtype="int8")
        step = abs(distance) * self.factor + self.bias                   # 基本指数动画运算
        step = step * (numpy.array(distance > 0, dtype="int8") * 2 - 1)  # 确定动画方向
        step = step * (1 - flag) + distance * flag                       # 差距小于偏置的项，返回差距

        self._velocity = self._velocity * self._velocity_inertia + step * (1 - self._velocity_inertia)

        self._current_value = self._current_value + self._velocity
        self.valueChanged.emit(self._current_value)
        try:
            self._target.setProperty(self._property_name, self._out_func(self._current_value))
        except RuntimeError:
            pass

    def _loadConversionFuncs(self) -> None:
        if self._property_type.__name__ in TypeConversionFuncs.functions.keys():
            self._in_func = TypeConversionFuncs.functions.get(self._property_type.__name__)[0]
            self._out_func = TypeConversionFuncs.functions.get(self._property_type.__name__)[1]
        else:
            self._in_func = lambda x: numpy.array(x)
            self._out_func = lambda x: self._property_type(numpy.array(x, dtype="float64"))
