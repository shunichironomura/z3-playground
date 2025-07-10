"""Hogwarts problem.

During a trial in a Hogwarts court, Ron claimed that the Flying Ford Anglia car was stolen by Hermione.
Then Hermione and Harry gave testimonies which, for some reason, were not recorded.
Later on in the trial it was found that the car was stolen by one of these three defendants,
and moreover, only the guilty one gave true testimony.
Who stole the car?
"""

from enum import Enum

from z3 import And, Bool, If, Implies, Not, Or, Solver, sat


class Person(Enum):
    Ron = 0
    Hermione = 1
    Harry = 2


told_truth = {person: Bool(f"{person}_told_truth") for person in Person}
is_guilty = {person: Bool(f"{person}_is_guilty") for person in Person}

s = Solver()

# Only one of them is guilty
s.add(Or(*(is_guilty[person] for person in Person)))
for person in Person:
    others = [p for p in Person if p != person]
    s.add(Implies(is_guilty[person], And(*(Not(is_guilty[p]) for p in others))))

# Only the guilty one told the truth
for person in Person:
    s.add(If(is_guilty[person], told_truth[person], Not(told_truth[person])))


# Ron told Hermione stole the car
s.add(If(told_truth[person.Ron], is_guilty[person.Hermione], Not(is_guilty[person.Hermione])))

if s.check() == sat:
    m = s.model()
    for person in Person:
        told_truth_val = "told the truth" if m[told_truth[person]] else "didn't tell the truth"
        is_guilty_val = "is guilty" if m[is_guilty[person]] else "is not guilty"
        print(f"{person} {told_truth_val} and {is_guilty_val}")
else:
    print("No solution found")
