from siui.components import SiLabel, SiLongPressButton, SiPushButton
from siui.core import SiColor, SiGlobal
from siui.templates.application.components.dialog.modal import SiModalDialog


class ModalDialogExample(SiModalDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.icon().load(SiGlobal.siui.iconpack.get("ic_fluent_save_filled",
                                                    color_code=SiColor.mix(
                                                        self.getColor(SiColor.SVG_NORMAL),
                                                        self.getColor(SiColor.INTERFACE_BG_B),
                                                        0.05))
                         )

        label = SiLabel(self)
        label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_E)}")
        label.setText(
            f'<span style="color: {self.getColor(SiColor.TEXT_B)}">是否保存刚刚编辑的文件？</span><br>'
            "<br>"
            "- 田所浩二志.doc<br>"
            "- 八十天游览下北泽——从百草园到三味书屋.docx<br>"
            "- 小黑子是怎样练成的.pdf"
        )
        label.adjustSize()
        self.contentContainer().addWidget(label)

        button1 = SiPushButton(self)
        button1.setFixedHeight(32)
        button1.attachment().setText("继续编辑我的文档")
        button1.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
        button1.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        button2 = SiPushButton(self)
        button2.setFixedHeight(32)
        button2.attachment().setText("保存并退出")
        button2.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
        button2.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        self.button3 = SiLongPressButton(self)
        self.button3.setFixedHeight(32)
        self.button3.attachment().setText("丢弃一切创作成果并退出")
        self.button3.longPressed.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        self.buttonContainer().addWidget(button1)
        self.buttonContainer().addWidget(button2)
        self.buttonContainer().addWidget(self.button3)

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.adjustSize()

    def deleteLater(self):
        # print("你好")
        self.button3.hold_thread.safe_to_stop = True
        self.button3.hold_thread.wait()
        self.button3.deleteLater()
        SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        super().deleteLater()
