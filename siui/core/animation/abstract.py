
import numpy
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class ABCAnimation(QObject):
    ticked = pyqtSignal(object)     # 动画进行一刻的信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.target = numpy.array(0)         # 目标值
        self.current = numpy.array(0)        # 当前值

        # 构建计时器
        self.timer = QTimer()
        self.timer.setInterval(int(1000/60))
        self.timer.timeout.connect(self._process)  # 每经历 interval 时间，传入函数就被触发一次

    def setTarget(self, target):
        """
        Set the target of the animation.
        :param target: Anything can be involved in calculations.
        :return: None
        """
        self.target = numpy.array(target)

    def setCurrent(self, current):
        """
        Set the current value of the animation.
        :param current: Anything can be involved in calculations.
        :return: None
        """
        self.current = numpy.array(current)

    def _distance(self):
        """
        Get the D-value between current and target.
        :return: D-value
        """
        return self.target - self.current

    def _step_length(self):
        raise NotImplementedError()

    def isCompleted(self):
        """
        To check whether we meet the point that the animation should stop
        :return: bool
        """
        return (self.distance() == 0).all()

    def _process(self):
        # 如果已经到达既定位置，终止计时器
        if self.isCompleted():
            self.stop()
            return

        step_length = self._step_length()

        # 更新数值
        self.setCurrent(self.current + step_length)

        # 发射信号
        self.ticked.emit(self.current)

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
        :return: None
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
