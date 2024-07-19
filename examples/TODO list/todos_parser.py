
class TODOParser:
    def __init__(self, path):
        self.path = path
        self.todos = []

        self.read()

    def read(self):
        """
        Read To-Dos from todos.ini
        """
        file = open(self.path, encoding="utf-8")
        todos = file.read().split("<TODO-START-MARK>")[1:]
        self.todos = todos

    def write(self):
        """
        Write current To-Do list into todos.ini
        """
        file = open(self.path, "w", encoding="utf-8")
        for item in self.todos:
            file.write(f"<TODO-START-MARK>{item}")

    def add(self, text: str):
        """
        Add new To-Do into self.todos
        :param text: To-Do
        """
        self.todos.append(text)
