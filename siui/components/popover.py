from __future__ import annotations

from PyQt5.QtCore import QEvent, QObject, QSize, Qt
from PyQt5.QtWidgets import QButtonGroup, QLabel, QMenu, QStackedWidget, QWidget

from siui.components.button import SiFlatButton, SiFlatButtonWithIndicator
from siui.components.container import SiDenseContainer
from siui.components.graphic import SiGraphicWrapperWidget
from siui.components.slider_ import SiWheelPickerHorizontal, SiWheelPickerVertical
from siui.core import SiQuickEffect
from siui.core.globals import SiGlobal
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiPopover(QMenu):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._padding = 32

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # *

        # 2025.5.3  * 如果使用 Qt.Popup, QGraphicProxyWidget 中的控件不能接收到 WheelEvent,
        #             因此通过重写 event 方法来实现类似 Popup 的行为

        self._shadow_frame = QWidget(self)

        self._wrapper = SiGraphicWrapperWidget(self)
        self._wrapper.setAttribute(Qt.WA_TranslucentBackground)

        self._initStyle()
        SiQuickEffect.applyDropShadowOn(self._shadow_frame, (0, 0, 0, 180), blur_radius=32)

    def _initStyle(self) -> None:
        self.setStyleSheet("background: transparent;")
        self._shadow_frame.setStyleSheet("background-color: #C88CD4; border-radius: 6px")

    def wrapper(self) -> SiGraphicWrapperWidget:
        return self._wrapper

    def resizeEvent(self, a0):
        p = self._padding
        self._shadow_frame.setGeometry(p+1, p+1, self.width()-2*p-2, self.height()-2*p-2)
        self._wrapper.setGeometry(p, p, self.width()-2*p, self.height()-2*p)

    def sizeHint(self):
        size = self._wrapper.widget().sizeHint()
        return QSize(size.width() + 2 * self._padding, size.height() + 2 * self._padding)

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().event(event)


class SiPopoverStackedWidget(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.TopToBottom)

        self._button_group = QButtonGroup(self)

        self._background = QWidget(self)
        self._btn_ctn_background = QWidget(self)

        self._button_container = SiDenseContainer(self, self.LeftToRight)
        self._stack_widget = QStackedWidget(self)

        self._no_button_label = QLabel(self)
        self._no_page_label = QLabel(self)
        self._close_button = SiFlatButton(self)

        self._button_container.addWidget(self._close_button, Qt.RightEdge)

        self.addWidget(self._button_container)
        self.addWidget(self._stack_widget)

        self._initStyle()

        self._close_button.clicked.connect(self.parent().close)

    def _initStyle(self) -> None:
        self.layout().setSpacing(0)

        self._no_button_label.setText("无页面")
        self._no_button_label.setStyleSheet("color: #918497")
        self._no_button_label.setFont(SiFont.getFont(size=14))
        self._no_button_label.setAlignment(Qt.AlignCenter)
        self._no_button_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self._no_page_label.setText("弹窗没有可供展示的页面")
        self._no_page_label.setStyleSheet("color: #D1CBD4")
        self._no_page_label.setFont(SiFont.getFont(size=14, weight=SiFont.Weight.Bold))
        self._no_page_label.setAlignment(Qt.AlignCenter)
        self._no_page_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self._button_container.setFixedHeight(64)
        self._button_container.setContentsMargins(10, 8, 16, 10)
        self._button_container.layout().setSpacing(8)

        self._stack_widget.setMinimumSize(320, 100)
        self._stack_widget.setContentsMargins(1, 0, 1, 1)

        self._close_button.setFixedSize(32, 32)
        self._close_button.setToolTip("关闭")
        self._close_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_dismiss_filled"))

        self.setStyleSheet("background-color: transparent")
        self._background.setStyleSheet("background-color: #332E38; border: 1px solid #3C3841; border-radius: 6px")
        self._btn_ctn_background.setStyleSheet("background-color: #25222A; border-radius: 5px; margin: 1px")

    def addPage(self, widget: SiGraphicWrapperWidget, name: str = "新页面") -> None:
        self._no_page_label.hide()
        self._no_button_label.hide()

        new_button = SiFlatButtonWithIndicator(self)
        new_button.setText(name)
        new_button.setFixedHeight(48)

        widget.resize(widget.widget().size())
        self._stack_widget.addWidget(widget)

        self._button_container.addWidget(new_button)
        self._button_group.addButton(new_button)

        if self._stack_widget.count() == 1:
            self._stack_widget.setCurrentIndex(0)
            new_button.click()

        new_button.clicked.connect(lambda: self._stack_widget.setCurrentWidget(widget))
        new_button.clicked.connect(widget.playMergeAnimations)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._background.resize(self.size())
        self._no_button_label.setGeometry(0, 0, self.width(), 64)
        self._no_page_label.setGeometry(0, 64, self.width(), self.height() - 64)
        self._btn_ctn_background.setGeometry(0, 0, self.width(), 64)


class SiPopoverDatePicker(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.LeftToRight)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent")

        self._year_picker = SiWheelPickerHorizontal(self)
        self._year_picker.spinBox().setAttribute(Qt.WA_TranslucentBackground)

        self.addWidget(self._year_picker)

        self._initStyle()

    def _initStyle(self) -> None:
        self._year_picker.setTitle("年")
        self._year_picker.spinBox().setMaximum(3000)
        self._year_picker.spinBox().setValue(2025)