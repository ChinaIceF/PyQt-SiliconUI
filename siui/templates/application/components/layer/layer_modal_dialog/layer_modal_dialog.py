from PyQt5.QtCore import Qt

from siui.components import SiWidget
from siui.core import Si

from ..layer import SiLayer


class LayerModalDialog(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dialog_ = None
        self.dialog_frame = SiWidget(self)
        self.dialog_frame.hideCenterWidgetFadeOut()
        self.dialog_frame.animationGroup().fromToken("showing").setBias(0.08)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def dialog(self):
        return self.dialog_

    def setDialog(self, dialog):
        if self.dialog() is not None:
            return

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
        self.dialog_frame.setSiliconWidgetFlag(Si.DeleteCenterWidgetOnCenterWidgetHidden, False)
        self.dialog_frame.showCenterWidgetFadeIn()

    def closeDialog(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.dialog_frame.hideCenterWidgetFadeOut()
        self.dialog_frame.setSiliconWidgetFlag(Si.DeleteCenterWidgetOnCenterWidgetHidden)
        self.dialog_ = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dialog_frame.resize(event.size())
