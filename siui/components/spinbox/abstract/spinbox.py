from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSpinBox

from siui.components import SiWidget


class ABCSiSpinBox(SiWidget):
    valueChanged = pyqtSignal(object)
    readOnlyStateChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value_ = 0
        self.single_step = 1
        self.maximum_ = 99
        self.minimum_ = 0
        self.is_read_only = False

    def value(self):
        return self.value_

    def setValue(self, value):
        value = min(self.maximum_, max(value, self.minimum_))
        self.value_ = value
        self.valueChanged.emit(value)

    def singleStep(self):
        return self.single_step

    def setSingleStep(self, single_step):
        self.single_step = single_step

    def maximum(self):
        return self.maximum_

    def setMaximum(self, maximum):
        self.maximum_ = maximum

    def minimum(self):
        return self.minimum_

    def setMinimum(self, minimum):
        self.minimum_ = minimum

    def setRange(self, minimum, maximum, single_step=1):
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setSingleStep(single_step)

    def stepUp(self):
        self.setValue(self.value() + self.singleStep())

    def stepDown(self):
        self.setValue(self.value() - self.singleStep())

    def isReadOnly(self):
        return self.is_read_only

    def setReadOnly(self, state):
        self.is_read_only = state
        self.readOnlyStateChanged.emit(state)
