from enum import Enum

from siui.components.menu.abstracts.menu import ABCSiMenu
from siui.core.color import SiColor
from PyQt5.QtCore import QPoint
from PyQt5.Qt import QApplication


class ABCAnimationManager:
    @staticmethod
    def on_parent_resized(parent: ABCSiMenu, event):
        return NotImplementedError()

    @staticmethod
    def on_parent_unfolded(parent: ABCSiMenu, x, y):
        return NotImplementedError()


class AnimationManagerPullDown(ABCAnimationManager):
    @staticmethod
    def on_parent_unfolded(parent, x, y):
        parent.unfoldSignal.emit()

        _, body_preferred_height = parent.body_.getPreferredSize()
        parent.move(x, y)
        parent.show()

        target_height = body_preferred_height + parent.margin * 2 + parent.padding * 2
        parent.resize(parent.width(), int(target_height * 0.6))
        parent.resizeTo(parent.width(), target_height)

        parent.flash_layer.setColor(SiColor.trans(parent.colorGroup().fromToken(SiColor.BUTTON_FLASH), 1))
        parent.flash_layer.setColorTo(SiColor.trans(parent.colorGroup().fromToken(SiColor.BUTTON_FLASH), 0))

    @staticmethod
    def on_parent_resized(parent, event):
        size = event.size()
        parent.flash_layer.setGeometry(parent.margin,
                                       parent.margin,
                                       size.width() - parent.margin * 2,
                                       size.height() - parent.margin * 2)
        parent.body_frame.setGeometry(parent.margin,
                                      parent.margin,
                                      size.width() - parent.margin * 2,
                                      size.height() - parent.margin * 2)
        parent.body_panel.resize(size.width() - parent.margin * 2,
                                 size.height() - parent.margin * 2)
        parent.body_.setGeometry(parent.padding,
                                 parent.padding,
                                 size.width() - parent.margin * 2 - parent.padding * 2,
                                 size.height() - parent.margin * 2 - parent.padding * 2)


class AnimationManagerExpand(ABCAnimationManager):
    @staticmethod
    def on_parent_unfolded(parent, x, y):
        parent.unfoldSignal.emit()

        _, body_preferred_height = parent.body_.getPreferredSize()
        parent.setAnchorByIndex(parent.index())
        # parent.getAnimationGroup().fromToken("resize").setInterval(500)
        parent.anchor_rate = (parent.moveAnchor().y() - parent.margin - parent.padding) / body_preferred_height
        parent.move(x, y)

        target_height = body_preferred_height + parent.margin * 2 + parent.padding * 2
        parent.resize(parent.width(), int(target_height * 0.7))
        parent.show()
        parent.resizeTo(parent.width(), target_height)

        parent.flash_layer.setColor(SiColor.trans(parent.colorGroup().fromToken(SiColor.BUTTON_FLASH), 1))
        parent.flash_layer.setColorTo(SiColor.trans(parent.colorGroup().fromToken(SiColor.BUTTON_FLASH), 0))

    @staticmethod
    def on_parent_resized(parent, event):
        # print(parent.anchor_rate)

        shift = parent.margin + parent.padding
        size = event.size()

        previous_anchor_x, previous_anchor_y = parent.moveAnchor().x(), parent.moveAnchor().y()
        parent.setMoveAnchor(previous_anchor_x,
                             int((parent.height() - shift*2) * parent.anchor_rate) + shift)

        parent.frame_debugging.resize(event.size())
        parent.flash_layer.setGeometry(parent.margin,
                                       parent.margin,
                                       size.width() - parent.margin * 2,
                                       size.height() - parent.margin * 2)
        parent.body_frame.setGeometry(parent.margin,
                                      parent.margin,
                                      size.width() - parent.margin * 2,
                                      size.height() - parent.margin * 2)
        parent.move(parent.pos().x() + previous_anchor_x, parent.pos().y() + previous_anchor_y)
        parent.body_panel.setGeometry(0,
                                      parent.moveAnchor().y() - shift - int(parent.body().getPreferredSize()[1] *
                                                                            parent.anchor_rate),
                                      size.width() - parent.margin * 2,
                                      size.height() - parent.margin * 2)
        parent.body_.setGeometry(parent.padding,
                                 parent.padding,
                                 size.width() - parent.margin * 2 - parent.padding * 2,
                                 size.height() - parent.margin * 2 - parent.padding * 2)


class AnimationManager(Enum):
    PULL_DOWN = AnimationManagerPullDown()
    EXPAND = AnimationManagerPullDown()
