from PyQt5.QtCore import pyqtSignal

from siui.components.widgets.label import SiLabel


class ABCSiNavigationBar(SiLabel):
    """
    抽象导航栏
    """
    indexChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 当前索引
        self.current_index_ = -1

        # 最大索引，需要最先设置
        self.maximum_index_ = 0

    def setCurrentIndex(self, index):
        """
        设置当前索引
        :param index: 索引
        """
        self.current_index_ = index % self.maximumIndex()
        self.indexChanged.emit(self.currentIndex())

    def currentIndex(self):
        """
        获取当前索引
        :return: 索引
        """
        return self.current_index_

    def setMaximumIndex(self, max_index):
        """
        设置最大的索引，超过最大索引的索引将会被取余数
        :param max_index: 最大索引
        """
        self.maximum_index_ = max_index
        self.setCurrentIndex(self.currentIndex())  # 如果最大索引变小，这样可以防止其超过界限

    def maximumIndex(self):
        """
        获取最大的索引
        """
        return self.maximum_index_

    def shift(self, step: int):
        """
        切换，这等价于将当前索引加step后设置索引
        :param step: 步长
        """
        self.setCurrentIndex(self.currentIndex() + step)
