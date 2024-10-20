import time
from enum import Enum

from PyQt5.QtWidgets import QApplication, QDesktopWidget

from siui.components.menu.abstracts.menu import ABCSiMenu
from siui.core import SiColor


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
        screen_geo = QDesktopWidget().screenGeometry()
        x = min(max(32, x), screen_geo.width() - parent.sizeHint().width())
        y = min(max(32, y), screen_geo.height() - parent.sizeHint().height())

        parent.unfoldSignal.emit()

        body_preferred_height = parent.body_.sizeHint().height()
        parent.move(x, y)
        parent.show()

        target_height = body_preferred_height + parent.margin * 2 + parent.padding * 2
        parent.resize(parent.width(), int(target_height * 0.6))
        parent.resizeTo(parent.width(), target_height)

        parent.flash_layer.setColor(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 1))
        parent.flash_layer.setColorTo(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 0))

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


class AnimationManagerRaiseUp(ABCAnimationManager):
    @staticmethod
    def on_parent_unfolded(parent, x, y):
        screen_geo = QDesktopWidget().screenGeometry()
        x = min(max(32, x), screen_geo.width() - parent.sizeHint().width())
        y = min(max(32, y), screen_geo.height() - parent.sizeHint().height())

        parent.unfoldSignal.emit()

        body_preferred_height = parent.body_.sizeHint().height()
        target_height = body_preferred_height + parent.margin * 2 + parent.padding * 2

        parent.move(x, y + int(target_height * 0) + 64)
        parent.show()

        parent.resize(parent.width(), int(target_height * 0.6))
        parent.resizeTo(parent.width(), target_height)
        parent.moveTo(x, y)

        parent.flash_layer.setColor(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 1))
        parent.flash_layer.setColorTo(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 0))

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

        parent.setAnchorByIndex(parent.index())
        print(parent.move_anchor)
        body_preferred_height = parent.body_.sizeHint().height()
        target_height = body_preferred_height + parent.margin * 2 + parent.padding * 2
        parent.anchor_rate = (parent.moveAnchor().y() - parent.margin - parent.padding) / body_preferred_height

        parent.setGeometry(x - parent.moveAnchor().x(), y - parent.moveAnchor().y(), parent.width(), target_height)
        parent.body().resize(parent.body().width(), 0)
        parent.show()

        parent.flash_layer.setColor(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 1))
        parent.flash_layer.setColorTo(SiColor.trans(parent.getColor(SiColor.BUTTON_FLASH), 0))

    @staticmethod
    def on_parent_resized(parent, event):
        # print(parent.anchor_rate)

        shift = parent.margin + parent.padding
        size = event.size()

        #parent.body().adjustWidgetsGeometry = print
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
        QApplication.processEvents()
        parent.move(parent.pos().x() + previous_anchor_x, parent.pos().y() + previous_anchor_y)
        QApplication.processEvents()
        parent.body_panel.setGeometry(0,
                                      parent.moveAnchor().y() - shift - int(parent.body().sizeHint().height() *
                                                                            parent.anchor_rate),
                                      size.width() - parent.margin * 2,
                                      size.height() - parent.margin * 2)
        QApplication.processEvents()
        parent.body_.setGeometry(parent.padding,
                                 parent.padding,
                                 size.width() - parent.margin * 2 - parent.padding * 2,
                                 size.height() - parent.margin * 2 - parent.padding * 2)

        #time.sleep(0.5)


class AnimationManager(Enum):
    PULL_DOWN = AnimationManagerPullDown()
    RAISE_UP = AnimationManagerRaiseUp()
    EXPAND = AnimationManagerPullDown()  # temporarily use pulling down due to flicks in expanding animations
