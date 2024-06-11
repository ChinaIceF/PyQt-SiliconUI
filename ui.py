from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
import numpy
import time
import os

import silicon
from silicon.SiHint import *
from silicon.SiOverlay import *
import silicon.SiGlobal as SiGlobal

import components as Components

# 加载图标
import icons
SiGlobal.icons = icons.ICON_DICT('./icons/icons.dat')

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化 Hint 提示条
        self.floating_window = FloatingWindow()
        self.floating_window.setWindowOpacity(0)  # 初始隐藏小窗口
        self.floating_window.show()
        SiGlobal.floating_window = self.floating_window

        # 初始化二级界面叠加层
        self.overlay = SiOverlay(self)
        SiGlobal.overlay = self.overlay

        # 构建界面
        self.initUI()

        # 叠加层置顶
        self.overlay.raise_()


    def showEvent(self, event):
        self.overlay.showup_animation.setCurrent(self.geometry().height())
        self.overlay.moveFrame(self.geometry().height())
        self.overlay.hide()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        if w < 600:
            return
        self.stackarea.setGeometry(0, 0, w, h)
        self.overlay.setGeometry(0, 0, w, h)

    def initUI(self):

        # 结构
        # silicon.SiStackArea
        #     silicon.SiStackOption （里面包含一个标题和一个silicon.SiScrollArea）
        #         silicon.SiFrame
        #             silicon.SiStack
        #                 silicon.SiOptionButton
        #                 silicon.SiOptionSwitch
        #                 silicon.SiOptionComboBox
        #                 ......


        # ========== 初始化窗口 ==========

        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setGeometry(0, 0, 1200, 700)
        self.setWindowTitle("Silicon UI 测试界面")

        self.stackarea = silicon.SiStackArea(self)
        self.stackarea.setGeometry(0, 0, 1200, 600)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('./img/logo.png'))
        self.logo.setGeometry(64+4, 16+4, 24, 24)

        self.window_title = QLabel(self)
        self.window_title.setStyleSheet('color:#cfcfcf')
        self.window_title.setGeometry(104, 0, 500, 64)
        self.window_title.setText('Silicon 画廊 - 测试界面')
        self.window_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.window_title.setFont(silicon.SiFont.font_L1_bold)

        # ========== 初始化各个界面 ==========

        self.homepage = silicon.SiStackOption(self)
        self.homepage.setTitleHeight(0)
        self.homepage.scrollarea.rightside_interval = 0
        self.homepage.attachFrame(Components.Homepage.SiHomePage(self.homepage))
        self.homepage.scrollarea.scrollbar.raise_()

        self.glaze_example = silicon.SiStackOption(self)
        self.glaze_example.setTitle('Silicon Glaze 示例')
        self.glaze_example.attachFrame(Components.Glaze.GlazeExample(self.glaze_example))
        self.glaze_example.scrollarea.scrollbar.raise_()

        self.widgets_example = silicon.SiStackOption(self)
        self.widgets_example.setTitle('控件')
        self.widgets_example.attachFrame(Components.Widgets.WidgetsExample(self.widgets_example))
        self.widgets_example.scrollarea.scrollbar.raise_()

        self.options = silicon.SiStackOption(self)
        self.options.setTitle('设置')
        self.options.attachFrame(Components.Options.Options(self.options))
        self.options.scrollarea.scrollbar.raise_()

        # 添加到 stackarea
        self.stackarea.addStack(self.homepage, SiGlobal.icons.get('fi-rr-home'), '主页面')
        self.stackarea.addStack(self.widgets_example, SiGlobal.icons.get('fi-rr-layout-fluid'), '控件')
        self.stackarea.addStack(self.glaze_example, SiGlobal.icons.get('fi-rr-list'), 'Silicon Glaze 示例')
        self.stackarea.addStack(self.options, SiGlobal.icons.get('fi-rr-settings'), '设置', 'bottom')
