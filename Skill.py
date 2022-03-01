class Skill:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def levelUp(self):
        self.level = self.level + 1

    def __eq__(self, other):
        return self.name == other.name