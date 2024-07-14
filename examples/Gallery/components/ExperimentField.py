import SiliconUI.SiGlobal as SiGlobal
from SiliconUI.SiFont import *
from siui.components import SiOptionCardLinear, SiOptionCardPlane, SiSliderH, SiProgressBar, SiTitledWidgetGroup
from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiLongPressButton,
    SiPushButton,
    SiRadioButton,
    SiScrollArea,
    SiSimpleButton,
    SiSwitch,
    SiToggleButton,
    SiLineEdit,
)

from .experifield.music_info_placeholder import MusicInfoPlaceholder
import random


class ExperimentField(SiliconUI.SiScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setStyleSheet('')

        self.discription = SiliconUI.SiOption(self)
        self.discription.setIcon(SiGlobal.icons.get('fi-rr-bulb'))
        self.discription.setText('实验场',
                                 '欢迎来到 Silicon 试验场。这里有一些由控件组合出来的小组件，展现 Silicon UI 蕴含的创造力与设计艺术')

        ## ================ Stack 开始 ===================

        self.stack_music_info_placeholder = SiliconUI.SiCategory(self)
        self.stack_music_info_placeholder.setTitle('音乐信息展示板')

        self.layout_music_info_placeholder = SiliconUI.SiLayoutH(self)

        # 其一
        self.music_info_placeholder = MusicInfoPlaceholder(self)
        self.music_info_placeholder.load('./img/cover.jpeg')
        self.music_info_placeholder.setText(
            title='只因你太美',
            artist='我家鸽鸽',
            album='你干嘛嗨嗨呦',
        )
        self.music_info_placeholder.resize(380, 132)
        self.music_info_placeholder.setProgress(0.7)

        # 其二
        self.music_info_placeholder_2 = MusicInfoPlaceholder(self)
        self.music_info_placeholder_2.load('./img/cover2.jpg')
        self.music_info_placeholder_2.setText(
            title='Axolotl',
            artist='C418',
            album='Axolotl',
        )
        self.music_info_placeholder_2.resize(380, 132)
        self.music_info_placeholder_2.setProgress(0)

        self.layout_music_info_placeholder.addItem(self.music_info_placeholder)
        self.layout_music_info_placeholder.addItem(self.music_info_placeholder_2)

        self.stack_music_info_placeholder.addItem(self.layout_music_info_placeholder)

        ## ================ Stack 开始 ===================

        self.stack_reconstruct_test = SiliconUI.SiCategory(self)
        self.stack_reconstruct_test.setTitle('重构测试')

        self.reconstruct_discription = SiliconUI.SiOption(self)
        self.reconstruct_discription.setIcon(SiGlobal.icons.get('fi-rr-bulb'))
        self.reconstruct_discription.setText('这里是重构测试', '此处进行项目重构的各种测试')

        self.button_layout = SiliconUI.SiLayoutH(self)
        self.button_layout.setFixedHeight(32)

        self.test_new_button = SiPushButton(self)
        self.test_new_button.setFixedSize(128, 32)
        self.test_new_button.attachment().setText("重构按钮")
        self.test_new_button.setHint("还有工具提示")
        self.test_new_button.setThemed(True)

        self.test_new_button2 = SiLongPressButton(self)
        self.test_new_button2.setFixedSize(128, 32)
        self.test_new_button2.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.test_new_button2.attachment().setText("新增图标")
        self.test_new_button2.clicked.connect(lambda: print("点击事件触发"))
        self.test_new_button2.longPressed.connect(lambda: print("长按事件触发"))

        self.test_new_button3 = SiPushButton(self)
        self.test_new_button3.setFixedSize(48, 32)
        self.test_new_button3.attachment().load(SiGlobal.icons.get('fi-rr-disk'))

        self.test_new_button4 = SiToggleButton(self)
        self.test_new_button4.attachment().load(SiGlobal.icons.get('fi-rr-disk'))
        self.test_new_button4.attachment().setText("自动保存模式")
        self.test_new_button4.adjustSize()

        self.test_new_button5 = SiRadioButton(self)
        self.test_new_button5.setText("赤石")

        self.test_new_button6 = SiRadioButton(self)
        self.test_new_button6.setText("豪赤啊")

        self.test_new_button7 = SiRadioButton(self)
        self.test_new_button7.setText("吃饱了")

        self.button_layout.addItem(self.test_new_button)
        self.button_layout.addItem(self.test_new_button2)
        self.button_layout.addItem(self.test_new_button3)
        self.button_layout.addItem(self.test_new_button4)
        self.button_layout.addItem(self.test_new_button5)
        self.button_layout.addItem(self.test_new_button6)
        self.button_layout.addItem(self.test_new_button7)

        self.button_layout2 = SiliconUI.SiLayoutH(self)
        self.button_layout2.setFixedHeight(32)
        self.button_layout2.setAlignCenter(True)

        self.test_new_button8 = SiCheckBox(self)
        self.test_new_button8.setText("鸡你太美")

        self.test_new_button9 = SiCheckBox(self)
        self.test_new_button9.setText("你干嘛嗨嗨呦")

        self.switch_test = SiSwitch(self)

        self.button_layout2.addItem(self.test_new_button8)
        self.button_layout2.addItem(self.test_new_button9)
        self.button_layout2.addItem(self.switch_test)

        self.container_h = SiDenseHContainer(self)
        self.container_h.setFixedHeight(128)
        self.container_h.setAdjustWidgetsSize(True)
        self.container_h.setStyleSheet("background-color: #05ffffff")

        self.container_v_left = SiDenseVContainer(self)
        self.container_v_left.setFixedWidth(128)
        self.container_v_left.setStyleSheet("background-color: #05ffffff")

        self.container_v_right = SiDenseVContainer(self)
        self.container_v_right.setFixedWidth(128)
        self.container_v_right.setStyleSheet("background-color: #05ffffff")

        self.button_lefttop = SiPushButton(self)
        self.button_lefttop.setFixedSize(128, 32)
        self.button_lefttop.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.button_lefttop.attachment().setText("左上角")

        self.button_leftbottom = SiPushButton(self)
        self.button_leftbottom.setFixedSize(128, 32)
        self.button_leftbottom.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.button_leftbottom.attachment().setText("左下角")

        self.button_righttop = SiPushButton(self)
        self.button_righttop.setFixedSize(128, 32)
        self.button_righttop.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.button_righttop.attachment().setText("右上角")

        self.button_rightbottom = SiPushButton(self)
        self.button_rightbottom.setFixedSize(128, 32)
        self.button_rightbottom.attachment().load(SiGlobal.icons.get('fi-rr-bulb'))
        self.button_rightbottom.attachment().setText("右下角")

        self.container_v_left.addWidget(self.button_lefttop)
        self.container_v_left.addWidget(self.button_leftbottom, "bottom")

        self.container_v_right.addWidget(self.button_righttop)
        self.container_v_right.addWidget(self.button_rightbottom, "bottom")


        self.container_h.addWidget(self.container_v_left)
        self.container_h.addWidget(self.container_v_right, "right")

        self.alabel = SiLabel(self)
        self.alabel.setAutoAdjustSize(True)
        self.alabel.setHint("你触发了工具提示")
        self.alabel.setText(
"""
合成器是一种在接收到红石信号时自动合成并丢出产物的方块。
合成器可以用5个铁锭、1个工作台、2个红石粉和1个投掷器合成。
合成器拥有3×3的合成方格，允许多名玩家同时操作。合成方格的每个槽位都可以被单独禁用，空手单击槽位可禁用该槽位，再次点击可取消禁用。
依照合成配方在合成器的合成方格内摆放物品时，右边的输出槽会显示产物，但不能像工作台一样直接取走产物。
漏斗、投掷器和其他合成器可以与合成器的任何一面互动，将物品转入合成器的未禁用槽位。漏斗和漏斗矿车可以从合成器中取出物品。
被激活后，合成器会消耗合成方格中的材料合成一份产物，同时将产物从正面掷出。如果合成器的前方存在容器（包括另一个合成器），且容器的槽位允许接收该产物，那么产物会直接存入容器。
图为Minecraft Live 2023展示的合成器。
在创造模式中，玩家拥有无限的方块用于创造，没有生命值、饥饿值和氧气值来阻碍他们的建造，因此不必担心有危险。创造模式允许玩家在没有拿剑、三叉戟或重锤时瞬间破坏大多数的方块，包括像基岩和末地传送门这种正常情况下不能破坏的方块，除隐形基岩[仅基岩版]等。使用一次性的物品不会使其被消耗。武器与工具也不会有耐久度的限制，不会损坏。由创造模式玩家发射的箭只能被创造模式玩家捡起。

创造模式给予玩家额外0.5格方块交互距离和额外2格实体交互距离。

创造模式给予玩家飞行的能力。玩家可通过快速按两下跳跃起飞，并通过按住跳跃上升高度，或通过潜行降低高度和着陆；使用移动可在同一高度下移动。另外，玩家在空中快速按两下跳跃可离开飞行状态并掉下来。在Java版中，如果飞行时降落在方块上，玩家会自动退出飞行状态；基岩版中则不会，但速度仍会降到行走的速度。飞行时进入矿车和床后再离开后，玩家将仍然处于飞行状态。


在创造模式中飞行的玩家
在Java版中，玩家在创造模式中无法受到除虚空和/kill外的伤害。当玩家的Y坐标低于世界建筑下限64格或更多时，就会受到虚空伤害；反之如果在世界建筑下限下方64格内，就不会受到虚空伤害，并可以在虚空中飞行。

在基岩版中，玩家在创造模式下不会受到任何伤害。如果在基岩版试图使用/kill杀死创造模式的玩家，聊天栏会提示“玩家在创造模式下无法被杀死”。

生物仍然会像在其他游戏模式中那样生成（包括从刷怪笼中生成），但都永远不会攻击玩家，也不会因被玩家攻击或其他在生存模式中可行的激怒方式被激怒。玩家在创造模式进入末地后，末影龙不会攻击玩家。在Java版中，即使玩家在创造模式下，增援的僵尸仍然会试图攻击玩家，不过不会造成任何伤害，并且在几秒后就会停止攻击。[1]

当一个世界被创建后，如果开启了作弊，可以通过/gamemode creative命令或设置[仅基岩版]来切换到创造模式。在多人游戏中，管理员可以通过/gamemode命令单独切换每一名玩家的游戏模式。这意味着在一个生存模式的世界中（根据管理员的意愿）玩家也可以使用创造模式，反之亦然。新玩家的默认游戏模式也能通过/defaultgamemode命令[仅Java版]或设置中默认游戏模式[仅基岩版]来切换。

如果游戏能确定方块是被创造模式的玩家所破坏的，那么不会有任何掉落物出现（潜影盒和蜂巢除外）。如果游戏不能确定，方块的物品形式仍会掉落。[2]

在基岩版中，无论是以创造模式创建新的世界还是进入旧的世界，都将永久关闭该世界的成就和排行榜的更新，但这并不会对游戏内容造成任何影响。换言之，成就和排行榜只有在一直保持在生存模式或冒险模式下才有效。

"""
        )

        self.scrollarea = SiScrollArea(self)
        self.scrollarea.setFixedHeight(256)
        self.scrollarea.setWidget(self.alabel)

        # 新测试
        self.titled_widget_group = SiTitledWidgetGroup(self)

        self.button_for_option_card = SiPushButton(self)
        self.button_for_option_card.attachment().setText("刷新")
        self.button_for_option_card.resize(128, 32)

        self.optioncard = SiOptionCardLinear(self)
        self.optioncard.load(SiGlobal.icons.get('fi-rr-bulb'))
        self.optioncard.setTitle("测试选项卡", "这是这个选项卡的一段说明性文字，但是它非常非常长")
        self.optioncard.addWidget(self.button_for_option_card)

        self.button_for_option_card2 = SiSimpleButton(self)
        self.button_for_option_card2.setCheckable(False)
        self.button_for_option_card2.attachment().load(SiGlobal.icons.get('fi-rr-link'))
        self.button_for_option_card2.attachment().setText("打开链接")
        self.button_for_option_card2.adjustSize()

        self.optioncard2 = SiOptionCardLinear(self)
        self.optioncard2.load(SiGlobal.icons.get('fi-rr-bulb'))
        self.optioncard2.setTitle("测试选项卡", "这是这个选项卡的一段说明性文字，但是它非常非常长")
        self.optioncard2.addWidget(self.button_for_option_card2)

        self.optioncard3 = SiOptionCardPlane(self)
        self.optioncard3.setTitle("平面选项卡")

        self.button_for_test = SiPushButton(self)
        self.button_for_test.attachment().setText("测试按钮")
        self.button_for_test.resize(128, 32)

        self.button_for_test2 = SiPushButton(self)
        self.button_for_test2.attachment().setText("另一个")
        self.button_for_test2.resize(128, 32)

        self.optioncard3.body().addWidget(self.button_for_test)
        self.optioncard3.body().addWidget(self.button_for_test2)
        self.optioncard3.body().addPlaceholder(24 - 8)
        self.optioncard3.adjustSize()

        self.new_slider = SiSliderH(self)
        #self.new_slider.setStyleSheet("background-color: #20FF0000")
        self.new_slider.setFixedHeight(16)

        self.new_progressbar = SiProgressBar(self)
        self.new_progressbar.setFixedHeight(32)

        self.random_progress_button = SiPushButton(self)
        self.random_progress_button.resize(128, 32)
        self.random_progress_button.attachment().setText("随机进度")
        self.random_progress_button.clicked.connect(lambda: self.new_progressbar.setValue(random.random()))

        self.lineedit = SiLineEdit(self)
        self.lineedit.setFixedHeight(32)

        self.titled_widget_group.setFixedWidth(800)
        #self.titled_widget_group.setStyleSheet("background-color: #20FF0000")
        self.titled_widget_group.addTitle("选项卡")
        self.titled_widget_group.addWidget(self.optioncard)
        self.titled_widget_group.addWidget(self.optioncard2)
        self.titled_widget_group.addWidget(self.optioncard3)
        self.titled_widget_group.addTitle("滑条")
        self.titled_widget_group.addWidget(self.new_slider)
        self.titled_widget_group.addTitle("进度条")
        self.titled_widget_group.addWidget(self.new_progressbar)
        self.titled_widget_group.addWidget(self.random_progress_button)
        self.titled_widget_group.addTitle("输入框")
        self.titled_widget_group.addWidget(self.lineedit)

        self.stack_reconstruct_test.addItem(self.reconstruct_discription)
        self.stack_reconstruct_test.addItem(self.button_layout)
        self.stack_reconstruct_test.addItem(self.button_layout2)
        self.stack_reconstruct_test.addItem(self.container_h)
        self.stack_reconstruct_test.addItem(self.scrollarea)
        self.stack_reconstruct_test.addItem(self.titled_widget_group)

        #self.stack_reconstruct_test.addItem(self.test_label)

        self.addItem(self.discription)
        self.addItem(self.stack_music_info_placeholder)
        self.addItem(self.stack_reconstruct_test)
