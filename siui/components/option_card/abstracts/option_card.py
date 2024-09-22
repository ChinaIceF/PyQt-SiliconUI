from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiLabel
from siui.core import SiGlobal


class ABCSiOptionCardPlane(SiLabel):
    """
    平面型选项卡，划分 header, body, footer，为一般场景提供支持
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacing_ = 24

        # 构建组成外观的控件
        self.outfit_label_lower = SiLabel(self)
        self.outfit_label_lower.setFixedStyleSheet("border-radius: 6px")

        self.outfit_label_upper = SiLabel(self)
        self.outfit_label_upper.setFixedStyleSheet("border-radius: 6px")

        # 创建容器
        self.container = SiDenseVContainer(self)
        self.container.setSpacing(0)
        self.container.setAdjustWidgetsSize(True)

        # 创建划分区域
        self.header_ = SiDenseHContainer(self)
        self.header_.resize(0, 0)

        self.body_ = SiDenseVContainer(self)  # 只有 body 是竖直密堆积容器
        self.body_.setSpacing(8)
        self.body_.resize(0, 0)

        self.footer_ = SiDenseHContainer(self)
        self.footer_.resize(0, 0)

        # 设置子控件适应容器，并把三个组成部分添加到自己

        self.container.addWidget(self.header_)
        self.container.addWidget(self.body_)
        self.container.addWidget(self.footer_, "bottom")

    def setSpacing(self, spacing):
        """
        设置容器与边缘左右的间隔
        :param spacing: 间隔
        """
        self.spacing_ = spacing

    def spacing(self):
        """
        获取容器与边缘左右的间隔
        :return: 间隔
        """
        return self.spacing_

    def header(self):
        """
        返回 header 容器
        :return: header 容器
        """
        return self.header_

    def body(self):
        """
        返回 body 容器
        :return: body 容器
        """
        return self.body_

    def footer(self):
        """
        返回 footer 容器
        :return: footer 容器
        """
        return self.footer_

    def adjustSize(self):
        self.resize(self.width(), self.header().height() + self.body().height() + self.footer().height() + 3)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.outfit_label_lower.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_A"]))
        self.outfit_label_upper.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_C"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.container.setGeometry(self.spacing(), 0, w-self.spacing()*2, h-3)

        self.outfit_label_lower.setGeometry(0, 8, w, h-8)  # 防止上边出现底色毛边
        self.outfit_label_upper.resize(w, h - 3)
