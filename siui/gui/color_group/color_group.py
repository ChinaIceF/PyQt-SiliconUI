
from siui.core import SiColor


class SiColorGroup:
    def __getitem__(self, item):
        return self.colors[item]

    def __init__(self,
                 overwrite=None,
                 reference=None):

        self.valid_state = True
        self.colors = {}

        if overwrite is not None:
            self.overwrite(overwrite)
            if reference is None:
                self.reference = overwrite.reference
            else:
                self.reference = reference
        else:
            self.reference = reference

    def assign(self, token, code):
        self.colors[token.name] = code

    def remove(self, token):
        if token.name in self.colors.keys():
            self.colors.pop(token.name)

    def fromToken(self, token):
        if token.name in self.colors.keys() and self.valid_state:
            return self.colors[token.name]
        if self.reference is None:
            raise ValueError(
                f"Color under token {token.name} is not assigned yet either in this group or in its reference\n"
                f"Valid state: {self.valid_state}"
            )
        else:
            return self.reference.fromToken(token)

    def isAssigned(self, token):
        if self.reference is None:
            return token.name in self.colors.keys()
        else:
            return ((token.name in self.colors.keys()) and self.valid_state) or self.reference.isAssigned(token)

    def overwrite(self, color_group):
        self.colors.update(color_group.colors)

    def setReference(self, color_group):
        self.reference = color_group

    def setValid(self, state):
        self.valid_state = state

    def isValid(self):
        return self.valid_state

