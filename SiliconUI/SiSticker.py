
from PyQt5.QtCore import Qt

from .SiFont import *
from .SiButton import *
from .SiLayout import SiLayoutH, SiLayoutV
from .SiGlobal import *

class SiSticker(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.setStyleSheet('')

        self.substrate = QLabel(self)
        self.substrate.setStyleSheet('''
            background-color: {};
            border-radius:6px '''.format(colorset.BG_GRAD_HEX[0]))

        self.bgimage = QLabel(self)
        self.bgimage.setStyleSheet('''
            background-color: {};
            border-radius:6px '''.format(colorset.BG_GRAD_HEX[2]))

        self.surface = QLabel(self)
        self.surface.setStyleSheet('''
            border-radius:6px;
            background-color:qlineargradient(x1:0, y1:0, x2:0, y2:0.6,
                                             stop:0 {}, stop:1 #00{});
            '''.format(colorset.BG_GRAD_HEX[2], colorset.BG_GRAD_HEX[2][1:]))

        self.head = SiLayoutH(self)  # 头

        self.title = QLabel(self)
        self.title.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[0]))
        self.title.setFont(font_L2_bold)
        self.title.setAlignment(Qt.AlignVCenter)

        self.head.addItem(self.title, side = 'left')

        self.content = QLabel(self)
        self.content.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[0]))
        self.content.setFont(font_L1)
        self.content.setAlignment(Qt.AlignTop)
        self.content.setWordWrap(True)

        self.layout = SiLayoutV(self)
        self.layout.move(24, 64)

    def setInterval(self, interval):
        self.layout.setInterval(interval)

    def addItem(self, obj, *args, **kwargs):
        self.layout.addItem(obj, *args, **kwargs)
        self.adjustSize()

    def adjustSize(self):
        self.layout.adjustSize()
        h = self.layout.height() + 64 + 32
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
        self.content.setGeometry(24, 16 + 32 + 16, w - 48, h - 64 - 32)
        self.layout.resize(w - 48, self.layout.height())


class SiStickerWithTitleButton(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.title_button = SiButtonFlat(self)
        self.title_button.resize(32, 32)

        self.head.addItem(self.title_button, side = 'right')

class SiStickerWithBottomButton(SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.bottom_button = SiButtonFlat(self)
        self.bottom_button.resize(32, 32)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.bottom_button.move((w-32)//2, h - 32 - 16)
