from typing import Optional

from Contributor import Contributor
from Skill import Skill


class Project:
    def __init__(self, name: str, duration: int, score: int, expiry: int, roles: list[Skill]):
        self.name = name
        self.duration = duration
        self.score = score
        self.expiry = expiry
        self.roles = roles
        self.done = False
        self.doing = False
        self.daysOfWorkDone = 0
        self.endDate: Optional[int] = None
        self.workers: list[(Skill, Contributor)] = []

    def markAsDone(self, day: int):
        self.done = True
        self.doing = False
        self.endDate = day

    def incrementDays(self):
        self.daysOfWorkDone += 1

    def markAsStarted(self, workers: list[(Skill, Contributor)]):
        self.doing = True
        self.workers = workers

    def isProjectDone(self) -> bool:
        return self.duration == self.daysOfWorkDone

    def getEstimatedScore(self, day: int) -> int:
        return min(max(self.score - day - self.duration + self.expiry, self.score), 0)
