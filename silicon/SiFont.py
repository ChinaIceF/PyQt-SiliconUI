from PyQt5.QtGui import QFont
import silicon

def adjusted(p):
    return int(p/silicon.SA_SCALE_FACTOR)

font_L1 = QFont("微软雅黑", adjusted(10), QFont.Normal)
font_L1_bold = QFont("微软雅黑",adjusted(10), QFont.Bold)

font_L2 = QFont("微软雅黑",adjusted(14), QFont.Normal)
font_L2_bold = QFont("微软雅黑",adjusted(14), QFont.Bold)

font_L3 = QFont("微软雅黑",adjusted(18), QFont.Normal)
font_L3_bold = QFont("微软雅黑",adjusted(18), QFont.Bold)

font_L4 = QFont("微软雅黑",adjusted(24), QFont.Normal)
font_L4_bold = QFont("微软雅黑",adjusted(24), QFont.Bold)

def fontraw(name, size, tag = QFont.Normal):
    return QFont(name ,size, tag)
