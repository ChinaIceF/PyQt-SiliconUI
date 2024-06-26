from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit

from .SiLabel import *
from .SiStack import *
from .SiButton import *

class SiLayoutV(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.contents_top = []
        self.contents_bottom = []
        self.align_center = False
        self.adjust_item = False       # 是否调节内容以适应 Layout 的尺寸
        self.interval = 16

    def setAdjustItem(self, b):
        self.adjust_item = b

    def setAlignCenter(self, b):
        self.align_center = b

    def setInterval(self, interval):
        self.interval = interval

    def addVacant(self, length, side = 'top'):
        new_label = QLabel(self)
        new_label.setStyleSheet('')
        new_label.resize(0, length)
        self.addItem(new_label, side = side)

    def addItem(self, item, side = 'top'):
        item.setParent(self)
        item.parent = self

        if side != 'top' and side != 'bottom':
            raise ValueError(side)

        if side == 'top':
            self.contents_top.append(item)
        if side == 'bottom':
            self.contents_bottom.append(item)
        self.refresh_components()
        self.adjustSize()

    def refresh_components(self):
        size = self.geometry()
        w, h = size.width(), size.height()

        top_used = 0
        bottom_used = 0

        for obj in self.contents_top:
            if self.adjust_item == True:
                obj.setFixedWidth(w)
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move((w - ow)//2 if self.align_center else 0, top_used)
            top_used += oh + self.interval

        for obj in self.contents_bottom:
            if self.adjust_item == True:
                obj.setFixedWidth(w)
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move((w - ow)//2 if self.align_center else 0, h - oh - bottom_used)
            bottom_used += oh + self.interval

        total_used = top_used + bottom_used
        total_used -= 0 if self.contents_top == [] else self.interval
        total_used -= 0 if self.contents_bottom == [] else self.interval

        self.setMinimumSize(0, total_used)

    def resizeEvent(self, event):
        self.refresh_components()

    def adjustSize(self):

        top_used = 0
        bottom_used = 0
        for obj in self.contents_top:
            top_used += obj.height() + self.interval
        for obj in self.contents_bottom:
            bottom_used += obj.height() + self.interval
        total_used = top_used + bottom_used
        total_used -= 0 if self.contents_top == [] else self.interval
        total_used -= 0 if self.contents_bottom == [] else self.interval
        prefered_h = total_used

        prefered_w = 0
        for obj in (self.contents_top + self.contents_bottom):
            if obj.width() > prefered_w:
                prefered_w = obj.width()   # 找最大的宽度

        prefered_w = max(prefered_w, self.width())
        prefered_h = max(prefered_h, self.height())

        self.resize(prefered_w, prefered_h)

class SiLayoutH(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.contents_left = []
        self.contents_right = []
        self.align_center = False
        self.adjust_item = False       # 是否调节内容以适应 Layout 的尺寸
        self.interval = 16

    def setAdjustItem(self, b):
        self.adjust_item = b

    def setAlignCenter(self, b):
        self.align_center = b

    def setInterval(self, interval):
        self.interval = interval

    def addVacant(self, length, side = 'left'):
        new_label = QLabel(self)
        new_label.setStyleSheet('')
        new_label.resize(length, 0)
        self.addItem(new_label, side = side)

    def addItem(self, item, side = 'left'):
        item.setParent(self)
        item.parent = self

        if side != 'left' and side != 'right':
            raise ValueError(side)

        if side == 'left':
            self.contents_left.append(item)
        if side == 'right':
            self.contents_right.append(item)
        self.refresh_components()
        self.adjustSize()

    def refresh_components(self):
        size = self.geometry()
        w, h = size.width(), size.height()

        left_used = 0
        right_used = 0

        for obj in self.contents_left:
            if self.adjust_item == True:
                obj.setFixedHeight(h)
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move(left_used, (h - oh) // 2 if self.align_center else 0)
            left_used += ow + self.interval

        for obj in self.contents_right:
            if self.adjust_item == True:
                obj.setFixedHeight(h)
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move(w - ow - right_used, (h - oh) // 2 if self.align_center else 0)
            right_used += ow + self.interval

        total_used = left_used + right_used
        total_used -= 0 if self.contents_left == [] else self.interval
        total_used -= 0 if self.contents_right == [] else self.interval

        self.setMinimumSize(total_used, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_components()

    def adjustSize(self):
        left_used = 0
        right_used = 0
        for obj in self.contents_left:
            left_used += obj.width() + self.interval
        for obj in self.contents_right:
            right_used += obj.width() + self.interval
        total_used = left_used + right_used
        total_used -= 0 if self.contents_left == [] else self.interval
        total_used -= 0 if self.contents_right == [] else self.interval
        prefered_w = total_used

        prefered_h = 0
        for obj in (self.contents_left + self.contents_right):
            if obj.height() > prefered_h:
                prefered_h = obj.height()   # 找最大的宽度


        prefered_w = max(prefered_w, self.width())
        prefered_h = max(prefered_h, self.height())

        self.resize(prefered_w, prefered_h)

class SiFlowLayout(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.items = []
        self.interval = [8, 8]

    def addItem(self, item, ani = True):
        self.items.append(item)
        item.setParent(self)
        self.adjustSize(ani)

    def setInterval(self, x, y):
        self.interval = [x, y]

    def adjustSize(self, ani = True):
        # 该方法不调整宽度，只调整高度
        # 因此宽度需要在调用此方法前设定

        interval_x, interval_y = self.interval

        line_w = 0      # 某行宽计数器
        line_h = 0      # 某行高计数器
        total_h = 0     # 总高计数器

        max_w = self.width()

        for item in self.items:
            item_w, item_h = item.width(), item.height()
            # 如果剩余宽度不够，进行换行操作
            if line_w + item_w >= max_w:
                total_h += line_h + interval_y
                line_w, line_h = 0, 0

            # 如果某个控件高，行高变高以适应
            line_h = max(item_h, line_h)

            # 尝试用带动画的对象
            try:
                if ani == True:
                    item.moveTo(line_w, total_h)
                else:
                    item.move(line_w, total_h)
            except:
                item.move(line_w, total_h)

            line_w += item_w + interval_x

        total_h += line_h  # 还有最后一行没加上
        self.resize(self.width(), total_h)

class SiStackedLayoutNavbar(SiStack):   # 这是 SiStackedLayout 的导航栏
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('')
        self.setInterval(0)
        self.parent = parent

        self.holder = QLabel(self)
        self.holder.setFixedHeight(6)

        self.holder_line = QLabel(self.holder)
        self.holder_line.setFixedHeight(1)
        self.holder_line.move(0, 2)
        self.holder_line.setStyleSheet('''
            border-radius: 1px;
            background-color: {}
        '''.format(colorset.BG_GRAD_HEX[1]))

        self.anchor = SiLabel(self)
        self.anchor.setGeometry(0, 28, 32, 4)
        self.anchor.setStyleSheet('''
            border-radius: 2px;
            background-color: {};
        '''.format(colorset.BTN_HL_HEX[1]))

        self.layout_page_label = SiLayoutH(self)
        self.layout_page_label.setFixedHeight(32)

        self.addItem(self.layout_page_label)
        self.addItem(self.holder)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        self.holder_line.setFixedWidth(w)


class SiStackedLayout(SiStack):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.page_labels = []
        self.pages = []

        self.navbar = SiStackedLayoutNavbar(self)

        self.addItem(self.navbar)

    def showEvent(self, event):
        super().showEvent(event)
        self.navbar.anchor.raise_()
        self._pageChangeHandler(self.pages[0], self.page_labels[0])

    def _pageChangeHandler(self, obj, obj_label):
        for page in self.pages:
            page.setVisible(False)
        obj.setVisible(True)

        for page_label in self.page_labels:
            page_label.setStyleSheet('''
                background-color: transparent;  padding: 4px;
                color: {};
                border-radius: 4px;
            '''.format(colorset.TEXT_GRAD_HEX[2]))

        obj_label.setStyleSheet('''
            background-color: {};  padding: 4px;
            color: {};
            border-radius: 4px;
        '''.format(colorset.BG_GRAD_HEX[3], colorset.TEXT_GRAD_HEX[0]))

        # 获取选项卡标签位置和大小
        x_label, w_label = obj_label.geometry().x(), obj_label.geometry().width()
        w_anchor = int(w_label * 0.618)
        self.navbar.anchor.moveTo(x_label + (w_label - w_anchor)//2, 28)
        self.navbar.anchor.resize(w_anchor, 4)


    def addPage(self, pagename):
        new_stack = SiStack(self)
        new_stack.move(0, 64)
        self.pages.append(new_stack)

        new_label = ClickableLabel(self)
        new_label.setFixedHeight(32)
        new_label.setStyleSheet('''
            color: {};
            padding: 4px;
            border-radius: 4px;
        '''.format(colorset.TEXT_GRAD_HEX[0]))
        new_label.setText(pagename)
        new_label.clicked.connect(
            lambda : self._pageChangeHandler(new_stack, new_label))
        self.page_labels.append(new_label)
        self.navbar.layout_page_label.addItem(new_label)

    def addItemToPage(self, pagename, obj):
        target_page = None
        for page, page_label in zip(self.pages, self.page_labels):
            if page_label.text() == pagename:
                target_page = page
                break
        if target_page is None:
            raise ValueError('没有指定的选项卡名：{}'.format(pagename))
        target_page.addItem(obj)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        for page in self.pages:
            page.setFixedWidth(w)
