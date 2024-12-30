import random
from typing import Union

from PyQt5.Qt import QColor
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget

from siui.components.widgets.abstracts.container import ABCSiDividedContainer
from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel


class PlaceHolderWidget(QWidget):
    pass


class ABCDenseContainer(SiWidget):
    """
    密堆容器抽象类
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.adjust_widgets_size = False  # 子控件适应高度
        self.shrinking = True  # 调整尺寸方法被调用时，允许尺寸变小
        self.use_moveto = False  # 使用 moveto 方法移动控件而非 move
        self.alignment_ = 0

        self.spacing = 16  # 各个控件间的距离

    def setUseMoveTo(self, b: bool):
        """
        在调整控件位置时是否使用 moveto 方法移动控件而非 move
        :param b: 是否使用 moveto
        """
        self.use_moveto = b

    def setAdjustWidgetsSize(self, b: bool):
        """
        设置子控件是否在垂直于容器的方向上自动适应
        :param b: 是否自动适应
        :return:
        """
        self.adjust_widgets_size = b

    def setShrinking(self, b: bool):
        """
        设置调整尺寸方法被调用时，是否尺寸变小
        :param b: 是否允许
        :return:
        """
        self.shrinking = b

    def setAlignCenter(self, b: bool):
        """
        设置是否将子控件放置在容器中轴线上
        :param b: 是否放置在中轴线上
        :return:
        """
        print("Warning: method `setAlignCenter` is deprecated, use setAlignment(Qt.AlignCenter) instead.")  # noqa: T201
        if b is True:
            self.setAlignment(self.alignment() | Qt.AlignCenter)

    def setAlignment(self, alignment):
        self.alignment_ = alignment

    def alignment(self):
        return self.alignment_

    def setSpacing(self, spacing: int):
        """
        设置控件之间的距离
        :param spacing: 距离 px
        :return:
        """
        self.spacing = spacing

    def widgets(self):
        raise NotImplementedError()

    @staticmethod
    def get_widget_except_placeholders(widgets):
        no_placeholders = []
        for widget in widgets:
            if isinstance(widget, PlaceHolderWidget) is False:
                no_placeholders.append(widget)
        return no_placeholders

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.adjustSize()  # 使用 with 语句时，自动调节大小


class SiDenseHContainer(ABCDenseContainer):
    """
    一个可以水平方向紧密靠左或靠右堆叠控件的容器
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets_left = []
        self.widgets_right = []
        self.alignment_ = Qt.AlignTop

    def addPlaceholder(self, length, side="left", index=10000):
        """
        添加占位符
        :param length: 占位符的宽度
        :param side: 添加到哪一侧
        :param index: 插入位置
        :return:
        """
        new_label = PlaceHolderWidget(self)
        new_label.setVisible(False)
        new_label.resize(length, 0)
        self.addWidget(new_label, side=side, index=index)

    def addWidget(self, widget, side="left", index=10000):
        """
        添加子控件，这将调整被添加的控件的父对象为该容器
        :param widget: 控件
        :param side: 添加到哪一侧
        :param index: 插入位置
        :return:
        """
        widget.setParent(self)

        if side != "left" and side != "right":
            raise ValueError(f"意外方向参数 {side}")

        if side == "left":
            self.widgets_left = self.widgets_left[:index] + [widget] + self.widgets_left[index:]
        if side == "right":
            self.widgets_right = self.widgets_right[:index] + [widget] + self.widgets_right[index:]

        self.adjustSize()

    def getUsedSpace(self, side):
        if side not in ["left", "right"]:
            raise ValueError(f"Unexpected side: {side}")
        if side == "left":
            return sum([obj.width() + self.spacing for obj in self.widgets_left])
        if side == "right":
            return sum([obj.width() + self.spacing for obj in self.widgets_right])

    def getSpareSpace(self):
        return self.width() - self.getUsedSpace("left") - self.getUsedSpace("right")

    def widgets(self, side=None):
        if side is None:
            widgets = self.widgets_left + self.widgets_right
        elif side == "left":
            widgets = self.widgets_left
        elif side == "right":
            widgets = self.widgets_right
        else:
            raise ValueError(f"Unexpected side: {side}")
        return self.get_widget_except_placeholders(widgets)

    def removeWidget(self, widget):
        """
        从容器中移除控件
        :param widget: 控件
        """
        if widget in self.widgets_left:
            index = self.widgets_left.index(widget)
            self.widgets_left.pop(index)
            return

        if widget in self.widgets_right:
            index = self.widgets_left.index(widget)
            self.widgets_left.pop(index)
            return

        raise ValueError(f"Widget provided ({widget}) is not in this container.")

    def sizeHint(self):
        # 创建计数器
        left_used = 0
        right_used = 0

        # 获取各侧宽度
        for obj in self.widgets_left:
            left_used += obj.width() + self.spacing
        for obj in self.widgets_right:
            right_used += obj.width() + self.spacing

        # 计算总共的宽度，并处理
        total_used = left_used + right_used
        total_used -= 0 if self.widgets_left == [] else self.spacing  # 删去多余的 spacing
        total_used -= 0 if self.widgets_right == [] else self.spacing  # 删去多余的 spacing
        total_used += self.spacing if self.widgets_left + self.widgets_right == [] else 0  # 防止极端情况下两侧控件紧贴
        preferred_w = total_used

        return QSize(preferred_w, max([0] + [widget.height() for widget in (self.widgets_left + self.widgets_right)]))

    def arrangeWidget(self):
        """
        调整子控件的几何信息。这包括排列子控件，置于中轴线上，以及适应容器s
        :return:
        """
        # 初始化已使用空间的计数器
        left_used = 0
        right_used = 0

        # 左侧控件
        for obj in self.widgets_left:
            # 是否适应容器
            if self.adjust_widgets_size is True:
                obj.resize(obj.width(), self.height())

            # 判断并设置对齐方式
            if (self.alignment_ & Qt.AlignTop) == Qt.AlignTop:
                y = 0
            elif (self.alignment_ & Qt.AlignVCenter) == Qt.AlignVCenter:
                y = (self.height() - obj.height()) // 2
            elif (self.alignment_ & Qt.AlignBottom) == Qt.AlignBottom:
                y = self.height() - obj.height()
            else:
                y = 0

            # 设置位置
            if self.use_moveto is True:
                obj.moveTo(left_used, y)
            else:
                obj.move(left_used, y)

            # 计数器添加控件的宽度和间距
            left_used += obj.width() + self.spacing

        # 右侧控件
        for obj in self.widgets_right:
            # 是否适应容器
            if self.adjust_widgets_size is True:
                obj.resize(obj.width(), self.height())

            # 判断并设置对齐方式
            if (self.alignment_ & Qt.AlignTop) == Qt.AlignTop:
                y = 0
            elif (self.alignment_ & Qt.AlignVCenter) == Qt.AlignVCenter:
                y = (self.height() - obj.height()) // 2
            elif (self.alignment_ & Qt.AlignBottom) == Qt.AlignBottom:
                y = self.height() - obj.height()
            else:
                y = 0

            # 设置位置
            if self.use_moveto is True:
                obj.moveTo(self.width() - obj.width() - right_used, y)
            else:
                obj.move(self.width() - obj.width() - right_used, y)

            # 计数器添加控件的宽度和间距
            right_used += obj.width() + self.spacing

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.arrangeWidget()  # 每当自身尺寸改变时，重新设置控件的位置

    def adjustSize(self):
        """
        根据自身具有的控件调整自身的大小
        :return:
        """
        # 获取最佳尺寸
        size = self.sizeHint()
        preferred_w, preferred_h = size.width(), size.height()

        if self.shrinking is False:
            # 和原本自身的尺寸比价，取最大者
            preferred_w = max(preferred_w, self.width())
            preferred_h = max(preferred_h, self.height())

        self.resize(preferred_w, preferred_h)


