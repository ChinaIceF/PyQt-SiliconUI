
import numpy
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

global_fps = 60

class Curve:
    def LINEAR(self, x):
        return x



class ABCAnimation(QObject):
    ticked = pyqtSignal(object)     # 动画进行一刻的信号
    finished = pyqtSignal(object)   # 动画完成的信号，回传目标值

    def __init__(self, parent=None):
        super().__init__(parent)

        self.target_ = numpy.array(0)         # 目标值
        self.current_ = numpy.array(0)        # 当前值
        self.counter = 0                     # 计数器

        # 构建计时器
        self.timer = QTimer()
        self.timer.setInterval(int(1000/global_fps))
        self.timer.timeout.connect(self._process)  # 每经历 interval 时间，传入函数就被触发一次

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

    def stop(self):
        """
        Stop the animation immediately
        :return:
        """
        self.timer.stop()

    def start(self):
        """
        Start the animation by using self.timer.start()
        :return:
        """
        self.timer.start()

    def setInterval(self, interval: int):
        """
        Set the time interval of the timer
        :param interval: Time interval (ms)
        :return:
        """
        self.timer.setInterval(interval)

    def try_to_start(self):
        """
        Start the animation but check whether the animation is active first
        :return: whether this attempt is succeeded.
        """
        if not self.isActive():
            self.start()
        return not self.isActive()
