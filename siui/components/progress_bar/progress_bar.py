import numpy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen

from siui.components.widgets import SiLabel
from siui.core import ABCSiAnimation, SiColor, SiExpAnimation


class SiProgressBar(SiLabel):
    valueChanged = pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 状态
        self.state_ = "processing"
        self.state_colors = {
            "processing": SiColor.PROGRESS_BAR_PROCESSING,
            "completing": SiColor.PROGRESS_BAR_COMPLETING,
            "paused": SiColor.PROGRESS_BAR_PAUSED,
        }

        # 已完成的百分比值
        self.value_ = 0

        # 进度条框架
        self.frame = SiLabel(self)

        # 进度条轨道
        self.track = SiLabel(self.frame)

        # 进度条已完成部分
        self.progress = SiLabel(self.frame)
        self.progress.setFixedHeight(6)

        # 闪烁层
        self.flash = SiLabel(self.frame)
        self.flash.setFixedHeight(6)
        self.flash.animationGroup().fromToken("color").setFactor(1 / 32)

        # 轨道高度，这决定了进度条进度显示部分的高度
        self.track_height = None
        self.setTrackHeight(4)

    def setTrackHeight(self, height: int):
        """
        Set the height of the progress bar's track
        :param height: height
        """
        self.track_height = height

        self.frame.setFixedHeight(height)
        self.progress.setFixedHeight(height)
        self.flash.setFixedHeight(height)

        self.track.setFixedStyleSheet(f"border-radius: {height//2}px")
        self.progress.setFixedStyleSheet(f"border-radius: {height//2}px")
        self.flash.setFixedStyleSheet(f"border-radius: {height//2}px")

    def setState(self, state: str):
        """
        设置进度条状态
        :param state: processing（加载）, completing（完成中）, paused（暂停）
        """
        if state not in ["processing", "completing", "paused"]:
            raise KeyError(f"Invalid state: {state}")

        self.state_ = state
        self.reloadStyleSheet()

    def state(self):
        """
        获取进度条状态
        :return: 状态
        """
        return self.state_

    def setValue(self, value: float):
        """
        设置进度条当前完成的百分比
        :param value: 百分比
        :return:
        """
        self.value_ = max(0.0, min(value, 1.0))

        self.valueChanged.emit(self.value_)
        self._resize_progress_according_to_value()  # 设置进度位置

        if self.value() == 1.0:
            self.setState("completing")
        elif self.state() == "completing":
            self.setState("processing")

        # 刷新工具提示
        self.refreshHint()

        # 闪烁层闪烁
        self._flash()

    def value(self):
        """
        获取进度条当前完成的百分比
        :return: 百分比
        """
        return self.value_

    def refreshHint(self):
        """
        刷新工具提示，重写该方法以自定义工具提示
        """
        self.setHint(f"{round(self.value()*100, 2)}<span style='color: {self.getColor(SiColor.TEXT_C)}'>%</span>")  # noqa: E501

    def _flash(self):
        """
        触发进度闪烁
        """
        self.flash.setColor(SiColor.trans(self.getColor(SiColor.PROGRESS_BAR_FLASHES), 0.8))
        self.flash.setColorTo(SiColor.trans(self.getColor(SiColor.PROGRESS_BAR_FLASHES), 0.0))

    def _resize_progress_according_to_value(self):
        """
        按照当前进度条的值来设置进度的尺寸
        """
        available_width = self.track.width() - self.frame.height()
        progress_width = self.frame.height() + int(self.value() * available_width)

        self.progress.resizeTo(progress_width, self.progress.height())
        self.flash.resizeTo(progress_width, self.progress.height())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.track.setStyleSheet(f"background-color: {self.getColor(SiColor.PROGRESS_BAR_TRACK)}")
        self.progress.setColorTo(self.getColor(self.state_colors[self.state()]))  # noqa: UP032

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.frame.setGeometry(0, (h - self.frame.height()) // 2, w, self.frame.height())
        self.track.resize(w, self.frame.height())

        # 重设大小之后，进度按比例缩放
        self._resize_progress_according_to_value()


class WaveAnimation(ABCSiAnimation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.t = 0
        self.step = 1/60 * numpy.pi * 2 * 2
        self.omiga = 0.6
        self.b = 0.95
        self.speed_factor = 0.1
        self.setCurrent(0)

    def setSpeedFactor(self, speed_factor):
        self.speed_factor = speed_factor

    def _process(self):
        step_length = self._step_length()
        self.setCurrent(self.current_ + step_length)
        self.ticked.emit(self.current_ * self.speed_factor)
        self.t += self.step

    def _step_length(self):
        return (1 - numpy.sin(self.t * self.omiga)) / (2 * self.b) + 0.45


class SiCircularProgressBar(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.indeterminate_ = False
        self.indeterminate_value = 0
        self.value_ = 0
        self.bar_width = 4
        self.ani_value = 0
        self.margins = (2, 2, -2, -2)

        self.animationGroup().addMember(WaveAnimation(self), "indeterminate_process")
        self.animationGroup().fromToken("indeterminate_process").ticked.connect(self.on_indeterminate_process_ani_ticked)
        self.animationGroup().fromToken("indeterminate_process").setSpeedFactor(1/16*0.2)

        self.animationGroup().addMember(SiExpAnimation(self), "value")
        self.animationGroup().fromToken("value").ticked.connect(self.on_value_ani_ticked)
        self.animationGroup().fromToken("value").setFactor(1/6)
        self.animationGroup().fromToken("value").setBias(0.001)

    def setIndeterminate(self, on):
        self.indeterminate_ = on
        if self.indeterminate_ is True:
            self.setHint("Processing...")
            self.animationGroup().fromToken("indeterminate_process").start()

    def setBarWidth(self, width):
        self.bar_width = width
        self.update()

    def value(self):
        return self.value_

    def setValue(self, value):
        self.value_ = max(0, min(value, 1))
        self.animationGroup().fromToken("value").setTarget(self.value_)
        self.animationGroup().fromToken("value").try_to_start()
        if self.indeterminate_ is False:
            self.setHint(f"{round(self.value_*100, 1)}%")

    def setMargins(self, left, top, right, bottom):
        self.margins = (left, top, -right, -bottom)

    def on_value_ani_ticked(self, value):
        self.ani_value = value
        self.update()

    def on_indeterminate_process_ani_ticked(self, value):
        self.indeterminate_value = value
        self.update()

    def hideEvent(self, a0):
        super().hideEvent(a0)
        self.animationGroup().fromToken("indeterminate_process").stop()

    def showEvent(self, a0):
        super().showEvent(a0)
        if self.indeterminate_ is True:
            self.animationGroup().fromToken("indeterminate_process").start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color_array = SiColor.toArray(self.getColor(SiColor.PROGRESS_BAR_PROCESSING))[1:4]
        pen = QPen(QColor(*color_array), self.bar_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        if self.indeterminate_ is True:
            start_angle = 360 * 16 * (self.indeterminate_value % 1)
            span_angle = 300 * 16
        else:
            start_angle = 360 * 16 * 0.25
            span_angle = -360 * 16 * (self.ani_value + 0.001) / 1.001  # 翻转方向，使进度顺时针方向旋转

        rect = self.rect()
        rect.adjust(*self.margins)

        painter.drawArc(rect, int(start_angle), int(span_angle))
