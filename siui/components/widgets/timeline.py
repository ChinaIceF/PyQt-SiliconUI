from PyQt5.QtCore import Qt, QSize

from siui.components import SiLabel, SiMasonryContainer, SiSvgLabel, SiWidget
from siui.core import SiColor, SiGlobal
from siui.gui import SiFont


class SiTimeLineItem(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = SiSvgLabel(self)
        self.icon.setSvgSize(24, 24)
        self.icon.setFixedSize(32, 32)
        self.icon.move(16, 0)

        self.anchor = SiLabel(self)
        self.anchor.setFixedSize(24, 24)
        self.anchor.setFixedStyleSheet("border-radius: 12px")
        self.anchor.setStyleSheet(
            f"border: 4px solid {self.getColor(SiColor.INTERFACE_BG_C)};"
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_E)};"
        )
        self.anchor.move(64 + 4, 4)

        self.anchor_dot = SiLabel(self.anchor)
        self.anchor_dot.setFixedSize(8, 8)
        self.anchor_dot.setFixedStyleSheet("border-radius: 4px")
        self.anchor_dot.move(8, 8)
        self.anchor_dot.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_C)};"
        )

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=12))
        self.title.setTextColor(self.getColor(SiColor.TEXT_D))
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setContentsMargins(0, 8, 0, 2)
        self.title.move(112, 0)
        self.title.adjustSize()

        self.description = SiLabel(self)
        self.description.setTextColor(self.getColor(SiColor.TEXT_B))
        self.description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.description.move(112, self.title.height())
        self.description.adjustSize()

    def setContent(self, title, description):
        self.title.setText(title)
        self.title.adjustSize()
        self.description.setText(description)
        self.description.adjustSize()

    def setIconHint(self, text):
        self.icon.setHint(text)

    def setThemeColor(self, code, background_color=None):
        background_color = self.getColor(SiColor.INTERFACE_BG_C) if background_color is None else background_color
        self.anchor.setStyleSheet(
            f"border: 4px solid {background_color};"
            f"background-color: {code};"
        )
        self.anchor_dot.setStyleSheet(
            f"background-color: {background_color};"
        )

    def setIcon(self, path_or_data):
        self.icon.load(path_or_data)

    def sizeHint(self):
        return QSize(self.width(), max(self.title.height() + self.description.height(), 64))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.title.resize(event.size().width() - 112, self.title.height())
        self.description.resize(event.size().width() - 112, self.description.height())
        self.description.move(112, self.title.height())


class SiTimeLine(SiMasonryContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumns(1)
        self.setColumnWidth(500)

        self.track = SiLabel(self)
        self.track.setFixedStyleSheet("border-radius: 2px")
        self.track.setColor(self.getColor(SiColor.INTERFACE_BG_E))
        self.track.setFixedWidth(4)
        self.track.resize(4, 100)
        self.track.move(14 + 64, 0)

        self.setMinimumWidth(500)

    def addWidget(self, widget, arrange=True, ani=True):
        super().addWidget(widget, arrange, ani)
        widget.resize(self.width(), widget.sizeHint().height())

    def resizeEvent(self, event):
        super().resizeEvent(event)

        for item in self.widgets():
            item.resize(event.size().width(), item.height())

        self.track.resize(4, event.size().height())
