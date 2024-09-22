
from PyQt5.QtCore import QPoint, QSize, Qt


class SiQuickAlignmentManager:
    @staticmethod
    def toPos(container_size: QSize,
              widget_size: QSize,
              flag):
        if (flag & Qt.AlignLeft) == Qt.AlignLeft:
            x = 0
        elif (flag & Qt.AlignHCenter) == Qt.AlignHCenter:
            x = (container_size.width() - widget_size.width()) // 2
        elif (flag & Qt.AlignRight) == Qt.AlignRight:
            x = container_size.width() - widget_size.width()
        else:
            x = 0

        if (flag & Qt.AlignTop) == Qt.AlignTop:
            y = 0
        elif (flag & Qt.AlignVCenter) == Qt.AlignVCenter:
            y = (container_size.height() - widget_size.height()) // 2
        elif (flag & Qt.AlignBottom) == Qt.AlignBottom:
            y = container_size.height() - widget_size.height()
        else:
            y = 0

        return QPoint(x, y)
