from Contributor import Contributor
from Projects import Project
from Skill import Skill


def atLeastOneProjectDoing(projects: list[Project]):
    for project in projects:
        if project.doing:
            return True


class Status:
    def __init__(self, file: str):
        self.current_day = 0
        self.projectsDone = 0
        self.contributors: set[Contributor] = set()
        self.projects: list[Project] = []
        self.finishedProjects: list[(Project, list[Contributor])] = []
        self.readFile(file)

    def selectNextProject(self) -> list[(Project, int)]:
        filtered: list[Project] = []

        for i in self.projects:
            if not i.doing:
                filtered.append(i)

        filtered.sort(key=lambda t: t.expiry - t.duration, reverse=False)

        weighted: list[(Project, int)] = []

        for i in filtered:
            weighted.append((i, max(min(i.score - self.current_day - i.duration + i.expiry, i.score), 0)))

        weighted.sort(key=lambda t: t[1], reverse=True)

        return weighted

    def readFile(self, file: str):
        with open(file, "r") as f:
            line = f.readline()[:-1].split(" ")  # kills off the newline char, splits by spaces

            num_contributors, num_projects = int(line[0]), int(line[1])

            for _ in range(num_contributors):
                line = f.readline()[:-1].split(" ")
                name = line[0]
                skills: list[Skill] = []
                for i in range(int(line[1])):
                    line = f.readline()[:-1].split(" ")
                    skills.append(Skill(line[0], int(line[1])))

                self.contributors.add(Contributor(name, skills))

            for _ in range(num_projects):
                line = f.readline()[:-1].split(" ")

                name = line[0]
                duration = int(line[1])
                score = int(line[2])
                expiry = int(line[3])
                number_roles = int(line[4])

                skills: list[Skill] = []

                for i in range(number_roles):
                    line = f.readline()[:-1].split(" ")
                    skills.append(Skill(line[0], int(line[1])))

                self.projects.append(Project(name, duration, score, expiry, skills))

    def findContributorForRole(self, role: Skill):
        eligibleContributors = self.getEligibleContributors(role)
        for contributor in eligibleContributors:  # check for same levels
            #  first check for if there are any same levels, then check for level-1 and mentor
            for skill in contributor.skills:
                if skill == role and skill.level >= role.level:
                    contributor.busy = True
                    return contributor
        return False

    def findMenteeForRole(self, role: Skill):
        eligibleContributors = self.getEligibleContributors(role)
        for possibleJunior in eligibleContributors:
            for juniorSkill in possibleJunior.skills:
                if juniorSkill == role and juniorSkill.level == role.level - 1:
                    possibleJunior.busy = True
                    return possibleJunior
        return False

    def getEligibleContributors(self, role: Skill):
        contributors: list[Contributor] = []
        for contributor in self.contributors:
            if contributor.busy:
                continue
            if contributor.isEligible(role):
                contributors.append(contributor)
        return contributors

    def projectIsCompletable(self, project: Project) -> bool:
        workers = self.assignWorkersToProject(project)
        contributors = [contributor for (role, contributor) in workers]
        return not None in contributors or len(contributors) == 0

    def assignWorkersToProject(self, project: Project) -> list[(Skill, Contributor)]:
        workers: list[(Skill, Contributor)] = []
        for role in project.roles:
            workers.append((role, self.findContributorForRole(role)))
            if workers[-1][1]:  # if you found someone qualified move on to next role
                continue
            else:  # delete the False and find a mentee
                del workers[-1]
                foundMentee = False
                for (e, contributor) in workers:
                    if contributor is not None and contributor.isEligibleNoMentees(role):  # if mentor exists in project
                        workers.append((role, self.findMenteeForRole(role)))
                        foundMentee = True
                if not foundMentee:
                    workers.append((role, None))
        return workers

    def day(self):
        for (project, i) in self.selectNextProject():
            if self.projectIsCompletable(project):
                workers = self.assignWorkersToProject(project)
                if len(workers) == 0:
                    continue

                cont = False

                for (_, x) in workers:
                    if x is None:
                        cont = True

                if cont:
                    continue

                project.markAsStarted(workers)

                for (_, x) in workers:
                    x.busy = True

        self.current_day += 1
        for i in self.projects:
            if i.doing:
                i.incrementDays()
                if i.isProjectDone():
                    i.markAsDone(self.current_day)
                    for b in i.workers:
                        b[1].busy = False

                    self.finishedProjects.append((i, (x[1] for x in i.workers)))

                    for x in i.workers:
                        worker = i.workers[x]

                        worker.level_up_skill(x)

    def simulate(self):
        while True:
            self.day()
            projects = self.selectNextProject()
            breakable = False

            if atLeastOneProjectDoing(self.projects):
                breakable = True

            for (i, j) in projects:
                if j != 0 or i.doing:
                    breakable = True

            if not breakable:
                break

    def __str__(self):
        output = ""
        output += str(len(self.finishedProjects)) + "\n"
        for project in self.finishedProjects:
            output += project[0] + "\n"
            for contributor in project[1]:
                output += contributor + " "
            output += "\n"
        return output




def main():
    status = Status("./input/a_an_example.in.txt")
    status.simulate()
    print(status)


if __name__ == '__main__':
    main()
