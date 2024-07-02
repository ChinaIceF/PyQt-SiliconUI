from PyQt5.QtGui import QFont
import SiliconUI

def adjusted(p):
    return int(p/SiliconUI.SA_SCALE_FACTOR)

font_L1 = QFont("微软雅黑", adjusted(0), QFont.Normal)
font_L1.setPixelSize(14)
font_L1_bold = QFont("微软雅黑",adjusted(10), QFont.Bold)
font_L1_bold.setPixelSize(14)

font_L2 = QFont("微软雅黑",adjusted(14), QFont.Normal)
font_L2.setPixelSize(20)
font_L2_bold = QFont("微软雅黑",adjusted(14), QFont.Bold)
font_L2_bold.setPixelSize(20)

font_L3 = QFont("微软雅黑",adjusted(18), QFont.Normal)
font_L3.setPixelSize(24)
font_L3_bold = QFont("微软雅黑",adjusted(18), QFont.Bold)
font_L3_bold.setPixelSize(24)

font_L4 = QFont("微软雅黑",adjusted(24), QFont.Normal)
font_L4.setPixelSize(32)
font_L4_bold = QFont("微软雅黑",adjusted(24), QFont.Bold)
font_L4_bold.setPixelSize(32)

def fontraw(name, size, tag = QFont.Normal):
    return QFont(name ,size, tag)
