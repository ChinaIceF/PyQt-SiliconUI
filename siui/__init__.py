

import siui.components as components
import siui.core as core
import siui.core.globals
import siui.gui as gui
import siui.widgets as widgets

# 当 siui 第一次被导入时，在 siui 命名空间下创建 globals，用于常量读取，全局操作等
globals = siui.core.globals.TokenizedDatabase("ROOT")

# 将三个项添加到 globals 的属性中
globals.color = siui.core.globals.TokenizedDatabase("COLOR")
globals.qss = siui.core.globals.TokenizedDatabase("QSS")
globals.windows = siui.core.globals.TokenizedDatabase("WINDOWS")

# 注册
globals.register("COLOR", globals.color)
globals.register("QSS", globals.qss)
globals.register("WINDOWS", globals.windows)


globals.color.register("TEXT_GRAD_0", "#FFFFFF")

globals.tree()