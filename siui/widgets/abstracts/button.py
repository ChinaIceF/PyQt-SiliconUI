from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QThread, pyqtSignal

from siui.core.animation import SiExpAnimation
from siui.widgets.abstracts import ABCAnimatedWidget
from siui.widgets.label import SiColoredLabel, SiLabel

import time

class ABCButton(QPushButton):
    """
    抽象按钮控件\n
    提供点击、按下、松开的信号和色彩动画
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        # 启用点击动画，通常在仅需要按下和抬起事件时禁用
        self.enabled_click_animation = True

        # 绑定点击事件到点击槽函数，这将触发点击动画
        self.clicked.connect(self._clicked_slot)

        # 提供悬停时的颜色变化动画
        self.hover_highlight = SiColoredLabel(self)
        self.hover_highlight.stackUnder(self)  # 置于按钮的底部
        self.hover_highlight.setColor("#00FFFFFF")
        self.hover_highlight.getAnimationGroup().fromToken("color").setBias(0.2)
        self.hover_highlight.getAnimationGroup().fromToken("color").setFactor(1 / 8)

        # 提供点击时的颜色变化动画
        self.flash = SiColoredLabel(self)
        self.flash.stackUnder(self)  # 置于按钮的底部
        self.flash.setColor("#00FFFFFF")
        self.flash.getAnimationGroup().fromToken("color").setBias(0.2)
        self.flash.getAnimationGroup().fromToken("color").setFactor(1 / 8)

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

    def reloadStylesheet(self):
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
        self.flash.setColor("#20FFFFFF")
        self.flash.setColorTo("#00FFFFFF")

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo("#10FFFFFF")

    def leaveEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo("#00FFFFFF")

    def resizeEvent(self, event):
        size = event.size()
        self.hover_highlight.resize(size)
        self.flash.resize(size)


class ABCPushButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 占位用的被绑定部件，显示在按钮正中央
        self.attachment = ABCAnimatedWidget()

        # 按钮表面
        self.body_top = SiLabel(self)
        self.body_top.lower()

        # 绘制最底层阴影部分
        self.body_bottom = SiLabel(self)
        self.body_bottom.lower()

    def setAttachment(self, widget):
        """
        设置绑定部件。被绑定部件将会被设为按钮的子控件，并显示在按钮的正中央
        :param widget: 部件
        :return:
        """
        self.attachment = widget
        self.attachment.setParent(self)
        self.resize(self.size())  # 实现刷新位置

    def reloadStylesheet(self):
        super().reloadStylesheet()

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
        size = event.size()
        w, h = size.width(), size.height()

        self.hover_highlight.resize(w, h - 3)
        self.flash.resize(w, h - 3)

        self.body_top.resize(w, h - 3)
        self.body_bottom.resize(w, h)

        self.attachment.move((w - self.attachment.width()) // 2, (h - 3 - self.attachment.height()) // 2)


class ABCHoldThread(QThread):
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
        self.animation.setFactor(1/16)
        self.animation.ticked.connect(self.ticked.emit)

    def parent(self):
        return self.parent_

    # 重写进程
    def run(self):
        # 初始化等待时间
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5: # 即便松开，在额定时间内继续按压仍然会继续计数

            # 如果父对象按钮处于按下状态并且动画尚未完成
            while self.parent().isPressed() and self.animation.current() < 1:
                # 重置等待时间
                time_start_waiting = time.time()

                # 更新进度并发射信号
                self.animation._process()

                # 等待帧
                time.sleep(1/60)

            # 如果循环被跳出，并且此时动画已经完成了
            if self.animation.current() == 1:
                # 发射长按已经超时信号，即此时点击已经被确认
                self.holdTimeout.emit()

                # 让进度停留一会，并跳出前进动画循环
                time.sleep(10/60)
                break

            time.sleep(1/60)

        # 如果前进的循环已经被跳出，并且此时动画进度不为0
        while self.animation.current() > 0:
            # 减少动画进度，直至0，并不断发射值改变信号
            self.animation.setCurrent(max(0, self.animation.current() - 0.1))
            self.animation.ticked.emit(self.animation.current())
            time.sleep(1/60)
