from PyQt5.Qt import *
from PyQt5.QtCore import *


class ABCAnimation(QObject):
    ticked = pyqtSignal(object)     # 动画进行一刻的信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.target = 0
        self.current = 0

        self.timer = QTimer()
        self.timer.setInterval(int(self.interval))
        self.timer.timeout.connect(self._process)  # 每经历 interval 时间，传入函数就被触发一次

    def setTarget(self, target):
        """
        Set the target of the animation.
        :param target: Anything can be involved in calculations.
        :return: None
        """
        self.target = target

    def setCurrent(self, current):
        """
        Set the current value of the animation.
        :param current: Anything can be involved in calculations.
        :return: None
        """
        self.current = current

    def distance(self):
        """
        Get the D-value between current and target.
        :return: D-value
        """
        return self.target - self.current

    def stepLength(self, dis):
        """
        Get the step length that animation should move forward with
        :param dis: the D-value between current and target.
        :return: step length
        """
        return self._step_length_function(dis)

    def _step_length_function(self, dis):
        return dis

    def isCompleted(self):
        """
        To check whether we meet the point that the animation should stop
        :return: bool
        """
        return None

    def _process(self):
        # 如果已经到达既定位置，终止计时器
        if self.isCompleted():
            self.stop()
            return

        dis = self.distance()
        step_length = self.stepLength(dis)

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
        self.timer.setInterval(self.interval)

    def try_to_start(self):
        """
        Start the animation but check whether the animation is active first
        :return: whether this attempt is succeeded.
        """
        if not self.isActive():
            self.start()
        return not self.isActive()
