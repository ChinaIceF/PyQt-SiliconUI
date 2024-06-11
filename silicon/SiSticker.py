from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtSvg import QSvgWidget

from .SiFont import *
from .SiButton import *
from .SiLayout import SiLayoutH, SiLayoutV

class SiSticker(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.substrate = QLabel(self)
        self.substrate.setStyleSheet('background-color:#1C191F; border-radius:6px')

        self.bgimage = QLabel(self)
        self.bgimage.setStyleSheet('background-color:#2C2930; border-radius:6px')

        self.surface = QLabel(self)
        self.surface.setStyleSheet('background-color:qlineargradient(x1:0, y1:0, x2:0, y2:0.6, stop:0 #2C2930, stop:1 #002C2930); border-radius:6px')

        self.head = SiLayoutH(self)  # 头

        self.title = QLabel(self)
        self.title.setStyleSheet('color:#ffffff')
        self.title.setFont(font_L2_bold)
        self.title.setAlignment(Qt.AlignVCenter)

        self.head.addItem(self.title, side = 'left')

        self.content = QLabel(self)
        self.content.setStyleSheet('color:#ffffff')
        self.content.setFont(font_L1)
        self.content.setAlignment(Qt.AlignTop)
        self.content.setWordWrap(True)

        self.layout = SiLayoutV(self)
        self.layout.move(24, 64)

    def addItem(self, obj, **kwargs):
        self.layout.addItem(obj, **kwargs)
        self.adjustSize()

    def adjustSize(self):
        h = self.layout.height() + 64 + 16
        self.resize(self.width(), h)

    def setTitle(self, title):
        self.title.setText(title)
        self.title.adjustSize()

    def setContent(self, content):
        self.content.setText(content)

    def resizeEvent(self, event):
        size = event.size()
        w, h = size.width(), size.height()

        self.substrate.resize(w, h)
        self.bgimage.resize(w, h - 3)
        self.surface.resize(w, h - 3)
        self.head.setGeometry(24, 16, w - 48, 32)
        self.content.setGeometry(24, 16 + 32 + 16, w - 48, h - 64 - 16)
        self.layout.resize(w - 48, self.layout.height())


class SiStickerWithTitleButton(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)

        self.title_button = SiButtonFlat(self)
        self.title_button.resize(32, 32)

        self.head.addItem(self.title_button, side = 'right')

class SiStickerWithBottomButton(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)

        self.bottom_button = SiButtonFlat(self)
        self.bottom_button.resize(32, 32)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.bottom_button.move((w-32)//2, h - 32 - 16)
