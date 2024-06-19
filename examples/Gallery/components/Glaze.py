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

class GlazeExample(SiliconUI.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        ## ================ Stack 开始 ===================

        self.stack_basics = SiliconUI.SiStack(self)
        self.stack_basics.setTitle('预设组合控件基类')

        self.example_silicon_option_basic = SiliconUI.SiOption(self.stack_basics)
        self.example_silicon_option_basic.setText('基类 Silicon 选项', '所有预设组合控件的基类，梦开始的地方')
        self.example_silicon_option_basic.setIcon(SiGlobal.icons.get('fi-rr-rectangle-panoramic'))

        self.example_silicon_option_basic_unavailable = SiliconUI.SiOption(self.stack_basics)
        self.example_silicon_option_basic_unavailable.setText('禁用', '可将选项设为禁用')
        self.example_silicon_option_basic_unavailable.setIcon(SiGlobal.icons.get('fi-rr-ban'))
        self.example_silicon_option_basic_unavailable.setUsability(False)

        # 添加
        self.stack_basics.addItem(self.example_silicon_option_basic)
        self.stack_basics.addItem(self.example_silicon_option_basic_unavailable)

        ## ================ Stack 开始 ===================

        self.stack_buttons = SiliconUI.SiStack(self)
        self.stack_buttons.setTitle('按钮选项')

        self.example_silicon_option_button = SiliconUI.SiOptionButton(self.stack_buttons)
        self.example_silicon_option_button.setText('具有按钮的 Silicon 选项', '这是一个具有按钮的 Silicon 选项', '确定')
        self.example_silicon_option_button.setIcon(SiGlobal.icons.get('fi-rr-apps'))

        self.example_silicon_option_button_highlighted = SiliconUI.SiOptionButton(self.stack_buttons)
        self.example_silicon_option_button_highlighted.setText('强调选项', '允许将按钮设为高亮，突出重点', '高亮按钮')
        self.example_silicon_option_button_highlighted.setIcon(SiGlobal.icons.get('fi-rr-apps-add'))
        self.example_silicon_option_button_highlighted.setStrong(True)

        self.example_silicon_option_button_hold = SiliconUI.SiOptionButtonHoldtoConfirm(self.stack_buttons)
        self.example_silicon_option_button_hold.setText('长按确定按钮', '避免手滑导致的不必要问题', '确定')
        self.example_silicon_option_button_hold.setIcon(SiGlobal.icons.get('fi-rr-apps-delete'))

        # 添加
        self.stack_buttons.addItem(self.example_silicon_option_button)
        self.stack_buttons.addItem(self.example_silicon_option_button_highlighted)
        self.stack_buttons.addItem(self.example_silicon_option_button_hold)

        ## ================ Stack 开始 ===================

        self.stack_switches = SiliconUI.SiStack(self)
        self.stack_switches.setTitle('开关选项')

        self.example_silicon_option_switch = SiliconUI.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch.setText('具有开关的 Silicon 选项', '单击开关，切换状态',)
        self.example_silicon_option_switch.setIcon(SiGlobal.icons.get('fi-rr-interactive'))

        self.example_silicon_option_switch_sender = SiliconUI.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch_sender.setText('绑定开关事件', '开关发射一个布尔值信号',)
        self.example_silicon_option_switch_sender.setIcon(SiGlobal.icons.get('fi-rr-interactive'))

        self.example_silicon_option_switch_receiver = SiliconUI.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch_receiver.setText('被绑定开关', '',)
        self.example_silicon_option_switch_receiver.setIcon(SiGlobal.icons.get('fi-rr-interactive'))
        self.example_silicon_option_switch_receiver.setUsability(False)

        self.example_silicon_option_switch_sender.switch.stateChanged.connect(self.example_silicon_option_switch_receiver.setUsability)

        # 添加
        self.stack_switches.addItem(self.example_silicon_option_switch)
        self.stack_switches.addItem(self.example_silicon_option_switch_sender)
        self.stack_switches.addItem(self.example_silicon_option_switch_receiver)

        ## ================ Stack 开始 ===================

        self.stack_sliderbars = SiliconUI.SiStack(self)
        self.stack_sliderbars.setTitle('滑条选项')

        self.example_silicon_option_sliderbar = SiliconUI.SiOptionSliderBar(self.stack_sliderbars)
        self.example_silicon_option_sliderbar.setText('一个 Silicon SliderBar 滑条', '滑动以设置值',)
        self.example_silicon_option_sliderbar.setIcon(SiGlobal.icons.get('fi-rr-settings-sliders'))

        self.example_silicon_option_sliderbar_dispersed = SiliconUI.SiOptionSliderBar(self.stack_sliderbars)
        self.example_silicon_option_sliderbar_dispersed.setText('离散取值滑条', '取值不连续，这是含8个档位的示例',)
        self.example_silicon_option_sliderbar_dispersed.setIcon(SiGlobal.icons.get('fi-rr-settings-sliders'))
        self.example_silicon_option_sliderbar_dispersed.sliderbar.slider.setDispersed(range(0,8))

        # 添加
        self.stack_sliderbars.addItem(self.example_silicon_option_sliderbar)
        self.stack_sliderbars.addItem(self.example_silicon_option_sliderbar_dispersed)

        ## ================ Stack 开始 ===================

        self.stack_inputboxes = SiliconUI.SiStack(self)
        self.stack_inputboxes.setTitle('输入框选项')

        self.example_silicon_option_inputbox = SiliconUI.SiOptionInputBox(self.stack_inputboxes)
        self.example_silicon_option_inputbox.setText('输入框', '接收用户输入的文字内容',)
        self.example_silicon_option_inputbox.setIcon(SiGlobal.icons.get('fi-rr-cursor-text'))

        # 添加
        self.stack_inputboxes.addItem(self.example_silicon_option_inputbox)


        ## ================ Stack 开始 ===================

        self.stack_combobox = SiliconUI.SiStack(self)
        self.stack_combobox.setTitle('下拉菜单选项')

        self.example_combobox = SiliconUI.SiOptionComboBox(self.stack_combobox)
        self.example_combobox.setText('下拉菜单', '一个下拉菜单示例，选择你最喜欢的科目')
        self.example_combobox.setIcon(SiGlobal.icons.get('fi-rr-align-left'))
        self.example_combobox.addOption('语文', 1)
        self.example_combobox.addOption('数学', 2)
        self.example_combobox.addOption('英语', 3)
        self.example_combobox.addOption('物理', 4)
        self.example_combobox.addOption('化学', 5)
        self.example_combobox.addOption('生物学', 6)
        self.example_combobox.addOption('历史', 7)
        self.example_combobox.addOption('地理', 8)
        self.example_combobox.addOption('思想政治', 9)
        self.example_combobox.setOption('语文')

        self.stack_combobox.addItem(self.example_combobox)

        ## ================ Stack 开始 ===================

        self.popup_interfaces = SiliconUI.SiStack(self)
        self.popup_interfaces.setTitle('二级界面选项')

        self.example_silicon_popup_interfaces = SiliconUI.SiOptionButton(self.popup_interfaces)
        self.example_silicon_popup_interfaces.setText('二级界面示例·其一', '一个网络通行证设置示例，包括高级设置', '打开')
        self.example_silicon_popup_interfaces.setIcon(SiGlobal.icons.get('fi-rr-layers'))
        self.example_silicon_popup_interfaces.button.clicked.connect(lambda : SiGlobal.overlay.setInterface('example_a'))
        self.example_silicon_popup_interfaces.button.clicked.connect(SiGlobal.overlay.show_animation)

        self.example_silicon_popup_interfaces_b = SiliconUI.SiOptionButton(self.popup_interfaces)
        self.example_silicon_popup_interfaces_b.setText('二级界面示例·其二', '一个文件备份设置示例，包含了多个设置组以及提示信息', '打开')
        self.example_silicon_popup_interfaces_b.setIcon(SiGlobal.icons.get('fi-rr-layers'))
        self.example_silicon_popup_interfaces_b.button.clicked.connect(lambda : SiGlobal.overlay.setInterface('example_b'))
        self.example_silicon_popup_interfaces_b.button.clicked.connect(SiGlobal.overlay.show_animation)

        # 添加
        self.popup_interfaces.addItem(self.example_silicon_popup_interfaces)
        self.popup_interfaces.addItem(self.example_silicon_popup_interfaces_b)








        self.addItem(self.stack_basics)
        self.addItem(self.stack_buttons)
        self.addItem(self.stack_switches)
        self.addItem(self.stack_sliderbars)
        self.addItem(self.stack_inputboxes)
        self.addItem(self.stack_combobox)
        self.addItem(self.popup_interfaces)

        SiGlobal.overlay.addInterface(SubInterface_A(self, 'example_a'))
        SiGlobal.overlay.addInterface(SubInterface_B(self, 'example_b'))
