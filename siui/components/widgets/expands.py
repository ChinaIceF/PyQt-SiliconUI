from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from siui.components import SiDenseHContainer, SiIconLabel, SiLabel, SiSvgLabel, SiWidget
from siui.core import SiColor, SiExpAccelerateAnimation, SiGlobal


class SiHExpandWidget(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attachment_ = SiWidget(self)

        self.expand_animation = SiExpAccelerateAnimation(self)
        self.expand_animation.setAccelerateFunction(lambda x: (x / 10) ** 3)
        self.expand_animation.setFactor(1/4)
        self.expand_animation.setBias(0.01)
        self.expand_animation.setCurrent(1)
        self.expand_animation.setTarget(1)
        self.expand_animation.ticked.connect(self.on_ani_ticked)

        self.animationGroup().addMember(self.expand_animation, "expand")

    def attachment(self):
        return self.attachment_

    def setAttachment(self, att: QWidget):
        self.attachment_.deleteLater()
        self.attachment_ = att
        att.setParent(self)

    def expand(self, percent):
        self.expand_animation.stop()
        self.expand_animation.setTarget(percent)
        self.expand_animation.setCurrent(percent)

    def expandTo(self, percent):
        self.expand_animation.setTarget(percent)
        self.expand_animation.try_to_start()

    def on_ani_ticked(self, value):
        value = float(value)  # 绑定控件半边的长度占整个控件半侧的百分比
        one_side_width = int(self.width() / 2 * value)
        x = self.width() // 2 - one_side_width
        width = one_side_width * 2
        self.attachment_.setGeometry(x, 0, width, self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.on_ani_ticked(self.expand_animation.current())  # 强制刷新绑定控件大小


class SiVExpandWidget(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attachment_ = SiWidget(self)

        self.expand_animation = SiExpAccelerateAnimation(self)
        self.expand_animation.setAccelerateFunction(lambda x: (x / 10) ** 3)
        self.expand_animation.setFactor(1/4)
        self.expand_animation.setBias(0.01)
        self.expand_animation.setCurrent(1)
        self.expand_animation.setTarget(1)
        self.expand_animation.ticked.connect(self.on_ani_ticked)

        self.animationGroup().addMember(self.expand_animation, "expand")

    def attachment(self):
        return self.attachment_

    def setAttachment(self, att: QWidget):
        self.attachment_.deleteLater()
        self.attachment_ = att
        att.setParent(self)

    def expand(self, percent):
        self.expand_animation.stop()
        self.expand_animation.setTarget(percent)
        self.expand_animation.setCurrent(percent)

    def expandTo(self, percent):
        self.expand_animation.setTarget(percent)
        self.expand_animation.try_to_start()

    def on_ani_ticked(self, value):
        value = float(value)  # 绑定控件半边的长度占整个控件半侧的百分比
        one_side_height = int(self.height() / 2 * value)
        y = self.height() // 2 - one_side_height
        height = one_side_height * 2
        self.attachment_.setGeometry(0, y, self.width(), height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.on_ani_ticked(self.expand_animation.current())  # 强制刷新绑定控件大小


class SiHoverExpandWidget(SiVExpandWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.h_expand_widget = SiHExpandWidget(self)

        self.frame = SiLabel(self)
        self.frame.setFixedStyleSheet("border-radius: 4px")
        self.frame.setColor(SiColor.mix(self.getColor(SiColor.INTERFACE_BG_D), self.getColor(SiColor.SIDE_MSG_THEME_SUCCESS)))

        self.container = SiDenseHContainer(self.frame)
        self.container.setFixedHeight(32)

        self.icon = SiSvgLabel(self)
        self.icon.load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_sync_filled"))
        self.icon.resize(32, 32)

        self.label = SiLabel(self)
        self.label.setTextColor(self.getColor(SiColor.TEXT_B))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("重载成功")
        self.label.setFixedHeight(32)
        self.label.adjustSize()

        self.container.setSpacing(0)
        self.container.addWidget(self.icon)
        self.container.addWidget(self.label)

        self.frame.adjustSize()

        self.h_expand_widget.setAttachment(self.frame)
        self.setAttachment(self.h_expand_widget)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.expandTo(1)
        self.h_expand_widget.expandTo(1)
        # self.frame.setOpacityTo(1)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.expandTo(1)
        self.h_expand_widget.expandTo(32 / self.width())
        # self.frame.setOpacityTo(0.1)
