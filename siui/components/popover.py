from __future__ import annotations

from PyQt5.QtCore import QDate, QEvent, QPoint, QPointF, QRectF, QSize, Qt, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QButtonGroup, QLabel, QMenu, QStackedWidget, QWidget

from siui.components.button import SiFlatButton, SiFlatButtonWithIndicator
from siui.components.container import SiDenseContainer
from siui.components.graphic import SiGraphicWrapperWidget
from siui.components.slider_ import SiWeekdaySpinBox, SiWheelPickerHorizontal, SiWheelPickerVertical
from siui.core import SiQuickEffect, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.globals import SiGlobal
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiPopover(QMenu):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._padding = 32

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # *

        # 2025.5.3  * 如果使用 Qt.Popup, QGraphicProxyWidget 中的控件不能接收到 WheelEvent,
        #             因此通过重写 event 方法来实现类似 Popup 的行为

        self._shadow_frame = QWidget(self)

        self._wrapper = SiGraphicWrapperWidget(self)
        self._wrapper.setAttribute(Qt.WA_TranslucentBackground)

        self._initStyle()
        SiQuickEffect.applyDropShadowOn(self._shadow_frame, (0, 0, 0, 180), blur_radius=32)

    def _initStyle(self) -> None:
        self.setStyleSheet("background: transparent;")
        self._shadow_frame.setStyleSheet("background-color: #D087DF; border-radius: 6px")

    def wrapper(self) -> SiGraphicWrapperWidget:
        return self._wrapper

    def resizeEvent(self, a0):
        p = self._padding
        self._shadow_frame.setGeometry(p+1, p+1, self.width()-2*p-2, self.height()-2*p-2)
        self._wrapper.setGeometry(p, p, self.width()-2*p, self.height()-2*p)

    def sizeHint(self):
        size = self._wrapper.widget().sizeHint()
        return QSize(size.width() + 2 * self._padding, size.height() + 2 * self._padding)

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
        return super().event(event)


class SiPopoverStackedWidget(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.TopToBottom)

        self._button_group = QButtonGroup(self)

        self._background = QWidget(self)
        self._btn_ctn_background = QWidget(self)

        self._button_container = SiDenseContainer(self, self.LeftToRight)
        self._stack_widget = QStackedWidget(self)

        self._no_button_label = QLabel(self)
        self._no_page_label = QLabel(self)
        self._close_button = SiFlatButton(self)

        self._button_container.addWidget(self._close_button, Qt.RightEdge)

        self.addWidget(self._button_container)
        self.addWidget(self._stack_widget)

        self._initStyle()

        self._close_button.clicked.connect(self.parent().close)

    def _initStyle(self) -> None:
        self.layout().setSpacing(0)

        self._no_button_label.setText("无页面")
        self._no_button_label.setStyleSheet("color: #918497")
        self._no_button_label.setFont(SiFont.getFont(size=14))
        self._no_button_label.setAlignment(Qt.AlignCenter)
        self._no_button_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self._no_page_label.setText("弹窗没有可供展示的页面")
        self._no_page_label.setStyleSheet("color: #D1CBD4")
        self._no_page_label.setFont(SiFont.getFont(size=14, weight=SiFont.Weight.Bold))
        self._no_page_label.setAlignment(Qt.AlignCenter)
        self._no_page_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self._button_container.setFixedHeight(64)
        self._button_container.setContentsMargins(10, 8, 16, 10)
        self._button_container.layout().setSpacing(8)

        self._stack_widget.setMinimumSize(320, 100)
        self._stack_widget.setContentsMargins(1, 0, 1, 1)

        self._close_button.setFixedSize(36, 36)
        self._close_button.setToolTip("关闭")
        self._close_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_dismiss_filled"))

        self.setStyleSheet("background-color: transparent")
        self._background.setStyleSheet("background-color: #332E38; border: 1px solid #3C3841; border-radius: 6px")
        self._btn_ctn_background.setStyleSheet("background-color: #25222A; border-radius: 5px; margin: 1px")

    def addPage(self, widget: SiGraphicWrapperWidget, name: str = "新页面") -> None:
        self._no_page_label.hide()
        self._no_button_label.hide()

        new_button = SiFlatButtonWithIndicator(self)
        new_button.setText(name)
        new_button.setFixedHeight(48)

        widget.resize(widget.widget().size())
        self._stack_widget.addWidget(widget)

        self._button_container.addWidget(new_button)
        self._button_group.addButton(new_button)

        if self._stack_widget.count() == 1:
            self._stack_widget.setCurrentIndex(0)
            new_button.click()

        new_button.clicked.connect(lambda: self._stack_widget.setCurrentWidget(widget))
        new_button.clicked.connect(widget.playMergeAnimations)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._background.resize(self.size())
        self._no_button_label.setGeometry(0, 0, self.width(), 64)
        self._no_page_label.setGeometry(0, 64, self.width(), self.height() - 64)
        self._btn_ctn_background.setGeometry(0, 0, self.width(), 64)


