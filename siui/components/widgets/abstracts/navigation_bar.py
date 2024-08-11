from PyQt5.QtCore import pyqtSignal

from siui.components.widgets.abstracts.widget import SiWidget


class ABCSiNavigationBar(SiWidget):
    """ 抽象导航栏 """
    indexChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 当前索引
        self.current_index_ = -1

        # 最大索引，需要最先设置
        self.maximum_index_ = -1

    def setCurrentIndex(self, index):
        """ 设置当前索引 """
        self.current_index_ = index % (self.maximumIndex() + 1)
        self.indexChanged.emit(self.currentIndex())

    def currentIndex(self):
        """ 获取当前索引 """
        return self.current_index_

    def setMaximumIndex(self, max_index):
        """ 设置最大的索引，超过最大索引的索引将会被取余数 """
        if max_index < self.maximumIndex():
            self.maximum_index_ = max_index
            self.setCurrentIndex(self.currentIndex())  # 如果最大索引变小，这样可以防止其超过界限
        else:
            self.maximum_index_ = max_index

    def maximumIndex(self):
        """ 获取最大的索引 """
        return self.maximum_index_

    def shift(self, step: int):
        """
        将当前索引加 step
        :param step: 步长
        """
        self.setCurrentIndex(self.currentIndex() + step)
