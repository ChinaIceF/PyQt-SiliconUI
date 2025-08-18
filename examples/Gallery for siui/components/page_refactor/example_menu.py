from contextlib import contextmanager

from PyQt5.QtWidgets import QAction, QActionGroup, QWidget

from siui.components.combobox_ import ComboboxItemWidget
from siui.components.menu_ import SiRoundedMenu
from siui.core import SiGlobal


def exampleSiRoundedMenu(parent: QWidget) -> SiRoundedMenu:
    @contextmanager
    def useMenu(menu: SiRoundedMenu):
        yield menu

    main_menu = SiRoundedMenu(parent)

    sub_menu_1 = SiRoundedMenu(main_menu)
    sub_menu_1.setTitle("纯文字菜单")
    sub_menu_1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_text_regular"))
    with useMenu(sub_menu_1) as menu:
        menu: SiRoundedMenu
        menu.addAction(QAction("名称"))
        menu.addAction(QAction("大小"))
        menu.addAction(QAction("项目类型"))
        menu.addAction(QAction("修改日期"))

    sub_menu_2 = SiRoundedMenu(main_menu)
    sub_menu_2.setTitle("带图标的菜单")
    sub_menu_2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_image_regular"))
    with useMenu(sub_menu_2) as menu:
        menu: SiRoundedMenu
        action1 = QAction("名称")
        action1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_rename_regular"))
        action2 = QAction("大小")
        action2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_resize_regular"))
        action3 = QAction("项目类型")
        action3.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_class_regular"))
        action4 = QAction("修改日期")
        action4.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_calendar_date_regular"))

        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        menu.addAction(action4)

    sub_menu_3 = SiRoundedMenu(main_menu)
    sub_menu_3.setTitle("图标与快捷键")
    sub_menu_3.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_keyboard_regular"))
    with useMenu(sub_menu_3) as menu:
        menu: SiRoundedMenu
        action1 = QAction("复制")
        action1.setShortcut("Ctrl+C")
        action1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_copy_regular"))
        action2 = QAction("剪切")
        action2.setShortcut("Ctrl+X")
        action2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_cut_regular"))
        action3 = QAction("粘贴")
        action3.setShortcut("Ctrl+V")
        action3.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_clipboard_paste_regular"))
        action4 = QAction("撤销")
        action4.setShortcut("Ctrl+Z")
        action4.setEnabled(False)
        action4.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_arrow_undo_regular"))

        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        menu.addSeparator()
        menu.addAction(action4)

    sub_menu_4 = SiRoundedMenu(main_menu)
    sub_menu_4.setTitle("可选择")
    sub_menu_4.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_table_checker_filled"))
    with useMenu(sub_menu_4) as menu:
        menu: SiRoundedMenu

        action1 = QAction("命令行模式")
        action1.setCheckable(True)
        action1.setChecked(True)
        action2 = QAction("窗口模式")
        action2.setCheckable(True)

        group1 = QActionGroup(parent)
        group1.addAction(action1)
        group1.addAction(action2)
        group1.setExclusionPolicy(group1.ExclusionPolicy.Exclusive)

        action1 = QAction("自动求和运算")
        action1.setCheckable(True)
        action1.setChecked(True)
        action2 = QAction("自动翻译")
        action2.setCheckable(True)
        action2.setChecked(True)

        group2 = QActionGroup(parent)
        group2.addAction(action1)
        group2.addAction(action2)
        group2.setExclusionPolicy(group2.ExclusionPolicy.None_)

        action3 = QAction("自动保存")
        action3.setCheckable(True)
        action3.setChecked(True)

        menu.addActions(group1.actions())
        menu.addSeparator()
        menu.addActions(group2.actions())
        menu.addSeparator()
        menu.addAction(action3)

    sub_menu_5 = SiRoundedMenu(main_menu)
    sub_menu_5.setTitle("可选择且带图标")
    sub_menu_5.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_table_checker_filled"))
    with useMenu(sub_menu_5) as menu:
        menu: SiRoundedMenu

        action1 = QAction("命令行模式")
        action1.setCheckable(True)
        action1.setChecked(True)
        action1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_window_console_regular"))
        action2 = QAction("窗口模式")
        action2.setCheckable(True)
        action2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_window_bullet_list_regular"))

        group1 = QActionGroup(parent)
        group1.addAction(action1)
        group1.addAction(action2)
        group1.setExclusionPolicy(group1.ExclusionPolicy.Exclusive)

        action1 = QAction("自动求和运算")
        action1.setCheckable(True)
        action1.setChecked(True)
        action1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_autosum_regular"))
        action2 = QAction("自动翻译")
        action2.setCheckable(True)
        action2.setChecked(True)
        action2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_translate_auto_regular"))

        group2 = QActionGroup(parent)
        group2.addAction(action1)
        group2.addAction(action2)
        group2.setExclusionPolicy(group2.ExclusionPolicy.None_)

        action3 = QAction("自动保存")
        action3.setCheckable(True)
        action3.setChecked(True)
        action3.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_save_regular"))

        menu.addActions(group1.actions())
        menu.addSeparator()
        menu.addActions(group2.actions())
        menu.addSeparator()
        menu.addAction(action3)

    sub_menu_6 = SiRoundedMenu(main_menu)
    sub_menu_6.setTitle("多层子菜单")
    sub_menu_6.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_stack_regular"))
    with useMenu(sub_menu_6) as menu1:
        menu1: SiRoundedMenu

        sub_1 = SiRoundedMenu(menu1)
        sub_1.setTitle("子菜单1")
        sub_1.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_stack_regular"))
        with useMenu(sub_1) as menu2:
            menu2: SiRoundedMenu

            sub_2 = SiRoundedMenu(menu2)
            sub_2.setTitle("子菜单2")
            sub_2.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_stack_regular"))
            with useMenu(sub_2) as menu:
                menu: SiRoundedMenu
                menu.addAction(QAction("名称"))
                menu.addAction(QAction("大小"))
                menu.addAction(QAction("项目类型"))
                menu.addAction(QAction("修改日期"))

            menu2.addMenu(sub_2)
        menu1.addMenu(sub_1)

    sub_menu_7 = SiRoundedMenu(main_menu)
    sub_menu_7.setTitle("长菜单")
    sub_menu_7.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_table_checker_filled"))
    with useMenu(sub_menu_7) as menu:
        menu: SiRoundedMenu

        for i in range(1, 50):
            menu.addAction(f"Action {i}")

    sub_menu_8 = SiRoundedMenu(main_menu)
    sub_menu_8.setTitle("Combobox 控件测试")
    sub_menu_8.setIcon(SiGlobal.siui.iconpack.toIcon("ic_fluent_table_checker_filled"))
    with useMenu(sub_menu_8) as menu:
        group = QActionGroup(parent)
        group.setExclusive(True)
        for i in range(10):
            new_action = QAction(f"选项 {i}")
            new_action.setCheckable(True)
            group.addAction(new_action)

        for action in group.actions():
            menu.addCustomWidget(action, ComboboxItemWidget)

    main_menu.addMenu(sub_menu_1)
    main_menu.addMenu(sub_menu_2)
    main_menu.addMenu(sub_menu_3)
    main_menu.addSeparator()
    main_menu.addMenu(sub_menu_4)
    main_menu.addMenu(sub_menu_5)
    main_menu.addSeparator()
    main_menu.addMenu(sub_menu_6)
    main_menu.addSeparator()
    main_menu.addMenu(sub_menu_7)
    main_menu.addMenu(sub_menu_8)

    return main_menu