class SiPopoverDatePicker(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.LeftToRight)

        self._date = QDate.currentDate()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent")

        self._year_picker = SiWheelPickerHorizontal(self)
        self._month_picker = SiWheelPickerHorizontal(self)
        self._day_picker = SiWheelPickerHorizontal(self)
        self._day_of_week_picker = SiWheelPickerHorizontal(self)
        self._set_to_today_button = SiFlatButton(self)

        self.addWidget(self._year_picker)
        self.addWidget(self._month_picker)
        self.addWidget(self._day_picker)
        self.addWidget(self._day_of_week_picker)
        self.addWidget(self._set_to_today_button, side=Qt.RightEdge)

        self._initStyle()
        self._initSignal()

        self.setToToday()

    def _initStyle(self) -> None:
        self.layout().setSpacing(20)
        self.setContentsMargins(24, 12, 16, 12)

        self._year_picker.setTitle("年份")
        self._year_picker.spinBox().setAttribute(Qt.WA_TranslucentBackground)
        self._year_picker.spinBox().setValue(2025)
        self._year_picker.spinBox().setMaximum(2999)

        self._month_picker.setTitle("月份")
        self._month_picker.spinBox().setAttribute(Qt.WA_TranslucentBackground)
        self._month_picker.spinBox().setValue(1)

        self._day_picker.setTitle("日期")
        self._day_picker.spinBox().setAttribute(Qt.WA_TranslucentBackground)
        self._day_picker.spinBox().setValue(1)

        self._day_of_week_picker.setMinimumWidth(135)
        self._day_of_week_picker.setTitle("星期")
        self._day_of_week_picker.setSpinBox(SiWeekdaySpinBox(self))
        self._day_of_week_picker.spinBox().setFont(SiFont.getFont(size=24, weight=SiFont.Weight.Bold))
        self._day_of_week_picker.spinBox().setAttribute(Qt.WA_TranslucentBackground)
        self._day_of_week_picker.spinBox().lineEdit().setValidator(None)
        self._day_of_week_picker.spinBox().lineEdit().setText("w")

        self._set_to_today_button.setFixedSize(36, 36)
        self._set_to_today_button.setToolTip("设为今天")
        self._set_to_today_button.setSvgIcon(
            SiGlobal.siui.iconpack.get("ic_fluent_calendar_arrow_counterclockwise_regular"))

    def _initSignal(self) -> None:
        self._set_to_today_button.clicked.connect(self.setToToday)

        self._year_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._year_picker))
        self._month_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._month_picker))
        self._day_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._day_picker))
        self._day_of_week_picker.spinBox().increased.connect(
            lambda: self._onPickerScrolled(1, self._day_of_week_picker))

        self._year_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._year_picker))
        self._month_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._month_picker))
        self._day_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._day_picker))
        self._day_of_week_picker.spinBox().decreased.connect(
            lambda: self._onPickerScrolled(-1, self._day_of_week_picker))

    def _updatePickerByDate(self) -> None:
        day = self._date.day()
        month = self._date.month()
        year = self._date.year()
        weekday = self._date.dayOfWeek() - 1

        self._day_picker.spinBox().setValue(day)
        self._month_picker.spinBox().setValue(month)
        self._year_picker.spinBox().setValue(year)
        self._day_of_week_picker.spinBox().setValue(weekday)

    def _onPickerScrolled(self, delta: int, obj: SiWheelPickerHorizontal) -> None:
        if obj == self._day_of_week_picker or obj == self._day_picker:
            self._date = self._date.addDays(delta)
        elif obj == self._month_picker:
            self._date = self._date.addMonths(delta)
        elif obj == self._year_picker:
            self._date = self._date.addYears(delta)
        self._updatePickerByDate()

    def date(self) -> QDate:
        return self._date

    def setDate(self, date: QDate) -> None:
        self._date = date
        self._updatePickerByDate()

    def setToToday(self) -> None:
        self._date = QDate.currentDate()
        self._updatePickerByDate()


