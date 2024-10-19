import calendar
import datetime

from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from siui.components import SiDenseHContainer, SiDenseVContainer, SiLabel, SiSimpleButton, SiWidget
from siui.components.menu.menu import SiInteractionMenu
from siui.core import SiColor, SiGlobal


class CalenderDateWidget(SiWidget):
    entered = pyqtSignal(QPoint)

    def __init__(self, date: datetime.date, parent):
        super().__init__(parent)

        self.date = None

        self.indicator = SiLabel(self)
        self.indicator.setFixedSize(36, 36)
        self.indicator.setFixedStyleSheet("border-radius: 18px")
        self.indicator.setColor(self.getColor(SiColor.SIDE_MSG_THEME_INFO))
        self.indicator.hide()

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


class CalenderWidget(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_date = datetime.date.today()
        self.displayed_date = datetime.date.today()
        self.setAlignment(Qt.AlignCenter)

        year_month_container = SiDenseHContainer(self)
        year_month_container.setFixedHeight(64)
        year_month_container.setSpacing(2)
        year_month_container.setAlignment(Qt.AlignCenter)

        self.year_month_label = SiLabel(self)
        self.year_month_label.setTextColor(self.getColor(SiColor.TEXT_B))
        self.year_month_label.setFixedSize(96, 48)
        self.year_month_label.setAlignment(Qt.AlignCenter)

        self.prev_month_button = SiSimpleButton(self)
        self.prev_month_button.attachment().load(SiGlobal.siui.iconpack.get(
            "ic_fluent_chevron_left_filled", color_code=self.getColor(SiColor.SVG_NORMAL)))
        self.prev_month_button.resize(32, 32)
        self.prev_month_button.setHint("上一页")

        self.next_month_button = SiSimpleButton(self)
        self.next_month_button.attachment().load(SiGlobal.siui.iconpack.get(
            "ic_fluent_chevron_right_filled", color_code=self.getColor(SiColor.SVG_NORMAL)))
        self.next_month_button.resize(32, 32)
        self.next_month_button.setHint("下一页")

        year_month_container.addWidget(self.prev_month_button)
        year_month_container.addWidget(self.year_month_label)
        year_month_container.addWidget(self.next_month_button)

        self.calender_date_container = SiWidget(self)

        self.highlight = SiLabel(self.calender_date_container)
        self.highlight.setFixedStyleSheet("border-radius: 18px")
        self.highlight.resize(36, 36)
        self.highlight.setColor(SiColor.trans(self.getColor(SiColor.SIDE_MSG_THEME_INFO), 0.2))

        year, month = self.displayed_date.year, self.displayed_date.month
        first_day = datetime.datetime(year, month, 1)
        days_in_month = calendar.monthrange(year, month)
        week_counter = 0
        for day in range(1, days_in_month[1]):
            this_widget = CalenderDateWidget(first_day, self.calender_date_container)
            this_widget.resize(36, 36)
            this_widget.move(first_day.weekday() * 40, week_counter * 40)
            this_widget.entered.connect(self.highlight_moveto)
            week_counter += 1 if first_day.weekday() == 6 else 0
            first_day = first_day.replace(day=first_day.day+1)
        self.calender_date_container.adjustSize()
        self.calender_date_container.enterEvent = lambda a0: self.highlight.setOpacityTo(0.99)
        self.calender_date_container.leaveEvent = lambda a0: self.highlight.setOpacityTo(0)

        self.addWidget(year_month_container)
        self.addWidget(self.calender_date_container)
        self.update_info()

    def highlight_moveto(self, point: QPoint):
        self.highlight.moveTo(point.x(), point.y())

    def getDisplayedDate(self):
        return self.displayed_date

    def update_info(self):
        year = self.selected_date.year
        month = self.selected_date.month
        self.year_month_label.setText(f"{year:04d}.{month:02d}")


class SiCalenderView(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu = SiInteractionMenu()
        self.menu.setContentFixedWidth(300)
        self.menu.padding = 0
        # self.menu.colorGroup().assign(SiColor.MENU_BG, self.getColor(SiColor.INTERFACE_BG_B))

        self.calender_header_bg = SiLabel(self.menu.body_panel)
        self.calender_header_bg.setFixedSize(306, 64)
        self.calender_header_bg.setFixedStyleSheet("border-radius: 4px")
        self.calender_header_bg.setColor(self.getColor(SiColor.INTERFACE_BG_B))
        self.calender_header_bg.move(1, 1)
        self.calender_header_bg.stackUnder(self.menu.body_)

        self.button = SiSimpleButton(self)
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_calendar_edit_regular"))
        self.button.resize(32, 32)
        self.button.clicked.connect(self._on_unfold_button_clicked)

        self.calender_widget = CalenderWidget(self)
        self.calender_widget.setFixedSize(300, 400)

        self.menu.body_.setAdjustWidgetsSize(True)
        self.menu.body_.addWidget(self.calender_widget)

    def _on_unfold_button_clicked(self):
        pos = self.mapToGlobal(
            QPoint((self.width() - (self.menu.width() - 2 * self.menu.margin - 2 * self.menu.padding)) // 2, 0))
        self.menu.unfold(pos.x(), pos.y())
