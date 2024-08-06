from ..layer import ABCSiLayer


class LayerChildPage(ABCSiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)