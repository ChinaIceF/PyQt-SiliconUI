from PyQt5.QtCore import Qt, pyqtSignal

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core import SiColor


class SiLabelHasClickedSignal(SiLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            event.accept()


class SiLayer(SiWidget):
    closed = pyqtSignal()
    showed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.close_on_dim_clicked = True

        self.dim_ = SiLabelHasClickedSignal(self)
        self.dim_.setColor(SiColor.trans(self.getColor(SiColor.LAYER_DIM), 0.0))
        self.dim_.clicked.connect(self.on_dim_layer_clicked)

    def setCloseOnDimClicked(self, on):
        self.close_on_dim_clicked = on

    def on_dim_layer_clicked(self):
        if self.close_on_dim_clicked is True:
            self.closeLayer()

    def closeLayer(self):
        self.closed.emit()
        self.hideDimMask()

    def showLayer(self):
        self.showed.emit()
        self.show()
        self.showDimMask()

    def showDimMask(self, ani=True):
        if ani is True:
            self.dim_.setColorTo(SiColor.trans(self.getColor(SiColor.LAYER_DIM), 1.0))
        else:
            self.dim_.setColor(SiColor.trans(self.getColor(SiColor.LAYER_DIM), 1.0))

    def hideDimMask(self, ani=True):
        if ani is True:
            self.dim_.setColorTo(SiColor.trans(self.getColor(SiColor.LAYER_DIM), 0.0))
        else:
            self.dim_.setColor(SiColor.trans(self.getColor(SiColor.LAYER_DIM), 0.0))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dim_.resize(event.size())
