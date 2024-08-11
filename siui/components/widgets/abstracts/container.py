from PyQt5.QtCore import QSize

from siui.components.widgets.abstracts.widget import SiWidget


class SiSection:
    def __init__(self, width=None, height=None, alignment=None):
        self.width_ = width
        self.height_ = height
        self.alignment_ = alignment

    def setWidth(self, width):
        self.width_ = width

    def setHeight(self, height):
        self.height_ = height

    def setAlignment(self, alignment):
        self.alignment_ = alignment

    def width(self):
        return self.width_

    def height(self):
        return self.height_

    def size(self):
        return QSize(self.width_, self.height_)

    def alignment(self):
        return self.alignment_


class SiSectionTemplate:
    def __init__(self):
        self.sections_ = []

    def sections(self):
        return self.sections_

    def addSection(self, width=None, height=None, alignment=None):
        self.sections_.append(SiSection(width, height, alignment))


class ABCSiDividedContainer(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sections_and_widgets = []

    def sections(self):
        return [a[0] for a in self.sections_and_widgets]

    def addSection(self, width=None, height=None, alignment=None):
        self.sections_and_widgets.append([SiSection(width, height, alignment), None])

    def loadTemplate(self, template: SiSectionTemplate):
        for index, section in enumerate(template.sections()):
            if index < len(self.sections_and_widgets):
                self.sections_and_widgets[index][0] = section
            else:
                self.sections_and_widgets.append([section, None])

    def widgets(self):
        return [a[1] for a in self.sections_and_widgets]

    def addWidget(self, widget, index=None):
        if index is None:
            index = self.widgets().index(None)

        widget.setParent(self)

        if self.sections_and_widgets[index][1] is not None:
            self.sections_and_widgets[index][1].deleteLater()
        self.sections_and_widgets[index][1] = widget
