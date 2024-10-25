
from PyQt5.QtCore import QPoint, pyqtSignal, QEvent
from PyQt5.QtWidgets import QLabel

from siui.core import Si, SiAnimationGroup, SiColor, SiExpAnimation, SiGlobal, SiQuickEffect
from siui.gui.color_group import SiColorGroup


# 2024.7.2 添加动画支持标签
class ABCAnimatedLabel(QLabel):
    moved = pyqtSignal(object)
    resized = pyqtSignal(object)
    opacityChanged = pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hint = ""
        self.fixed_stylesheet = ""
        self.silicon_widget_flags = {}

        # 颜色组
        self.color_group = SiColorGroup(reference=SiGlobal.siui.colors)

        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.move_anchor = QPoint(0, 0)  # 移动时的基准点位置

        self.animation_move = SiExpAnimation(self)
        self.animation_move.setFactor(1/4)
        self.animation_move.setBias(1)
        self.animation_move.setCurrent([0, 0])
        self.animation_move.setTarget([0, 0])
        self.animation_move.ticked.connect(self._move_ani_handler)

        self.animation_resize = SiExpAnimation(self)
        self.animation_resize.setFactor(1/4)
        self.animation_resize.setBias(1)
        self.animation_resize.setCurrent([0, 0])
        self.animation_resize.setTarget([0, 0])
        self.animation_resize.ticked.connect(self._resize_ani_handler)

        self.animation_opacity = SiExpAnimation(self)
        self.animation_opacity.setFactor(1/4)
        self.animation_opacity.setBias(0.01)
        self.animation_opacity.ticked.connect(self._opacity_ani_handler)

        self.animation_color = SiExpAnimation(self)
        self.animation_color.setFactor(1/4)
        self.animation_color.setBias(1)
        self.animation_color.ticked.connect(self._set_color_handler)

        self.animation_text_color = SiExpAnimation(self)
        self.animation_text_color.setFactor(1/4)
        self.animation_text_color.setBias(1)
        self.animation_text_color.ticked.connect(self._set_text_color_handler)

        # 创建动画组，以tokenize以上动画
        self.animation_group = SiAnimationGroup()
        self.animation_group.addMember(self.animation_move, token="move")
        self.animation_group.addMember(self.animation_resize, token="resize")
        self.animation_group.addMember(self.animation_opacity, token="opacity")
        self.animation_group.addMember(self.animation_color, token="color")
        self.animation_group.addMember(self.animation_text_color, token="text_color")

    def setStyleSheet(self, stylesheet: str):
        if self.fixed_stylesheet == "":
            super().setStyleSheet(stylesheet)
        else:
            super().setStyleSheet(self.fixed_stylesheet + ";" + stylesheet)

    def reloadStyleSheet(self):
        """
        重载样式表，建议将所有设置样式表的内容重写在此方法中\n
        此方法在窗口show方法被调用时、主题改变时被调用
        """
        return

    def setSiliconWidgetFlag(self,
                             flag,
                             on: bool = True):
        """
        Set a silicon widget flag on or off to a widget
        :param flag: silicon widget flag
        :param on: set to on or off
        """
        self.silicon_widget_flags[flag.name] = on

    def isSiliconWidgetFlagOn(self, flag):
        """
        Check whether the flag is on
        :param flag: silicon widget flag
        :return: True or False
        """
        if flag.name not in self.silicon_widget_flags.keys():
            return False
        return self.silicon_widget_flags[flag.name]

    def getColor(self, token):
        return self.color_group.fromToken(token)

    def colorGroup(self):
        """
        Get the color group of this widget
        :return: SiColorGroup
        """
        return self.color_group

    def animationGroup(self):
        """
        返回动画组
        :return: 动画组
        """
        return self.animation_group

    def setFixedStyleSheet(self, fixed_stylesheet: str):
        """
        设置样式表前置固定内容，同时将其设为样式表，此后每次运行 setStyleSheet 方法时，都会在样式表前附加这段固定内容
        :param fixed_stylesheet: 样式表内容
        :return:
        """
        self.fixed_stylesheet = fixed_stylesheet
        self.setStyleSheet(fixed_stylesheet)

    def _move_ani_handler(self, arr):
        x, y = arr
        super().move(int(x), int(y))

    def _resize_ani_handler(self, arr):
        w, h = arr
        super().resize(int(w), int(h))

    def _opacity_ani_handler(self, opacity: float):
        self.setOpacity(opacity)

    def _set_color_handler(self, color_value):
        self.setStyleSheet(f"background-color: {SiColor.toCode(color_value)}")

    def _set_text_color_handler(self, color_value):
        self.setStyleSheet(f"color: {SiColor.toCode(color_value)}")

    def setMoveLimits(self,
                      x1: int,
                      y1: int,
                      x2: int,
                      y2: int):
        """
        设置移动限制，移动限制会阻止动画目标超出矩形范围限制
        :param x1: 左上 横坐标
        :param y1: 左上 纵坐标
        :param x2: 右下 横坐标
        :param y2: 右下 纵坐标
        :return:
        """
        # 拖动控件只能在这个范围内运动
        # 注意！必须满足 x1 <= x2, y1 <= y2
        self.setSiliconWidgetFlag(Si.HasMoveLimits, True)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def _legalize_moving_target(self, x: int, y: int):
        # 使移动的位置合法
        if self.isSiliconWidgetFlagOn(Si.HasMoveLimits) is False:
            return x, y

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x = max(x1, min(x2 - self.width(), x))
        y = max(y1, min(y2 - self.height(), y))
        return x, y

    def setColor(self, color_code):
        """ 设置标签背景颜色 """
        color_value = SiColor.toArray(color_code)
        self.animation_color.setCurrent(color_value)
        self._set_color_handler(color_value)

    def setColorTo(self, color_code):
        """ 设置标签背景颜色（具动画） """
        self.animation_color.setTarget(SiColor.toArray(color_code))
        self.animation_color.try_to_start()

    def setTextColor(self, color_code):
        """ 设置标签文字颜色 """
        color_value = SiColor.toArray(color_code)
        self.animation_text_color.setCurrent(color_value)
        self._set_text_color_handler(color_value)

    def setTextColorTo(self, color_code):
        """ 设置标签文字颜色（具动画） """
        self.animation_text_color.setTarget(SiColor.toArray(color_code))
        self.animation_text_color.try_to_start()

    def setOpacity(self, opacity: float):
        """
        设置透明度
        :param opacity: 透明度值 0-1
        :return:
        """
        self.animation_opacity.setCurrent(opacity)
        SiQuickEffect.applyOpacityOn(self, opacity)

        if opacity == 0:
            self.hide()

        if (opacity > 0) and (self.isVisible() is False):
            self.show()

        if self.isSiliconWidgetFlagOn(Si.EnableAnimationSignals):
            self.opacityChanged.emit(opacity)

    def setOpacityTo(self, opacity: float):
        """
        带动画地设置控件的透明度
        :param opacity: 透明度值 0-1
        :return:
        """
        if self.isSiliconWidgetFlagOn(Si.InstantSetOpacity) is False:
            self.animation_opacity.setTarget(opacity)
            self.activateSetOpacity()
        else:
            self.setOpacity(opacity)

    def activateSetOpacity(self):
        self.animation_opacity.try_to_start()

    def deactivateSetOpacity(self):
        self.animation_opacity.stop()

    def isSetOpacityActive(self):
        return self.animation_opacity.isActive()

    def activateMove(self):
        self.animation_move.try_to_start()

    def deactivateMove(self):
        self.animation_move.stop()

    def isMoveActive(self):
        return self.animation_move.isActive()

    def activateResize(self):
        self.animation_resize.try_to_start()

    def deactivateResize(self):
        self.animation_resize.stop()

    def isResizeActive(self):
        return self.animation_resize.isActive()

    def setMoveAnchor(self, x, y):
        self.move_anchor = QPoint(x, y)

    def moveAnchor(self):
        return self.move_anchor

    def move(self, *args):  # 重写移动方法，从而按照锚点的位置移动控件
        point = QPoint(*args)
        anchor_adjusted_point = point - self.move_anchor
        super().move(anchor_adjusted_point)

    def moveTo(self, x: int, y: int):
        """ 带动画地将控件移动到指定位置 """
        x, y = self._legalize_moving_target(x, y)
        if self.isSiliconWidgetFlagOn(Si.InstantMove) is False:
            self.animation_move.setTarget([x, y])
            self.activateMove()
        else:
            self.move(x, y)

    def moveEvent(self, event):
        # moveEvent 事件一旦被调用，控件的位置会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 pos()
        super().moveEvent(event)
        pos = event.pos() + self.move_anchor
        self.animation_move.setCurrent([pos.x(), pos.y()])

        if self.isSiliconWidgetFlagOn(Si.EnableAnimationSignals):
            self.moved.emit([event.pos().x(), event.pos().y()])

    def resizeTo(self, w: int, h: int):
        """ 具动画重设大小到目标尺寸 """
        if self.isSiliconWidgetFlagOn(Si.InstantResize) is False and self.isVisible() is True:
            self.animation_resize.setTarget([w, h])
            self.activateResize()
        else:
            self.resize(w, h)

    def resizeEvent(self, event):
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.animation_resize.setCurrent([w, h])
        if self.isSiliconWidgetFlagOn(Si.EnableAnimationSignals):
            self.resized.emit([w, h])

    def setHint(self, text: str):
        """
        Set the tooltip for the label
        :param text: tooltip content. Rich text is supported
        """
        self.hint = text
        self.setToolTip(text)

        # 把新的工具提示推送给工具提示窗口
        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            if SiGlobal.siui.windows["TOOL_TIP"].nowInsideOf() == self:  # 如果鼠标正在该控件内
                SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint,
                                                          flash=self.isSiliconWidgetFlagOn(Si.FlashOnHintUpdated))

    def setText(self, text: str):
        super().setText(text)
        if self.isSiliconWidgetFlagOn(Si.AdjustSizeOnTextChanged) is True:
            self.adjustSize()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(self)
            SiGlobal.siui.windows["TOOL_TIP"].show_()
            SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
            SiGlobal.siui.windows["TOOL_TIP"].hide_()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)