from PyQt5.QtGui import QDoubleValidator, QIntValidator

from siui.components.widgets.button import SiSimpleButton
from siui.components.widgets.line_edit import SiLineEdit
from siui.core import SiGlobal


class ABCSiSpinBox(SiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_step_ = 1
        self.value_ = 0
        self.minimum_ = 0
        self.maximum_ = 99

        self.button_plus = SiSimpleButton(self)
        self.button_plus.resize(24, 24)
        self.button_plus.attachment().setSvgSize(12, 12)
        self.button_plus.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_chevron_up_regular"))
        self.button_plus.setRepetitiveClicking(True)
        self.button_plus.clicked.connect(self.stepForth)

        self.button_minus = SiSimpleButton(self)
        self.button_minus.resize(24, 24)
        self.button_minus.attachment().setSvgSize(12, 12)
        self.button_minus.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_chevron_down_regular"))
        self.button_minus.setRepetitiveClicking(True)
        self.button_minus.clicked.connect(self.stepBack)

        self.container().setSpacing(0)
        self.container().addPlaceholder(8, "right")
        self.container().addWidget(self.button_plus, "right")
        self.container().addPlaceholder(4, "right")
        self.container().addWidget(self.button_minus, "right")

    def singleStep(self):
        return self.single_step_

    def setSingleStep(self, step):
        self.single_step_ = step

    def minimum(self):
        return self.minimum_

    def setMinimum(self, minimum):
        self.minimum_ = minimum

    def maximum(self):
        return self.maximum_

    def setMaximum(self, maximum):
        self.maximum_ = maximum

    def value(self):
        return self.value_

    def setValue(self, value):
        self.value_ = min(self.maximum_, max(value, self.minimum_))

    def stepForth(self):
        self.setValue(self.value() + self.singleStep())

    def stepBack(self):
        self.setValue(self.value() - self.singleStep())

    def stepBy(self, step):
        self.setValue(self.value() + step)


class SiIntSpinBox(ABCSiSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lineEdit().setValidator(QIntValidator())
        self.lineEdit().setText(str(self.value()))
        self.lineEdit().editingFinished.connect(self.on_editing_finished)

    def on_editing_finished(self):
        value = int(self.lineEdit().text())
        self.setValue(value)
        if value < self.minimum() or value > self.maximum():
            try:
                SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
                    title="输入值超出范围",
                    text=f"限制输入值为介于 {self.minimum()} 到 {self.maximum()} 的整数\n"
                         "已修改为最接近的值",
                    msg_type=3,
                    icon=SiGlobal.siui.iconpack.get("ic_fluent_warning_regular"),
                    fold_after=2500,
                )
            except ValueError:
                pass

    def setValue(self, value):
        super().setValue(value)
        self.lineEdit().setText(str(self.value()))


class SiDoubleSpinBox(ABCSiSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSingleStep(0.1)

        self.lineEdit().setValidator(QDoubleValidator())
        self.lineEdit().setText(str(self.value()))
        self.lineEdit().editingFinished.connect(self.on_editing_finished)

    def on_editing_finished(self):
        value = float(self.lineEdit().text())
        self.setValue(value)
        if value < self.minimum() or value > self.maximum():
            try:
                SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
                    title="输入值超出范围",
                    text=f"限制输入值为介于 {self.minimum()} 到 {self.maximum()} 的浮点数\n"
                         "已修改为最接近的值",
                    msg_type=3,
                    icon=SiGlobal.siui.iconpack.get("ic_fluent_warning_regular"),
                    fold_after=2500,
                )
            except ValueError:
                pass

    def setValue(self, value):
        # 重写以解决浮点数有效位溢出问题
        self.value_ = round(min(self.maximum_, max(value, self.minimum_)), 13)  # 舍掉一些精度以追求计算准确
        self.lineEdit().setText(str(self.value()))
