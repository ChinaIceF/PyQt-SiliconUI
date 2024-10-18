from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.container import SiDenseHContainer
from siui.components.widgets.label import SiLabel
from siui.core import SiColor, GlobalFont
from siui.core import SiGlobal
from siui.gui import SiFont


class SiSimpleLineEdit(QLineEdit):
    onFocus = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置字体
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))

    def reloadStyleSheet(self):
        self.setStyleSheet(
            "QLineEdit {"
            "    selection-background-color: #493F4E;"
            "    background-color: transparent;"
            f"    color: {self.parent().getColor(SiColor.TEXT_C)};"
            "    border: 0px"
            "}"
        )

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.onFocus.emit(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.onFocus.emit(False)


class ABCSiLineEdit(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_focus_in = False
        self.padding_ = 0

        self.container_ = SiDenseHContainer(self)
        self.container_.setAlignment(Qt.AlignVCenter)

        self.outfit_label_top = SiLabel(self)
        self.outfit_label_top.lower()
        self.outfit_label_top.setFixedStyleSheet(
            "border-top-left-radius:     4px;"
            "border-top-right-radius:    4px;"
            "border-bottom-left-radius:  2px;"
            "border-bottom-right-radius: 2px;"
        )

        self.outfit_label_bottom = SiLabel(self)
        self.outfit_label_bottom.stackUnder(self.outfit_label_top)
        self.outfit_label_bottom.setFixedStyleSheet("border-radius: 4px")

    def container(self):
        return self.container_

    def setPadding(self, padding):
        self.padding_ = padding
        self.resize(self.size())

    def padding(self):
        return self.padding_

    def setFocusState(self, state):
        self.is_focus_in = state
        self.on_focus_changed(self.is_focus_in)

    def focusState(self):
        return self.is_focus_in

    def on_focus_changed(self, is_on):
        w, h = self.size().width(), self.size().height()
        if is_on:
            self.outfit_label_top.resize(w, h - 2)
        else:
            self.outfit_label_top.resize(w, h - 1)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.outfit_label_top.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_B)};"
            f"border-left:  1px solid {self.getColor(SiColor.INTERFACE_BG_D)};"
            f"border-right: 1px solid {self.getColor(SiColor.INTERFACE_BG_D)};"
            f"border-top:   1px solid {self.getColor(SiColor.INTERFACE_BG_D)};"
        )
        self.outfit_label_bottom.setStyleSheet(
            "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
            f"    stop:0 {self.getColor(SiColor.THEME_TRANSITION_A)},"
            f"    stop:1 {self.getColor(SiColor.THEME_TRANSITION_B)}"
            ")"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container_.resize(event.size())
        self.outfit_label_bottom.resize(event.size())
        self.outfit_label_top.setGeometry(
            self.padding_, 0, event.size().width() - 2 * self.padding_, event.size().height() - 1)
