from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from siui.components import SiLabel, SiWidget, SiTitledWidgetGroup
from siui.components.page import SiPage
from siui.templates.application.components.layer.layer import SiLayer


class Drawer(SiWidget):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        for child in self.children():
            if isinstance(child, QWidget):
                child.resize(event.size())


class SiLayerDrawer(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_opened = False

        self.drawer = Drawer(self)
        self.drawer_panel = SiLabel(self.drawer)
        self.drawer_page = SiPage(self.drawer)

        self.setDrawerWidth(400)
        self.closeLayer()

    def isOpened(self):
        return self.is_opened

    def setOpened(self, state):
        self.is_opened = state

    def setDrawerWidth(self, width):
        self.drawer.resize(width, self.drawer.height())

    def showLayer(self):
        super().showLayer()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setOpened(True)

    def closeLayer(self):
        super().closeLayer()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setOpened(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.drawer.resize(self.drawer.width(), event.size().height())
