from siui.components import SiLabel, SiMasonryContainer, SiScrollArea, SiWidget
from siui.components.widgets.abstracts.table import ABCSiTabelManager, ABCSiTable, SiRow
from siui.core import GlobalFont, Si, SiColor
from siui.gui import SiFont


class SiTableValueManagerLabels(ABCSiTabelManager):
    def _value_read_parser(self, row_index, col_index):
        return self.parent().getRowWidget(row_index)[col_index].text()

    def _value_write_parser(self, row_index, col_index, value):
        self.parent().getRowWidget(row_index)[col_index].setText(value)

    def _widget_creator(self, col_index):
        label = SiLabel(self.parent())
        label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        label.setFixedStyleSheet("color: #e5e5e5")
        return label

    def on_header_created(self, header: SiRow):
        for name in self.parent().column_names:
            new_label = SiLabel(self.parent())
            new_label.setFont(SiFont.tokenized(GlobalFont.S_BOLD))
            new_label.setTextColor(self.parent().getColor(SiColor.TEXT_B))
            new_label.setText(name)
            new_label.adjustSize()
            header.container().addWidget(new_label)

        header.container().arrangeWidgets()


class SiTableView(ABCSiTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.padding = 20

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet("border-radius: 8px")

        self.header_panel = SiLabel(self)
        self.header_panel.setFixedStyleSheet("border-top-left-radius: 8px; border-top-right-radius: 8px")

        self.container_ = SiMasonryContainer(self)
        self.container_.setSpacing(vertical=0)
        self.container_.setColumns(1)

        self.scroll_area = SiScrollArea(self)
        self.scroll_area.setAttachment(self.container_)

        self.setManager(SiTableValueManagerLabels(self))
        self.header_row = SiRow(self)

        self.indicator_frame = SiWidget(self)
        self.indicator_frame.setFixedHeight(6)
        self.indicator_frame.move(8, 44)
        self.indicator_frame.hide()

        self.indicator_track = SiLabel(self.indicator_frame)
        self.indicator_track.setFixedStyleSheet("border-radius: 1px")
        self.indicator_track.move(0, 2)

    def addRow(self, widgets: list = None, data: list = None):
        super().addRow(widgets, data)

        if len(self.rows_) % 2 == 0:
            color = self.getColor(SiColor.INTERFACE_BG_C)
        else:
            color = self.getColor(SiColor.INTERFACE_BG_B)

        self.rows_[-1].setFixedStyleSheet("border-radius: 6px")
        self.rows_[-1].setColor(color)
        self.rows_[-1].resize(self.width() - self.padding * 2, 40)
        self.container().arrangeWidgets()

    def addColumn(self,
                  name: str,
                  width: int = None,
                  height: int = None,
                  alignment=None):
        super().addColumn(name, width, height, alignment)
        self._load_header()

    def _load_header(self):
        self.header_row.deleteLater()
        self.header_row = SiRow(self)
        self.header_row.container().setTemplate(self.sectionTemplate())
        self.header_row.setGeometry(self.padding, 4, self.width() - self.padding * 2, 40)
        self.manager().on_header_created(self.header_row)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.panel.setStyleSheet(
            f"border: 1px solid {self.getColor(SiColor.INTERFACE_BG_D)};"
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_B)};"
        )

        self.header_panel.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)};"
        )

        self.indicator_track.setStyleSheet(
            f"background-color: {self.getColor(SiColor.THEME)}"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.panel.resize(event.size())
        self.header_panel.resize(event.size().width(), 48)
        self.header_row.setGeometry(self.padding, 4, event.size().width() - self.padding * 2, 40)
        self.indicator_frame.resize(event.size().width() - self.indicator_frame.x() * 2, 6)
        self.indicator_track.resize(self.indicator_frame.width(), 3)

        self.scroll_area.setGeometry(self.padding, 48, event.size().width() - self.padding, event.size().height() - 48 - 1)
        self.container().setGeometry(0, 0, event.size().width() - self.padding * 2, self.container().height())
        for row in self.rows():
            row.resize(event.size().width() - self.padding * 2, 40)
        self.container().arrangeWidgets()
