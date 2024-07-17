"""
基础控件
ABCAnimatedLabel 提供各类简单易用的属性动画支持
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel

from siui.core.animation import SiAnimationGroup, SiExpAnimation
from siui.core.color import Color
from siui.core.globals import SiGlobal


# 2024.7.2 添加动画支持标签
class ABCAnimatedLabel(QLabel):
    moved = pyqtSignal(object)
    resized = pyqtSignal(object)
    opacityChanged = pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fixed_stylesheet = ""
        self.hint = ""  # 工具提示

        self.flash_when_hint_updated = False    # 在工具提示被重新设置时，使工具提示闪烁
        self.instant_move = False               # 是否立即移动而不运行动画
        self.instant_resize = False             # 是否立即重设大小而不运行动画
        self.instant_set_opacity = False        # 是否立即重设透明度而不运行动画
        self.move_limits = False                # 是否有移动限定区域
        self.auto_adjust_size = False           # 是否在setText被调用时自动调整空间大小
        self.enable_signal_emission = False     # 是否启用moved，resized，opacityChanged信号
        self.force_use_animations = False       # 强制使用动画，这将替换 move, resize 方法

        self.x1, self.y1, self.x2, self.y2 = None, None, None, None

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
        self.animation_opacity.setCurrent(1)
        self.animation_opacity.ticked.connect(self._opacity_ani_handler)

        self.animation_color = SiExpAnimation(self)
        self.animation_color.setFactor(1/4)
        self.animation_color.setBias(1)
        self.animation_color.ticked.connect(self._set_color_handler)

        # 创建动画组，以tokenize以上动画
        self.animation_group = SiAnimationGroup()
        self.animation_group.addMember(self.animation_move, token="move")
        self.animation_group.addMember(self.animation_resize, token="resize")
        self.animation_group.addMember(self.animation_opacity, token="opacity")
        self.animation_group.addMember(self.animation_color, token="color")

    def setColorTo(self, color_code):
        """
        设置目标颜色，同时启动动画
        :param color_code: 色号
        :return:
        """
        self.animation_color.setTarget(Color.decodeColor(color_code))
        self.animation_color.try_to_start()

    def setColor(self, color_code):
        """
        设置颜色
        :param color_code: 色号
        :return:
        """
        color_value = Color.decodeColor(color_code)
        self.animation_color.setCurrent(color_value)
        self._set_color_handler(color_value)

    def _set_color_handler(self, color_value):
        self.setStyleSheet(f"background-color: {Color.encodeColor(color_value)}")

    def getAnimationGroup(self):
        """
        返回动画组
        :return: 动画组
        """
        return self.animation_group

    def reloadStyleSheet(self):
        """
        重载样式表，建议将所有设置样式表的内容重写在此方法中\n
        此方法在窗口show方法被调用时、主题改变时被调用
        :return:
        """
        return

    def setStyleSheet(self, stylesheet: str):
        if self.fixed_stylesheet == "":
            super().setStyleSheet(stylesheet)
        else:
            super().setStyleSheet(self.fixed_stylesheet + ";" + stylesheet)

    def setFixedStyleSheet(self, fixed_stylesheet: str):
        """
        设置样式表前置固定内容，同时将其设为样式表，此后每次运行 setStyleSheet 方法时，都会在提供的样式表前附加这段固定内容
        :param fixed_stylesheet: 样式表内容
        :return:
        """
        self.fixed_stylesheet = fixed_stylesheet
        self.setStyleSheet(fixed_stylesheet)

    def setForceUseAnimations(self, b: bool):
        """
        设置强制使用动画，这将覆盖原来的方法
        :return:
        """
        self.force_use_animations = b
        if b is True:
            self.move = self.moveTo
            self.resize = self.resizeTo

    def setUseSignals(self, b: bool):
        """
        设置是否使用 moved，resized，opacityChanged 信号，通常来说这是关闭的，因为这可能会带来较大的性能开销
        :param b: 是否使用信号
        :return:
        """
        self.enable_signal_emission = b

    def setFlashWhenHintUpdated(self, b: bool):
        """
        在工具提示被重新设置时，是否使工具提示闪烁
        :param b: 是否闪烁
        :return:
        """
        self.flash_when_hint_updated = b

    def setHint(self, text: str):
        """
        设置工具提示
        :param text: 内容
        :return:
        """
        self.hint = text

        # 把新的工具提示推送给工具提示窗口
        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            if SiGlobal.siui.windows["TOOL_TIP"].nowInsideOf() == self:  # 如果鼠标正在该控件内
                SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint, flash=self.flash_when_hint_updated)

    def setText(self, text: str):
        """
        设置标签的文本
        :param text: 文本
        :return:
        """
        super().setText(text)
        if self.auto_adjust_size is True:
            self.adjustSize()

    def setAutoAdjustSize(self, b: bool):
        """
        设置每次调用 setText 方法后自动调整标签的尺寸
        :param b: 是否自动调整
        :return:
        """
        self.auto_adjust_size = b

    def _move_ani_handler(self, arr):
        x, y = arr
        super().move(int(x), int(y))

    def _resize_ani_handler(self, arr):
        w, h = arr
        super().resize(int(w), int(h))

    def _opacity_ani_handler(self, opacity: float):
        self.setOpacity(opacity)

    def resizeTo(self, w: int, h: int):
        """
        具动画重设大小到目标尺寸
        :param w: 宽
        :param h: 高
        :return:
        """
        if self.instant_resize is False and self.isVisible() is True:
            self.animation_resize.setTarget([w, h])
            self.activateResize()
        else:
            super().resize(w, h)

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
        self.move_limits = True
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def hasMoveLimits(self):
        return self.move_limits

    def removeMoveLimits(self):
        self.move_limits = False

    def _legalize_moving_target(self, x: int, y: int):
        # 使移动的位置合法
        if self.move_limits is False:
            return x, y

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x = max(x1, min(x2 - self.width(), x))
        y = max(y1, min(y2 - self.height(), y))
        return x, y

    def moveTo(self, x: int, y: int):
        """
        带动画地将标签移动到指定位置
        :param x: 目标横坐标
        :param y: 目标纵坐标
        :return:
        """
        # moveTo 方法不同于 move，它经过动画（如果开启）
        x, y = self._legalize_moving_target(x, y)
        if self.instant_move is False:
            self.animation_move.setTarget([x, y])
            self.activateMove()
        else:
            super().move(x, y)

    def setOpacity(self, opacity: float):
        """
        设置透明度
        :param opacity: 透明度值 0-1
        :return:
        """
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(opacity)
        self.setGraphicsEffect(self.opacity_effect)
        if self.enable_signal_emission:
            self.opacityChanged.emit(self.opacity)

    def setOpacityTo(self, opacity: float):
        """
        带动画地设置控件的透明度
        :param opacity: 透明度值 0-1
        :return:
        """
        if self.instant_set_opacity is False:
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

    def setInstantMove(self, b: bool):
        """
        设置控件是否立即移动，不再运行移动动画
        :param b: 是否立即移动
        :return:
        """
        self.instant_move = b
        if b is True:  # 如果更改为立即移动，立即终止动画，并完成动画
            self.deactivateMove()
            try:
                x, y = self.animation_move.target_
                self.move(x, y)
            except:
                pass

    def setInstantResize(self, b: bool):
        """
        设置控件是否立即重设大小，不再运行重设大小动画
        :param b: 是否立即重设大小
        :return:
        """
        self.instant_resize = b
        if b is True:  # 如果更改为立即重设大小，立即终止动画，并完成动画
            self.deactivateResize()
            try:
                w, h = self.animation_resize.target_
                self.resize(w, h)
            except:
                pass

    def setInstantSetOpacity(self, b: bool):
        """
        设置控件是否立即设置透明度，不再运行设置透明度动画
        :param b: 是否立即设置透明度
        :return:
        """
        self.instant_set_opacity = b
        if b is True:
            self.deactivateSetOpacity()
            opacity = self.animation_opacity.target_
            self.setOpacity(opacity)

    def moveEvent(self, event):
        # moveEvent 事件一旦被调用，控件的位置会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 pos()
        super().moveEvent(event)
        pos = event.pos()
        x, y = pos.x(), pos.y()
        self.animation_move.setCurrent([x, y])
        if self.enable_signal_emission:
            self.moved.emit([x, y])

    def resizeEvent(self, event):
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.animation_resize.setCurrent([w, h])
        if self.enable_signal_emission:
            self.resized.emit([w, h])

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
