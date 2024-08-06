from PyQt5.QtCore import Qt, pyqtSignal

from siui.components import SiSimpleButton
from siui.components.widgets.label import SiLabel
from siui.components.widgets.abstracts.widget import SiWidget
from siui.core.color import SiColor


class SiLabelHasClickedSignal(SiLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            event.accept()


class SiLayer(SiWidget):
    closed = pyqtSignal()
    closedToUpper = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.close_upper_layer_on_dim_clicked = True

        self.dim_ = SiLabelHasClickedSignal(self)
        self.dim_.setColor(self.colorGroup().fromToken(SiColor.LAYER_DIM))
        self.dim_.setOpacity(0)
        self.dim_.clicked.connect(self.on_dim_layer_clicked)

    def setCloseUpperLayerOnDimClicked(self, on):
        self.close_upper_layer_on_dim_clicked = on

    def on_dim_layer_clicked(self):
        if self.close_upper_layer_on_dim_clicked is True:
            self.hideDimMask()
        self.closedToUpper.emit(self.close_upper_layer_on_dim_clicked)

    def closeLayer(self):
        self.closed.emit()
        self.closedToUpper.emit(self.close_upper_layer_on_dim_clicked)

    def showDimMask(self, ani=True):
        if ani is True:
            self.dim_.setOpacityTo(1)
        else:
            self.dim_.setOpacity(1)

    def hideDimMask(self, ani=True):
        if ani is True:
            self.dim_.setOpacityTo(0)
        else:
            self.dim_.setOpacity(0)