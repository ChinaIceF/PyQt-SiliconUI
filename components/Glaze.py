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

from .sub_example_A import *
from .sub_example_B import *

class GlazeExample(silicon.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        ## ================ Stack 开始 ===================

        self.stack_basics = silicon.SiStack(self)
        self.stack_basics.setTitle('预设组合控件基类 Silicon.SiOption')

        self.example_silicon_option_basic = silicon.SiOption(self.stack_basics)
        self.example_silicon_option_basic.setText('基类 Silicon 选项', '所有预设组合控件的基类，梦开始的地方')
        self.example_silicon_option_basic.setIcon(SiGlobal.icons.get('fi-rr-rectangle-panoramic'))

        self.example_silicon_option_basic_unavailable = silicon.SiOption(self.stack_basics)
        self.example_silicon_option_basic_unavailable.setText('禁用', '可将选项设为禁用')
        self.example_silicon_option_basic_unavailable.setIcon(SiGlobal.icons.get('fi-rr-ban'))
        self.example_silicon_option_basic_unavailable.setUsability(False)

        self.stack_basics_link = silicon.SiOptionSourceCode(self.stack_basics)
        self.stack_basics_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.stack_basics.addItem(self.example_silicon_option_basic)
        self.stack_basics.addItem(self.example_silicon_option_basic_unavailable)
        self.stack_basics.addItem(self.stack_basics_link)

        ## ================ Stack 开始 ===================

        self.stack_buttons = silicon.SiStack(self)
        self.stack_buttons.setTitle('具有按钮的选项 Silicon.SiOptionButton')

        self.example_silicon_option_button = silicon.SiOptionButton(self.stack_buttons)
        self.example_silicon_option_button.setText('具有按钮的 Silicon 选项', '这是一个具有按钮的 Silicon 选项', '确定')
        self.example_silicon_option_button.setIcon(SiGlobal.icons.get('fi-rr-apps'))

        self.example_silicon_option_button_highlighted = silicon.SiOptionButton(self.stack_buttons)
        self.example_silicon_option_button_highlighted.setText('强调选项', '允许将按钮设为高亮，突出重点', '高亮按钮')
        self.example_silicon_option_button_highlighted.setIcon(SiGlobal.icons.get('fi-rr-apps-add'))
        self.example_silicon_option_button_highlighted.setStrong(True)
        self.example_silicon_option_button_highlighted.setEmphasize(False)

        self.example_silicon_option_button_hold = silicon.SiOptionButtonHoldtoConfirm(self.stack_buttons)
        self.example_silicon_option_button_hold.setText('长按确定按钮', '避免手滑导致的不必要问题', '确定')
        self.example_silicon_option_button_hold.setIcon(SiGlobal.icons.get('fi-rr-apps-delete'))

        self.stack_buttons_link = silicon.SiOptionSourceCode(self.stack_buttons)
        self.stack_buttons_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.stack_buttons.addItem(self.example_silicon_option_button)
        self.stack_buttons.addItem(self.example_silicon_option_button_highlighted)
        self.stack_buttons.addItem(self.example_silicon_option_button_hold)
        self.stack_buttons.addItem(self.stack_buttons_link)

        ## ================ Stack 开始 ===================

        self.stack_switches = silicon.SiStack(self)
        self.stack_switches.setTitle('具有开关的选项 silicon.SiOptionSwitch')

        self.example_silicon_option_switch = silicon.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch.setText('具有开关的 Silicon 选项', '单击开关，切换状态',)
        self.example_silicon_option_switch.setIcon(SiGlobal.icons.get('fi-rr-interactive'))

        self.example_silicon_option_switch_sender = silicon.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch_sender.setText('绑定开关事件', '开关发射一个布尔值信号',)
        self.example_silicon_option_switch_sender.setIcon(SiGlobal.icons.get('fi-rr-interactive'))

        self.example_silicon_option_switch_receiver = silicon.SiOptionSwitch(self.stack_switches)
        self.example_silicon_option_switch_receiver.setText('被绑定开关', '',)
        self.example_silicon_option_switch_receiver.setIcon(SiGlobal.icons.get('fi-rr-interactive'))
        self.example_silicon_option_switch_receiver.setUsability(False)

        self.example_silicon_option_switch_sender.switch.click_signal.connect(self.example_silicon_option_switch_receiver.setUsability)

        self.stack_switches_link = silicon.SiOptionSourceCode(self.stack_switches)
        self.stack_switches_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.stack_switches.addItem(self.example_silicon_option_switch)
        self.stack_switches.addItem(self.example_silicon_option_switch_sender)
        self.stack_switches.addItem(self.example_silicon_option_switch_receiver)
        self.stack_switches.addItem(self.stack_switches_link)

        ## ================ Stack 开始 ===================

        self.stack_sliderbars = silicon.SiStack(self)
        self.stack_sliderbars.setTitle('具有滑条的选项 silicon.SiOptionSliderBar')

        self.example_silicon_option_sliderbar = silicon.SiOptionSliderBar(self.stack_sliderbars)
        self.example_silicon_option_sliderbar.setText('一个 Silicon SliderBar 滑条', '滑动以设置值',)
        self.example_silicon_option_sliderbar.setIcon(SiGlobal.icons.get('fi-rr-settings-sliders'))

        self.example_sliderbar_text = QLabel(self)
        self.example_sliderbar_text.resize(64, 32)
        self.example_sliderbar_text.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.example_sliderbar_text.setFont(silicon.SiFont.font_L1)
        self.example_sliderbar_text.setStyleSheet('color:#fefefe')

        self.example_silicon_option_sliderbar_with_label = silicon.SiOptionSliderBar(self.stack_sliderbars)
        self.example_silicon_option_sliderbar_with_label.setText('绑定 Silicon SliderBar 的滑条值变化信号', '拖动滑条，观察值变化',)
        self.example_silicon_option_sliderbar_with_label.setIcon(SiGlobal.icons.get('fi-rr-settings-sliders'))
        self.example_silicon_option_sliderbar_with_label.sliderbar.value_change_signal.connect(lambda x: self.example_sliderbar_text.setText(str(round(x, 4))))
        self.example_silicon_option_sliderbar_with_label.addItem(self.example_sliderbar_text)

        self.example_silicon_option_sliderbar_dispersed = silicon.SiOptionSliderBar(self.stack_sliderbars)
        self.example_silicon_option_sliderbar_dispersed.setText('离散取值滑条', '取值不连续，这是含8个档位的示例',)
        self.example_silicon_option_sliderbar_dispersed.setIcon(SiGlobal.icons.get('fi-rr-settings-sliders'))
        self.example_silicon_option_sliderbar_dispersed.sliderbar.slider.setDispersed(range(0,8))

        self.stack_sliderbars_link = silicon.SiOptionSourceCode(self.stack_sliderbars)
        self.stack_sliderbars_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.stack_sliderbars.addItem(self.example_silicon_option_sliderbar)
        self.stack_sliderbars.addItem(self.example_silicon_option_sliderbar_with_label)
        self.stack_sliderbars.addItem(self.example_silicon_option_sliderbar_dispersed)
        self.stack_sliderbars.addItem(self.stack_sliderbars_link)

        ## ================ Stack 开始 ===================

        self.stack_inputboxes = silicon.SiStack(self)
        self.stack_inputboxes.setTitle('具有输入框的选项 silicon.SiOptionInputBox')

        self.example_silicon_option_inputbox = silicon.SiOptionInputBox(self.stack_inputboxes)
        self.example_silicon_option_inputbox.setText('输入框', '接收用户输入的文字内容',)
        self.example_silicon_option_inputbox.setIcon(SiGlobal.icons.get('fi-rr-cursor-text'))


        self.example_silicon_option_inputbox_button = silicon.SiButton(self.stack_inputboxes)
        self.example_silicon_option_inputbox_button.setGeometry(0, 0, 50, 32)
        self.example_silicon_option_inputbox_button.setText('确认')

        self.example_silicon_option_inputbox_with_button = silicon.SiOptionInputBox(self.stack_inputboxes)
        self.example_silicon_option_inputbox_with_button.addItem(self.example_silicon_option_inputbox_button, reverse = True)
        self.example_silicon_option_inputbox_with_button.setText('结合按钮', '也可以简单地附加一个按钮',)
        self.example_silicon_option_inputbox_with_button.setIcon(SiGlobal.icons.get('fi-rr-cursor-text'))

        self.stack_inputboxes_link = silicon.SiOptionSourceCode(self.stack_inputboxes)
        self.stack_inputboxes_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.stack_inputboxes.addItem(self.example_silicon_option_inputbox)
        self.stack_inputboxes.addItem(self.example_silicon_option_inputbox_with_button)
        self.stack_inputboxes.addItem(self.stack_inputboxes_link)


        ## ================ Stack 开始 ===================

        self.stack_combobox = silicon.SiStack(self)
        self.stack_combobox.setTitle('下拉菜单 silicon.SiOptionComboBox')

        self.example_combobox = silicon.SiOptionComboBox(self.stack_combobox)
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

        self.popup_interfaces = silicon.SiStack(self)
        self.popup_interfaces.setTitle('二级界面')

        self.example_silicon_popup_interfaces = silicon.SiOptionButton(self.popup_interfaces)
        self.example_silicon_popup_interfaces.setText('二级界面示例·其一', '一个网络通行证设置示例，包括高级设置', '打开')
        self.example_silicon_popup_interfaces.setIcon(SiGlobal.icons.get('fi-rr-layers'))
        self.example_silicon_popup_interfaces.button.clicked.connect(lambda : SiGlobal.overlay.setInterface('example_a'))
        self.example_silicon_popup_interfaces.button.clicked.connect(SiGlobal.overlay.show_animation)

        self.example_silicon_popup_interfaces_b = silicon.SiOptionButton(self.popup_interfaces)
        self.example_silicon_popup_interfaces_b.setText('二级界面示例·其二', '一个文件备份设置示例，包含了多个设置组以及提示信息', '打开')
        self.example_silicon_popup_interfaces_b.setIcon(SiGlobal.icons.get('fi-rr-layers'))
        self.example_silicon_popup_interfaces_b.button.clicked.connect(lambda : SiGlobal.overlay.setInterface('example_b'))
        self.example_silicon_popup_interfaces_b.button.clicked.connect(SiGlobal.overlay.show_animation)

        self.popup_interfaces_link = silicon.SiOptionSourceCode(self.popup_interfaces)
        self.popup_interfaces_link.setURL('https://github.com/ChinaIceF/PyQt-SiliconUI')

        # 添加
        self.popup_interfaces.addItem(self.example_silicon_popup_interfaces)
        self.popup_interfaces.addItem(self.example_silicon_popup_interfaces_b)
        self.popup_interfaces.addItem(self.popup_interfaces_link)








        self.addItem(self.stack_basics)
        self.addItem(self.stack_buttons)
        self.addItem(self.stack_switches)
        self.addItem(self.stack_sliderbars)
        self.addItem(self.stack_inputboxes)
        self.addItem(self.stack_combobox)
        self.addItem(self.popup_interfaces)

        SiGlobal.overlay.addInterface(SubInterface_A(self, 'example_a'))
        SiGlobal.overlay.addInterface(SubInterface_B(self, 'example_b'))
