from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractButton

from siui.components.widgets.abstracts import ABCButton, ABCPushButton, ABCToggleButton, LongPressThread
from siui.components.widgets.label import SiIconLabel, SiLabel, SiSvgLabel
from siui.core import GlobalFont, Si, SiColor, SiExpAnimation, SiGlobal
from siui.gui import SiFont
from siui.gui.color_group import SiColorGroup


class SiPushButton(ABCPushButton):
    """
    点击按钮，可以设置文字、图标或是兼有\n
    被绑定部件是一个 SiIconLabel，需要使用 attachment 方法来访问它
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.use_transition = False     # 是否使用过渡色

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
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
        if self.use_transition is True:
            # 使用过渡色
            self.body_top.setStyleSheet(
                f"""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.getColor(SiColor.BUTTON_THEMED_BG_A)},
                    stop:1 {self.getColor(SiColor.BUTTON_THEMED_BG_B)})
                """
            )
            self.body_bottom.setStyleSheet(
                f"""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.getColor(SiColor.BUTTON_THEMED_SHADOW_A)},
                    stop:1 {self.getColor(SiColor.BUTTON_THEMED_SHADOW_B)})
                """
            )

        else:
            # 纯色
            self.body_top.setStyleSheet(f"background-color: {self.getColor(SiColor.BUTTON_PANEL)}")
            self.body_bottom.setStyleSheet(f"background-color: {self.getColor(SiColor.BUTTON_SHADOW)}")

    def setUseTransition(self, b: bool):
        """
        设置按钮是否成为主题按钮
        :param b: 是否设为主题按钮
        :return:
        """
        self.use_transition = b


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
        self.setFlashOnClicked(False)

        # 实例化按压线程，并绑定槽函数
        self.hold_thread = LongPressThread(self)
        self.hold_thread.ticked.connect(self._process_changed_handler)
        self.hold_thread.holdTimeout.connect(self._run_clicked_ani)
        self.hold_thread.holdTimeout.connect(self.longPressed.emit)
        # self.destroyed.connect(self.hold_thread.stopRunning, Qt.AutoConnection)
        self.destroyed.connect(self.hold_thread.terminate, Qt.AutoConnection)

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 设置偏移量，以保证在按钮明亮面显示
        self.setAttachmentShifting(0, -1)

        # 绑定到主体
        self.setAttachment(self.label)

    def _process_changed_handler(self, p):
        self.body_top.setStyleSheet(
            f"""
            background-color: qlineargradient(x1:{p-0.001}, y1:0, x2:{p}, y2:0,
                 stop:0 {self.getColor(SiColor.BUTTON_LONG_PRESS_PROGRESS)},
                 stop:1 {self.getColor(SiColor.BUTTON_LONG_PRESS_PANEL)})
            """
        )

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")

        self.body_top.setStyleSheet(f"background-color: {self.getColor(SiColor.BUTTON_LONG_PRESS_PANEL)}")
        self.body_bottom.setStyleSheet(f"background-color: {self.getColor(SiColor.BUTTON_LONG_PRESS_SHADOW)}")  # noqa: E501

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
        self.label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 绑定到主体
        self.setAttachment(self.label)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")


class SiSimpleButton(SiToggleButton):
    """
    仅有纯色背景的按钮
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        # 禁用选中功能
        self.setCheckable(False)

        # 设置默认颜色为透明
        self.colorGroup().assign(SiColor.BUTTON_ON, "#00FFFFFF")
        self.colorGroup().assign(SiColor.BUTTON_OFF, "#00FFFFFF")

    def setIdleColor(self, color_code):
        self.colorGroup().assign(SiColor.BUTTON_ON, color_code)
        self.colorGroup().assign(SiColor.BUTTON_OFF, color_code)