class SiCalenderDateWidget(QWidget):
    hovered = pyqtSignal(QWidget)
    clicked = pyqtSignal(QWidget)

    class VisualState:
        Muted = 0
        Normal = 1
        Highlighted = 2

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._font_normal = SiFont.getFont(size=12, weight=SiFont.Weight.Normal)
        self._font_bold = SiFont.getFont(size=12, weight=SiFont.Weight.Bold)

        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(self._font_normal)

        self._center_widget = label
        self._date = QDate.currentDate()

        self._click_flag = False
        self._default_visual_state = self.VisualState.Normal
        self._visual_state = self.VisualState.Normal

        self._initStyle()

    def _initStyle(self) -> None:
        self._center_widget.setStyleSheet("color: #D1CBD4")

    def setDate(self, date: QDate):
        # You can reimplement this method for a custom center widget
        self._center_widget.setText(str(date.day()))
        self._date = date

    def date(self) -> QDate:
        return self._date

    def centerWidget(self) -> QWidget:
        return self._center_widget

    def setCenterWidget(self, widget: QWidget) -> None:
        self._center_widget = widget
        self._center_widget.setParent(self)

    def resizeEvent(self, a0):
        self._center_widget.setGeometry(0, 0, self.width(), self.height())

    def enterEvent(self, a0):
        self.hovered.emit(self)

    def click(self):
        self.clicked.emit(self)

    def setVisualState(self, state) -> None:
        if state == self.VisualState.Muted:
            self._center_widget.setFont(self._font_normal)
            self._center_widget.setStyleSheet("color: #918497")

        if state == self.VisualState.Normal:
            self._center_widget.setFont(self._font_normal)
            self._center_widget.setStyleSheet("color: #D1CBD4")

        if state == self.VisualState.Highlighted:
            self._center_widget.setFont(self._font_bold)
            self._center_widget.setStyleSheet("color: #FFFFFF")

        self._visual_state = state

    def visualState(self) -> int:
        return self._visual_state

    def setDefaultVisualState(self, state) -> None:
        self._default_visual_state = state

    def defaultVisualState(self) -> int:
        return self._default_visual_state

    def mousePressEvent(self, a0):
        self._click_flag = True

    def mouseReleaseEvent(self, a0):
        if self._click_flag is True:
            self.click()
            self._click_flag = False


class AnimatedCalenderStyleData:
    indi_color_idle = QColor("#00D087DF")
    indi_color_active = QColor("#D087DF")
    cur_indi_color_idle = QColor("#004C4554")
    cur_indi_color_active = QColor("#4C4554")


