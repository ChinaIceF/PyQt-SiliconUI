
import datetime

from dateutil.relativedelta import relativedelta
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from siui.components import SiDenseHContainer, SiDenseVContainer, SiFlashLabel, SiLabel, SiSimpleButton, SiWidget
from siui.components.menu.abstracts import AnimationManager
from siui.components.menu.menu import SiInteractionMenu
from siui.core import SiColor, SiGlobal
from siui.gui import SiFont


class CalenderDateWidget(SiWidget):
    entered = pyqtSignal(QPoint)
    clicked = pyqtSignal(datetime.date)

    def __init__(self, date: datetime.date, parent):
        super().__init__(parent)

        self.date = None
        self.pressed_flag = False

        self.indicator = SiLabel(self)
        self.indicator.setFixedSize(36, 36)
        self.indicator.setFixedStyleSheet("border-radius: 18px")
        self.indicator.setColor(self.getColor(SiColor.SIDE_MSG_THEME_INFO))
        self.indicator.setOpacity(0)
        # self.indicator.hide()

        self.day_label = SiLabel(self)
        self.day_label.setFixedSize(36, 36)
        self.day_label.setAlignment(Qt.AlignCenter)
        self.day_label.setTextColor(self.getColor(SiColor.TEXT_B))

        self.setDate(date)

    def setDate(self, date):
        self.date = date
        self.day_label.setText(str(self.date.day))
        self.day_label.adjustSize()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.entered.emit(self.pos())

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        self.pressed_flag = True

    def mouseReleaseEvent(self, a0):
        super().mouseReleaseEvent(a0)
        if self.pressed_flag:
            self.clicked.emit(self.date)
            self.pressed_flag = False


