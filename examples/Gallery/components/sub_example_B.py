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


class SubInterface_B(SiliconUI.SiOverlay.SubInterface):
    def __init__(self, parent, name):
        super().__init__()
        self.parent = parent
        self.width_ = 740
        self.body = Body_B(parent)
        self.operation = Operation_B(parent)
        self.name = name

class Operation_B(SiliconUI.SiLayoutH):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setAlignCenter(True)

        self.btn1 = SiliconUI.SiButton(self)
        self.btn1.resize(128, 32)
        self.btn1.setText('取消')
        self.btn1.setStrong(False)

        self.btn2 = SiliconUI.SiButton(self)
        self.btn2.resize(128, 32)
        self.btn2.setText('应用')
        self.btn2.setStrong(True)

        self.btn3 = SiliconUI.SiButton(self)
        self.btn3.resize(128, 32)
        self.btn3.setText('管理备份文件夹')
        self.btn3.setStrong(False)

        self.addItem(self.btn1, 'left')
        self.addItem(self.btn2, 'right')
        self.addItem(self.btn3, 'right')

class Body_B(SiliconUI.SiTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setTitle('管理文件备份')

        self.frame = SiliconUI.SiFrame(self)

        # ========= stack 开始 =========

        self.stack_dir = SiliconUI.SiStack(self.frame)
        self.stack_dir.setTitle('目录设置')

        self.aim = SiliconUI.SiOptionInputBox(self.stack_dir)
        self.aim.setText('备份目标', '需要备份的目录或文件夹',)
        self.aim.setIcon(SiGlobal.icons.get('fi-rr-cloud-upload'))

        self.store = SiliconUI.SiOptionInputBox(self.stack_dir)
        self.store.setText('备份储存位置', '备份的文件储存的目录，留空将设置为工作目录',)
        self.store.setIcon(SiGlobal.icons.get('fi-rr-cloud-download'))

        # 添加
        self.stack_dir.addItem(self.aim)
        self.stack_dir.addItem(self.store)


        # ========= stack 开始 =========

        self.stack_settings = SiliconUI.SiStack(self.frame)
        self.stack_settings.setTitle('备份设置')

        self.frequency = SiliconUI.SiOptionInputBox(self.stack_settings)
        self.frequency.setText('设置备份频率', '每天备份的次数',)
        self.frequency.setIcon(SiGlobal.icons.get('fi-rr-time-fast'))

        self.independency = SiliconUI.SiOptionSwitch(self.stack_settings)
        self.independency.setText('按备份时间创建目录', '每次备份储存在独立文件夹，这可能导致较大的储存占用',)
        self.independency.setIcon(SiGlobal.icons.get('fi-rr-folder'))

        self.mode = SiliconUI.SiOptionComboBox(self.stack_settings)
        self.mode.setText('储存模式', '选择创建备份时的行为',)
        self.mode.setIcon(SiGlobal.icons.get('fi-rr-folder'))
        self.mode.addOption('源文件', 0)
        self.mode.addOption('创建压缩文件', 1)
        self.mode.setOption('源文件')

        self.info_layout_v = SiliconUI.SiLayoutV(self.stack_settings)
        self.info_layout_v.setAlignCenter(True)

        self.info_layout_h = SiliconUI.SiLayoutH(self.info_layout_v)
        self.info_layout_h.setAlignCenter(False)

        self.info = SiliconUI.SiInfo(self.info_layout_h)
        self.info.setFixedWidth(320)
        self.info.setType(0)
        self.info.setContent('提示', '· 备份目录将会被以 日期-次数-时间 的格式命名，并分立存放在储存目录下。\n· 当目标名称已存在时，会尝试在上述名称后加编号。')

        self.warning = SiliconUI.SiInfo(self.info_layout_h)
        self.warning.setFixedWidth(160)
        self.warning.setType(2)
        self.warning.setContent('注意', '· 请务必确认程序具有读写权限以访问和操作备份文件，否则备份可能无效')

        self.info_layout_h.addItem(self.info)
        self.info_layout_h.addItem(self.warning)
        self.info_layout_h.adjustSize()

        self.info_layout_v.addItem(self.info_layout_h)
        self.info_layout_v.adjustSize()

        # 添加
        self.stack_settings.addItem(self.frequency)
        self.stack_settings.addItem(self.independency)
        self.stack_settings.addItem(self.mode)
        self.stack_settings.addItem(self.info_layout_v, 16)


        # 添加到 frame
        self.frame.addItem(self.stack_dir)
        self.frame.addItem(self.stack_settings)

        # 绑定 frame
        self.attachFrame(self.frame)
