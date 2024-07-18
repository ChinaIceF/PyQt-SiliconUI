import time

import numpy
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton

from siui.core.animation import SiExpAnimation
from siui.core.globals import SiGlobal
from siui.components.widgets.abstracts.widget import ABCAnimatedWidget
from siui.components.widgets.label import SiLabel
from siui.core.color import Color


class ABCButton(QPushButton):
    """
    抽象按钮控件\n
    提供点击、按下、松开的信号和色彩动画
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        # 工具提示内容
        self.hint = ""

        # 占位用的被绑定部件，显示在按钮正中央
        self.attachment_ = ABCAnimatedWidget()

        # 被绑定部件偏离中心的像素数
        self.attachment_shifting = numpy.array([0, 0])

        # 启用点击动画，通常在仅需要按下和抬起事件时禁用
        self.enabled_click_animation = True

        # 绑定点击事件到点击槽函数，这将触发点击动画
        self.clicked.connect(self._clicked_slot)

        # 提供悬停时的颜色变化动画
        self.hover_highlight = SiLabel(self)
        self.hover_highlight.stackUnder(self)  # 置于按钮的底部
        self.hover_highlight.setColor("#00FFFFFF")
        self.hover_highlight.getAnimationGroup().fromToken("color").setBias(0.2)
        self.hover_highlight.getAnimationGroup().fromToken("color").setFactor(1 / 8)

        # 提供点击时的颜色变化动画
        self.flash = SiLabel(self)
        self.flash.stackUnder(self)  # 置于按钮的底部
        self.flash.setColor("#00FFFFFF")
        self.flash.getAnimationGroup().fromToken("color").setBias(0.2)
        self.flash.getAnimationGroup().fromToken("color").setFactor(1 / 8)

    def setAttachmentShifting(self, x, y):
        """
        设置被绑定部件偏离中心的像素数，偏移量将直接与其坐标相加作为最终位置
        :param x: 横坐标偏移多少像素
        :param y: 纵坐标偏移多少像素
        :return:
        """
        self.attachment_shifting = numpy.array([x, y])

    def setAttachment(self, widget):
        """
        设置绑定部件。被绑定部件将会被设为按钮的子控件，并显示在按钮的正中央
        :param widget: 部件
        :return:
        """
        # 删除旧的绑定部件
        self.attachment_.deleteLater()

        self.attachment_ = widget
        self.attachment_.setParent(self)
        self.resize(self.size())  # 实现刷新位置

    def attachment(self):
        """
        返回被绑定的部件
        :return: 被绑定部件
        """
        return self.attachment_

    def setHint(self, text: str):
        """
        设置工具提示
        :param text: 内容
        :return:
        """
        self.hint = text

    def setFixedStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件固定的样式表\n
        注意，这不会设置按钮本身的固定样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        :param style_sheet: 固定样式表
        :return:
        """
        self.hover_highlight.setFixedStyleSheet(style_sheet)
        self.flash.setFixedStyleSheet(style_sheet)

    def setStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件样式表\n
        注意，这不会设置按钮本身的样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        :param style_sheet: 样式表
        :return:
        """
        self.hover_highlight.setStyleSheet(style_sheet)
        self.flash.setStyleSheet(style_sheet)

    def reloadStyleSheet(self):
        """
        重载样式表，建议将所有设置样式表的内容重写在此方法中\n
        此方法在窗口show方法被调用时、主题改变时被调用
        :return:
        """
        return

    def setEnableClickAnimation(self, b: bool):
        """
        设置是否启用点击动画
        :param b: 是否启用
        :return:
        """
        self.enabled_click_animation = b

    def _clicked_slot(self):
        if self.enabled_click_animation is True:
            self._run_clicked_ani()

    def _run_clicked_ani(self):
        self.flash.setColor(SiGlobal.siui.colors["BUTTON_FLASH"])
        self.flash.setColorTo(Color.transparency(SiGlobal.siui.colors["BUTTON_FLASH"], 0))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(SiGlobal.siui.colors["BUTTON_HOVER"])

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(self)
            SiGlobal.siui.windows["TOOL_TIP"].show_()
            SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint)

    def leaveEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(Color.transparency(SiGlobal.siui.colors["BUTTON_HOVER"], 0))

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
            SiGlobal.siui.windows["TOOL_TIP"].hide_()

    def adjustSize(self):
        """
        根据被绑定控件的大小调整按钮的大小
        :return:
        """
        att_size = self.attachment().size()
        preferred_width = max(32, att_size.width() + 24)
        preferred_height = max(32, att_size.height() + 8)

        self.resize(preferred_width, preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.hover_highlight.resize(size)
        self.flash.resize(size)

        self.attachment_.move((w - self.attachment_.width()) // 2 + self.attachment_shifting[0],
                              (h - self.attachment_.height()) // 2 + self.attachment_shifting[1])


class ABCPushButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 按钮表面
        self.body_top = SiLabel(self)
        self.body_top.lower()

        # 绘制最底层阴影部分
        self.body_bottom = SiLabel(self)
        self.body_bottom.lower()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置按钮表面的圆角边框
        self.body_top.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

        # 设置按钮阴影的圆角边框
        self.body_bottom.setFixedStyleSheet("border-radius: 4px")

        # 把有效区域设置成 PushButton 的形状
        self.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.hover_highlight.resize(w, h - 3)
        self.flash.resize(w, h - 3)

        self.body_top.resize(w, h - 3)
        self.body_bottom.resize(w, h)


class LongPressThread(QThread):
    """
    长按按钮的线程，用于处理长按计时、信号触发和动画
    """
    ticked = pyqtSignal(float)
    holdTimeout = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_ = parent

        # 创建一个动画，不激活动画，而是每次运行时调用一次_process方法
        self.animation = SiExpAnimation(self)
        self.animation.setCurrent(0)
        self.animation.setTarget(1)
        self.animation.setBias(0.001)
        self.animation.setFactor(1 / 16)
        self.animation.ticked.connect(self.ticked.emit)

    def parent(self):
        return self.parent_

    # 重写进程
    def run(self):
        # 初始化等待时间
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5:  # 即便松开，在额定时间内继续按压仍然会继续计数

            # 如果父对象按钮处于按下状态并且动画尚未完成
            while self.parent().isPressed() and self.animation.current() < 1:
                # 重置等待时间
                time_start_waiting = time.time()

                # 更新进度并发射信号
                self.animation._process()

                # 等待帧
                time.sleep(1 / 60)

            # 如果循环被跳出，并且此时动画已经完成了
            if self.animation.current() == 1:
                # 发射长按已经超时信号，即此时点击已经被确认
                self.holdTimeout.emit()

                # 让进度停留一会，并跳出前进动画循环
                time.sleep(10 / 60)
                break

            time.sleep(1 / 60)

        # 如果前进的循环已经被跳出，并且此时动画进度不为0
        while self.animation.current() > 0:
            # 减少动画进度，直至0，并不断发射值改变信号
            self.animation.setCurrent(max(0, self.animation.current() - 0.1))
            self.animation.ticked.emit(self.animation.current())
            time.sleep(1 / 60)


class ABCToggleButton(ABCButton):
    """
    切换按钮抽象类，注意：这并非是复选框的抽象类
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 圆角半径
        self.border_radius = 4

        # 设置自己为可选中
        self.setCheckable(True)

        # 颜色叠层的颜色状态
        self.color_when_is_on = "20ffffff"
        self.color_when_is_off = "#00ffffff"

        # 创建一个颜色叠层，用于标识被选中的状态
        self.color_label = SiLabel(self)
        self.color_label.setColor(self.color_when_is_off)   # 初始是关闭状态

        # 把状态切换信号绑定到颜色切换的槽函数上
        self.toggled.connect(self._toggled_handler)

        # 闪光和悬停置顶，防止设定不透明颜色时没有闪光
        self.hover_highlight.raise_()
        self.flash.raise_()

    def setStateColor(self, when_off: str, when_on: str):
        """
        设置不同状态下按钮的颜色
        :param when_off: 当设置为关时的颜色
        :param when_on: 当设置为开时的颜色
        :return:
        """
        self.color_when_is_off = when_off
        self.color_when_is_on = when_on

        # 刷新当前颜色
        self._toggled_handler(self.isChecked())

    def setBorderRadius(self, r: int):
        """
        设置边框圆角半径
        :param r: 半径
        """
        self.border_radius = r

    def reloadStyleSheet(self):
        # 设置颜色块圆角
        self.color_label.setFixedStyleSheet(f"border-radius: {self.border_radius}px")

        # 设置自身圆角
        self.setFixedStyleSheet(f"border-radius: {self.border_radius}px")

    def _toggled_handler(self, state):
        if state is True:
            self.color_label.setColorTo(self.color_when_is_on)
        else:
            self.color_label.setColorTo(self.color_when_is_off)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.color_label.resize(event.size())