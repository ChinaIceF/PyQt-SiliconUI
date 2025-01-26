from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiDraggableLabel, SiLabel
from siui.core import Si, SiExpAnimation
from siui.core import SiExpAccelerateAnimation
from siui.core import SiGlobal


class SiScrollArea(SiWidget):
    """
    滚动区域
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 定义一个占位用的子控件
        self.attachment_ = SiLabel(self)

        # 定义滚动条的框架
        self.scroll_bar_frame_vertical = SiLabel(self)
        self.scroll_bar_frame_horizontal = SiLabel(self)

        # 定义滚动条
        self.scroll_bar_vertical = SiDraggableLabel(self.scroll_bar_frame_vertical)
        self.scroll_bar_vertical.setFixedStyleSheet("border-radius: 4px")  # 固定样式表
        self.scroll_bar_vertical.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.scroll_bar_vertical.dragged.connect(self._scroll_vertical_handler)

        self.scroll_bar_horizontal = SiDraggableLabel(self.scroll_bar_frame_horizontal)
        self.scroll_bar_horizontal.setFixedStyleSheet("border-radius: 4px")  # 固定样式表
        self.scroll_bar_horizontal.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.scroll_bar_horizontal.dragged.connect(self._scroll_horizontal_handler)

        # 定义滚动动画，为了让所有控件都能用上滚动动画
        self.widget_scroll_animation = SiExpAnimation(self)
        self.widget_scroll_animation.setFactor(1/6)
        self.widget_scroll_animation.setBias(2)
        self.widget_scroll_animation.setCurrent([0, 0])
        self.widget_scroll_animation.setTarget([0, 0])
        self.widget_scroll_animation.ticked.connect(lambda pos: self.attachment_.move(int(pos[0]), int(pos[1])))

        self.animationGroup().addMember(self.widget_scroll_animation, "scroll")

    def reloadStyleSheet(self):
        """
        重载样式表
        :return:
        """
        super().reloadStyleSheet()
        self.scroll_bar_vertical.setStyleSheet(f"background-color: {SiGlobal.siui.colors['SCROLL_BAR']}")
        self.scroll_bar_horizontal.setStyleSheet(f"background-color: {SiGlobal.siui.colors['SCROLL_BAR']}")

    def setAttachment(self, widget):
        """
        绑定子控件，作为滚动的部件
        :param widget:
        :return:
        """
        self.attachment_.deleteLater()

        self.attachment_ = widget
        self.attachment_.setParent(self)
        self.attachment_.lower()

    def attachment(self):
        """
        获取被绑定控件
        :return: 被绑定控件
        """
        return self.attachment_

    def _scroll_vertical_handler(self, pos):
        # 计算目标纵坐标
        _, y = pos
        progress = y / (self.height() - self.scroll_bar_vertical.height())
        target = - int(progress * (self.attachment_.height() - self.height()))

        # 设置目标值并尝试启动
        # 2024.8.24  直接使用 move，以提高拖动滚动条时的操作体验
        self.widget_scroll_animation.stop()
        self.widget_scroll_animation.setCurrent([self.attachment_.x(), target])
        self.widget_scroll_animation.setTarget([self.attachment_.x(), target])
        self.attachment_.move(self.attachment_.x(), target)

        # self.widget_scroll_animation.setTarget([self.attachment_.x(), target])
        # self.widget_scroll_animation.try_to_start()

    def _scroll_horizontal_handler(self, pos):
        # 计算目标横坐标
        x, _ = pos
        progress = x / (self.width() - self.scroll_bar_horizontal.width())
        target = - int(progress * (self.attachment_.width() - self.width()))

        # 设置目标值并尝试启动
        # 2024.8.24  直接使用 move，以提高拖动滚动条时的操作体验
        self.widget_scroll_animation.stop()
        self.widget_scroll_animation.setCurrent([target, self.attachment_.y()])
        self.widget_scroll_animation.setTarget([target, self.attachment_.y()])
        self.attachment_.move(target, self.attachment_.y())

        # self.widget_scroll_animation.setTarget([target, self.attachment_.y()])
        # self.widget_scroll_animation.try_to_start()

    def resizeEvent(self, event):
        # 注意：滚动区域并不会改变子控件的大小，适应需要重写父级的resizeEvent
        super().resizeEvent(event)

        # 重设框架的尺寸
        self.scroll_bar_frame_vertical.setGeometry(self.width() - 8, 0, 8, self.height())
        self.scroll_bar_frame_horizontal.setGeometry(0, self.height() - 8, self.width(), 8)

        # 根据滚动区域的大小和子控件的大小，计算出滚动条的长度或宽度
        self.scroll_bar_horizontal.resize(self.width() * self.width() // self.attachment_.width(), 8)
        self.scroll_bar_vertical.resize(8, self.height() * self.height() // self.attachment_.height())

        # 判断长宽是否超过自身的长宽，从而确定是否显示滚动条
        # 水平
        if self.attachment_.width() <= self.width():
            self.scroll_bar_horizontal.setVisible(False)
        else:
            self.scroll_bar_horizontal.setVisible(True)

        # 竖直
        if self.attachment_.height() <= self.height():
            self.scroll_bar_vertical.setVisible(False)
        else:
            self.scroll_bar_vertical.setVisible(True)

        # 设置拖动限制
        self.scroll_bar_horizontal.setMoveLimits(0, 0, self.width(), 8)
        self.scroll_bar_vertical.setMoveLimits(0, 0, 8, self.height())

        # 相当于刷新位置，保证滚动内容，滚动条其仍在限制区域内
        self.attachment().move(self.attachment().x(),
                               min(0, max(self.attachment().y(), self.height() - self.attachment().height())))

    def wheelEvent(self, event):
        # 滚轮只在竖直方向上滚动
        # TODO: 后期滚动条和滚动区域分开，鼠标移动到不同滚动条上控制不同方向上的滚动

        # 滚动强度，决定一个滚动单位需滚动多少像素
        strength = 100

        # 读取子控件的移动动画目标值
        target = self.widget_scroll_animation.target()

        # 根据滚动方向，目标值加或减滚动强度，并更新目标值
        target[1] += strength if event.angleDelta().y() > 0 else -strength
        target[1] = min(0, max(self.height() - self.attachment_.height(), target[1]))  # 防止滚出限制范围
        self.widget_scroll_animation.setTarget(target)

        # 计算滚动条的目标位置
        process = -target[1] / (self.attachment_.height() - self.height())
        scroll_bar_vertical_target_y = int(process * (self.height() - self.scroll_bar_vertical.height()))

        # 如果竖直方向滚动条可见，尝试启动动画
        if self.scroll_bar_vertical.isVisible():
            self.scroll_bar_vertical.moveTo(0, scroll_bar_vertical_target_y)
            self.widget_scroll_animation.try_to_start()
            event.accept()
