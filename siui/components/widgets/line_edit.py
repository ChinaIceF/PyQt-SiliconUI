from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from siui.components.widgets import SiLabel, SiWidget
from siui.components.widgets.abstracts import ABCSiLineEdit, SiSimpleLineEdit
from siui.components.widgets.button import SiSimpleButton
from siui.core import SiGlobal, SiColor, SiExpAnimation


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
        self.base_panel.setFixedStyleSheet("border-radius: 6px")
        self.base_panel.animation_color.setBias(1)
        self.base_panel.animation_color.setFactor(1/32)

        self.edit_panel = SiLabel(self)
        self.edit_panel.setFixedStyleSheet("border-radius: 6px")

        self.name_label = SiLabel(self)
        self.name_label.setContentsMargins(16, 0, 16, 0)
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.line_edit = SiSimpleLineEdit(self.edit_panel)
        self.line_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.line_edit.setTextMargins(16, 0, 16, 0)
        self.line_edit.textEdited.connect(self.flash_on_edited)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        c = self.getColor(SiColor.INTERFACE_BG_C)
        b = self.getColor(SiColor.INTERFACE_BG_B)
        a = self.getColor(SiColor.INTERFACE_BG_A)

        self.base_panel.setColor(SiColor.mix(c, b, 0.3))
        self.edit_panel.setColor(SiColor.mix(b, a, 0.5))
        self.name_label.setTextColor(self.getColor(SiColor.TEXT_D))

    def flash_on_edited(self):
        c = self.getColor(SiColor.INTERFACE_BG_C)
        b = self.getColor(SiColor.INTERFACE_BG_B)
        self.base_panel.setColor(self.getColor(SiColor.INTERFACE_BG_E))
        self.base_panel.setColorTo(SiColor.mix(c, b, 0.3))

    def setName(self, name: str):
        self.name_label.setText(name)

    def lineEdit(self):
        return self.line_edit

    def setNameSpacing(self, spacing):
        self.name_spacing = spacing
        self.resize(self.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.base_panel.resize(event.size())
        self.edit_panel.setGeometry(
            self.name_spacing, 0, event.size().width() - self.name_spacing, event.size().height())
        self.name_label.resize(self.name_spacing, event.size().height())
        self.line_edit.resize(self.edit_panel.size())
