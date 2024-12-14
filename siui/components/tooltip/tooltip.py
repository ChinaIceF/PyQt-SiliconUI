
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core import GlobalFont, Si, SiGlobal, SiQuickEffect
from siui.gui import SiFont


class ToolTipWindow(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_shown = False
        self.completely_hid = False
        """ 是否已经完全隐藏（透明度是不是0） """
        self.now_inside_of = None
        """ 在哪个控件内部（最近一次被谁触发过显示事件） """
        self.margin = 8
        """ 周围给阴影预留的间隔空间 """
        self.shadow_size = 8
        """ 阴影大小 """

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        SiQuickEffect.applyDropShadowOn(self, (0, 0, 0, 128), blur_radius=int(self.shadow_size*1.5))

        self._initWidget()
        self._initStyle()
        self._initLayout()
        self._initAnimation()

        self.setText("", flash=False)  # 通过输入空文本初始化大小

    def _initWidget(self):
        self.bg_label = SiLabel(self)
        """背景颜色，可以用于呈现不同类型的信息"""

        self.text_container = SiLabel(self)
        """文字标签的父对象，防止文字超出界限"""

        self.text_label = SiLabel(self.text_container)
        """文字标签，显示工具提示内容"""

        self.highlight_mask = SiLabel(self)
        """高光遮罩，当信息刷新时会闪烁一下"""

    def _initStyle(self):
        self.bg_label.setFixedStyleSheet("border-radius: 6px")
        self.text_label.setFixedStyleSheet("padding: 8px")
        self.text_label.setSiliconWidgetFlag(Si.InstantResize)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.text_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.highlight_mask.setFixedStyleSheet("border-radius: 6px")
        self.highlight_mask.setColor("#00FFFFFF")

    def _initLayout(self):
        self.bg_label.move(self.margin, self.margin)
        self.text_container.move(self.margin, self.margin)
        self.highlight_mask.move(self.margin, self.margin)

    def _initAnimation(self):
        self.tracker_timer = QTimer()  # 跟踪鼠标的计时器
        self.tracker_timer.setInterval(int(1000/60))
        self.tracker_timer.timeout.connect(self._refresh_position)
        self.tracker_timer.start()

        # 当透明度动画结束时处理隐藏与否
        self.animationGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)

    def reloadStyleSheet(self):
        self.bg_label.setColor(SiGlobal.siui.colors["TOOLTIP_BG"])
        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def show_(self):
        self.is_shown = True
        self.setOpacityTo(1.0)

    def hide_(self):
        self.is_shown = False
        self.setOpacityTo(0)

    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self.completely_hid = True
            self.resize(2 * self.margin, 36 + 2 * self.margin)  # 变单行内容的高度，宽度不足以显示任何内容 # 2024.11.1 宽度设0解决幽灵窗口
            self.text_label.setText("")   # 清空文本内容
        else:
            self.completely_hid = False

    def setNowInsideOf(self, widget):
        """
        设置当前位于哪个控件内部。对于 siui 的控件，这将会在设置工具提示显示时被调用并传入调用者，在隐藏时被调用并传入 None
        :param widget: 在哪个控件的内部（被谁触发了显示）
        :return:
        """
        self.now_inside_of = widget

    def nowInsideOf(self):
        """
        返回最后一次被调用显示时的发出者
        :return: 控件或None
        """
        return self.now_inside_of

    def setText(self, text, flash=True):
        """
        设置工具提示的内容，支持富文本
        :param text: 内容，将被转化为字符串
        :param flash: 是否闪烁高光层
        :return:
        """
        text_changed = self.text_label.text() != text
        self.text_label.setText(str(text))
        self._refresh_size()
        if flash and text_changed:
            self.flash()

    def _refresh_size(self):
        """ 用于设置大小动画结束值并启动动画 """
        w = self.text_label.width()
        h = self.text_label.height()
        self.resizeTo(w + 2 * self.margin, h + 2 * self.margin)  # 设为文字标签的大小加上阴影间距

    def flash(self):
        """ 激活高光层动画，使高光层闪烁 """
        self.highlight_mask.setColor("#7FFFFFFF")
        self.highlight_mask.setColorTo("#00FFFFFF")

    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x(), pos.y()
        self.moveTo(x + 4, y - self.height())    # 动画跟踪，效果更佳，有了锚点直接输入鼠标坐标即可

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width() - 2 * self.margin, size.height() - 2 * self.margin

        # 重设内部控件大小
        self.bg_label.resize(w, h)
        self.text_container.resize(w, h)
        self.highlight_mask.resize(w, h)

        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        # self.text_label.move(0, h - self.text_label.height()) 2024.9.23 - 存在快速滑动鼠标时文字错位的情况
        self.text_label.move(0, h - self.height() + 16)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()
