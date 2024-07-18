from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractButton

from siui.components.widgets.abstracts import ABCButton, ABCPushButton, ABCToggleButton, LongPressThread
from siui.components.widgets.label import SiIconLabel, SiLabel, SiSvgLabel
from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.core.globals import SiGlobal
from siui.gui import GlobalFont, SiFont


class SiPushButton(ABCPushButton):
    """
    点击按钮，可以设置文字、图标或是兼有\n
    被绑定部件是一个 SiIconLabel，需要使用 attachment 方法来访问它
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themed = False  # 是否使用主题颜色

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setAutoAdjustSize(True)
        self.label.setFont(SiFont.fromToken(GlobalFont.S_BOLD))
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 设置偏移量，以保证在按钮明亮面显示
        self.setAttachmentShifting(0, -1)

        # 绑定到主体
        self.setAttachment(self.label)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.label.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_B']}")

        # 设置按钮表面和阴影的颜色
        if self.themed is True:
            # 主题样式
            self.body_top.setStyleSheet("""
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 {}, stop:1 {})
                """.format(SiGlobal.siui.colors["BUTTON_THEMED_BG_A"], SiGlobal.siui.colors["BUTTON_THEMED_BG_B"])
            )
            self.body_bottom.setStyleSheet("""
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 {}, stop:1 {})
                """.format(SiGlobal.siui.colors["BUTTON_THEMED_SHADOW_A"],
                           SiGlobal.siui.colors["BUTTON_THEMED_SHADOW_B"])
            )

        else:
            # 非主题样式
            self.body_top.setStyleSheet(f"background-color: {SiGlobal.siui.colors['BUTTON_NORMAL_BG']}")
            self.body_bottom.setStyleSheet(f"background-color: {SiGlobal.siui.colors['BUTTON_NORMAL_SHADOW']}")

    def setThemed(self, b: bool):
        """
        设置按钮是否成为主题按钮
        :param b: 是否设为主题按钮
        :return:
        """
        self.themed = b


class SiLongPressButton(ABCPushButton):
    """
    需要持续长按一段时间才能触发点击事件的按钮，可以设置文字、图标或是兼有\n
    被绑定部件是一个 SiIconLabel，需要使用 attachment 方法来访问它
    """
    longPressed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHint("长按以确定")

        # 跟踪按钮按下的状态，用于长按动画的处理
        self.pressed_state = False

        # 关闭自身触发点击的动画，以仅在按下超时后子再触发
        self.setEnableClickAnimation(False)

        # 实例化按压线程，并绑定槽函数
        self.hold_thread = LongPressThread(self)
        self.hold_thread.ticked.connect(self._process_changed_handler)
        self.hold_thread.holdTimeout.connect(self._run_clicked_ani)
        self.hold_thread.holdTimeout.connect(self.longPressed.emit)

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setAutoAdjustSize(True)
        self.label.setFont(SiFont.fromToken(GlobalFont.S_BOLD))
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 设置偏移量，以保证在按钮明亮面显示
        self.setAttachmentShifting(0, -1)

        # 绑定到主体
        self.setAttachment(self.label)

    def _process_changed_handler(self, p):
        self.body_top.setStyleSheet("""
            background-color:qlineargradient(x1:{}, y1:0, x2:{}, y2:0,
                                             stop:0 {}, stop:1 {})
        """.format(p-0.01, p, SiGlobal.siui.colors["BUTTON_LONG_PROGRESS"], SiGlobal.siui.colors["BUTTON_LONG_BG"]))

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.label.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_A']}")

        self.body_top.setStyleSheet(f"background-color: {SiGlobal.siui.colors['BUTTON_LONG_BG']}")
        self.body_bottom.setStyleSheet(f"background-color: {SiGlobal.siui.colors['BUTTON_LONG_SHADOW']}")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed_state = True

        # 尝试启动线程
        # 如果线程没在运行，就启动
        if self.hold_thread.isRunning() is False:
            self.hold_thread.start()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.pressed_state = False

    def isPressed(self):
        """
        返回当前按钮是否处于被按下状态，这个方法往往用于内部使用
        :return: 是否被按下
        """
        return self.pressed_state


class SiToggleButton(ABCToggleButton):
    """
    具有两个状态可以切换的按钮，可以设置文字、图标或是兼有\n
    被绑定部件是一个 SiIconLabel，需要使用 attachment 方法来访问它
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setAutoAdjustSize(True)
        self.label.setFont(SiGlobal.siui.fonts["S_BOLD"])
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 绑定到主体
        self.setAttachment(self.label)

        # 设置状态颜色为主题色
        self.setStateColor(Color.transparency(SiGlobal.siui.colors["THEME"], 0.2),
                           SiGlobal.siui.colors["THEME"])

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.label.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_B']}")


