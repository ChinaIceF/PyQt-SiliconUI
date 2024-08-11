from siui.components import SiDenseHContainer, SiPixLabel, SiDenseVContainer, SiLabel, SiSimpleButton
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.gui import SiFont, GlobalFont
from siui.templates.application.components.message.box import SiSideMessageBox


def send_simple_message(type_):
    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
        "这是一条测试消息\n"
        "比具标题信息更加简洁方便",
        msg_type=type_,
    )


def send_titled_message(type_):
    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
        title="Sent Successfully",
        text="A titled message has been successfully sent to the sidebar.\n" +
             "Click this message box for more information.",
        msg_type=type_,
        slot=lambda: print("You clicked me")
    )


def send_custom_message(type_):
    container = SiDenseHContainer()
    container.setAdjustWidgetsSize(True)
    container.setFixedHeight(80)
    container.setSpacing(0)

    info_label = SiLabel()
    info_label.setFont(SiFont.fromToken(GlobalFont.S_NORMAL))
    info_label.setStyleSheet(f"color: {info_label.colorGroup().fromToken(SiColor.TEXT_D)}; padding-left: 16px")
    info_label.setText("以下账号已成功登录")
    info_label.adjustSize()

    split_line = SiLabel()
    split_line.resize(300, 1)
    split_line.setFixedStyleSheet("margin-left: 20px")
    split_line.setColor(SiColor.trans(split_line.colorGroup().fromToken(SiColor.TEXT_D), 0.3))

    avatar = SiPixLabel(container)
    avatar.resize(80, 80)
    avatar.setBorderRadius(40)
    avatar.load("./img/avatar1.png")
    avatar.setHint("霏泠Ice")

    container_v = SiDenseVContainer(container)
    container_v.setFixedWidth(200)
    container_v.setSpacing(0)

    name_label = SiLabel()
    name_label.setFont(SiFont.fromToken(GlobalFont.M_BOLD))
    name_label.setStyleSheet(f"color: {name_label.colorGroup().fromToken(SiColor.TEXT_B)}; padding-left:8px")
    name_label.setText("霏泠Ice")
    name_label.adjustSize()

    button_1 = SiSimpleButton()
    button_1.setFixedHeight(22)
    button_1.attachment().setText("打开我的主页")
    button_1.colorGroup().assign(SiColor.TEXT_B, button_1.colorGroup().fromToken(SiColor.TITLE_INDICATOR))
    button_1.adjustSize()
    button_1.reloadStyleSheet()

    button_2 = SiSimpleButton()
    button_2.setFixedHeight(22)
    button_2.attachment().setText("退出账号")
    button_2.colorGroup().assign(SiColor.TEXT_B, button_2.colorGroup().fromToken(SiColor.TITLE_INDICATOR))
    button_2.adjustSize()
    button_2.reloadStyleSheet()

    container_v.addWidget(name_label)
    container_v.addPlaceholder(8)
    container_v.addWidget(button_1)
    container_v.addWidget(button_2)
    container_v.adjustSize()

    container.addPlaceholder(24)
    container.addWidget(avatar)
    container.addPlaceholder(8)
    container.addWidget(container_v)
    container.adjustSize()

    new_message_box = SiSideMessageBox()
    new_message_box.setMessageType(type_)
    new_message_box.content().container().setSpacing(0)
    new_message_box.content().container().addPlaceholder(16)
    new_message_box.content().container().addWidget(info_label)
    new_message_box.content().container().addPlaceholder(8)
    new_message_box.content().container().addWidget(split_line)
    new_message_box.content().container().addPlaceholder(24)
    new_message_box.content().container().addWidget(container)
    new_message_box.content().container().addPlaceholder(32)
    new_message_box.adjustSize()

    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().sendMessageBox(new_message_box)