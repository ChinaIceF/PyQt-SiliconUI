from contextlib import contextmanager
from typing import Callable, List, Iterable

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAbstractButton, QWidget

from siui.components.button import SiPushButtonRefactor
from siui.components.graphic import SiGraphicWrapperWidget
from siui.components.popover import SiPopover, SiPopoverDatePicker, SiPopoverStackedWidget, SiPopoverCalenderPicker


def _createWrapper(widget: QWidget, animation: Iterable[Callable]) -> SiGraphicWrapperWidget:
    wrapper = SiGraphicWrapperWidget()
    wrapper.setWidget(widget)
    wrapper.setMergeAnimations(*animation)
    return wrapper


def _createButtonSlot(button: QAbstractButton, popover: SiPopover) -> Callable:
    def slot():
        pos = button.mapToGlobal(button.pos()) - QPoint(0, popover.sizeHint().height())
        popover.wrapper().playMergeAnimations()
        popover.popup(pos)

    return slot


def exampleDatePickerPopover(parent: QWidget) -> SiPushButtonRefactor:

    # 本示例将使用 SiPopover 创建一个 popover
    # 包含一个类似 QStackedWidget 的页面堆叠控件 SiPopoverStackedWidget
    # 其具有一个页面，用于展示日期选择器 SiPopoverDatePicker
    # 最后，示例创建一个按钮，用于弹出这个 popover

    # 本示例完整地展示了 popover 的使用方法，并提供详细的注释供参阅。
    # 下面有更多示例，但不再带有详细注释。

    # 创建 popover
    popover = SiPopover()

    # 创建堆叠控件 SiPopoverStackedWidget
    # 这是接下来要显示在 popover 中的控件
    stack_widget = SiPopoverStackedWidget(popover)

    # 创建 SiPopoverDatePicker
    # 这是接下来要添加到 stack_widget 中的控件
    date_picker = SiPopoverDatePicker()

    # 创建 "日期选择" 页面所需的图形包装器，并将 date_picker 添加到包装器里。
    # 使用图形包装器，我们可以实现更强大的视觉变换效果，如仿射变换，透明度等等
    # 这里，我们仅利用其实现页面的弹出动画
    page_wrapper = SiGraphicWrapperWidget()
    page_wrapper.setWidget(date_picker)

    # SiGraphicWrapperWidget 提供了强大且丰富的动画预设，它们可以直接组合在一起
    # 更多动画可以在 SiGraphicWrapperWidget.TransitionAnimations 下获取，
    # 部分支持的动画已经给出，你可以尝试移除注释组合他们
    # 你也可以仿照这些动画的实现，创造你自己的动画。不过对于大多数场景，预设动画及其组合已经足够
    page_wrapper.setMergeAnimations(
        # SiGraphicWrapperWidget.TransitionAnimations.scaleUp,
        # SiGraphicWrapperWidget.TransitionAnimations.fadeIn,
        SiGraphicWrapperWidget.TransitionAnimations.floatUp,
        # SiGraphicWrapperWidget.TransitionAnimations.floatLeftIn,
    )

    # 将构建的 page_wrapper 添加到 stack_widget 中
    stack_widget.addPage(page_wrapper, "日期选择")

    # 最后，将 stack_widget 添加到 popover 的 wrapper 中
    # 需要说明的是，SiPopover 的内容同样是 Graphic View Framework 驱动的
    # 因此，同样也可以给它设置弹出动画。
    popover.wrapper().setWidget(stack_widget)
    popover.wrapper().setMergeAnimations(
        SiGraphicWrapperWidget.TransitionAnimations.floatUp,
    )

    # 以上的构建过程实际上可以使用 with 语句简化代码。但此处展示具体步骤而展开编写。
    # 总体来说，在本示例中，控件之间的关系为：
    # SiPopover -(wrapper)-> SiPopoverStackedWidget -(wrapper)-> SiPopoverDatePicker

    # 创建按钮
    button = SiPushButtonRefactor(parent)
    button.setText("打开 日期选择器 示例")
    button_slot = _createButtonSlot(button, popover)

    button.clicked.connect(button_slot)

    return button


def exampleCalenderPickerPopover(parent: QWidget) -> SiPushButtonRefactor:
    popover = SiPopover()
    stack_widget = SiPopoverStackedWidget(popover)

    page1 = _createWrapper(
        widget=SiPopoverCalenderPicker(parent),
        animation=(
            SiGraphicWrapperWidget.TransitionAnimations.floatUp,
        )
    )

    stack_widget.addPage(page1, "日历选择器")

    popover.wrapper().setWidget(stack_widget)
    popover.wrapper().setMergeAnimations(
        SiGraphicWrapperWidget.TransitionAnimations.floatUp,
    )

    button = SiPushButtonRefactor(parent)
    button.setText("打开 日历选择器 示例")
    button_slot = _createButtonSlot(button, popover)

    button.clicked.connect(button_slot)

    return button
