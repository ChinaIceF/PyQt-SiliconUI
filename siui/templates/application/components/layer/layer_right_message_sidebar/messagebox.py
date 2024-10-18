from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from siui.components.widgets.label import SiLabel, SiSvgLabel
from siui.components.widgets.button import SiSimpleButton
from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.container import SiDenseVContainer
from siui.core import SiColor
from siui.core import SiGlobal
from siui.core import Si


class SiSideMessageContent(SiWidget):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_wing_width = 32
        self.msg_type = 0
        self.msg_color_tokens = [
            SiColor.SIDE_MSG_THEME_NORMAL,
            SiColor.SIDE_MSG_THEME_SUCCESS,
            SiColor.SIDE_MSG_THEME_INFO,
            SiColor.SIDE_MSG_THEME_WARNING,
            SiColor.SIDE_MSG_THEME_ERROR
        ]

        self.background = SiLabel(self)
        self.background.setFixedStyleSheet("border-radius: 6px; border-top-right-radius: 8px")

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet("border-radius: 6px; border-top-left-radius: 2px")

        self.theme_icon = SiSvgLabel(self)
        self.theme_icon.resize(32, 32)
        self.theme_icon.setSvgSize(20, 20)
        self.theme_icon.load(SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))

        self.container_ = SiDenseVContainer(self)
        self.container_.setAdjustWidgetsSize(True)
        self.container_.setMinimumHeight(64)

        self.close_button = SiSimpleButton(self)
        self.close_button.setBorderRadius(6)
        self.close_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_checkmark_regular"))
        self.close_button.clicked.connect(self.parent().closeLater)

        self.flash_layer = SiLabel(self)
        self.flash_layer.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.flash_layer.setFixedStyleSheet("border-radius: 6px")
        self.flash_layer.setColor(SiColor.trans(self.getColor(SiColor.SIDE_MSG_FLASH), 0))
        self.flash_layer.animationGroup().fromToken("color").setFactor(1/8)
        self.flash_layer.animationGroup().fromToken("color").setBias(0.001)

        self.reloadStyleSheet()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.background.setColor(self.getColor(SiColor.SIDE_MSG_THEME_WARNING))
        self.panel.setColor(self.getColor(SiColor.INTERFACE_BG_C))
        self.close_button.reloadStyleSheet()

    def setMessageType(self, index):
        self.msg_type = index
        self.background.setColor(self.getColor(self.msg_color_tokens[self.msg_type]))

    def container(self):
        return self.container_

    def themeIcon(self):
        return self.theme_icon

    def flash(self):
        self.flash_layer.setColor(self.getColor(SiColor.SIDE_MSG_FLASH))
        self.flash_layer.setColorTo(SiColor.trans(self.getColor(SiColor.SIDE_MSG_FLASH), 0))

    def adjustSize(self):
        self.container_.adjustSize()
        self.resize(self.container_.width() + self.theme_wing_width + 32, self.container_.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(event.size().width(), event.size().height())
        self.flash_layer.resize(event.size())

        self.panel.setGeometry(self.theme_wing_width,
                               0,
                               event.size().width() - self.theme_wing_width,
                               event.size().height() - 1)

        self.theme_icon.move(0, (event.size().height() - self.theme_icon.height()) // 2)

        self.container_.setGeometry(self.theme_wing_width,
                                    0,
                                    event.size().width() - self.theme_wing_width - 32,
                                    event.size().height() - 1)

        self.close_button.setGeometry(self.width() - self.theme_wing_width - 2,
                                      2,
                                      32,
                                      self.height() - 4)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.flash_layer.setColorTo(SiColor.trans(self.getColor(SiColor.SIDE_MSG_FLASH), 0.07))
        self.parent().fold_timer.stop()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.flash_layer.setColorTo(SiColor.trans(self.getColor(SiColor.SIDE_MSG_FLASH), 0))
        self.parent().fold_timer.start()

    def mouseReleaseEvent(self, a0):
        super().mouseReleaseEvent(a0)
        self.clicked.emit()

    def closeEvent(self, a0):
        super().closeEvent(a0)


class SiSideMessageBox(SiWidget):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_ = SiSideMessageContent(self)
        self.content_.clicked.connect(self.clicked.emit)
        self.content_.show()

        self.fold_timer = QTimer(self)
        self.fold_timer.setSingleShot(True)
        self.fold_timer.setInterval(1000)

    def startShowTimer(self):
        self.show_timer.start()

    def show(self):
        super().show()
        self.fold_timer.start()
        self.showContent()

    def content(self):
        return self.content_

    def showContent(self):
        self.content_.flash()

    def setMessageType(self, index):
        self.content_.setMessageType(index)

    def setFoldAfter(self, msec):
        self.fold_timer.setInterval(msec)
        self.fold_timer.timeout.connect(self.closeLater)

    def closeLater(self):
        self.lower()
        self.setSiliconWidgetFlag(Si.HasMoveLimits, False)
        self.moveTo(self.width() + self.x() + 24, self.y())
        self.parent().removeWidget(self, delete_later=False)
        self.parent().arrangeWidgets(adjust_size=False)
        delete_timer = QTimer(self)
        delete_timer.setSingleShot(True)
        delete_timer.timeout.connect(self.deleteLater)
        delete_timer.timeout.connect(self.parent().adjustSize)
        delete_timer.setInterval(1000)
        delete_timer.start()

    def adjustSize(self):
        self.content_.adjustSize()
        self.resize(self.content_.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.content_.resize(event.size().width(), event.size().height())
