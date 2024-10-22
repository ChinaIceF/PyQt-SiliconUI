from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QAbstractSlider

from siui.components.widgets import SiDraggableLabel, SiLabel
from siui.core import Si, SiColor, SiGlobal
from siui.gui import SiColorGroup


class SiSliderH(QAbstractSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 颜色组
        self.color_group = SiColorGroup(reference=SiGlobal.siui.colors)

        # 设定值对应的颜色
        self.color_low = self.color_group.fromToken(SiColor.THEME_TRANSITION_A)
        self.color_high = self.color_group.fromToken(SiColor.THEME_TRANSITION_B)

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
        self.handle.setTrack(False)  # 取消自动跟踪鼠标，为了实现换挡动画0
        self.handle.setFixedStyleSheet("border-radius: 4px")
        self.handle.dragged.connect(self._dragged_handler)
        self.handle.moved.connect(self._moved_handler)
        self.handle.setHint(str(self.value()))

        self.setMaximum(100)
        self.setMinimum(-100)

    def getHintFromValue(self, value):
        return str(value)

    def setValueColor(self, low, high):
        self.color_low = low
        self.color_high = high
        self.reloadStyleSheet()

    def reloadStyleSheet(self):
        # 滑条着色
        self._moved_handler(None)
        # 滑轨着色
        self.track.setStyleSheet(
            f"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.color_low}, stop:1 {self.color_high});"  # noqa: E501
        )
        # 滑轨遮罩
        self.mask.setStyleSheet(f"background-color: {self.color_group.fromToken(SiColor.INTERFACE_BG_B)}")

    def setValue(self,
                 value: int,
                 move_to: bool = True):
        """
        设置滑块的值并移动滑块到指定位置
        :param value: 值
        :param move_to: Use moving animation
        """
        super().setValue(value)
        self.handle.setHint(self.getHintFromValue(self.value()))
        self._move_handle_according_to_value(move_to=move_to)

    def mousePressEvent(self, event):
        """
        处理滑条的鼠标按下事件。

        当鼠标按钮被按下时触发此方法。如果点击的是左键，
        它会获取鼠标相对于滑块的位置，并计算出对应的
        滑块值。然后更新滑块的值以反映该位置。
        """
        if event.button() == Qt.LeftButton:
            # 获取鼠标在 slider 上的位置
            mouse_pos = event.pos()
            # 根据鼠标位置计算对应的 value
            value = self._slider_position_from_mouse(mouse_pos)
            self.setValue(value)
            self.handle.enterEvent(event)  # 显示工具提示
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        处理滑条的鼠标移动事件。

        当鼠标左键按下并移动时触发此方法。它会检测鼠标在滑块上的移动，
        并根据当前鼠标的位置计算滑块的值。然后更新滑块的值以反映该位置，
        使滑块在拖动时能够实时调整。
        """
        if event.buttons() & Qt.LeftButton:  # 检查鼠标左键是否按下
            # 获取鼠标在 slider 上的位置
            mouse_pos = event.pos()
            # 根据鼠标位置计算对应的 value
            value = self._slider_position_from_mouse(mouse_pos)
            self.setValue(value)
        super().mouseMoveEvent(event)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.handle.leaveEvent(a0)  # 保证工具提示消失

    def _slider_position_from_mouse(self, mouse_pos: QPoint) -> int:
        """
        根据鼠标位置计算滑块的值。

        此方法将鼠标位置转换为滑块值，
        通过确定鼠标在滑块长度内的相对位置。
        它确保计算出的值保持在滑块的最小值和最大值之间。

        参数:
            mouse_pos (QPoint): 鼠标相对于滑块的当前位置。

        返回:
            int: 计算出的滑块值，范围在最小值和最大值之间。
        """
        # 将鼠标位置转换为 slider 的 value
        length = self.width() - self.handle.width()
        position = mouse_pos.x() - self.handle.width() // 2
        value = int(position / length * (self.maximum() - self.minimum())) + self.minimum()

        return max(self.minimum(), min(value, self.maximum()))

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
        # 刷新滑块位置，防止因初始化时长度未设置成功而导致设置的位置与实际位置不同
        self._move_handle_according_to_value(move_to=False)

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
