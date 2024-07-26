from PyQt5.QtWidgets import QAbstractSlider

from siui.components.widgets import SiDraggableLabel, SiLabel
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si


class SiSliderH(QAbstractSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设定值对应的颜色
        self.color_low = SiGlobal.siui.colors["THEME_TRANSITION_A"]
        self.color_high = SiGlobal.siui.colors["THEME_TRANSITION_B"]

        # 框架
        self.frame = SiLabel(self)
        self.frame.setFixedHeight(8)

        # 滑动轨道
        self.track = SiLabel(self.frame)
        self.track.setFixedHeight(4)
        self.track.setFixedStyleSheet("border-radius: 2px")

        # 遮罩
        self.mask = SiLabel(self.track)
        self.mask.setFixedHeight(4)
        self.mask.setFixedStyleSheet("border-radius: 2px")

        # 滑块
        self.handle = SiDraggableLabel(self.frame)
        self.handle.resize(32, 8)
        self.handle.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.handle.setTrack(False)  # 取消自动跟踪鼠标，为了实现换挡动画
        self.handle.setFixedStyleSheet("border-radius: 4px")
        self.handle.dragged.connect(self._dragged_handler)
        self.handle.moved.connect(self._moved_handler)
        self.handle.setHint(str(self.value()))

        self.setMaximum(100)
        self.setMinimum(-100)

    def reloadStyleSheet(self):
        # 滑条着色
        self._moved_handler(None)

        # 滑轨着色
        self.track.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {}, stop:1 {});
            """.format(self.color_low, self.color_high))  # noqa: UP032

        # 滑轨遮罩
        self.mask.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_B"]))

    def setValue(self,
                 value: int,
                 move_to: bool = True):
        """
        设置滑块的值并移动滑块到指定位置
        :param value: 值
        :param move_to: Use moving animation
        """
        super().setValue(value)
        self.handle.setHint(str(self.value()))
        self._move_handle_according_to_value(move_to=True)

    def _move_handle_according_to_value(self, move_to=False):
        """
        由自身的值，将滑块移动到正确的位置上
        """
        sections_amount = (self.maximum() - self.minimum()) / self.singleStep()
        section_length = self.track.width() / sections_amount
        current_section_index = self.value() - self.minimum()

        # 移动滑块到区域位置
        if move_to:
            self.handle.moveTo(int(current_section_index * section_length), 0)
        else:
            self.handle.move(int(current_section_index * section_length), 0)

    def _rate_from_handle_pos(self):
        """
        从滑块坐标得到已滑动长度与总长度的比率
        """
        return self.handle.x() / self.track.width()

    def _dragged_handler(self, pos):   # 当滑块 dragged 信号发射时，调用这个方法
        # 将整个滑条均分成 (最大值 - 最小值) / 步长 个区域，每个区域的长度是 总长度 / 区域数量，并计算当前的区域编号
        sections_amount = (self.maximum() - self.minimum()) / self.singleStep()
        section_length = self.track.width() / sections_amount
        current_section_index = int(pos[0] / section_length + 0.5)

        # 设置自身取值为区域编号 + 最小值
        self.setValue(self.minimum() + current_section_index)

    def _moved_handler(self, _):   # 当滑块 moved 信号发射时，调用这个方法
        self.handle.setColor(SiColor.mix(self.color_high, self.color_low, self._rate_from_handle_pos()))
        self.mask.setGeometry(self.handle.x(), 0, self.track.width() - self.handle.x(), self.mask.height())

    def showEvent(self, a0):
        super().showEvent(a0)
        self._move_handle_according_to_value(move_to=False)  # 刷新滑块位置，防止因初始化时长度未设置成功而导致设置的位置与实际位置不同  # noqa: E501

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.frame.setGeometry(0, (h - self.frame.height()) // 2,
                               w, self.frame.height())
        self.track.setGeometry(self.handle.width() // 2, (self.frame.height() - self.track.height()) // 2,
                               w - self.handle.width(), self.track.height())
        self.mask.resize(self.track.width(), self.track.height())
        self.handle.setMoveLimits(0, 0, w, self.frame.height())

        # 依照自己的 value, 保证滑块在正确的位置上
        self._move_handle_according_to_value()
