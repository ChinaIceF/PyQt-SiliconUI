from PyQt5.QtWidgets import QLabel

class SiFrame(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.items = []
        self.h = 0
        self.margin = 64 # 两侧间距
        self.delta = 16  # 每个 item 之间的间隔
        self.stop_resize_threshold_width = 800  # 宽度超过这个值，就停止拉长内容，转而中置
        self.max_width_policy = True

    def getH(self):
        return self.h

    def addH(self, num):
        self.h += num

    def addItem(self, stack, addH = True):
        self.items.append(stack)
        stack.setParent(self)
        stack.move(self.margin, self.h)

        g = stack.geometry()
        if addH:
            self.addH(g.height() + self.delta)

        self.adjustSize()

    def adjustSize(self):
        g = self.geometry()
        self.setGeometry(g.x(), g.y(), g.width(), self.getH())


    def resizeEvent(self, event):
        w = event.size().width()

        for item in self.items:
            try:
                if item.noresize == True:
                    continue
            except:
                pass
            g = item.geometry()
            new_w = w - self.margin * 2
            threshold = self.stop_resize_threshold_width
            if new_w <= threshold or self.max_width_policy == False:
                item.setGeometry(self.margin, g.y(), new_w, g.height())
            else:
                item.setGeometry((w - threshold)//2, g.y(), threshold, g.height())
