from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

from siui.core.globals import SiGlobal


class ABCSiLineEdit(QLineEdit):
    """
    LineEdit 的抽象类，继承自 QLineEdit
    """
    onFocus = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置字体
        self.setFont(SiGlobal.siui.fonts["S_NORMAL"])

    def reloadStyleSheet(self):
        """
        重载样式表
        """
        self.setStyleSheet("""
            QLineEdit {
                selection-background-color: #493F4E;
                background-color: transparent;
                color: #ffffff;
                border: 0px
            }
            """
        )

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.onFocus.emit(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.onFocus.emit(False)
