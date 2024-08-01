from siui.components import SiLabel, SiSimpleButton
from siui.components.widgets.abstracts import SiWidget
from PyQt5.QtCore import Qt


class MessageLayer(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.central_msg_body = SiLabel(self)
        self.central_msg_body.resize(300, 160)
        self.central_msg_body.setFixedStyleSheet("border-radius: 16px")
        self.central_msg_body.setColor("#000000")
        self.central_msg_body.setOpacity(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.central_msg_body.move((event.size().width() - self.central_msg_body.width())//2,
                                   int((event.size().height() - self.central_msg_body.height())*(1-0.618)*2))