from PyQt5.QtWidgets import QWidget

from siui.components import SiLabel, SiWidget
from siui.core import SiColor, SiExpAnimation


class SiHExpandWidget(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attachment_ = SiWidget(self)

        self.expand_animation = SiExpAnimation(self)
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


class SiHoverExpandWidget(SiHExpandWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.test_label = SiLabel(self)
        self.test_label.setFixedStyleSheet("border-radius: 4px")
        self.test_label.setColor(self.getColor(SiColor.PROGRESS_BAR_COMPLETING))

        self.setAttachment(self.test_label)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.expandTo(1)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.expandTo(0.95)
