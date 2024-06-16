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
import silicon.SiGlobal as SiGlobal


class SubInterface_A(silicon.SiOverlay.SubInterface):
    def __init__(self, parent, name):
        super().__init__()
        self.parent = parent
        self.width = 724
        self.body = Body_A(parent)
        self.operation = Operation_A(parent)
        self.name = name

class Operation_A(silicon.SiLayoutH):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setCenter(True)

        self.btn1 = silicon.SiButton(self)
        self.btn1.resize(128, 32)
        self.btn1.setText('取消')
        self.btn1.setStrong(False)

        self.btn2 = silicon.SiButton(self)
        self.btn2.resize(128, 32)
        self.btn2.setText('应用')
        self.btn2.setStrong(True)

        self.btn3 = silicon.SiButton(self)
        self.btn3.resize(128, 32)
        self.btn3.setText('检查可用性')
        self.btn3.setStrong(False)

        self.addItem(self.btn1, 'left')
        self.addItem(self.btn2, 'right')
        self.addItem(self.btn3, 'right')

class Body_A(silicon.SiTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setTitle('设置通行证A')

        self.frame = silicon.SiFrame(self)

        # ========= stack 开始 =========

        self.stack_basics = silicon.SiStack(self.frame)

        self.inputpass = silicon.SiOptionInputBox(self.stack_basics)
        self.inputpass.setText('通行证秘钥', '秘钥形如 XXXXX-XXXXX-XXXXX',)
        self.inputpass.setIcon(SiGlobal.icons.get('fi-rr-fingerprint'))

        self.proxy = silicon.SiOptionInputBox(self.stack_basics)
        self.proxy.setText('代理', '代理服务器 IP，无可留空',)
        self.proxy.setIcon(SiGlobal.icons.get('fi-rr-data-transfer'))

        # 添加
        self.stack_basics.addItem(self.inputpass)
        self.stack_basics.addItem(self.proxy)


        # ========= stack 开始 =========

        self.stack_advances = silicon.SiStack(self.frame)
        self.stack_advances.setTitle('高级')

        self.try_to_update = silicon.SiOptionSwitch(self.stack_advances)
        self.try_to_update.setText('自动更新通行证', '每次创建新连接时尝试向主机请求更新',)
        self.try_to_update.setIcon(SiGlobal.icons.get('fi-rr-network'))

        # 添加
        self.stack_advances.addItem(self.try_to_update)


        # 添加到 frame
        self.frame.addItem(self.stack_basics)
        self.frame.addItem(self.stack_advances)

        # 绑定 frame
        self.attachFrame(self.frame)
