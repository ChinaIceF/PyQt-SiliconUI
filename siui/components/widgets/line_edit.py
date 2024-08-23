from PyQt5.QtCore import Qt

from siui.components.widgets.abstracts import ABCSiLineEdit, SiSimpleLineEdit
from siui.components.widgets.button import SiSimpleButton
from siui.core.globals import SiGlobal


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
