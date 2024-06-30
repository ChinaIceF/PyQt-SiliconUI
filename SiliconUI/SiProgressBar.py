from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from . import SiAnimationObject, SiGlobal, SiLabel
from .SiGlobal import *


class ProgressBarFrame(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def enterEvent(self, event):
        super().enterEvent(event)
        SiGlobal.floating_window.show_animation()
        SiGlobal.floating_window.setText(str(round(self.parent.progress * 100, 1)) + "%")

    def leaveEvent(self, event):
        super().leaveEvent(event)
        SiGlobal.floating_window.hide_animation()


class SiProgressBar(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.border_radius = 4
        self.progress_colors = {
            "loading": "#66CBFF",
            "warning": "#FED966",
            "paused": "#7F7F7F",
        }
        self.status_names = ["loading", "warning", "paused"]

        self.progress = 0
        self.start_color = "#66CBFF"
        self.current_color = "#66CBFF"
        self.target_color = "#66CBFF"

        self.animation_progress = SiAnimationObject.SiAnimationStandard(self)
        self.animation_progress.setFactor(1 / 4)
        self.animation_progress.setBias(1)
        self.animation_progress.ticked.connect(self._animationProgressHandler)

        self.animation_color = SiAnimationObject.SiAnimationStandard(self)
        self.animation_color.setFactor(1 / 8)
        self.animation_color.setBias(0.01)
        self.animation_color.setTarget(1)
        self.animation_color.ticked.connect(self._animationColorHandler)

        self.frame = ProgressBarFrame(self)
        self.frame.setStyleSheet(
            f"""
            background-color: {colorset.BG_GRAD_HEX[0]};
            border-radius: {self.border_radius};
        """
        )

        self.bar = QLabel(self.frame)
        self.bar.setStyleSheet(
            f"""
            background-color: {self.current_color};
            border-radius: {self.border_radius};
        """
        )
        self.bar.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def getProgress(self):
        return self.progress

    def getBarWidth(self):
        p = self.progress
        w = self.border_radius * 2 + (self.width() - self.border_radius * 2) * p
        return int(w)

    def setStatus(self, status):
        self.setBarColor(self.progress_colors[self.status_names[status]])

    def stepping(self, delta):
        self.setProgress(self.getProgress() + delta)

    def setProgress(self, progress):
        self.progress = max(min(progress, 1), 0)
        self.animation_progress.setTarget(self.getBarWidth())
        self.animation_progress.try_to_start()

        if self.progress == 1:
            self.setStatus(1)  # 标识处理已加载完的内容
        else:
            if self.current_color in self.progress_colors.values():  # 当前颜色是预设颜色不是自定义颜色，则更新状态
                self.setStatus(0)
            else:  # 当前颜色是自定义颜色，则不更新状态
                pass

    def setBarColor(self, color_hex):
        self.target_color = color_hex
        self.start_color = self.current_color
        self.animation_color.stop()
        self.animation_color.setCurrent(0)
        self.animation_color.try_to_start()

    def setBorderRadius(self, radius):
        self.border_radius = radius
        self.frame.setStyleSheet(
            f"""
            background-color: {colorset.BG_GRAD_HEX[0]};
            border-radius: {self.border_radius};
        """
        )
        self.bar.setStyleSheet(
            f"""
            background-color: {self.current_color};
            border-radius: {self.border_radius};
        """
        )

    def updateBarColor(self):
        self.bar.setStyleSheet(
            f"""
            background-color: {self.current_color};
            border-radius: {self.border_radius};
        """
        )

    def _animationProgressHandler(self, width):
        self.bar.resize(int(width), self.bar.height())

    def _animationColorHandler(self, weight):
        self.current_color = Color.mix(self.target_color, self.start_color, weight)
        self.updateBarColor()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.frame.resize(w, h)
        self.bar.resize(self.getBarWidth(), h)  # 宽度变了 宽度需要重新设置
