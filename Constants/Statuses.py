from enum import IntFlag, auto

class Statuses(IntFlag):
    Sleep1 = auto()
    Sleep2 = auto()
    Sleep4 = auto()
    Poison = auto()
    Burn = auto()
    Freeze = auto()
    Paralyze = auto()

Statuses.Sleep3 = Statuses.Sleep1 | Statuses.Sleep2
Statuses.Sleep5 = Statuses.Sleep1 | Statuses.Sleep4
Statuses.Sleep6 = Statuses.Sleep2 | Statuses.Sleep4
Statuses.Sleep7 = Statuses.Sleep1 | Statuses.Sleep2 | Statuses.Sleep4
Statuses.Sleep = Statuses.Sleep1 | Statuses.Sleep2 | Statuses.Sleep4
