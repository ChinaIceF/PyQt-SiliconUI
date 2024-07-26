from PyQt5.QtCore import pyqtSignal

from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.components.widgets import SiLabel


class SiProgressBar(SiLabel):
    """
    进度条
    """
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
        self.flash.getAnimationGroup().fromToken("color").setFactor(1/32)

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
        self.setHint(f"{round(self.value()*100, 2)}<span style='color: {self.colorGroup().fromToken(SiColor.TEXT_C)}'>%</span>")  # noqa: E501

    def _flash(self):
        """
        触发进度闪烁
        """
        self.flash.setColor(SiColor.trans(self.colorGroup().fromToken(SiColor.PROGRESS_BAR_FLASHES), 0.8))
        self.flash.setColorTo(SiColor.trans(self.colorGroup().fromToken(SiColor.PROGRESS_BAR_FLASHES), 0.0))

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

        self.track.setStyleSheet(f"background-color: {self.colorGroup().fromToken(SiColor.PROGRESS_BAR_TRACK)}")
        self.progress.setColorTo(self.colorGroup().fromToken(self.state_colors[self.state()]))  # noqa: UP032

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.frame.setGeometry(0, (h - self.frame.height()) // 2, w, self.frame.height())
        self.track.resize(w, self.frame.height())

        # 重设大小之后，进度按比例缩放
        self._resize_progress_according_to_value()
