import time

import numpy
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QPushButton

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core import SiExpAnimation
from siui.core import SiColor
from siui.core import SiGlobal
from siui.gui.color_group import SiColorGroup


class ABCButton(QPushButton):
    """
    抽象按钮控件\n
    提供点击、按下、松开的信号和色彩动画
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        self.hint = ""
        self.color_group = SiColorGroup(reference=SiGlobal.siui.colors)
        self.flash_on_clicked = True
        self.enabled_repetitive_clicking = False

        self.attachment_ = SiWidget()                       # 占位用的被绑定部件，显示在按钮正中央
        self.attachment_shifting = numpy.array([0, 0])      # 被绑定部件偏离中心的像素数

        # 提供悬停时的颜色变化动画
        self.hover_highlight = SiLabel(self)
        self.hover_highlight.stackUnder(self)  # 置于按钮的底部
        self.hover_highlight.setColor(SiColor.trans(self.getColor(SiColor.BUTTON_HOVER), 0.0))
        self.hover_highlight.animationGroup().fromToken("color").setBias(0.2)
        self.hover_highlight.animationGroup().fromToken("color").setFactor(1 / 8)

        # 提供点击时的颜色变化动画
        self.flash_label = SiLabel(self)
        self.flash_label.stackUnder(self)  # 置于按钮的底部
        self.flash_label.setColor(SiColor.trans(self.getColor(SiColor.BUTTON_FLASH), 0.0))
        self.flash_label.animationGroup().fromToken("color").setBias(0.2)
        self.flash_label.animationGroup().fromToken("color").setFactor(1 / 8)

        self.clicked.connect(self._on_self_clicked)

        self.repeat_clicking_timer = QTimer(self)
        self.repeat_clicking_timer.setInterval(50)
        self.repeat_clicking_timer.timeout.connect(self.clicked.emit)

        self.repeat_clicking_trigger_timer = QTimer(self)
        self.repeat_clicking_trigger_timer.setSingleShot(True)
        self.repeat_clicking_trigger_timer.timeout.connect(self.repeat_clicking_timer.start)
        self.repeat_clicking_trigger_timer.setInterval(500)

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
        设置绑定部件。绑定部件会被设为按钮的子控件，并显示在按钮的正中央
        :param widget: 部件
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

    def getColor(self, token):
        return self.color_group.fromToken(token)

    def colorGroup(self):
        """
        Get the color group of this widget
        :return: SiColorGroup
        """
        return self.color_group

    def setHint(self, text: str):
        """
        设置工具提示
        :param text: 内容
        :return:
        """
        self.hint = text

    def setRepetitiveClicking(self, state):
        self.enabled_repetitive_clicking = state

    def setFixedStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件固定的样式表\n
        注意，这不会设置按钮本身的固定样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        :param style_sheet: 固定样式表
        :return:
        """
        self.hover_highlight.setFixedStyleSheet(style_sheet)
        self.flash_label.setFixedStyleSheet(style_sheet)

    def setStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        设置按钮组件样式表\n
        注意，这不会设置按钮本身的样式表，而且不能改变相应的颜色设置，本方法只应用于更改边框圆角半径等属性
        :param style_sheet: 样式表
        :return:
        """
        self.hover_highlight.setStyleSheet(style_sheet)
        self.flash_label.setStyleSheet(style_sheet)

    def reloadStyleSheet(self):
        """
        重载样式表，建议将所有设置样式表的内容重写在此方法中\n
        此方法在窗口show方法被调用时、主题改变时被调用
        :return:
        """
        self.attachment().reloadStyleSheet()
        return

    def flashLabel(self):
        """ get the label that preform flashing animations """
        return self.flash_label

    def hoverLabel(self):
        """ get the hover-highlight label """
        return self.hover_highlight

    def setFlashOnClicked(self, b: bool):
        """
        设置是否启用点击动画
        :param b: 是否启用
        :return:
        """
        self.flash_on_clicked = b

    def _on_self_clicked(self):
        if self.flash_on_clicked is True:
            self._run_clicked_ani()

    def _run_clicked_ani(self):
        self.flash_label.setColor(self.color_group.fromToken(SiColor.BUTTON_FLASH))
        self.flash_label.setColorTo(SiColor.trans(self.color_group.fromToken(SiColor.BUTTON_FLASH), 0))

    def flash(self):
        """ play flash animation once but do nothing else """
        self._run_clicked_ani()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(self.color_group.fromToken(SiColor.BUTTON_HOVER))

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(self)
            SiGlobal.siui.windows["TOOL_TIP"].show_()
            SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint)

    def leaveEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(SiColor.trans(self.color_group.fromToken(SiColor.BUTTON_HOVER), 0))

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
            SiGlobal.siui.windows["TOOL_TIP"].hide_()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if self.enabled_repetitive_clicking:
            self.repeat_clicking_trigger_timer.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.repeat_clicking_trigger_timer.stop()
        self.repeat_clicking_timer.stop()

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
        self.flash_label.resize(size)

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
        self.flash_label.resize(w, h - 3)

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
        self.safe_to_stop = False

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
        self.safe_to_stop = False

        # 初始化等待时间
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5:  # 即便松开，在额定时间内继续按压仍然会继续计数

            # 如果父对象按钮处于按下状态并且动画尚未完成
            while self.parent().isPressed() and self.animation.current() < 1:
                # 重置等待时间
                time_start_waiting = time.time()

                if self.safe_to_stop:
                    self.safe_to_stop = False
                    print("直接返回1")
                    return

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
            if self.safe_to_stop:
                self.safe_to_stop = False
                print("直接返回2")
                return

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

        # 创建一个颜色叠层，用于标识被选中的状态
        self.color_label = SiLabel(self)
        self.color_label.setColor(self.getColor(SiColor.BUTTON_OFF))  # 初始是关闭状态

        # 把状态切换信号绑定到颜色切换的槽函数上
        self.toggled.connect(self._toggled_handler)

        # 闪光和悬停置顶，防止设定不透明颜色时没有闪光
        self.hover_highlight.raise_()
        self.flash_label.raise_()

    def colorLabel(self):
        return self.color_label

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

        # 刷新颜色
        self.color_label.setColor(self.getColor(SiColor.BUTTON_ON if self.isChecked() else SiColor.BUTTON_OFF))  # noqa: E501

    def _toggled_handler(self, state):
        if state is True:
            self.color_label.setColorTo(self.getColor(SiColor.BUTTON_ON))
        else:
            self.color_label.setColorTo(self.getColor(SiColor.BUTTON_OFF))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.color_label.resize(event.size())
