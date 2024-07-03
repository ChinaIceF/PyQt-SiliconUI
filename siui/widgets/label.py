from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.widgets.abstracts import ABCAnimatedLabel


class SiLabel(ABCAnimatedLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class SiLabelColored(ABCAnimatedLabel):
    """
    面向显示颜色的标签，支持改变颜色动画
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.animation_color = SiExpAnimation(self)
        self.animation_color.setFactor(1/4)
        self.animation_color.setBias(1)
        self.animation_color.ticked.connect(self._set_color_handler)

        self.getAnimationGroup().addMember(self.animation_color, "color")

    def setColorTo(self, color_code):
        """
        设置目标颜色，同时启动动画
        :param color_code: 色号
        :return:
        """
        self.animation_color.setTarget(Color.decodeColor(color_code))
        self.animation_color.try_to_start()

    def setColor(self, color_code):
        """
        设置颜色
        :param color_code: 色号
        :return:
        """
        color_value = Color.decodeColor(color_code)
        self.animation_color.setCurrent(color_value)
        self._set_color_handler(color_value)

    def _set_color_handler(self, color_value):
        self.setStyleSheet(f"background-color: {Color.encodeColor(color_value)}")
