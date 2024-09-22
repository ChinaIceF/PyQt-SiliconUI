import os

from PyQt5.QtCore import Qt

from siui.components import SiOptionCardPlane
from siui.components.widgets import SiLabel, SiSimpleButton
from siui.core import SiGlobal
from siui.core import Si


class OptionCardPlaneForWidgetDemos(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source_code_url = None

        self.additional_description = SiLabel(self)
        self.additional_description.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.additional_description.setFixedHeight(24)
        self.additional_description.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.button_bug = SiSimpleButton(self)
        self.button_bug.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_bug_regular"))
        self.button_bug.resize(32, 32)
        self.button_bug.setHint("报告问题")
        self.button_bug.clicked.connect(
            lambda: os.system("start https://github.com/ChinaIceF/PyQt-SiliconUI/issues/new"))

        self.button_source_code = SiSimpleButton(self)
        self.button_source_code.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
        self.button_source_code.resize(32, 32)
        self.button_source_code.setHint("查看源代码")
        self.button_source_code.clicked.connect(self.openSourceCode)

        self.header().addWidget(self.additional_description, "left")
        self.header().addWidget(self.button_source_code, "right")
        self.header().addWidget(self.button_bug, "right")

        self.body().setSpacing(16)

    def setSourceCodeURL(self, url):
        self.source_code_url = url

    def openSourceCode(self):
        if self.source_code_url is None:
            raise ValueError("未指定源代码 URL")
        os.system(f"start {self.source_code_url}")

    def setAdditionalDescription(self, text: str):
        self.additional_description.setText(text)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.additional_description.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_C"]))