class SiSimpleButton(SiToggleButton):
    """
    仅有纯色背景的按钮
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # 禁用选中功能
        self.setCheckable(False)

        # 设置默认颜色为透明
        self.setStateColor("#00FFFFFF", "#00FFFFFF")

    def setColor(self, color_code: str):
        """
        设置按钮的背景颜色
        :param color_code: 色号
        :return:
        """
        self.setStateColor(color_code, color_code)


class SiRadioButton(SiLabel):
    """
    单选组件，提供一个单选按钮和一个文字标签
    """
    toggled = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 一个标签用于表现选中状态
        self.indicator_label = SiLabel(self)
        self.indicator_label.resize(20, 20)
        self.indicator_label.setFixedStyleSheet("border-radius: 10px")  # 注意：这里是固定样式表

        # 创建选项按钮
        self.indicator = ABCButton(self)
        self.indicator.resize(20, 20)
        self.indicator.setFixedStyleSheet("border-radius: 10px")  # 注意：这里是固定样式表
        self.indicator.toggled.connect(self._toggled_handler)
        self.indicator.toggled.connect(self.toggled.emit)

        # 创建选项文字
        self.text_label = SiLabel(self)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.text_label.setFont(SiFont.fromToken(GlobalFont.S_NORMAL))
        self.text_label.setAutoAdjustSize(True)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.text_label.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_A']}")

        # 设置选项按钮样式表，调用自己的事件处理器以刷新
        self._toggled_handler(self.isChecked())

    def text(self):
        """
        返回选项的文本
        :return: 文本
        """
        return self.text_label.text()

    def setText(self, text):
        """
        设置选项的文本
        :param text: 文本
        :return:
        """
        self.text_label.setText(text)
        self.adjustSize()

    def adjustSize(self):
        self.resize(20 + 8 + self.text_label.width(), 32)

    def setChecked(self, state):
        """
        设置选项的选中状态
        :param state: 是否被选中
        :return:
        """
        self.indicator.setChecked(state)
        self.indicator.toggled.emit(state)

    def isChecked(self):
        """
        获取选项是否已经被选中
        :return: 被选中的状态
        """
        return self.indicator.isChecked()

    def _toggled_handler(self, check: bool):
        if check is True:
            # 消除其他所有选项的被选择状态
            self._uncheck_all_in_same_parent()

            # 禁止其切换模式，防止被取消选择
            self.indicator.setCheckable(False)
            self.indicator_label.setStyleSheet(f"border: 4px solid {SiGlobal.siui.colors['THEME']}")
        else:
            # 如果被选中状态为假，就允许其切换模式
            self.indicator.setCheckable(True)
            self.indicator_label.setStyleSheet(f"border: 2px solid {SiGlobal.siui.colors['INTERFACE_BG_A']}")

    def _uncheck_all_in_same_parent(self):
        """
        消除父对象中所有单选框的选择状态，这保证了一个父对象下最多只有一个单选框被选中
        :return:
        """
        # 遍历自己父对象的所有子对象
        for child in self.parentWidget().children():
            if isinstance(child, SiRadioButton) and (child != self):
                child.setChecked(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = event.size().height()

        self.indicator.move(0, (h-20)//2)
        self.indicator_label.move(0, (h - 20) // 2)
        self.text_label.move(28, (h - self.text_label.height()) // 2 - 1)  # 减1是为了让偏下的文字显示正常一点


class SiCheckBox(SiLabel):
    """
    多选组件，提供一个多选按钮和一个文字标签
    """
    toggled = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 一个标签用于表现选中状态
        self.indicator_label = SiLabel(self)
        self.indicator_label.resize(20, 20)
        self.indicator_label.setFixedStyleSheet("border-radius: 4px")  # 注意：这里是固定样式表

        # 一个标签显示打钩的图标
        svg_data = '<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M22.319,4.431,8.5,18.249a1,1,0,0,1-1.417,0L1.739,12.9a1,1,0,0,0-1.417,0h0a1,1,0,0,0,0,1.417l5.346,5.345a3.008,3.008,0,0,0,4.25,0L23.736,5.847a1,1,0,0,0,0-1.416h0A1,1,0,0,0,22.319,4.431Z" fill="#000000" /></svg>'
        self.indicator_icon = SiSvgLabel(self)
        self.indicator_icon.resize(20, 20)
        self.indicator_icon.setSvgSize(12, 12)
        self.indicator_icon.load(svg_data.encode())

        # 创建选项按钮
        self.indicator = ABCButton(self)
        self.indicator.setCheckable(True)
        self.indicator.resize(20, 20)
        self.indicator.setFixedStyleSheet("border-radius: 4px")  # 注意：这里是固定样式表
        self.indicator.toggled.connect(self._toggled_handler)
        self.indicator.toggled.connect(self.toggled.emit)

        # 创建选项文字
        self.text_label = SiLabel(self)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.text_label.setFont(SiFont.fromToken(GlobalFont.S_NORMAL))
        self.text_label.setAutoAdjustSize(True)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.text_label.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_A']}")

        # 设置选项按钮样式表，调用自己的事件处理器以刷新
        self._toggled_handler(self.isChecked())

    def text(self):
        """
        返回选项的文本
        :return: 文本
        """
        return self.text_label.text()

    def setText(self, text):
        """
        设置选项的文本
        :param text: 文本
        :return:
        """
        self.text_label.setText(text)
        self.adjustSize()

    def adjustSize(self):
        self.resize(20 + 8 + self.text_label.width(), 32)

    def setChecked(self, state):
        """
        设置选项的选中状态
        :param state: 是否被选中
        :return:
        """
        self.indicator.setChecked(state)

    def isChecked(self):
        """
        获取选项是否已经被选中
        :return: 被选中的状态
        """
        return self.indicator.isChecked()

    def _toggled_handler(self, check: bool):
        if check is True:
            self.indicator_icon.setVisible(True)
            self.indicator_label.setStyleSheet(f"background-color: {SiGlobal.siui.colors['THEME']}")
        else:
            self.indicator_icon.setVisible(False)
            self.indicator_label.setStyleSheet(f"border: 1px solid {SiGlobal.siui.colors['TEXT_D']}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = event.size().height()

        self.indicator.move(0, (h-20)//2)
        self.indicator_label.move(0, (h - 20) // 2)
        self.indicator_icon.move(0, (h - 20) // 2)
        self.text_label.move(28, (h - self.text_label.height()) // 2 - 1)  # 减1是为了让偏下的文字显示正常一点

    def showEvent(self, a0):
        super().showEvent(a0)
        self._toggled_handler(self.isChecked())

class SiSwitch(QAbstractButton):
    """
    开关
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCheckable(True)

        # 设置自身固定大小
        self.setFixedSize(40, 20)

        # 绑定切换事件
        self.toggled.connect(self._toggle_handler)

        # 开关框架
        self.switch_frame = SiLabel(self)
        self.switch_frame.setGeometry(0, 0, 40, 20)
        self.switch_frame.setFixedStyleSheet("border-radius: 10px")  # 注意这里是固定样式表

        # 开关拉杆
        self.switch_lever = SiLabel(self.switch_frame)
        self.switch_lever.setGeometry(3, 3, 14, 14)
        self.switch_lever.setFixedStyleSheet("border-radius: 7px")  # 注意这里是固定样式表

        # 创建动画
        self.toggle_animation = SiExpAnimation(self)
        self.toggle_animation.setFactor(1/5)
        self.toggle_animation.setBias(1)
        self.toggle_animation.setCurrent(3)
        self.toggle_animation.ticked.connect(self._lever_move_animation_handler)

    def reloadStyleSheet(self):
        """
        重载样式表
        :return:
        """
        self._lever_move_animation_handler(self.switch_lever.x())

    def _lever_move_animation_handler(self, x):
        self.switch_lever.move(int(x), self.switch_lever.y())

        # 检测拉杆的位置，如果过了半程，则改变边框样式
        if (x - 3) / 20 >= 0.5:
            self.switch_frame.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {}, stop:1 {});
                """.format(SiGlobal.siui.colors["THEME_TRANSITION_A"], SiGlobal.siui.colors["THEME_TRANSITION_B"])
                                            )
            self.switch_lever.setStyleSheet("background-color:{}".format(SiGlobal.siui.colors["SWITCH_ACTIVATE"]))

        else:
            self.switch_frame.setStyleSheet("border: 1px solid {}".format(SiGlobal.siui.colors["SWITCH_DEACTIVATE"]))
            self.switch_lever.setStyleSheet("background-color:{}".format(SiGlobal.siui.colors["SWITCH_DEACTIVATE"]))

    def _set_animation_target(self, is_checked):
        if is_checked is True:
            self.toggle_animation.setTarget(23)
        else:
            self.toggle_animation.setTarget(3)

    def paintEvent(self, e):
        pass

    def _toggle_handler(self, is_checked):
        self._set_animation_target(is_checked)
        self.toggle_animation.try_to_start()
