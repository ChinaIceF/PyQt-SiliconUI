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

import SiliconUI
import SiliconUI.SiGlobal as SiGlobal

from .sub_example_A import *
from .sub_example_B import *
from SiliconUI.SiGlobal import colorset
from SiliconUI.SiFont import *

class Log(object):
    def __init__(self, title):
        self.title = title
        self.columns = []

    def addColumn(self, title):
        self.columns.append([title, ''])

    def addText(self, text):
        self.columns[-1][1] = self.columns[-1][1] + text

class UpdateLogs(SiliconUI.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.max_width_policy = False  # 取消过长中置
        self.setStyleSheet('')

        self.log_width = 600

        # 内容的布局，左边是更新版本导航栏，右边是日志内容
        self.layout_main = SiliconUI.SiLayoutH(self)
        self.layout_main.setInterval(64)

        # 版本的 sticker
        self.sticker_versions = SiliconUI.SiSticker(self)
        self.sticker_versions.setTitle('历史版本')
        self.sticker_versions.setFixedWidth(256)
        self.sticker_versions.setFixedHeight(128)

        self.flowlayout_versions = SiliconUI.SiFlowLayout(self)
        self.flowlayout_versions.setFixedWidth(256 - 48)

        self.sticker_versions.addItem(self.flowlayout_versions)

        self.layout_main.addItem(self.sticker_versions)

        self.addItem(self.layout_main)

        self.loadUpdates()


    def _log_parser(self, path):
        f = open(path)
        content = f.readlines()
        logs = []

        for line in content:
            if line[0:2] == '::':   # 识别到标题行
                logs.append(Log(line[3:].replace('\n', '')))  # 新建一个新日志
                continue

            if line[0:2] == '##':   # 识别到内容标题行
                logs[-1].addColumn(line[3:].replace('\n', ''))
                continue

            logs[-1].addText(line)

        return logs

    def loadUpdates(self):
        logs = self._log_parser('./updatelogs/updates.txt')

        for log in logs:

            new_button = SiliconUI.ClickableLabel(self)
            new_button.setStyleSheet('''
                background-color: {};
                color: {};
                padding: 4px;
                border-radius: 4px;
            '''.format(colorset.BG_GRAD_HEX[3], colorset.TEXT_GRAD_HEX[0]))
            new_button.setFixedHeight(32)
            new_button.setText(log.title)
            self.flowlayout_versions.addItem(new_button)


            version_tab =  SiliconUI.SiTab(self)
            version_tab.left_margin = 0
            version_tab.resize(self.log_width, 600)
            version_tab.setTitle(log.title)
            version_tab.move(400, -32)

            version_stack = SiliconUI.SiStack(self)
            version_stack.setFixedWidth(self.log_width)
            version_stack.delta = 0

            for column in log.columns:
                title, text = column
                if text == '' or text == '\n' :
                    continue  # 跳过没有内容的column
                new_stack = SiliconUI.SiStack(self)
                new_stack.setTitle(title)

                new_label = SiliconUI.SiLabel(self)
                new_label.setFixedWidth(self.log_width)
                new_label.setText(text)
                new_label.setWordWrap(True)

                new_stack.addItem(new_label)
                version_stack.addItem(new_stack)

            version_tab.attachFrame(version_stack)

        self.sticker_versions.adjustSize()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = event.size().height()
        self.layout_main.setFixedHeight(h)
