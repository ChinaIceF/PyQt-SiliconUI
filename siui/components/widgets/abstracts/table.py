from PyQt5.QtCore import pyqtSignal

from siui.components import SiDividedHContainer, SiLabel, SiWidget
from siui.components.widgets.abstracts.container import SiSectionTemplate


class ABCSiTabelManager:
    def __init__(self, parent):
        self.parent_ = parent

    def parent(self):
        return self.parent_

    def setParent(self, parent):
        self.parent_ = parent

    def _widget_creator(self, col_index):
        # Implement the method of creating widgets here
        raise NotImplementedError()

    def _value_read_parser(self, row_index, col_index):
        # Implement the method of obtaining values here
        raise NotImplementedError()

    def _value_write_parser(self, row_index, col_index, value):
        # Implement the method of writing values here
        raise NotImplementedError()

    def read(self, row_index, col_index):
        self._value_read_parser(row_index, col_index)

    def write(self, row_index, col_index, value):
        self._value_write_parser(row_index, col_index, value)

    def new_widget(self, col_index):
        return self._widget_creator(col_index)


class SiRow(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container_ = SiDividedHContainer(self)

    def container(self):
        return self.container_

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container_.setGeometry(16, 0, event.size().width() - 32, event.size().height())


class ABCSiTable(SiWidget):
    rowAdded = pyqtSignal(int)
    rowDeleted = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.column_names = []
        self.rows_ = []
        self.container_ = None
        self.manager_ = ABCSiTabelManager(self)

        self.section_template = SiSectionTemplate()
        self.section_template.setSpacing(8)

    def container(self):
        return self.container_

    def setContainer(self, widget):
        widget.setParent(self)
        self.container_ = widget

    def setManager(self, manager: ABCSiTabelManager):
        manager.setParent(self)
        self.manager_ = manager

    def manager(self):
        return self.manager_

    def sectionTemplate(self):
        return self.section_template

    def readCell(self, row_index, col_index):
        return self.manager_.read(row_index, col_index)

    def writeCell(self, row_index, col_index, value):
        self.manager_.write(row_index, col_index, value)

    def addColumn(self,
                  name: str,
                  width: int = None,
                  height: int = None,
                  alignment=None):
        self.section_template.addSection(width, height, alignment)
        self.column_names.append(name)

    def columnNames(self):
        return self.column_names

    def getColumnWidget(self, index):
        return [row.container().widgets[index] for row in self.rows_]

    def readColumn(self, index):
        return [self.manager_.read(i, index) for i in range(len(self.rows_))]

    def writeColumn(self, index, values: list):
        if len(values) != len(self.rows_):
            raise ValueError(f"Shape does not match when writing column {index}: got {len(values)}, expected {len(self.rows_)}")  # noqa: E501
        for i in range(len(self.rows_)):
            self.writeCell(i, index, values[i])
        for row in self.rows_:
            row.container().arrangeWidgets()

    def addRow(self, widgets: list = None, data: list = None):
        new_row = SiRow(self)
        new_row.container().setTemplate(self.sectionTemplate())
        if widgets is not None:
            for widget in widgets:
                new_row.container().addWidget(widget)
        else:
            for i in range(len(self.column_names)):
                new_row.container().addWidget(self.manager_.new_widget(i))

        new_row.container().arrangeWidgets()
        self.rows_.append(new_row)
        self.container_.addWidget(new_row)
        self.rowAdded.emit(self.rows_.index(new_row))

        if data is not None:
            self.writeRow(self.rows_.index(new_row), data)

    def deleteRow(self, index):
        deleted_row = self.rows_.pop(index)
        deleted_row.deleteLater()
        self.rowDeleted.emit(index)

    def rows(self):
        return self.rows_

    def getRowWidget(self, index):
        return self.rows_[index].container().widgets()

    def readRow(self, index):
        return [self.manager_.read(index, i) for i in range(len(self.column_names))]

    def writeRow(self, index, values: list):
        if len(values) != len(self.column_names):
            raise ValueError(f"Shape does not match when writing row {index}: got {len(values)}, expected {len(self.column_names)}")  # noqa: E501
        for i in range(len(self.column_names)):
            self.writeCell(index, i, values[i])
        self.rows_[index].container().arrangeWidgets()