class SiDenseVContainer(ABCDenseContainer):
    """
    一个可以竖直方向紧密靠上或靠下堆叠控件的容器
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets_bottom = []
        self.widgets_top = []
        self.alignment_ = Qt.AlignLeft

    def addPlaceholder(self, length, side="top", index=10000):
        """
        添加占位符
        :param length: 占位符的高
        :param side: 添加到哪一侧
        :param index: 插入位置
        :return:
        """
        new_label = PlaceHolderWidget(self)
        new_label.setVisible(False)
        new_label.resize(0, length)
        self.addWidget(new_label, side=side, index=index)

    def addWidget(self, widget, side="top", index=10000):
        """
        添加子控件，这将调整被添加的控件的父对象为该容器
        :param widget: 子控件
        :param side: 添加到哪一侧
        :param index: 插入的位置
        :return:
        """
        widget.setParent(self)

        if side != "top" and side != "bottom":
            raise ValueError(f"意外方向参数 {side}")

        if side == "bottom":
            self.widgets_bottom = self.widgets_bottom[:index] + [widget] + self.widgets_bottom[index:]
        if side == "top":
            self.widgets_top = self.widgets_top[:index] + [widget] + self.widgets_top[index:]

        self.adjustSize()

    def sizeHint(self):
        # 创建计数器
        bottom_used = 0
        top_used = 0

        # 获取各侧高度
        for obj in self.widgets_bottom:
            bottom_used += obj.height() + self.spacing
        for obj in self.widgets_top:
            top_used += obj.height() + self.spacing

        # 计算总共的高度，并处理
        total_used = bottom_used + top_used
        total_used -= 0 if self.widgets_bottom == [] else self.spacing  # 删去多余的 spacing
        total_used -= 0 if self.widgets_top == [] else self.spacing  # 删去多余的 spacing
        total_used += self.spacing if (self.widgets_bottom != [] and self.widgets_top != []) else 0  # 防止两侧控件紧贴
        preferred_h = total_used

        return QSize(max([0] + [widget.width() for widget in (self.widgets_top + self.widgets_bottom)]), preferred_h)

    def getUsedSpace(self, side):
        if side not in ["top", "bottom"]:
            raise ValueError(f"Unexpected side: {side}")
        if side == "top":
            return sum([obj.height() + self.spacing for obj in self.widgets_top])
        if side == "bottom":
            return sum([obj.height() + self.spacing for obj in self.widgets_bottom])

    def getSpareSpace(self):
        return self.height() - self.getUsedSpace("top") - self.getUsedSpace("bottom")

    def widgets(self, side=None):
        if side is None:
            widgets = self.widgets_top + self.widgets_bottom
        elif side == "top":
            widgets = self.widgets_top
        elif side == "bottom":
            widgets = self.widgets_bottom
        else:
            raise ValueError(f"Unexpected side: {side}")
        return self.get_widget_except_placeholders(widgets)

    def removeWidget(self, widget):
        """
        从容器中移除控件
        :param widget: 控件
        """
        if widget in self.widgets_top:
            index = self.widgets_top.index(widget)
            self.widgets_top.pop(index)
            return

        if widget in self.widgets_bottom:
            index = self.widgets_bottom.index(widget)
            self.widgets_bottom.pop(index)
            return

        raise ValueError(f"Widget provided ({widget}) is not in this container.")

    def arrangeWidget(self):  # noqa: C901
        """
        调整子控件的几何信息。这包括排列子控件，置于中轴线上，以及适应容器
        :return:
        """
        # 初始化已使用空间的计数器
        top_used = 0
        bottom_used = 0

        # 下侧控件
        for obj in self.widgets_top:
            # 是否适应容器
            if self.adjust_widgets_size is True:
                obj.resize(self.width(), obj.height())

            # 判断并设置对齐方式
            if (self.alignment_ & Qt.AlignLeft) == Qt.AlignLeft:
                x = 0
            elif (self.alignment_ & Qt.AlignHCenter) == Qt.AlignHCenter:
                x = (self.width() - obj.width()) // 2
            elif (self.alignment_ & Qt.AlignRight) == Qt.AlignRight:
                x = self.width() - obj.width()
            else:
                x = 0

            # 设置位置
            if self.use_moveto is True:
                obj.moveTo(x, top_used)
            else:
                obj.move(x, top_used)

            # 计数器添加控件的宽度和间距
            top_used += obj.height() + self.spacing

        # 上侧控件
        for obj in self.widgets_bottom:
            # 是否适应容器
            if self.adjust_widgets_size is True:
                obj.resize(self.width(), obj.height())

            # 判断并设置对齐方式
            if (self.alignment_ & Qt.AlignLeft) == Qt.AlignLeft:
                x = 0
            elif (self.alignment_ & Qt.AlignHCenter) == Qt.AlignHCenter:
                x = (self.width() - obj.width()) // 2
            elif (self.alignment_ & Qt.AlignRight) == Qt.AlignRight:
                x = self.width() - obj.width()
            else:
                x = 0

            # 设置位置
            if self.use_moveto is True:
                obj.moveTo(x, self.height() - obj.height() - bottom_used)
            else:
                obj.move(x, self.height() - obj.height() - bottom_used)

            # 计数器添加控件的宽度和间距
            bottom_used += obj.height() + self.spacing

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.arrangeWidget()  # 每当自身尺寸改变时，重新设置控件的位置

    def adjustSize(self):
        """
        根据自身具有的控件调整自身的大小
        :return:
        """
        # 获取最佳尺寸
        size = self.sizeHint()
        preferred_w, preferred_h = size.width(), size.height()

        if self.shrinking is False:
            # 和原本自身的尺寸比价，取最大者
            preferred_w = max(preferred_w, self.width())
            preferred_h = max(preferred_h, self.height())

        self.resize(preferred_w, preferred_h)


class SiDividedHContainer(ABCSiDividedContainer):
    def sizeHint(self):
        total_spacing = self.spacing() * max(0, (len(self.sections()) - 1))
        total_section_width = sum([section.width() for section in self.sections()])
        largest_height = max([section.height() for section in self.sections()])
        return QSize(total_section_width + total_spacing, largest_height)

    def arrangeWidgets(self):
        x_counter = 0
        for section, widget in zip(self.sections(), self.widgets()):
            alignment = section.alignment()
            if (alignment & Qt.AlignLeft) == Qt.AlignLeft:
                x = x_counter
            elif (alignment & Qt.AlignHCenter) == Qt.AlignHCenter:
                x = x_counter + (section.width() - widget.width()) // 2
            elif (alignment & Qt.AlignRight) == Qt.AlignRight:
                x = x_counter + (section.width() - widget.width())
            else:
                x = x_counter   # use Qt.AlignLeft if horizontal alignment arg is not assign

            if (alignment & Qt.AlignTop) == Qt.AlignTop:
                y = 0
            elif (alignment & Qt.AlignVCenter) == Qt.AlignVCenter:
                y = (section.height() - widget.height()) // 2
            elif (alignment & Qt.AlignBottom) == Qt.AlignBottom:
                y = section.height() - widget.height()
            else:
                y = 0   # use Qt.AlignTop if vertical alignment arg is not assign

            widget.move(x, y)
            x_counter += section.width() + self.spacing()


class SiDividedVContainer(ABCSiDividedContainer):
    def sizeHint(self):
        total_spacing = self.spacing() * max(0, (len(self.sections()) - 1))
        total_section_height = sum([section.height() for section in self.sections()])
        largest_width = max([section.width() for section in self.sections()])
        return QSize(largest_width, total_section_height + total_spacing)

    def arrangeWidgets(self):
        y_counter = 0
        for section, widget in zip(self.sections(), self.widgets()):
            alignment = section.alignment()
            if (alignment & Qt.AlignLeft) == Qt.AlignLeft:
                x = 0
            elif (alignment & Qt.AlignHCenter) == Qt.AlignHCenter:
                x = (section.width() - widget.width()) // 2
            elif (alignment & Qt.AlignRight) == Qt.AlignRight:
                x = section.width() - widget.width()
            else:
                x = 0   # use Qt.AlignLeft if horizontal alignment arg is not assign

            if (alignment & Qt.AlignTop) == Qt.AlignTop:
                y = y_counter
            elif (alignment & Qt.AlignVCenter) == Qt.AlignVCenter:
                y = y_counter + (section.height() - widget.height()) // 2
            elif (alignment & Qt.AlignBottom) == Qt.AlignBottom:
                y = y_counter + (section.height() - widget.height())
            else:   # use Qt.AlignTop if vertical alignment arg is not assign
                y = y_counter

            widget.move(x, y)
            y_counter += section.height() + self.spacing()


class SiStackedContainer(SiLabel):
    """
    允许堆叠的容器，可以绑定多个界面，并只显示其中一个
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 当前索引
        self.current_index_ = -1

        # 所有页面
        self.widgets = []

    def widgetsAmount(self):
        """
        获取子控件的数量
        :return: 子控件数量
        """
        return len(self.widgets)

    def addWidget(self, widget):
        """
        添加子控件（页面）
        :param widget: 子控件
        :return:
        """
        self.insertWidgets(widget, 10000)

    def insertWidgets(self, widget, index: int):
        """
        添加子控件（页面），如果插入位置过大，会置于序列最后
        :param widget: 子控件
        :param index: 索引
        """
        widget.setParent(self)
        widget.resize(self.size())
        widget.move(0, 0)
        widget.hide()
        self.widgets = self.widgets[:index] + [widget] + self.widgets[index:]

        if len(self.widgets) == 1:
            self.setCurrentIndex(0)

    def currentIndex(self):
        """
        获取当前索引
        :return: 索引
        """
        return self.current_index_

    def setCurrentIndex(self, index: int):
        """
        设置当前索引
        :param index: 索引
        """
        self.current_index_ = index
        for widget in self.widgets:
            widget.hide()
        self.widgets[index].show()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        for widget in self.widgets:
            widget.resize(event.size())


