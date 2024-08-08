from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication

from siui.components import SiWidget
from siui.core.silicon import Si
from ..layer import SiLayer


class LayerModalDialog(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dialog_ = None
        self.dialog_frame = SiWidget(self)
        self.dialog_frame.hideCenterWidgetFadeOut()
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def dialog(self):
        return self.dialog_

    def setDialog(self, dialog):
        self.dialog_ = dialog
        self.dialog_.show()
        self.dialog_frame.setCenterWidget(self.dialog_)
        self.showLayer()

    def showLayer(self):
        super().showLayer()
        self.showDialog()

    def closeLayer(self):
        super().closeLayer()
        self.closeDialog()

    def showDialog(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.dialog_frame.showCenterWidgetFadeIn()

    def closeDialog(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dialog_frame.hideCenterWidgetFadeOut()
        self.dialog_frame.delete_timer = QTimer()
        self.dialog_frame.delete_timer.singleShot(500, self.dialog_frame.centerWidget().deleteLater)
        self.dialog_ = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dialog_frame.resize(event.size())
