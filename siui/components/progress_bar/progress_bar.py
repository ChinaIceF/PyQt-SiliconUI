from PyQt5.QtCore import pyqtSignal

from siui.core.color import Color
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
        self.state_ = "loading"
        self.state_colors = {
            "loading": SiGlobal.siui.colors["PROGRESSBAR_LOADING"],
            "processing": SiGlobal.siui.colors["PROGRESSBAR_PROCESSING"],
            "paused": SiGlobal.siui.colors["PROGRESSBAR_PAUSED"],
        }

        # 已完成的百分比值
        self.value_ = 0

        # 进度条框架
        self.frame = SiLabel(self)
        self.frame.setFixedHeight(6)

        # 进度条轨道
        self.track = SiLabel(self.frame)
        self.track.setFixedStyleSheet("border-radius: 3px")

        # 进度条已完成部分
        self.progress = SiLabel(self.frame)
        self.progress.setFixedHeight(6)
        self.progress.setFixedStyleSheet("border-radius: 3px")

        # 闪烁层
        self.flash = SiLabel(self.frame)
        self.flash.setFixedHeight(6)
        self.flash.getAnimationGroup().fromToken("color").setFactor(1/32)
        self.flash.setFixedStyleSheet("border-radius: 3px")

    def setState(self, state: str):
        """
        设置进度条状态
        :param state: loading（加载）, processing（处理）, paused（暂停）
        """
        if state not in ["loading", "processing", "paused"]:
            raise KeyError(f"Invalid state: {state}")

        self.state_ = state
        self.reloadStyleSheet()

        if state in ["loading", "processing"]:
            self.flash_timer.start()
        else:
            self.flash_timer.stop()

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
        self.setHint(f"{round(self.value()*100, 2)}<span style='color: {SiGlobal.siui.colors['TEXT_C']}'>%</span>")

    def _flash(self):
        """
        触发进度闪烁
        """
        self.flash.setColor(Color.transparency(SiGlobal.siui.colors["PROGRESSBAR_FLASHES"], 0.8))
        self.flash.setColorTo(Color.transparency(SiGlobal.siui.colors["PROGRESSBAR_FLASHES"], 0.0))

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

        self.track.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_B"]))
        self.progress.setColorTo(self.state_colors[self.state()])  # noqa: UP032

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.frame.setGeometry(0, (h - self.frame.height()) // 2, w, self.frame.height())
        self.track.resize(w, self.frame.height())

        # 重设大小之后，进度按比例缩放
        self._resize_progress_according_to_value()