class ABCSiFlowContainer(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widgets_ = []
        self.dragging_widget = None
        self.spacing = [8, 8]

    def setSpacing(self, horizontal=None, vertical=None):
        if horizontal is not None:
            self.spacing[0] = horizontal
        if vertical is not None:
            self.spacing[1] = vertical

    def widgets(self):
        """ Get the widgets of this container """
        return self.widgets_

    def addWidget(self, widget, arrange=True, ani=True):
        """ Add widget to this container """
        widget.setParent(self)
        self.widgets_.append(widget)
        if arrange is True:
            self.arrangeWidgets(ani=ani)

    def removeWidget(self,
                     widget,
                     has_existence_check: bool = True,
                     delete_later: bool = True,
                     fade_out: bool = False,
                     fade_out_delay: int = 0):
        """
        Remove a widget in self.widgets()
        :param widget: widget you want to remove
        :param has_existence_check: whether check the existence of the widget in self.widgets()
        :param delete_later: whether run widget.deleteLater()
        :param fade_out: run fade out animation when removing this widget
        :param fade_out_delay: delay before run fade out animation
        """
        if widget in self.widgets_:
            self.widgets_.pop(self.widgets_.index(widget))

            if fade_out:
                widget.animationGroup().fromToken("opacity").setTarget(0)
                widget.animationGroup().fromToken("opacity").start(delay=fade_out_delay)
                if delete_later:
                    delete_timer = QTimer(widget)
                    delete_timer.singleShot(fade_out_delay + 100, widget.deleteLater)
            else:
                if delete_later:
                    widget.deleteLater()

        elif has_existence_check:
            raise ValueError(f"Widget {widget} is not in this container")
        else:
            pass

    def arrangeWidgets(self, ani=True):
        """ Arrange widgets as its order in self.widgets() """
        raise NotImplementedError("arrangeWidgets method must be rewrote.")

    def shuffle(self, **kwargs):
        """ shuffle widgets and rearrange them """
        random.shuffle(self.widgets_)
        self.arrangeWidgets(**kwargs)

    def swapByIndex(self, from_index, to_index):
        widget_a = self.widgets()[from_index]
        widget_b = self.widgets()[to_index]
        self.widgets_[from_index] = widget_b
        self.widgets_[to_index] = widget_a
        self.arrangeWidgets()

    def insertToByIndex(self, from_index, to_index, **kwargs):
        widget = self.widgets()[from_index]
        self.widgets_[from_index] = None

        if from_index > to_index:
            self.widgets_ = self.widgets_[:to_index] + [widget] + self.widgets_[to_index:]
        else:
            self.widgets_ = self.widgets_[:to_index + 1] + [widget] + self.widgets_[to_index + 1:]

        self.widgets_.pop(self.widgets_.index(None))
        self.arrangeWidgets(**kwargs)

    def regDraggableWidget(self, widget):
        """ register a widget as a draggable widget """
        def on_dragging(pos):
            if self.dragging_widget is None:
                # drop shadow effect
                shadow = QGraphicsDropShadowEffect()
                shadow.setColor(QColor(0, 0, 0, 80))
                shadow.setOffset(0, 0)
                shadow.setBlurRadius(32)
                widget.setGraphicsEffect(shadow)
                self.dragging_widget = widget
            self._on_widget_dragged(widget)

        widget.dragged.connect(on_dragging)

    def _on_widget_dragged(self, dragged_widget):
        self.on_dragging = True
        dragged_widget.raise_()
        center_point = dragged_widget.geometry().center()

        for widget in self.widgets():
            if widget == dragged_widget:
                continue

            if (widget.geometry().contains(center_point) and
                    (widget.animationGroup().fromToken("move").isActive() is False)):
                # insert dragged widget to where this widget is.
                self.insertToByIndex(self.widgets().index(dragged_widget),
                                     self.widgets().index(widget),
                                     no_arrange_exceptions=[dragged_widget])
                break

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        if self.dragging_widget is not None:
            self.dragging_widget.setGraphicsEffect(None)
            self.dragging_widget = None
            self.arrangeWidgets()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.arrangeWidgets()
        for widget in self.widgets_:
            widget.setMoveLimits(0, 0, self.width(), self.height())


class SiFlowContainer(ABCSiFlowContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_height = 32
        self.preferred_height = 0

    def adjustSize(self):
        self.resize(self.width(), self.preferred_height)

    def setLineHeight(self, height, rearrange=True):
        self.line_height = height
        if rearrange:
            self.arrangeWidgets(ani=True)

    def arrangeWidgets(self,
                       ani: bool = True,
                       all_fade_in: bool = False,
                       fade_in_delay: int = 200,
                       fade_in_delay_cumulate_rate: int = 10,
                       no_arrange_exceptions: Union[list, None] = None,
                       no_ani_exceptions: Union[list, None] = None):
        """
        :param ani: whether widgets perform animation when arranging them
        :param all_fade_in: let all widgets fade in when arranging them
        :param fade_in_delay: time delay before run fade in animation
        :param fade_in_delay_cumulate_rate: cumulate rate of delay
        :param no_arrange_exceptions: widgets that will not be arranged
        :param no_ani_exceptions: widgets that will not perform moving animation.
        """
        used_width = 0
        used_height = 0
        delay_counter = 0
        if no_arrange_exceptions is None:
            no_arrange_exceptions = []
        if no_ani_exceptions is None:
            no_ani_exceptions = []

        for widget in self.widgets_:
            # warp when haven't got enough space.
            if self.width() - used_width - self.spacing[0] < widget.width():
                used_height += self.spacing[1] + self.line_height
                used_width = 0

            # perform fade in effect
            if all_fade_in or (widget in no_ani_exceptions):
                widget.animationGroup().fromToken("opacity").stop()
                widget.setOpacity(0)
                widget.animationGroup().fromToken("opacity").setTarget(1)
                widget.animationGroup().fromToken("opacity").start(delay=fade_in_delay + delay_counter)
            delay_counter += fade_in_delay_cumulate_rate

            # if we needn't perform animations...
            if (ani is False) or (widget in no_ani_exceptions):
                if (widget in no_arrange_exceptions) is False:
                    widget.animationGroup().fromToken("move").stop()
                    widget.move(used_width, used_height)

            # perform animations
            else:
                if (widget in no_arrange_exceptions) is False:
                    widget.moveTo(used_width, used_height)

            # add width of this widget to counter
            used_width += widget.width() + self.spacing[0]

        self.preferred_height = used_height + self.spacing[1] + self.line_height


class SiMasonryContainer(ABCSiFlowContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns = 2  # How many columns that this container has
        self.column_width = 160  # width of each column
        self.preferred_height = 0
        self.auto_adjust_column_amount = False

    def setAutoAdjustColumnAmount(self, state):
        self.auto_adjust_column_amount = state

    def setColumns(self, n):
        self.columns = n

    def setColumnWidth(self, width):
        self.column_width = width

    def arrangeWidgets(self,
                       ani=True,
                       no_arrange_exceptions: Union[list, None] = None,
                       no_ani_exceptions: Union[list, None] = None,
                       adjust_size: bool = True):

        used_height = [0 for _ in range(self.columns)]
        ani_delay_counter = 0
        if no_arrange_exceptions is None:
            no_arrange_exceptions = []
        if no_ani_exceptions is None:
            no_ani_exceptions = []

        for index, widget in enumerate(self.widgets_):
            column_index = index % self.columns

            if widget not in no_arrange_exceptions:
                if (ani is True) and (widget not in no_ani_exceptions):
                    widget.animationGroup().fromToken("move").stop()
                    widget.animationGroup().fromToken("move").setTarget(
                        [column_index * (self.column_width + self.spacing[0]), used_height[column_index]])
                    widget.animationGroup().fromToken("move").start()
                else:
                    widget.animationGroup().fromToken("move").stop()
                    widget.move(column_index * (self.column_width + self.spacing[0]), used_height[column_index])

            used_height[column_index] += widget.height() + self.spacing[1]
            ani_delay_counter += 10

        self.preferred_height = max(max(used_height) - self.spacing[1], 0)
        if adjust_size is True:
            self.adjustSize()

    def adjustColumnAmount(self, width=None):
        """ Adjust the column amount of this container based on its width. """
        if width is None:
            width = self.width()
        else:
            self.resize(width, self.height())

        self.setColumns(self.calculateColumnAmount(width))
        self.arrangeWidgets()

    def calculateColumnAmount(self, width):
        """ Calculate column amount based on width provided. """
        return (width + self.spacing[0]) // (self.column_width + self.spacing[0])

    def adjustSize(self):
        self.resize(self.width(), self.preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.auto_adjust_column_amount:
            self.adjustColumnAmount()