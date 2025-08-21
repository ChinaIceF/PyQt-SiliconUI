import time

from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QWidget

from siui.components.tooltip import ToolTipWindow
from siui.core import SiGlobal


class DebugEventFilter(QObject):
    """
    用于将某个对象的事件打印出来，可以设置屏蔽事件
    """
    EventNames = {value: name for name, value in QEvent.__dict__.items() if isinstance(value, QEvent.Type)}

    def __init__(self, parent=None):
        super().__init__(parent)

        self._ignorance = []
        self._name_getter = lambda: self.parent().objectName()

    def eventFilter(self, obj, event):
        etype = event.type()
        ename = self.EventNames.get(etype, f"Unknown({etype})")
        parent_type = type(self.parent())
        parent_name = self._name_getter()

        if etype not in self._ignorance:
            print(f"{time.asctime()} [{parent_type}] {parent_name} got event: {ename} ({etype})")

        return False

    def setIgnorance(self, ignorance: list) -> None:
        self._ignorance = ignorance

    def ignorance(self) -> list:
        return self._ignorance

    def setNameGetter(self, func) -> None:
        self._name_getter = func


class WidgetTooltipAcceptEventFilter(QObject):
    """
    阻断原版工具提示事件
    """
    def eventFilter(self, obj: QWidget, event):
        if event.type() == QEvent.ToolTip:
            return True

        return False


class WidgetToolTipRedirectEventFilter(QObject):
    """
    忽略原版工具提示，并把工具提示发送到自定义工具提示窗口上，提供操作工具提示窗口的接口
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._tooltip_window = self._initTooltipWindow()
        self._entered = False

    def _initTooltipWindow(self) -> ToolTipWindow:
        return SiGlobal.siui.windows.get("TOOL_TIP")

    def setTooltip(self, text: str, do_flash: bool = True) -> None:
        if self._tooltip_window is None:
            return
        if text == "":
            return
        self._tooltip_window.setText(text, flash=do_flash)
        self._tooltip_window.show_()

    def showTooltip(self, do_flash: bool = True) -> None:
        if self._tooltip_window is None:
            return
        self._tooltip_window.show_()
        if do_flash:
            self._tooltip_window.flash()

    def hideTooltip(self) -> None:
        if self._tooltip_window is None:
            return
        self._tooltip_window.hide_()

    def raiseWindow(self) -> None:
        if self._tooltip_window is None:
            return
        self._tooltip_window.raise_()

    def isEntered(self) -> bool:
        return self._entered

    def eventFilter(self, obj: QWidget, event):
        if event.type() == QEvent.Enter:
            text = obj.toolTip()
            self.setTooltip(text)
            self.raiseWindow()
            self._entered = True

        elif event.type() == QEvent.Leave:
            self.hideTooltip()
            self._entered = False

        elif event.type() == QEvent.ToolTip:
            return True

        return False


class ScaleOnPressEventFilter(QObject):
    """
    实现鼠标按下控件时产生缩放效果，需要父控件具有 `animation` 方法，且具有 `scaleFactor` 属性
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._max_scale_factor = 1.0
        self._min_scale_factor = 0.9

    def setMaxScaleFactor(self, value: float) -> None:
        self._max_scale_factor = value

    def setMinScaleFactor(self, value: float) -> None:
        self._min_scale_factor = value

    def maxScaleFactor(self) -> float:
        return self._max_scale_factor

    def minScaleFactor(self) -> float:
        return self._min_scale_factor

    def eventFilter(self, obj: QWidget, event):
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonDblClick:
            ani = self.parent().animation("scaleFactor")
            ani.setFactor(1/16)
            ani.setBias(0)
            ani.setEndValue(self._min_scale_factor)
            ani.start()

        elif event.type() == QEvent.MouseButtonRelease:
            ani = self.parent().animation("scaleFactor")
            ani.setFactor(1/4)
            ani.setBias(0.001)
            ani.setEndValue(self._max_scale_factor)
            ani.start()

        return False