class SiAnimatedCalender(SiDenseContainer):
    pageChanged = pyqtSignal(int)
    selectedDateChanged = pyqtSignal(QDate)
    # focus

    class Property:
        IndicatorPos = "indicatorPos"
        IndicatorColor = "indicatorColor"
        CursorIndicatorPos = "cursorIndicatorPos"
        CursorIndicatorColor = "cursorIndicatorColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.TopToBottom)

        self._date_widgets = []
        self._focused_date = QDate.currentDate()
        self._selected_date = QDate.currentDate()
        self._selected_widget = None  # 用于还原状态时节省性能，不可靠，应使用 _selected_date

        self.style_data = AnimatedCalenderStyleData()

        self._indi_size = QSize(36, 36)
        self._indi_pos = QPointF(0, 0)
        self._indi_color = QColor("#00D087DF")
        self._cur_indi_pos = QPointF(0, 0)
        self._cur_indi_color = QColor("#004C4554")

        self.ani_indi_pos = SiExpAnimationRefactor(self, self.Property.IndicatorPos)
        self.ani_indi_pos.init(1/4, 0.01, self._indi_pos, self._indi_pos)

        self.ani_indi_color = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.ani_indi_color.init(1/8, 0.01, self._indi_color, self._indi_color)

        self.ani_cur_indi_pos = SiExpAnimationRefactor(self, self.Property.CursorIndicatorPos)
        self.ani_cur_indi_pos.init(1/4, 0.01, self._cur_indi_pos, self._cur_indi_pos)

        self.ani_cur_indi_color = SiExpAnimationRefactor(self, self.Property.CursorIndicatorColor)
        self.ani_cur_indi_color.init(1/8, 0.01, self._cur_indi_color, self._cur_indi_color)

        self._createDayTypeLabels()
        self._createDayWidgets()
        self._initStyle()

        self.setSelectedDate(QDate.currentDate())

    def _initStyle(self) -> None:
        self.layout().setSpacing(0)
        self.layout().removeWidget(self.stretchWidget())

    @pyqtProperty(QPointF)
    def indicatorPos(self):
        return self._indi_pos

    @indicatorPos.setter
    def indicatorPos(self, value: QPointF):
        self._indi_pos = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indi_color

    @indicatorColor.setter
    def indicatorColor(self, value: QColor):
        self._indi_color = value
        self.update()

    @pyqtProperty(QPointF)
    def cursorIndicatorPos(self):
        return self._cur_indi_pos

    @cursorIndicatorPos.setter
    def cursorIndicatorPos(self, value: QPointF):
        self._cur_indi_pos = value
        self.update()

    @pyqtProperty(QColor)
    def cursorIndicatorColor(self):
        return self._cur_indi_color

    @cursorIndicatorColor.setter
    def cursorIndicatorColor(self, value: QColor):
        self._cur_indi_color = value
        self.update()

    def setFocusedDate(self, date: QDate) -> None:
        if self._focused_date.month() != date.month() or self._focused_date.year() != date.year():
            self._emitPageChangedSignal(1 if date > self._focused_date else -1)
            self._teleportIndicatorToDeltaPage(1 if date > self._focused_date else -1)

        self._focused_date = date

        year = date.year()
        month = date.month()
        days_in_month = QDate(year, month, 1).daysInMonth()
        first_weekday = QDate(year, month, 1).dayOfWeek()  # 1=Monday, 7=Sunday

        # 以当前月第一天为基础向前推 (first_weekday - 1) 天
        start_day = QDate(year, month, 1).addDays(- (first_weekday - 1))
        all_dates = [start_day.addDays(i) for i in range(42)]

        selected_date = self._selected_date

        for widget, day in zip(self._date_widgets, all_dates):
            widget.setDate(day)

            if day == selected_date:
                widget.setVisualState(widget.VisualState.Highlighted)
                widget.setDefaultVisualState(widget.VisualState.Normal)
                self._switchHighlightedWidgetTo(widget)

            elif day.month() == month:
                widget.setVisualState(widget.VisualState.Normal)
                widget.setDefaultVisualState(widget.VisualState.Normal)

            else:
                widget.setVisualState(widget.VisualState.Muted)
                widget.setDefaultVisualState(widget.VisualState.Muted)

        # 如果焦点的月份和已选择的月份不一样，隐藏指示器
        if self._focused_date.month() != self._selected_date.month():
            self._fadeOutIndicator()
        else:
            self._fadeInIndicator()

        # # 移动高亮指示器到当前月份中被选中的 widget 上
        # if selected_date and selected_date.month == month:
        #     for widget in self._date_widgets:
        #         if widget.date() == selected_date:
        #             self._switchHighlightedWidgetTo(widget)
        #             break
        # else:
        #     if self._selected_widget:
        #         self._selected_widget.setVisualState(self._selected_widget.defaultVisualState())

    def focusedDate(self) -> QDate:
        return self._focused_date

    def setSelectedDate(self, date: QDate) -> None:
        prev_date = self._selected_date
        self._selected_date = date
        self.setFocusedDate(date)
        if date != prev_date:
            self.selectedDateChanged.emit(date)

    def selectedDate(self) -> QDate:
        return self._selected_date

    def _createDayTypeLabels(self) -> None:
        container = SiDenseContainer(self, self.LeftToRight)
        container.layout().setSpacing(0)
        container.layout().removeWidget(container.stretchWidget())
        # container.setStyleSheet("background-color: red")

        text = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        font = SiFont.getFont(size=12, weight=SiFont.Weight.Bold)

        for i in range(7):
            new_label = QLabel(self)
            new_label.setFont(font)
            new_label.setText(text[i])
            new_label.setAlignment(Qt.AlignCenter)
            new_label.setStyleSheet("color: #D1CBD4")

            container.addWidget(new_label)

        self.addWidget(container)

    def _createDayWidgets(self) -> None:
        widgets = []
        for y in range(6):
            container = SiDenseContainer(self, self.LeftToRight)
            container.layout().setSpacing(0)
            container.layout().removeWidget(container.stretchWidget())

            for x in range(7):
                new_widget = SiCalenderDateWidget(self)
                new_widget.hovered.connect(self._onDateWidgetHovered)
                new_widget.clicked.connect(self._onDateWidgetClicked)
                new_widget.setDate(QDate.currentDate())
                widgets.append(new_widget)

                container.addWidget(new_widget)

            self.addWidget(container)

        self._date_widgets = widgets

    def _onDateWidgetHovered(self, widget: SiCalenderDateWidget):
        dx = (widget.width() - self._indi_size.width()) // 2
        dy = (widget.height() - self._indi_size.height()) // 2
        self.ani_cur_indi_pos.setEndValue(QPointF(widget.mapTo(self, QPoint(dx, dy))))
        self.ani_cur_indi_pos.start()

        self.ani_cur_indi_color.setEndValue(self.style_data.cur_indi_color_active)
        self.ani_cur_indi_color.start()

    def _onDateWidgetClicked(self, widget: SiCalenderDateWidget):
        self.ani_indi_color.setCurrentValue(self.style_data.indi_color_idle)
        self.ani_indi_color.setEndValue(self.style_data.indi_color_active)
        self.ani_indi_color.start()

        # update widget state
        self._switchHighlightedWidgetTo(widget)

        self.setSelectedDate(widget.date())

    def _fadeOutCursorIndicator(self) -> None:
        self.ani_cur_indi_color.setEndValue(self.style_data.cur_indi_color_idle)
        self.ani_cur_indi_color.start()

    def _fadeOutIndicator(self) -> None:
        self.ani_indi_color.setEndValue(self.style_data.indi_color_idle)
        self.ani_indi_color.start()

    def _fadeInIndicator(self) -> None:
        self.ani_indi_color.setEndValue(self.style_data.indi_color_active)
        self.ani_indi_color.start()

    def _emitPageChangedSignal(self, state: int):
        self.pageChanged.emit(state)

    def _teleportIndicatorToDeltaPage(self, state: int):
        self.ani_indi_pos.stop()
        self.ani_indi_pos.setCurrentValue(self.ani_indi_pos.currentValue() + QPointF(0, self.height()) * (-state))

    def _switchHighlightedWidgetTo(self, widget: SiCalenderDateWidget) -> None:
        dx = (widget.width() - self._indi_size.width()) // 2
        dy = (widget.height() - self._indi_size.height()) // 2
        self.ani_indi_pos.setEndValue(QPointF(widget.mapTo(self, QPoint(dx, dy))))
        self.ani_indi_pos.start()

        # if self.isVisible() is False:
        #     self.ani_indi_pos.setCurrentValue(self.ani_indi_pos.endValue())
        #     self.ani_indi_pos.toProperty()

        if self._selected_widget is not None:
            self._selected_widget.setVisualState(self._selected_widget.defaultVisualState())

        self._selected_widget = widget
        widget.setVisualState(widget.VisualState.Highlighted)

    def _drawIndicator(self, painter: QPainter) -> None:
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(self._indi_pos.x(), self._indi_pos.y(),
                   self._indi_size.width(), self._indi_size.height()),
            self._indi_size.width() / 2, self._indi_size.height() / 2
        )
        painter.setBrush(self._indi_color)
        painter.drawPath(path)

    def _drawCursorIndicator(self, painter: QPainter) -> None:
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(self._cur_indi_pos.x(), self._cur_indi_pos.y(),
                   self._indi_size.width(), self._indi_size.height()),
            self._indi_size.width() / 2, self._indi_size.height() / 2
        )
        painter.setBrush(self._cur_indi_color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        rect = self.rect()
        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawCursorIndicator(painter)
            self._drawIndicator(painter)

    def leaveEvent(self, a0):
        self._fadeOutCursorIndicator()


class SiPopoverCalenderPicker(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, self.LeftToRight)

        self._date = QDate.currentDate()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent")

        self._calender = SiAnimatedCalender(self)
        self._separator = QWidget(self)

        self._pickers_container = SiDenseContainer(self, self.TopToBottom)
        self._all_btn_container = SiDenseContainer(self, self.LeftToRight)
        self._calender_btn_container = SiDenseContainer(self, self.TopToBottom)
        self._picker_btn_container = SiDenseContainer(self, self.TopToBottom)

        self._createPickers()
        self._createCalenderButton()
        self._createPickerButton()

        self._pickers_container.addWidget(self._all_btn_container, Qt.BottomEdge)

        self.addWidget(self._calender)
        self.addWidget(self._separator)
        self.addWidget(self._pickers_container, side=Qt.RightEdge)

        self._initStyle()
        self._initSignal()

        self.setToToday()

    def _createPickers(self) -> None:
        self._year_picker = SiWheelPickerVertical(self)
        self._month_picker = SiWheelPickerVertical(self)
        self._day_picker = SiWheelPickerVertical(self)

        self._year_picker.setTitle("年")
        self._month_picker.setTitle("月")
        self._day_picker.setTitle("日")

        self._year_picker.spinBox().setRange(1840, 3000)
        self._month_picker.spinBox().setRange(1, 12)
        self._day_picker.spinBox().setRange(1, 31)

        self._year_picker.setDirection(self.RightToLeft)
        self._month_picker.setDirection(self.RightToLeft)
        self._day_picker.setDirection(self.RightToLeft)

        self._pickers_container.addWidget(self._year_picker)
        self._pickers_container.addWidget(self._month_picker)
        self._pickers_container.addWidget(self._day_picker)

        self._pickers_container.layout().setAlignment(self._year_picker, Qt.AlignRight)

    def _createCalenderButton(self) -> None:
        self._prev_page_btn = SiFlatButton(self)
        self._prev_page_btn.setToolTip("上一页")
        self._next_page_btn = SiFlatButton(self)
        self._next_page_btn.setToolTip("下一页")

        self._calender_btn_container.addWidget(self._next_page_btn, Qt.BottomEdge)
        self._calender_btn_container.addWidget(self._prev_page_btn, Qt.BottomEdge)

        self._all_btn_container.addWidget(self._calender_btn_container, Qt.LeftEdge)

    def _createPickerButton(self) -> None:
        self._set_to_today_btn = SiFlatButton(self)
        self._set_to_today_btn.setToolTip("设为今天")

        self._picker_btn_container.addWidget(self._set_to_today_btn, Qt.BottomEdge)
        self._all_btn_container.addWidget(self._picker_btn_container, Qt.RightEdge)

    def _initStyle(self) -> None:
        self.layout().setSpacing(4)

        self._separator.setFixedWidth(1)
        self._separator.setStyleSheet("background-color: #25222A; margin: 24px 0px 20px 0px")

        self._calender.setFixedSize(306, 300)
        self._calender.layout().setContentsMargins(12, 8, 12, 8)

        self._pickers_container.setMinimumWidth(128+18+16)
        self._pickers_container.layout().setContentsMargins(0, 20, 18, 16)
        self._pickers_container.layout().setSpacing(10)

        self._next_page_btn.setFixedSize(36, 36)
        self._next_page_btn.setSvgIcon(
            SiGlobal.siui.iconpack.get("ic_fluent_caret_down_filled"))

        self._prev_page_btn.setFixedSize(36, 36)
        self._prev_page_btn.setSvgIcon(
            SiGlobal.siui.iconpack.get("ic_fluent_caret_up_filled"))

        self._set_to_today_btn.setFixedSize(36, 36)
        self._set_to_today_btn.setSvgIcon(
            SiGlobal.siui.iconpack.get("ic_fluent_calendar_arrow_counterclockwise_regular"))

        self._calender_btn_container.layout().setSpacing(8)
        self._calender_btn_container.muteStretchWidget()

    def _initSignal(self) -> None:
        # self._set_to_today_button.clicked.connect(self.setToToday)

        self._year_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._year_picker))
        self._month_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._month_picker))
        self._day_picker.spinBox().increased.connect(lambda: self._onPickerScrolled(1, self._day_picker))

        self._year_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._year_picker))
        self._month_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._month_picker))
        self._day_picker.spinBox().decreased.connect(lambda: self._onPickerScrolled(-1, self._day_picker))

        self._calender.selectedDateChanged.connect(self._onSelectedDateChanged)

        self._set_to_today_btn.clicked.connect(self.setToToday)
        self._prev_page_btn.clicked.connect(
            lambda: self._calender.setFocusedDate(self._calender.focusedDate().addMonths(-1)))
        self._next_page_btn.clicked.connect(
            lambda: self._calender.setFocusedDate(self._calender.focusedDate().addMonths(1)))

    def _updatePickerByDate(self) -> None:
        day = self._date.day()
        month = self._date.month()
        year = self._date.year()

        self._day_picker.spinBox().setValue(day)
        self._month_picker.spinBox().setValue(month)
        self._year_picker.spinBox().setValue(year)

        self._calender.setSelectedDate(self._date)

    def _onPickerScrolled(self, delta: int, obj: SiWheelPickerHorizontal) -> None:
        if obj == self._day_picker:
            self._date = self._date.addDays(delta)
        elif obj == self._month_picker:
            self._date = self._date.addMonths(delta)
        elif obj == self._year_picker:
            self._date = self._date.addYears(delta)
        self._updatePickerByDate()

    def _onSelectedDateChanged(self, date: QDate) -> None:
        self._date = date
        self._updatePickerByDate()

    def date(self) -> QDate:
        return self._date

    def setDate(self, date: QDate) -> None:
        self._date = date
        self._updatePickerByDate()

    def setToToday(self) -> None:
        self.setDate(QDate.currentDate())
