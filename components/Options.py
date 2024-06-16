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

from silicon.SiSticker import SiSticker
from silicon.SiFont import *
from silicon.SiButton import SiButtonLabel


class NameTag(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 所有内容的 LayoutH
        self.layout_all_content = silicon.SiLayoutH(self)
        self.layout_all_content.move(24, 24)

        self.selfie = silicon.SiPixLabel(self)
        self.selfie.setRadius(32)
        self.selfie.resize(80, 80)

        # 文字信息得到 LayoutV
        self.layout_labels = silicon.SiLayoutV(self.layout_all_content)
        self.layout_labels.setInterval(1)

        self.name = silicon.SiLabel(self.layout_labels)
        self.name.setFont(font_L2)
        self.name.setStyleSheet('color: #ffffff; padding-left: 2px; padding-bottom: 6px')
        self.layout_labels.addItem(self.name)

        self.layout_all_content.addItem(self.selfie, 'left')
        self.layout_all_content.addItem(self.layout_labels, 'left')

        self.adjustSize()

    def load(self, path):
        self.selfie.load(path)

    def setName(self, name):
        self.name.setText(name)
        self.name.adjustSize()
        self.layout_labels.adjustSize()
        self.adjustSize()

    def addItem(self, text, url, hint = ''):
        newItem = SiButtonLabel(self)
        newItem.setStyleSheet('''
            color: #d986e8;
            padding-left: 4px;
            padding-right: 4px;
            padding-top: 1px;
            padding-bottom: 1px;
            ''')
        newItem.setText(text)
        newItem.clicked.connect(lambda : os.system('start {}'.format(url)))
        newItem.setHint(hint)
        self.layout_labels.addItem(newItem, 'top')
        self.layout_labels.adjustSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.layout_all_content.resize(w - 48, h - 48)
        self.layout_labels.resize(self.layout_labels.width(), h - 48)


class Options(silicon.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        ## ================ Stack 开始 ===================

        self.stack_developers = silicon.SiStack(self)
        self.stack_developers.setTitle('开发者')

        self.layout_developers = silicon.SiLayoutH(self.stack_developers)
        self.layout_developers.setFixedHeight(132)

        self.nametag = NameTag(self.stack_developers)
        self.nametag.setFixedWidth(380)
        self.nametag.setFixedHeight(132)
        self.nametag.load('./img/headpic.png')
        self.nametag.setName('霏泠Ice')
        self.nametag.addItem('访问 GitHub 主页', 'https://github.com/chinaicef', 'https://github.com/chinaicef')
        self.nametag.addItem('访问 哔哩哔哩 主页', 'https://space.bilibili.com/390832893', 'https://space.bilibili.com/390832893')

        self.nametag_1 = NameTag(self.stack_developers)
        self.nametag_1.setFixedWidth(380)
        self.nametag_1.setFixedHeight(132)
        self.nametag_1.load('./img/headpic2.jpg')
        self.nametag_1.setName('你干嘛~嗨嗨呦↓')
        self.nametag_1.addItem('访问 GitHub 主页', 'www.github.com', 'www.github.com')
        self.nametag_1.addItem('访问 哔哩哔哩 主页', 'www.bilibili.com', 'www.bilibili.com')

        self.layout_developers.addItem(self.nametag)
        self.layout_developers.addItem(self.nametag_1)

        self.stack_developers.addItem(self.layout_developers)

        ## ================ Stack 开始 ===================

        self.stack_about = silicon.SiStack(self)
        self.stack_about.setTitle('关于')

        self.about = silicon.SiOption(self.stack_about)
        self.about.setIcon(SiGlobal.icons.get('fi-rr-info'))
        self.about.setText('关于 Silicon UI',
                           '''<strong>版本号</strong> 1.01 &nbsp;&nbsp;&nbsp;<strong>构建日期</strong>2024.05.26''')

        self.license = silicon.SiOption(self.stack_about)
        self.license.setText('开源许可','本项目遵循 GNU General Public License v3.0')
        self.license.setIcon(SiGlobal.icons.get('fi-rr-diploma'))

        self.copyright = silicon.SiOption(self.stack_about)
        self.copyright.setText('版权','<strong>霏泠冰 IceF</strong> 版权所有')
        self.copyright.setIcon(SiGlobal.icons.get('fi-rr-copyright'))

        # 添加
        self.stack_about.addItem(self.about)
        self.stack_about.addItem(self.license)
        self.stack_about.addItem(self.copyright)


        ## ================ Stack 开始 ===================

        self.stack_quotes = silicon.SiStack(self)
        self.stack_quotes.setTitle('第三方资源')

        self.icons = silicon.SiOptionSourceCode(self.stack_about)
        self.icons._setMinimumHeight(80)
        self.icons.setText('图标','Silicon Gallery 使用了 FLATICON 的图标，<strong>这些图标不应被认为是 Silicon UI 的一部分</strong>')
        self.icons.setIcon(SiGlobal.icons.get('fi-rr-quote-right'))
        self.icons.load(SiGlobal.icons.get('fi-rr-link'))
        self.icons.setURL('www.flaticon.com')

        self.stack_quotes.addItem(self.icons)



        self.addItem(self.stack_developers)
        self.addItem(self.stack_about)
        self.addItem(self.stack_quotes)
