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
import random

import SiliconUI
import SiliconUI.SiGlobal as SiGlobal
from SiliconUI.SiFont import *
import siui
from SiliconUI.SiGlobal import *

from .experifield.music_info_placeholder import MusicInfoPlaceholder

from siui.widgets import SiPushButton, SiLongPressButton, SiToggleButton, SiRadioButton, SiCheckBox
from siui.gui import SiFont

class ExperimentField(SiliconUI.SiScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.setStyleSheet('')

        self.discription = SiliconUI.SiOption(self)
        self.discription.setIcon(SiGlobal.icons.get('fi-rr-bulb'))
        self.discription.setText('实验场', '欢迎来到 Silicon 试验场。这里有一些由控件组合出来的小组件，展现 Silicon UI 蕴含的创造力与设计艺术')

        ## ================ Stack 开始 ===================

        self.stack_music_info_placeholder = SiliconUI.SiCategory(self)
        self.stack_music_info_placeholder.setTitle('音乐信息展示板')

        self.layout_music_info_placeholder = SiliconUI.SiLayoutH(self)

        # 其一
        self.music_info_placeholder = MusicInfoPlaceholder(self)
        self.music_info_placeholder.load('./img/cover.jpeg')
        self.music_info_placeholder.setText(
            title = '只因你太美',
            artist = '我家鸽鸽',
            album = '你干嘛嗨嗨呦',
        )
        self.music_info_placeholder.resize(380, 132)
        self.music_info_placeholder.setProgress(0.7)

        # 其二
        self.music_info_placeholder_2 = MusicInfoPlaceholder(self)
        self.music_info_placeholder_2.load('./img/cover2.jpg')
        self.music_info_placeholder_2.setText(
            title = 'Axolotl',
            artist = 'C418',
            album = 'Axolotl',
        )
        self.music_info_placeholder_2.resize(380, 132)
        self.music_info_placeholder_2.setProgress(0)

        self.layout_music_info_placeholder.addItem(self.music_info_placeholder)
        self.layout_music_info_placeholder.addItem(self.music_info_placeholder_2)

        self.stack_music_info_placeholder.addItem(self.layout_music_info_placeholder)


        ## ================ Stack 开始 ===================

        self.stack_reconstruct_test = SiliconUI.SiCategory(self)
        self.stack_reconstruct_test.setTitle('重构测试')

        self.reconstruct_discription = SiliconUI.SiOption(self)
        self.reconstruct_discription.setIcon(SiGlobal.icons.get('fi-rr-bulb'))
        self.reconstruct_discription.setText('这里是重构测试', '此处进行项目重构的各种测试')

        self.button_layout = SiliconUI.SiLayoutH(self)
        self.button_layout.setFixedHeight(32)

        self.test_new_button = SiPushButton(self)
        self.test_new_button.setFixedSize(128, 32)
        self.test_new_button.attachment().setText("重构按钮")

        self.test_new_button2 = SiLongPressButton(self)
        self.test_new_button2.setFixedSize(128, 32)
        self.test_new_button2.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.test_new_button2.attachment().setText("新增图标")
        self.test_new_button2.clicked.connect(lambda: print("点击事件触发"))
        self.test_new_button2.longPressed.connect(lambda: print("长按事件触发"))

        self.test_new_button3 = SiPushButton(self)
        self.test_new_button3.setFixedSize(48, 32)
        self.test_new_button3.attachment().load(SiGlobal.icons.get('fi-rr-disk'))

        self.test_new_button4 = SiToggleButton(self)
        self.test_new_button4.attachment().load(SiGlobal.icons.get('fi-rr-disk'))
        self.test_new_button4.attachment().setText("自动保存模式")
        self.test_new_button4.adjustSize()

        self.test_new_button5 = SiRadioButton(self)
        self.test_new_button5.setText("赤石")

        self.test_new_button6 = SiRadioButton(self)
        self.test_new_button6.setText("豪赤啊")

        self.test_new_button7 = SiRadioButton(self)
        self.test_new_button7.setText("吃饱了")

        self.button_layout.addItem(self.test_new_button)
        self.button_layout.addItem(self.test_new_button2)
        self.button_layout.addItem(self.test_new_button3)
        self.button_layout.addItem(self.test_new_button4)
        self.button_layout.addItem(self.test_new_button5)
        self.button_layout.addItem(self.test_new_button6)
        self.button_layout.addItem(self.test_new_button7)


        self.button_layout2 = SiliconUI.SiLayoutH(self)
        self.button_layout2.setFixedHeight(32)

        self.test_new_button8 = SiCheckBox(self)
        self.test_new_button8.setText("鸡你太美")

        self.test_new_button9 = SiCheckBox(self)
        self.test_new_button9.setText("你干嘛嗨嗨呦")

        self.button_layout2.addItem(self.test_new_button8)
        self.button_layout2.addItem(self.test_new_button9)

        self.stack_reconstruct_test.addItem(self.reconstruct_discription)
        self.stack_reconstruct_test.addItem(self.button_layout)
        self.stack_reconstruct_test.addItem(self.button_layout2)
        #self.stack_reconstruct_test.addItem(self.test_label)

        self.addItem(self.discription)
        self.addItem(self.stack_music_info_placeholder)
        self.addItem(self.stack_reconstruct_test)
