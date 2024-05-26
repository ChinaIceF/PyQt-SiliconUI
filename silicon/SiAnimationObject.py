from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import numpy

from . import SiGlobal

class SiAnimation(QObject):
    ticked = pyqtSignal(object) # 动画进行一刻的信号

    def __init__(self, distance = None, stepLength = None, interval = 1000 / SiGlobal.fps, isCompleted = None):
        super().__init__()
        self.distance_ = distance            # 获取与目标参数还差多少
        self.stepLength_ = stepLength        # 计算这一步的步长
        self.interval = interval            # 每一刻的时间间隔，单位 ms
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
        dis = self.distance()
        steplength = self.stepLength(dis)

        # 发射信号
        self.ticked.emit(steplength)

        # 如果已经到达既定位置，终止计时器
        if self.isCompleted():
            self.stop()

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