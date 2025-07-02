from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QWidget

from siui.components.tooltip import ToolTipWindow


class TooltipManager(QObject):
    def __init__(self, tooltip_window: ToolTipWindow):
        super().__init__()
        self._tooltip_window = tooltip_window
        self._entered = False

    def setToolTip(self, text: str, do_flash: bool = True) -> None:
        if self._tooltip_window is None:
            return
        if text == "":
            return
        self._tooltip_window.setText(text, flash=do_flash)
        self._tooltip_window.show_()

    def showToolTip(self, do_flash: bool = True) -> None:
        if self._tooltip_window is None:
            return
        self._tooltip_window.show_()
        if do_flash:
            self._tooltip_window.flash()

    def hideToolTip(self) -> None:
        if self._tooltip_window is None:
            return
        self._tooltip_window.hide_()

    def isEntered(self) -> bool:
        return self._entered

    def eventFilter(self, obj: QWidget, event):
        if event.type() == QEvent.Enter:
            text = obj.toolTip()
            self.setToolTip(text)
            self._entered = True

        elif event.type() == QEvent.Leave:
            self.hideToolTip()
            self._entered = False

        elif event.type() == QEvent.ToolTip:
            return True

        return False
