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
from silicon import *

# 简单加俩按钮
class WidgetSticker(silicon.SiSticker.SiSticker):
    def __init__(self, parent):
        super().__init__(parent)

        self.button_github = SiButtonFlat(self)
        self.button_github.resize(32, 32)
        self.button_github.load(SiGlobal.icons.get('fi-rr-link'))
        self.button_github.setHint('查看源代码')

        self.button_example = SiButtonFlat(self)
        self.button_example.resize(32, 32)
        self.button_example.load(SiGlobal.icons.get('fi-rr-bug'))
        self.button_example.setHint('报告问题')

        self.head.addItem(self.button_github, side = 'right')
        self.head.addItem(self.button_example, side = 'right')


class WidgetsExample(silicon.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        w = 660

        ## ================ Stack 开始 ===================

        self.stack_labels = silicon.SiStack(self)
        self.stack_labels.setTitle('标签')

        self.sticker_label = WidgetSticker(self.stack_labels)
        self.sticker_label.setTitle('文字标签')
        self.sticker_label.setFixedWidth(w)

        self.label_with_no_hint = silicon.SiLabel(self)
        self.label_with_no_hint.setText('测试标签')

        self.label_with_hint = silicon.SiLabel(self)
        self.label_with_hint.setText('测试标签（具有提示信息）')
        self.label_with_hint.setHint('你好，我是提示信息')

        # 添加到 Sticker
        self.sticker_label.addItem(self.label_with_no_hint)
        self.sticker_label.addItem(self.label_with_hint)


        self.sticker_pixlabel_with_hint = WidgetSticker(self.stack_labels)
        self.sticker_pixlabel_with_hint.setTitle('图片标签')
        self.sticker_pixlabel_with_hint.setFixedWidth(w)

        self.layout_pixlabel = SiLayoutH(self)

        self.pixlabel_with_hint = silicon.SiPixLabel(self)
        self.pixlabel_with_hint.resize(80, 80)
        self.pixlabel_with_hint.setRadius(40)
        self.pixlabel_with_hint.load('./img/headpic.png')
        self.pixlabel_with_hint.setHint('关注霏泠谢谢喵')

        self.pixlabel_with_hint_roundrect = silicon.SiPixLabel(self)
        self.pixlabel_with_hint_roundrect.resize(80, 80)
        self.pixlabel_with_hint_roundrect.setRadius(32)
        self.pixlabel_with_hint_roundrect.load('./img/headpic.png')
        self.pixlabel_with_hint_roundrect.setHint('尺寸 80*80，圆角半径 20')

        self.layout_pixlabel.addItem(self.pixlabel_with_hint)
        self.layout_pixlabel.addItem(self.pixlabel_with_hint_roundrect)
        self.layout_pixlabel.setFixedHeight(80)

        # 添加到 Sticker
        self.sticker_pixlabel_with_hint.addItem(self.layout_pixlabel)

        # 添加
        self.stack_labels.addItem(self.sticker_label)
        self.stack_labels.addItem(self.sticker_pixlabel_with_hint)



        ## ================ Stack 开始 ===================

        self.stack_buttons = silicon.SiStack(self)
        self.stack_buttons.setTitle('按钮')

        self.sticker_button_normal = WidgetSticker(self.stack_labels)
        self.sticker_button_normal.setTitle('标准按钮')
        self.sticker_button_normal.setFixedWidth(w)

        self.layout_button_normal = SiLayoutH(self)

        self.button_normal_A = SiButton(self)
        self.button_normal_A.setStrong(False)
        self.button_normal_A.setText('普通按钮')
        self.button_normal_A.resize(128, 32)

        self.button_normal_B = SiButton(self)
        self.button_normal_B.setStrong(True)
        self.button_normal_B.setText('高亮按钮')
        self.button_normal_B.resize(128, 32)

        self.button_normal_C = SiButtonHoldtoConfirm(self)
        self.button_normal_C.setText('长按按钮')
        self.button_normal_C.resize(128, 32)

        self.layout_button_normal.addItem(self.button_normal_A, 'left')
        self.layout_button_normal.addItem(self.button_normal_B, 'left')
        self.layout_button_normal.addItem(self.button_normal_C, 'left')
        self.layout_button_normal.setFixedHeight(32)

        # 添加到 sticker
        self.sticker_button_normal.addItem(self.layout_button_normal)


        self.sticker_button_icon = WidgetSticker(self.stack_labels)
        self.sticker_button_icon.setTitle('图标按钮')
        self.sticker_button_icon.setFixedWidth(w)

        self.button_icon = SiButtonFlat(self)
        self.button_icon.setHint('我是按钮示例')
        self.button_icon.load(SiGlobal.icons.get('fi-rr-disk'))
        self.button_icon.resize(32, 32)

        # 添加到 sticker
        self.sticker_button_icon.addItem(self.button_icon)



        self.sticker_button_label = WidgetSticker(self.stack_labels)
        self.sticker_button_label.setTitle('标签按钮')
        self.sticker_button_label.setFixedWidth(w)

        self.button_label = ClickableLabel(self)
        self.button_label.setStyleSheet('color: #ffffff; padding: 8px')
        self.button_label.setFont(font_L1_bold)
        self.button_label.setFixedHeight(32)
        self.button_label.setText('标签按钮测试')
        self.button_label.adjustSize()

        self.button_label_flow = ClickableLabel(self)   # TODO: 这部分以后整合到预设
        self.button_label_flow.radius = 14
        self.button_label_flow.setStyleSheet('''
            background-color: #20ffffff;
            color: #ffffff;
            padding: 4px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 14px;
            ''')
        self.button_label_flow.setFont(font_L1_bold)
        self.button_label_flow.setFixedHeight(28)
        self.button_label_flow.setText('流式标签')
        self.button_label_flow.adjustSize()

        # 添加到 sticker
        self.sticker_button_label.addItem(self.button_label)
        self.sticker_button_label.addItem(self.button_label_flow)



        self.sticker_button_icon_label = WidgetSticker(self.stack_labels)
        self.sticker_button_icon_label.setTitle('图标标签按钮')
        self.sticker_button_icon_label.setFixedWidth(w)

        self.button_icon_label = SiButtonFlatWithLabel(self)
        self.button_icon_label.setFixedHeight(32)
        self.button_icon_label.setText('鸡你太美')
        self.button_icon_label.label.setFont(font_L1_bold)
        self.button_icon_label.load(SiGlobal.icons.get('fi-rr-basketball'))

        # 添加到 sticker
        self.sticker_button_icon_label.addItem(self.button_icon_label)

        # 添加
        self.stack_buttons.addItem(self.sticker_button_normal)
        self.stack_buttons.addItem(self.sticker_button_icon)
        self.stack_buttons.addItem(self.sticker_button_label)
        self.stack_buttons.addItem(self.sticker_button_icon_label)


        ## ================ Stack 开始 ===================

        self.stack_menus = silicon.SiStack(self)
        self.stack_menus.setTitle('菜单')

        self.sticker_combobox = WidgetSticker(self.stack_menus)
        self.sticker_combobox.setTitle('下拉菜单')
        self.sticker_combobox.setFixedWidth(w)

        self.combobox = SiComboBox(self)
        self.combobox.resize(128, 32)
        self.combobox.addOption('唱', 1)
        self.combobox.addOption('跳', 2)
        self.combobox.addOption('Rap', 3)
        self.combobox.addOption('篮球', 4)
        self.combobox.setOption('篮球')

        # 添加到 Sticker
        self.sticker_combobox.addItem(self.combobox)

        # 添加到 Stack
        self.stack_menus.addItem(self.sticker_combobox)


        ## ================ Stack 开始 ===================

        self.stack_switchs = silicon.SiStack(self)
        self.stack_switchs.setTitle('开关')

        self.sticker_switch = WidgetSticker(self.stack_switchs)
        self.sticker_switch.setTitle('开关')
        self.sticker_switch.setFixedWidth(w)

        self.switch = SiSwitch(self)
        self.switch.resize(150, 32)

        # 添加到 Sticker
        self.sticker_switch.addItem(self.switch)

        # 添加到 Stack
        self.stack_switchs.addItem(self.sticker_switch)


        ## ================ Stack 开始 ===================

        self.stack_sliderbar = silicon.SiStack(self)
        self.stack_sliderbar.setTitle('滑动条')

        self.sticker_sliderbar_free = WidgetSticker(self.stack_sliderbar)
        self.sticker_sliderbar_free.setTitle('连续滑动条')
        self.sticker_sliderbar_free.setFixedWidth(w)

        self.sliderbar_free = SiSliderBar(self)
        self.sliderbar_free.resize(500, 32)

        # 添加到 Sticker
        self.sticker_sliderbar_free.addItem(self.sliderbar_free)


        self.sticker_sliderbar_levelized = WidgetSticker(self.stack_sliderbar)
        self.sticker_sliderbar_levelized.setTitle('分档滑动条')
        self.sticker_sliderbar_levelized.setFixedWidth(w)

        self.sliderbar_levelized = SiSliderBar(self)
        self.sliderbar_levelized.resize(500, 32)
        self.sliderbar_levelized.setDispersed(range(0, 7))

        # 添加到 Sticker
        self.sticker_sliderbar_levelized.addItem(self.sliderbar_levelized)

        # 添加到 Stack
        self.stack_sliderbar.addItem(self.sticker_sliderbar_free)
        self.stack_sliderbar.addItem(self.sticker_sliderbar_levelized)


        ## ================ Stack 开始 ===================

        self.stack_inputboxes = silicon.SiStack(self)
        self.stack_inputboxes.setTitle('输入框')

        self.sticker_inputboxes = WidgetSticker(self.stack_inputboxes)
        self.sticker_inputboxes.setTitle('输入框')
        self.sticker_inputboxes.setFixedWidth(w)

        self.inputbox = SiInputBox(self)
        self.inputbox.resize(300, 32)

        # 添加到 Sticker
        self.sticker_inputboxes.addItem(self.inputbox)

        # 添加到 Stack
        self.stack_inputboxes.addItem(self.sticker_inputboxes)


        self.addItem(self.stack_labels)
        self.addItem(self.stack_buttons)
        self.addItem(self.stack_menus)
        self.addItem(self.stack_switchs)
        self.addItem(self.stack_sliderbar)
        self.addItem(self.stack_inputboxes)