class SiRadioButton(SiLabel):
    """
    单选组件，提供一个单选按钮和一个文字标签，会自动设置默认大小
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
        self.text_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.text_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")

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
        self.resize(20 + 8 + self.text_label.width(), 24)

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
            self.indicator_label.setStyleSheet(f"border: 4px solid {self.getColor(SiColor.RADIO_BUTTON_CHECKED)}")  # noqa: E501
        else:
            # 如果被选中状态为假，就允许其切换模式
            self.indicator.setCheckable(True)
            self.indicator_label.setStyleSheet(f"border: 3px solid {self.getColor(SiColor.RADIO_BUTTON_UNCHECKED)}")  # noqa: E501

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
        svg_data = ('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" '
                    'xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" viewBox="0 '
                    '0 507.506 507.506" style="enable-background:new 0 0 507.506 507.506;" xml:space="preserve" '
                    'width="512" height="512"><g><path d="M163.865,436.934c-14.406,'
                    '0.006-28.222-5.72-38.4-15.915L9.369,304.966c-12.492-12.496-12.492-32.752,0-45.248l0,'
                    '0   c12.496-12.492,32.752-12.492,45.248,0l109.248,109.248L452.889,79.942c12.496-12.492,'
                    '32.752-12.492,45.248,0l0,0   c12.492,12.496,12.492,32.752,0,45.248L202.265,421.019C192.087,'
                    '431.214,178.271,436.94,163.865,436.934z" '
                    f'fill="{self.getColor(SiColor.CHECKBOX_SVG)}" /></g></svg>')
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
        self.text_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置文字颜色
        self.text_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)}")

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
        self.resize(20 + 8 + self.text_label.width(), 24)

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
            self.indicator_label.setStyleSheet(f"background-color: {self.getColor(SiColor.CHECKBOX_CHECKED)}")  # noqa: E501
        else:
            self.indicator_icon.setVisible(False)
            self.indicator_label.setStyleSheet(f"border: 1px solid {self.getColor(SiColor.CHECKBOX_UNCHECKED)}")  # noqa: E501

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

        # 自定义状态属性，初始值为 False
        self._checked = False

        # 颜色组
        self.color_group = SiColorGroup(reference=SiGlobal.siui.colors)

        # 设置自身固定大小
        self.setFixedSize(40, 20)

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

        # 记录拉杆与鼠标偏移量
        self._initial_pos: QPoint = QPoint(0, 0)
        self._drag_offset = 0

    def reloadStyleSheet(self):
        """
        重载样式表
        :return:
        """
        self._lever_move_animation_handler(self.switch_lever.x())

    def getColor(self, token):
        return self.color_group.fromToken(token)

    def colorGroup(self):
        """
        Get the color group of this widget
        :return: SiColorGroup
        """
        return self.color_group

    def _lever_move_animation_handler(self, x):
        self.switch_lever.move(int(x), self.switch_lever.y())

        # 检测拉杆的位置，如果过了半程，则改变边框样式
        if self._process_lever_position():
            self.switch_frame.setStyleSheet(
                f"""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.getColor(SiColor.THEME_TRANSITION_A)},
                stop:1 {self.getColor(SiColor.THEME_TRANSITION_B)});
                """
            )
            self.switch_lever.setStyleSheet(f"background-color:{self.getColor(SiColor.SWITCH_ACTIVATE)}")

        else:
            self.switch_frame.setStyleSheet(f"border: 1px solid {self.getColor(SiColor.SWITCH_DEACTIVATE)}")  # noqa: E501
            self.switch_lever.setStyleSheet(f"background-color:{self.getColor(SiColor.SWITCH_DEACTIVATE)}")  # noqa: E501

    def _set_animation_target(self, is_checked):
        self.toggle_animation.setCurrent(self.switch_lever.x())
        self.toggle_animation.setTarget(23 if is_checked else 3)

    def _process_lever_position(self) -> bool:
        """
        根据滑杆位置决定开关的选中状态。
        """
        lever_position = self.switch_lever.x()
        return (lever_position - 3) / 20 >= 0.5

    def paintEvent(self, e):
        pass

    def isChecked(self):
        return self._checked  # 返回自定义状态

    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.toggled.emit(self._checked)  # 发射信号
            self._toggle_handler(self._checked)  # 更新动画

    def mousePressEvent(self, event):
        """
        处理鼠标按下事件，记录鼠标点击位置与滑杆的相对位置。
        """
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.pos().x() - self.switch_lever.x()  # 记录偏移量
            self._initial_pos = event.pos()  # 记录初始点击位置
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        处理滑条的鼠标移动事件，拖动时移动滑杆。
        """
        if event.buttons() & Qt.LeftButton:  # 检查鼠标左键是否按下
            # 获取鼠标在 slider 上的位置，并使用之前记录的偏移量来移动滑杆
            mouse_pos = event.pos()
            target_pos = mouse_pos.x() - self._drag_offset  # 保持相对位置
            self._lever_move_animation_handler(min(max(target_pos, 3), 23))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        处理鼠标松开事件，区分点击和拖动操作。
        """
        if event.button() == Qt.LeftButton:
            release_pos = event.pos()
            drag_distance = abs(release_pos.x() - self._initial_pos.x())

            if drag_distance < 3:  # 点击操作
                self._checked = not self._checked  # 切换状态
                self.toggled.emit(self._checked)  # 手动发射toggled信号
            else:  # 拖动操作
                new_checked_state = self._process_lever_position()
                if self._checked != new_checked_state:
                    self._checked = new_checked_state
                    self.toggled.emit(self._checked)  # 手动发射toggled信号

            # 更新动画
            self._toggle_handler(self._checked)

        super().mouseReleaseEvent(event)

    def _toggle_handler(self, is_checked):
        self._set_animation_target(is_checked)
        self.toggle_animation.try_to_start()
