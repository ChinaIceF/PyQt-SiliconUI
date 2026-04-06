
from PyQt6.QtCore import QPoint, QSize, Qt


class SiQuickAlignmentManager:
    @staticmethod
    def toPos(container_size: QSize,
              widget_size: QSize,
              flag):
        if (flag & Qt.AlignmentFlag.AlignLeft) == Qt.AlignmentFlag.AlignLeft:
            x = 0
        elif (flag & Qt.AlignmentFlag.AlignHCenter) == Qt.AlignmentFlag.AlignHCenter:
            x = (container_size.width() - widget_size.width()) // 2
        elif (flag & Qt.AlignmentFlag.AlignRight) == Qt.AlignmentFlag.AlignRight:
            x = container_size.width() - widget_size.width()
        else:
            x = 0

        if (flag & Qt.AlignmentFlag.AlignTop) == Qt.AlignmentFlag.AlignTop:
            y = 0
        elif (flag & Qt.AlignmentFlag.AlignVCenter) == Qt.AlignmentFlag.AlignVCenter:
            y = (container_size.height() - widget_size.height()) // 2
        elif (flag & Qt.AlignmentFlag.AlignBottom) == Qt.AlignmentFlag.AlignBottom:
            y = container_size.height() - widget_size.height()
        else:
            y = 0

        return QPoint(x, y)
