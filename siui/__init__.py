

import siui.components as components
import siui.core as core
import siui.core.globals
import siui.gui as gui
import siui.components.widgets as widgets
import siui.templates as templates

import siui

# 载入色彩字典
siui.core.globals.SiGlobal.siui.loadColors(siui.gui.colorsets.ColorsetDark.colors)

# 加载全局缩放比例
siui.gui.reload_scale_factor()
