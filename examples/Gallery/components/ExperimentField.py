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
from SiliconUI.SiGlobal import *

from .experifield.music_info_placeholder import MusicInfoPlaceholder

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




        self.addItem(self.discription)
        self.addItem(self.stack_music_info_placeholder)
