from siui.components import SiLongPressButton, SiPushButton, SiLabel
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application.components.dialog.modal import SiModalDialog


class ModalDialogExample(SiModalDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.icon().load(SiGlobal.siui.iconpack.get("ic_fluent_save_filled",
                                                    color_code=SiColor.mix(
                                                        self.colorGroup().fromToken(SiColor.SVG_NORMAL),
                                                        self.colorGroup().fromToken(SiColor.INTERFACE_BG_B),
                                                        0.05))
                         )

        label = SiLabel(self)
        label.setStyleSheet(f"color: {self.colorGroup().fromToken(SiColor.TEXT_E)}")
        label.setText(
            f'<span style="color: {self.colorGroup().fromToken(SiColor.TEXT_B)}">是否保存刚刚编辑的文件？</span><br>'
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
        button1.colorGroup().assign(SiColor.BUTTON_PANEL, self.colorGroup().fromToken(SiColor.INTERFACE_BG_D))
        button1.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        button2 = SiPushButton(self)
        button2.setFixedHeight(32)
        button2.attachment().setText("保存并退出")
        button2.colorGroup().assign(SiColor.BUTTON_PANEL, self.colorGroup().fromToken(SiColor.INTERFACE_BG_D))
        button2.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        button3 = SiLongPressButton(self)
        button3.setFixedHeight(32)
        button3.attachment().setText("丢弃一切创作成果并退出")
        button3.longPressed.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        self.buttonContainer().addWidget(button1)
        self.buttonContainer().addWidget(button2)
        self.buttonContainer().addWidget(button3)

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.adjustSize()
