from siui.core.animation.abstract import ABCSiAnimation


class SiAnimationGroup:
    """
    动画组，为多个动画的管理提供支持，允许使用token访问动画对象
    """
    def __init__(self):
        self.animations = []
        self.tokens = []

    def addMember(self, ani, token: str):
        if token in self.tokens:
            raise ValueError(f"代号已经存在：{token}")
        self.animations.append(ani)
        self.tokens.append(token)

    def fromToken(self, aim_token: str) -> ABCSiAnimation:
        for ani, token in zip(self.animations, self.tokens):
            if token == aim_token:
                return ani
        raise ValueError(f"未在代号组中找到传入的代号：{aim_token}")
