from siui.core.animation import abstract
from siui.core.animation.animation import SiCounterAnimation, SiExpAnimation  # noqa: F401
from siui.core.animation.group import SiAnimationGroup  # noqa: F401


def set_global_fps(fps):
    """
    设置全局动画帧率
    :param fps: FPS you want to set
    :return:
    """
    abstract.global_fps = fps


def get_global_fps():
    """
    返回全局动画帧率
    """
    return abstract.global_fps
