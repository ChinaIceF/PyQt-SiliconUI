from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from . import SiFont
import time

from .SiGlobal import *

class SiSwitch(QLabel):
    clicked = QtCore.pyqtSignal()
    stateChanged = QtCore.pyqtSignal(bool)
    animation_refreshed = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.setStyleSheet('')
        
        self.name = None
        self.status = False

        self.target_position = 5

        self.status_width = 62

        # 状态标签（显示 开/关）
        self.status_label = QLabel(self)
        self.status_label.setFont(SiFont.font_L1)
        self.status_label.setGeometry(0, 0, self.status_width, 24)
        self.status_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.status_label.setText('关闭')

        # 按钮的框架
        self.switch_frame = QLabel(self)
        self.switch_frame.setGeometry(self.status_width + 24, 2, 40, 20)

        # 按钮圆
        self.switch_lever = QLabel(self.switch_frame)
        self.switch_lever.setGeometry(3, 3, 14, 14)

        self.fps = 60
        self.timer = QTimer()

        self.animation_refreshed.connect(self.change_position)

        self.timer.setInterval(int(1000 / self.fps))
        self.timer.timeout.connect(self.process)

        self.initialize_stylesheet()

    def stepLength(self, dis):
        return abs(dis) * 0.2 + 1

    def distance(self):
        return self.target_position - self.switch_lever.geometry().x()

    def direction(self, number):
        if number > 0:
            return 1
        if number < 0:
            return -1
        return 0

    def process(self):

        dis = self.distance()
        delta = self.stepLength(dis)
        self.animation_refreshed.emit(self.direction(dis) * int(delta))

        # 如果已经到达既定位置，终止计时器
        if self.distance() == 0:
            self.timer.stop()


    def startAnimation(self):
        self.timer.start()


    def initialize_stylesheet(self):
        self.status_label.setStyleSheet('color: {}'.format(colorset.SWC_HEX[0]))
        self.switch_frame.setStyleSheet('border: 1px solid {}; border-radius: 10px'.format(colorset.SWC_HEX[0]))
        self.switch_lever.setStyleSheet('background-color:{}; border-radius: 7px'.format(colorset.SWC_HEX[0]))

    def changeStatus(self, status, signal = False):
        self.status = status
        if status == True:
            #self.switch_lever.setGeometry(5 + 16, 5, 14, 14)
            self.target_position = 3 + 20
            self.status_label.setText('开启')
        else:
            #self.switch_lever.setGeometry(5, 5, 14, 14)
            self.target_position = 3
            self.status_label.setText('关闭')

        if self.timer.isActive() == False:    # 如果线程没在运行，就启动
            self.startAnimation()

        if signal == True:
            self.clicked.emit()
            self.stateChanged.emit(self.status)

    def change_position(self, distance):
        g = self.switch_lever.geometry()
        self.switch_lever.move(int(g.x() + distance), g.y())

        if (g.x() + distance - 3) / 20 >= 0.5:
            self.switch_frame.setStyleSheet('''
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 {}, stop:1 {});
                border-radius: 10px'''.format(*colorset.THEME_HEX))
            self.switch_lever.setStyleSheet('''
                background-color:{};
                border-radius: 7px'''.format(colorset.SWC_HEX[1]))

        else:
            self.switch_frame.setStyleSheet('border: 1px solid {}; border-radius: 10px'.format(colorset.SWC_HEX[0]))
            self.switch_lever.setStyleSheet('background-color:{}; border-radius: 7px'.format(colorset.SWC_HEX[0]))


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 被左键点击
            if self.timer.isActive() == True:    # 如果线程运行中，忽略这一次点击
                return

            self.changeStatus(not self.status, signal = True)
