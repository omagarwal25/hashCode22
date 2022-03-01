from Skill import Skill


class Contributor:
    def __init__(self, name: str, skills: list[Skill]):
        self.name = name
        self.skills = skills
        self.busy = False

    def level_up_skill(self, skill: Skill):
        for i in self.skills:
            if i.name == skill.name and i.level <= skill.level:
                i.levelUp()
                return
        self.skills.append(Skill(skill.name, 1))

    def isEligible(self, role: Skill):
        for skill in self.skills:
            if skill == role and skill.level >= role.level - 1:
                return True
        return False

    def isEligibleNoMentees(self, role: Skill):
        for skill in self.skills:
            if skill == role and skill.level >= role.level:
                return True
        return False
