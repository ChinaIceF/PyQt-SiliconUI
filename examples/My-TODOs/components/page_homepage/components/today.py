import datetime
import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor, QFont

from siui.components import SiDenseHContainer, SiDenseVContainer, SiLabel, SiWidget
from siui.core import Si, SiColor
from siui.gui import SiFont

from ...core import Task
from ...widgets import RectButtonWithIconAndDescription


class TaskIndicator(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.padding_top = 0
        self.time_stamp = 0

        self.indicator = SiLabel(self)
        self.indicator.setFixedSize(8, 20)
        self.indicator.setFixedStyleSheet("border-radius: 4px")
        self.indicator.setColor(self.getColor(SiColor.PROGRESS_BAR_PROCESSING))
        self.indicator.move(0, 0)

    def setTimeStamp(self, time_stamp):
        self.time_stamp = time_stamp

    def timeStamp(self):
        return self.time_stamp

    def setColor(self, color_code):
        self.indicator.setColor(color_code)

    def setPadding(self, padding_top):
        self.padding_top = padding_top
        self.resize(self.size())

    def enterEvent(self, a0):
        super().enterEvent(a0)
        parent = self.parent().parent()
        parent.setTracking(False)
        parent.task_selector.moveTo(self.x(), 0)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        parent = self.parent().parent()
        parent.setTracking(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.indicator.move((event.size().width() - self.indicator.width()) // 2, self.padding_top)


class TaskIndicatorContainer(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indicators = []

    def addTask(self, task: Task):
        d = datetime.datetime.fromtimestamp(task.due_time_stamp)
        r = d - datetime.datetime.fromtimestamp(time.time())
        dim_color = SiColor.mix(self.getColor(SiColor.TEXT_B), task.color)

        new_task = TaskIndicator(self)
        new_task.setFixedStyleSheet("border-radius: 4px")
        new_task.setFixedWidth(20)
        new_task.setColor(task.color)
        new_task.setTimeStamp(task.due_time_stamp)

        new_task.setHint(
            f'<span style="color: {task.color}"><strong>{task.name}</strong></span><br>'
            f"{task.description}<p>"
            f'<span style="color: {dim_color}">截止时间：</span>{d.hour:02d}h {d.minute:02d}m<br>'
            f'<span style="color: {dim_color}">剩余时间：</span>{r.seconds // 3600:02d}h {(r.seconds % 3600) // 60:02d}m'
        )

        self.indicators.append(new_task)

    def setPadding(self, padding):
        for indicator in self.indicators:
            indicator.setPadding(padding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        td_timestamp = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()

        for indicator in self.indicators:
            percentage = (indicator.timeStamp() - td_timestamp) / (24 * 60 * 60)
            x = int((self.width() - indicator.width()) * percentage)
            indicator.setGeometry(x, 0, indicator.width(), event.size().height())


class DateDisplay(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.debug = SiLabel(self)
        self.debug.resize(196, 196)
        self.setCenterWidget(self.debug)

        self.month_widget = SiWidget(self)
        self.month_label = SiLabel(self.month_widget)
        self.month_mask = SiLabel(self.month_widget)

        self.date_widget = SiWidget(self)
        self.date_label = SiLabel(self.date_widget)

        self.month_label.setFont(SiFont.getFont(size=64, weight=QFont.Weight.Light, italic=True))
        self.date_label.setFont(SiFont.getFont(size=64, weight=QFont.Weight.Bold, italic=False))

        self.month_label.setTextColor(self.getColor(SiColor.TEXT_D))
        self.date_label.setTextColor(self.getColor(SiColor.TEXT_B))

        self.month_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.date_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.month_label.setFixedSize(128, 56)
        self.date_label.setFixedSize(128, 56)

        self.month_widget.move(-8, 50)
        self.date_widget.move(82, 50 + 27)

    def setMonthAndDate(self, month, date):
        self.month_label.setText(f"{month:02d} ")
        self.date_label.setText(f"{date:02d}")


class TaskSelector(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.padding_top = 10
        self.margin_top = 0

        self.stick_up = SiLabel(self)
        self.stick_down = SiLabel(self)

        self.stick_up.setFixedStyleSheet("border-radius: 1px")
        self.stick_down.setFixedStyleSheet("border-radius: 1px")

        self.stick_up.setColor(self.getColor(SiColor.TEXT_B))
        self.stick_down.setColor(self.getColor(SiColor.TEXT_B))

        self.selector = SiLabel(self)
        self.selector.resize(20, 32)

        self.selector.hide()
        self.stick_up.setFixedWidth(2)
        self.stick_down.setFixedWidth(2)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.selector.setStyleSheet(
            "border-radius: 8px;"
            f"border: 3px solid {self.getColor(SiColor.TEXT_B)}"
        )

    def setPadding(self, padding):
        self.padding_top = padding
        self.resize(self.size())

    def setMarginTop(self, margin):
        self.margin_top = margin
        self.resize(self.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()

        self.stick_up.setGeometry((w - self.stick_up.width()) // 2,
                                  self.margin_top,
                                  self.stick_up.width(),
                                  self.padding_top - self.margin_top)

        self.stick_down.setGeometry((w - self.stick_up.width()) // 2,
                                    self.stick_up.height() + self.selector.height() + self.margin_top,
                                    self.stick_down.width(),
                                    h - self.stick_up.height() - self.selector.height() - self.margin_top * 2)

        self.selector.move(0, self.stick_up.height())


class TaskDisplay(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.enabled_tracking = True
        self.setMouseTracking(True)

        self.task_track = SiLabel(self)
        self.task_track.setFixedStyleSheet("border-radius: 2px")
        self.task_track.setColor(self.getColor(SiColor.INTERFACE_BG_E))
        self.task_track.setFixedHeight(4)

        self.task_selector = TaskSelector(self)
        self.task_selector.setFixedWidth(20)
        self.task_selector.setMarginTop(0)
        self.task_selector.setOpacity(0)

        self.current_time_selector = TaskSelector(self)
        self.current_time_selector.setFixedWidth(20)
        self.current_time_selector.setMarginTop(12)
        self.current_time_selector.setOpacity(1)

        self.task_indicator_container = TaskIndicatorContainer(self)

        new_task_data1 = Task("回家睡觉", "躺下来闭上眼，睡觉就行", time.time() + 10000,
                              self.getColor(SiColor.PROGRESS_BAR_COMPLETING))
        new_task_data2 = Task("写作业", "不写作业怎么交作业呢", time.time() - 20000,
                              self.getColor(SiColor.PROGRESS_BAR_PROCESSING))
        self.task_indicator_container.addTask(new_task_data1)
        self.task_indicator_container.addTask(new_task_data2)

        self.mouse_tracking_timer = QTimer(self)
        self.mouse_tracking_timer.setInterval(1000 // 60)
        self.mouse_tracking_timer.timeout.connect(self.mouse_tracking)

        self.time_updating_timer = QTimer(self)
        self.time_updating_timer.setInterval(50000)
        self.time_updating_timer.timeout.connect(self.time_updating)
        self.time_updating_timer.start()

    def setTracking(self, state):
        self.enabled_tracking = state

    def mouse_tracking(self):
        if self.enabled_tracking is False:
            return
        self.task_selector.moveTo(self.mapFromGlobal(QCursor.pos()).x() - self.task_selector.width() // 2, 0)

    def time_updating(self):
        today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        now = datetime.datetime.now()
        seconds_passed = (now - today_start).seconds
        total_seconds_today = 24 * 60 * 60
        percentage_passed = seconds_passed / total_seconds_today

        self.current_time_selector.move(
            int((self.width() - self.current_time_selector.width()) * percentage_passed), 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        y = int(event.size().height() * 0.618)

        self.task_selector.resize(self.task_selector.width(), event.size().height())
        self.task_selector.setMoveLimits(0, 0, event.size().width(), event.size().height())
        self.task_selector.setPadding(y - 14)

        self.current_time_selector.resize(self.current_time_selector.width(), event.size().height())
        self.current_time_selector.setPadding(y - 14)

        self.task_indicator_container.setPadding(y - 8)
        self.task_indicator_container.setGeometry(0, 0, event.size().width() - 0, event.size().height())

        self.task_track.setGeometry(10, y, event.size().width() - 20, 4)

        self.time_updating()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.task_selector.setOpacityTo(1)
        self.current_time_selector.setOpacityTo(0.2)
        self.mouse_tracking_timer.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.task_selector.setOpacityTo(0)
        self.current_time_selector.setOpacityTo(1)
        self.mouse_tracking_timer.stop()


class DataItem(SiDenseVContainer):
    def __init__(self, title, data, size_title, size_data, parent=None):
        super().__init__(parent)

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=size_title, weight=QFont.Weight.Normal))
        self.title.setTextColor(self.getColor(SiColor.TEXT_D))
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.setText(str(title))

        self.data = SiLabel(self)
        self.data.setFont(SiFont.getFont(size=size_data, weight=QFont.Weight.Light))
        self.data.setTextColor(self.getColor(SiColor.TEXT_B))
        self.data.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.data.setText(str(data))

        self.setAlignment(Qt.AlignLeft)
        self.setSpacing(0)
        self.addWidget(self.title)
        self.addWidget(self.data)

    def load(self, title, data):
        self.title.setText(str(title))
        self.data.setText(str(data))


class TodayTasksTimeLine(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.month = 0
        self.date = 0

        self.task_display = TaskDisplay(self)
        self.task_display.resize(0, 120)

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        half_height = (event.size().height() - self.task_display.height()) // 2
        self.task_display.setGeometry(half_height, half_height, event.size().width(), self.task_display.height())


class TodayDataTop(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_date = DataItem("当前日期", "-", 14, 32, parent=self)
        self.data_time = DataItem("当前时间", "-", 14, 32, parent=self)
        self.data_remaining_tasks = DataItem("今天剩余待办数", "-", 14, 32, parent=self)
        self.data_time.setFixedWidth(120)

        self.refresh_data()
        self.data_date.adjustSize()
        self.data_time.adjustSize()
        self.data_remaining_tasks.adjustSize()

        self.setSpacing(32)
        self.addWidget(self.data_date)
        self.addWidget(self.data_time)
        self.addWidget(self.data_remaining_tasks)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(500)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start()

    def refresh_data(self):
        now = datetime.datetime.now()
        self.data_date.load("当前日期", f"{now.year}.{now.month}.{now.day}")
        self.data_time.load("当前时间", f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}")
        self.data_remaining_tasks.load("今天剩余待办数", "2")


class TodayDataBottom(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accumulate_tasks = DataItem("累计完成待办", "114", 12, 24, parent=self)
        self.accumulate_memos = DataItem("累计完成备忘", "514", 12, 24, parent=self)
        self.accumulate_focus = DataItem("累计专注时长", "1919h", 12, 24, parent=self)

        self.setSpacing(32)
        self.addWidget(self.accumulate_tasks)
        self.addWidget(self.accumulate_memos)
        self.addPlaceholder(2, side="right")
        self.addWidget(self.accumulate_focus, side="right")

        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(500)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start()

    def refresh_data(self):
        self.accumulate_tasks.load("累计完成待办", "114")
        self.accumulate_memos.load("累计完成备忘", "514")
        self.accumulate_focus.load("累计专注时长", "1919h")



class TodayOperation(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(8)
        self.setAdjustWidgetsSize(True)

        self.new_task = RectButtonWithIconAndDescription("新建待办", "提醒自己该做什么", "ic_fluent_check_filled", parent=self)
        self.new_task.setFixedHeight(80)

        self.new_memo = RectButtonWithIconAndDescription("新建备忘", "摆脱遗忘的烦恼", "ic_fluent_notebook_filled", parent=self)
        self.new_memo.setFixedHeight(80)

        self.start_focusing = RectButtonWithIconAndDescription("开始专注", "记录下你的付出", "ic_fluent_timer_filled", parent=self)
        self.start_focusing.setFixedHeight(80)

        self.addWidget(self.start_focusing, side="bottom")
        self.addWidget(self.new_memo, side="bottom")
        self.addWidget(self.new_task, side="bottom")

    def resizeEvent(self, event):
        super().resizeEvent(event)


class TodayMainWidget(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.today_data_top = TodayDataTop(self)
        self.today_data_top.adjustSize()

        self.today_tasks = TodayTasksTimeLine(self)
        self.today_tasks.setFixedHeight(129)

        self.today_data_bottom = TodayDataBottom(self)
        self.today_data_bottom.adjustSize()

        self.today_operation = TodayOperation(self)
        self.today_operation.setFixedWidth(240)

        # self.memos_container = SiLabel(self)
        # self.memos_container.setFixedStyleSheet("border-radius: 4px")
        # self.memos_container.setColor(self.getColor(SiColor.INTERFACE_BG_C))

    def adjustSize(self):
        height = self.today_data_top.height() + 8 + self.today_tasks.height() + 8 + self.today_data_bottom.height()
        self.resize(self.width(), height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        gap = self.today_operation.width() + 16
        self.today_data_top.resize(event.size().width() - gap, self.today_data_top.height())

        self.today_tasks.setGeometry(
            0, self.today_data_top.height() + 8, event.size().width() - gap, self.today_tasks.height())

        self.today_data_bottom.setGeometry(
            0, self.today_data_top.height() + 8 + self.today_tasks.height() + 8,
            event.size().width() - gap, self.today_data_bottom.height())

        self.today_operation.setGeometry(
            event.size().width() - gap + 16, 0, self.today_operation.width(), event.size().height())

        # self.memos_container.setGeometry(event.size().width() - gap - 160 - 8, 0, 160, 54)
