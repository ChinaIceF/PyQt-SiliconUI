from typing import Union

from siui.components import SiLabel, SiMasonryContainer
from siui.core import GlobalFont, Si, SiColor, SiQuickEffect
from siui.gui import SiFont

from .messagebox import SiSideMessageBox


class MessageSidebar(SiMasonryContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumns(1)
        self.setColumnWidth(400)
        self.setSpacing(horizontal=None, vertical=16)

        self.debug_label = SiLabel(self)
        # self.debug_label.setColor("#20FF0000")

    def sendMessageBox(self, message_box):
        self.addWidget(message_box)
        message_box.setFixedWidth(self.width()-20)
        message_box.move(80, self.height() - message_box.height())
        message_box.show()

    def send(self,
             text: str,
             title: str = None,
             msg_type: int = 0,
             icon: Union[bytes, str] = None,
             slot=None,
             close_on_clicked=True,
             fold_after: int = None):
        """ Create a simple message box which only has a label and send it to sidebar """
        new_message_box = SiSideMessageBox(self)
        new_message_box.setMessageType(msg_type)
        new_message_box.setFixedWidth(self.width()-20)

        if slot is not None:
            new_message_box.clicked.connect(slot)

        if close_on_clicked is True:
            new_message_box.clicked.connect(new_message_box.closeLater)

        if title is None:
            label = SiLabel(self)
            label.setFixedWidth(380 - new_message_box.content().theme_wing_width - 32)
            label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            label.setWordWrap(True)
            label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
            label.setFixedStyleSheet(
                "padding-top: 16px;"
                "padding-bottom: 16px;"
                "padding-left: 12px;"
                "padding-right: 12px;"
                "color: {}".format(self.getColor(SiColor.TEXT_D))
            )
            label.setText(text)
            new_message_box.content().container().addWidget(label)
        else:
            new_message_box.content().container().setSpacing(0)
            title_label = SiLabel(self)
            title_label.setFixedWidth(380 - new_message_box.content().theme_wing_width - 32)
            title_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            title_label.setWordWrap(True)
            title_label.setFont(SiFont.tokenized(GlobalFont.S_BOLD))
            title_label.setFixedStyleSheet(
                "padding-top: 16px;"
                "padding-bottom: 1px;"
                "padding-left: 12px;"
                "padding-right: 12px;"
                "color: {}".format(self.getColor(SiColor.TEXT_B))
            )
            title_label.setText(title)

            description_label = SiLabel(self)
            description_label.setFixedWidth(380 - new_message_box.content().theme_wing_width - 32)
            description_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            description_label.setWordWrap(True)
            description_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
            description_label.setFixedStyleSheet(
                "padding-top: 1px;"
                "padding-bottom: 16px;"
                "padding-left: 12px;"
                "padding-right: 12px;"
                "color: {}".format(self.getColor(SiColor.TEXT_D))
            )
            description_label.setText(text)

            new_message_box.content().container().addWidget(title_label)
            new_message_box.content().container().addWidget(description_label)

        if fold_after is not None:
            new_message_box.setFoldAfter(fold_after)

        if icon is not None:
            new_message_box.content().themeIcon().load(icon)

        new_message_box.adjustSize()
        self.sendMessageBox(new_message_box)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.debug_label.resize(event.size())


class LayerRightMessageSidebar(MessageSidebar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        SiQuickEffect.applyDropShadowOn(self,
                                        color=(28, 25, 31, 200),
                                        blur_radius=64)