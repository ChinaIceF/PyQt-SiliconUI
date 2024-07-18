import time


class SiliconUIGlobal:
    """
    SiliconUI 内部使用的全局数据\n
    如果你也需要使用全局数据，可以将你的类添加到 SiGlobal 的一个属性
    """
    # 窗口字典，储存窗口对象
    windows = {}

    # 颜色字典，存储全部动态设置的颜色
    # 值为 RRGGBB 或 AARRGGBB 色号
    colors = {}

    # 图标字典，储存所有 SVG 类型的图标数据
    # 值为 SVG信息的 bytes
    icons = {}

    # 样式表字典，储存所有动态样式表
    # 值为字符串
    qss = {}

    # 字体字典，储存所有字体
    # 值为 QFont 类型的字体
    fonts = {}

    def loadWindows(self, dictionary):
        SiliconUIGlobal.windows.update(dictionary)

    def loadColors(self, dictionary):
        SiliconUIGlobal.colors.update(dictionary)

    def loadIcons(self, dictionary):
        SiliconUIGlobal.icons.update(dictionary)

    def loadQSS(self, dictionary):
        SiliconUIGlobal.qss.update(dictionary)

    def loadFonts(self, dictionary):
        SiliconUIGlobal.fonts.update(dictionary)

    def reloadAllWindowsStyleSheet(self):
        """
        调用各个窗口下的reloadStyleSheet方法并递归，重载所有窗口下所有控件的样式表
        """
        for window in self.windows.values():
            try:
                window.reloadStyleSheet()
            except:
                pass
            self._reloadWidgetStyleSheet(window)

    def _reloadWidgetStyleSheet(self, widget):
        for child in widget.children():
            self._reloadWidgetStyleSheet(child)
            try:
                child.reloadStyleSheet()
            except:
                pass
        return


class SiGlobal:
    """
    全局数据\n
    在 siui 模块被第一次导入时初始化 .siui 下的变量
    """
    siui = SiliconUIGlobal()


class NewGlobal:
    """
    新全局数据
    """
    create_time = time.time()

