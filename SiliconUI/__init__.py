
import os
import ctypes

def get_windows_scaling_factor():
    try:
        # 调用 Windows API 函数获取缩放比例
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()

        # 计算缩放比例
        return scaling_factor / 96.0

    except Exception as e:
        print("无法获取缩放比例，设置为1，错误:", e)
        return 1

SA_SCALE_FACTOR = get_windows_scaling_factor()
os.environ['QT_SCALE_FACTOR'] = str(SA_SCALE_FACTOR)

from .SiFont import *
from .SiButton import *
from .SiOption import *
from .SiFrame import *
from .SiStack import *
from .SiScrollArea import *
from .SiTab import *
from .SiTabArea import *
from .SiStyle import *
from .SiInfo import *
from .SiLabel import *
