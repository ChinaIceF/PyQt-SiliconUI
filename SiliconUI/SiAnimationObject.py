from PyQt5.Qt import *
from PyQt5.QtCore import *
import numpy

from . import SiGlobal

class SiAnimation(QObject):
    ticked = pyqtSignal(object) # 动画进行一刻的信号

    def __init__(self, distance = None,
                       stepLength = None,
                       interval = 1000 / SiGlobal.fps,
                       isCompleted = None):
        super().__init__()
        self.distance_ = distance            # 获取与目标参数还差多少
        self.stepLength_ = stepLength        # 计算这一步的步长
        self.interval = interval             # 每一刻的时间间隔，单位 ms
        self.isCompleted_ = isCompleted

        self.target = 0
        self.current = 0

        self.timer = QTimer()
        self.timer.setInterval(int(self.interval))
        self.timer.timeout.connect(self.process)  # 每经历 interval 时间，传入函数就被触发一次

    def setTarget(self, target):
        self.target = target

    def setCurrent(self, current):
        self.current = current

    def distance(self):
        return self.distance_()

    def stepLength(self, dis):
        return self.stepLength_(dis)

    def isCompleted(self):
        return self.isCompleted_()

    def process(self):
        # 如果已经到达既定位置，终止计时器
        if self.isCompleted():
            self.stop()
            return

        dis = self.distance()
        steplength = self.stepLength(dis)

        # 更新数值
        self.setCurrent(self.current + steplength)

        # 发射信号
        self.ticked.emit(self.current)


    def isActive(self):
        return self.timer.isActive()

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start()

    def setInterval(self, interval):
        self.interval = interval
        self.timer.setInterval(self.interval)

    def try_to_start(self):
        if self.isActive() == False:
            self.start()
            return True
        else:
            return False


class SiAnimationStandard(SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.factor = 1/8
        self.bias = 0.01

    def setFactor(self, factor):
        self.factor = factor

    def setBias(self, bias):
        self.bias = bias

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= self.bias:
            return dis
        else:
            return (abs(dis) * self.factor + self.bias) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0


class SiAnimationStandardForArray(SiAnimationStandard):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

    def setTarget(self, target):
        if type(target) == float or type(target) == int:
            print('警告：你使用了适用于数组的动画类，但是传入了单个数字，这可能具有误导性')
        self.target = numpy.array(target)

    def setCurrent(self, current):
        if type(current) == float or type(current) == int:
            print('警告：你使用了适用于数组的动画类，但是传入了单个数字，这可能具有误导性')
        self.current = numpy.array(current)

    def stepLength(self, dis):
        if (abs(dis) <= self.bias).all() == True:
            return dis

        cut = numpy.array(abs(dis) <= self.bias, dtype = 'int8')
        arr = abs(dis) * self.factor + self.bias                    # 基本指数动画运算
        arr = arr * (numpy.array(dis > 0, dtype = 'int8') * 2 - 1)  # 确定动画方向
        arr = arr * (1 - cut) + dis * cut                           # 对于差距小于偏置的项，直接返回差距
        return arr

    def isCompleted(self):
        return (self.distance() == 0).all()