class CalenderWidget(SiDenseVContainer):
    dateChanged = pyqtSignal(datetime.date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_date = datetime.date.today()
        self.displayed_date = datetime.date.today()
        self.setAlignment(Qt.AlignCenter)

        year_month_container = SiDenseHContainer(self)
        year_month_container.setFixedWidth(300 - 24)
        year_month_container.setFixedHeight(64)
        year_month_container.setSpacing(0)
        year_month_container.setAlignment(Qt.AlignCenter)

        self.year_month_label = SiFlashLabel(self)
        self.year_month_label.flash_layer.setFixedStyleSheet("border-radius: 4px")
        self.year_month_label.setTextColor(self.getColor(SiColor.TEXT_B))
        self.year_month_label.resize(96, 32)
        self.year_month_label.setContentsMargins(12, 6, 12, 6)
        self.year_month_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.prev_month_button = SiSimpleButton(self)
        self.prev_month_button.attachment().setSvgSize(16, 16)
        self.prev_month_button.attachment().load(SiGlobal.siui.iconpack.get(
            "ic_fluent_caret_up_filled", color_code=self.getColor(SiColor.SVG_NORMAL)))
        self.prev_month_button.resize(32, 32)
        self.prev_month_button.setHint("上一页")
        self.prev_month_button.clicked.connect(lambda: self.modifyDisplayedDate(-1))

        self.next_month_button = SiSimpleButton(self)
        self.next_month_button.attachment().setSvgSize(16, 16)
        self.next_month_button.attachment().load(SiGlobal.siui.iconpack.get(
            "ic_fluent_caret_down_filled", color_code=self.getColor(SiColor.SVG_NORMAL)))
        self.next_month_button.resize(32, 32)
        self.next_month_button.setHint("下一页")
        self.next_month_button.clicked.connect(lambda: self.modifyDisplayedDate(1))

        year_month_container.addWidget(self.year_month_label)
        year_month_container.addWidget(self.next_month_button, side="right")
        year_month_container.addPlaceholder(8, side="right")
        year_month_container.addWidget(self.prev_month_button, side="right")

        self.calender_date_container = SiWidget(self)

        self.highlight = SiLabel(self.calender_date_container)
        self.highlight.setFixedStyleSheet("border-radius: 18px")
        self.highlight.resize(36, 36)
        self.highlight.setColor(SiColor.trans(self.getColor(SiColor.INTERFACE_BG_D), 1))

        # year, month = self.displayed_date.year, self.displayed_date.month
        # first_day = datetime.datetime(year, month, 1)
        # days_in_month = calendar.monthrange(year, month)
        # week_counter = 0
        # for day in range(1, days_in_month[1]):
        #     this_widget = CalenderDateWidget(first_day, self.calender_date_container)
        #     this_widget.resize(36, 36)
        #     this_widget.move(first_day.weekday() * 40, week_counter * 40)
        #     this_widget.entered.connect(self.highlight_moveto)
        #     week_counter += 1 if first_day.weekday() == 6 else 0
        #     first_day = first_day.replace(day=first_day.day+1)
        weekday_name = ["MON", "TUE", "WED", "TUS", "FRI", "SAT", "SUN"]
        # weekday_name = ["一", "二", "三", "四", "五", "六", "日"]
        for i in range(7):
            this_widget = SiLabel(self.calender_date_container)
            this_widget.setFont(SiFont.getFont(size=12, weight=QFont.Weight.DemiBold))
            this_widget.resize(36, 36)
            this_widget.setAlignment(Qt.AlignCenter)
            this_widget.setTextColor(self.getColor(SiColor.TEXT_B))
            this_widget.setText(weekday_name[i])
            this_widget.move(i * 40, 0)

        self.date_labels = []
        for i in range(6):
            self.row_labels = []
            for j in range(7):
                this_widget = CalenderDateWidget(self.displayed_date, self.calender_date_container)
                this_widget.resize(36, 36)
                this_widget.move(j * 40, i * 38 + 40)
                this_widget.entered.connect(self.highlight_moveto)
                this_widget.clicked.connect(self.on_date_chose)
                self.row_labels.append(this_widget)
            self.date_labels.append(self.row_labels)

        self.calender_date_container.adjustSize()
        self.calender_date_container.enterEvent = lambda a0: self.highlight.setOpacityTo(0.99)
        self.calender_date_container.leaveEvent = lambda a0: self.highlight.setOpacityTo(0)

        self.addWidget(year_month_container)
        self.addWidget(self.calender_date_container)
        self.updateCalendar()
        self.updateYearMonthLabel()

    def modifyDisplayedDate(self, month_delta):
        self.displayed_date = self.displayed_date.replace(day=1)  # 归一化，防止因日期引起的切换错误，日期不重要，月份重要
        self.displayed_date = self.displayed_date + relativedelta(months=month_delta)
        self.updateCalendar()
        self.updateYearMonthLabel()

    def getDisplayedDate(self):
        return self.displayed_date

    def updateCalendar(self):
        today = self.displayed_date
        first_day_of_month = today.replace(day=1)
        weekday_of_first = first_day_of_month.weekday()

        start_day = first_day_of_month - datetime.timedelta(days=weekday_of_first)

        for i in range(6):
            for j in range(7):
                current_day = start_day + datetime.timedelta(days=i * 7 + j)
                self.date_labels[i][j].setDate(current_day)
                self.date_labels[i][j].indicator.setOpacityTo(0)

                if current_day.month == today.month:
                    self.date_labels[i][j].day_label.setTextColor(self.getColor(SiColor.TEXT_B))
                else:
                    self.date_labels[i][j].day_label.setTextColor(SiColor.trans(self.getColor(SiColor.TEXT_B), 0.4))

                if current_day == self.selected_date:
                    self.date_labels[i][j].indicator.setOpacityTo(0.99)

    def highlight_moveto(self, point: QPoint):
        self.highlight.moveTo(point.x(), point.y())

    def on_date_chose(self, date: datetime.date):
        self.selected_date = date
        self.dateChanged.emit(date)
        self.updateCalendar()

    def updateYearMonthLabel(self):
        year = self.displayed_date.year
        month = self.displayed_date.month
        self.year_month_label.setText(f"{year:04d}年{month:02d}月")
        self.year_month_label.adjustSize()
        self.year_month_label.flash()


class SiCalenderView(SiWidget):
    dateChanged = pyqtSignal(datetime.date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu = SiInteractionMenu()
        self.menu.padding = 0
        self.menu.setContentFixedWidth(306)
        self.menu.setAnimationManager(AnimationManager.RAISE_UP)
        # self.menu.colorGroup().assign(SiColor.MENU_BG, self.getColor(SiColor.INTERFACE_BG_B))

        self.calender_header_bg = SiLabel(self.menu.body_panel)
        self.calender_header_bg.setFixedSize(304, 64)
        self.calender_header_bg.setFixedStyleSheet("border-radius: 4px")
        self.calender_header_bg.setColor(self.getColor(SiColor.INTERFACE_BG_B))
        self.calender_header_bg.move(1, 1)
        self.calender_header_bg.stackUnder(self.menu.body_)

        self.button = SiSimpleButton(self)
        self.button.attachment().setText("选择日期")
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_calendar_edit_regular"))
        self.button.adjustSize()
        self.button.clicked.connect(self._on_unfold_button_clicked)

        self.calender_widget = CalenderWidget(self)
        self.calender_widget.setFixedSize(306, 364)
        self.calender_widget.dateChanged.connect(self.on_date_changed)

        self.menu.body_.setAdjustWidgetsSize(True)
        self.menu.body_.addWidget(self.calender_widget)

    def on_date_changed(self, date: datetime.date):
        self.dateChanged.emit(date)
        self.button.attachment().setText(str(date))
        self.button.adjustSize()
        self.adjustSize()
        self.menu.close()

    def _on_unfold_button_clicked(self):
        gap = 2 * self.menu.margin + 2 * self.menu.padding
        pos = self.mapToGlobal(
            QPoint((self.width() - (self.menu.width() - gap)) // 2, -self.menu.sizeHint().height() + gap))
        self.menu.unfold(pos.x(), pos.y())

    def setDate(self, date: datetime.date):
        self.calender_widget.on_date_chose(date)

