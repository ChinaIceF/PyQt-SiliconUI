from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from siui.components.widgets import SiLabel, SiWidget
from siui.components.widgets.abstracts import ABCSiLineEdit, SiSimpleLineEdit
from siui.components.widgets.button import SiSimpleButton
from siui.core import SiGlobal, SiColor


class SiLineEdit(ABCSiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.line_edit = SiSimpleLineEdit(self)
        self.line_edit.setTextMargins(12, 0, 12, 1)
        self.line_edit.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.line_edit.onFocus.connect(self.on_focus_changed)
        self.line_edit.returnPressed.connect(self.line_edit.clearFocus)  # 按下回车，移出焦点
        self.container().addWidget(self.line_edit)

    def adjustLineEditSize(self):
        preferred_width = self.container().width() - self.container().getUsedSpace("right")
        self.line_edit.resize(preferred_width, self.line_edit.height())

    def lineEdit(self):
        return self.line_edit

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustLineEditSize()


class SiLineEditWithDeletionButton(SiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deletion_button = SiSimpleButton(self)
        self.deletion_button.resize(24, 24)
        self.deletion_button.attachment().setSvgSize(16, 16)
        self.deletion_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_delete_regular"))
        self.deletion_button.clicked.connect(self.clear_text)
        self.container().setSpacing(0)
        self.container().addPlaceholder(8, "right")
        self.container().addWidget(self.deletion_button, "right")

    def clear_text(self):
        self.lineEdit().setText("")


class SiLineEditWithItemName(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name_spacing = 128

        self.base_panel = SiLabel(self)
        self.base_panel.setFixedStyleSheet("border-radius: 16px")

        self.edit_panel = SiLabel(self)
        self.edit_panel.setFixedStyleSheet("border-radius: 16px")

        self.name_label = SiLabel(self)
        self.name_label.setContentsMargins(16, 0, 16, 0)
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.line_edit = SiSimpleLineEdit(self.edit_panel)
        self.line_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.line_edit.setTextMargins(16, 0, 16, 0)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        c = self.colorGroup().fromToken(SiColor.INTERFACE_BG_C)
        b = self.colorGroup().fromToken(SiColor.INTERFACE_BG_B)
        self.base_panel.setColor(SiColor.mix(c, b, 0.5))
        self.edit_panel.setColor(b)
        self.name_label.setColor(self.colorGroup().fromToken(SiColor.TEXT_D))

    def lineEdit(self):
        return self.line_edit

    def setNameSpacing(self, spacing):
        self.name_spacing = spacing
        self.resize(self.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.base_panel.resize(event.size())
        self.edit_panel.setGeometry(self.name_spacing, 0, event.size().width() - self.name_spacing)
        self.name_label.resize(self.name_spacing, event.size().height())
        self.line_edit.resize(self.edit_panel.size())
