from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

from . import SiFont
from . import SiStyle
from . import SiGlobal


class SiLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.hint = ''
        self.setFont(SiFont.font_L1)
        self.setStyleSheet('color:#ffffff')

    def setHint(self, hint):
        self.hint = hint

    def setText(self, text):
        super().setText(text)
        self.adjustSize()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.show_animation()
            SiGlobal.floating_window.setText(self.hint)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.hide_animation()


class SiPixLabel(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.radius = 32
        self.path = None

    def setRadius(self, r):
        self.radius = r

    def load(self, path):
        self.path = path
        self.draw()

    def draw(self):
        if self.path is None:
            return

        w, h = self.width(), self.height()
        self.setMaximumSize(w, h)
        self.setMinimumSize(w, h)

        self.target = QPixmap(self.size())
        self.target.fill(Qt.transparent)

        p = QPixmap(self.path).scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
