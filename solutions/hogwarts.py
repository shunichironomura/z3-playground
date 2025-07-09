"""During a trial in a Hogwarts court, *Ron claimed that the Flying Ford Anglia car was stolen by Hermione*.

Then Hermione and Harry gave testimonies which, for some reason, were not recorded.
Later on in the trial it was found that the car was stolen by one of these three defendants,
and moreover, *only the guilty one gave true testimony*.

Who stole the car?
"""

from z3 import And, Bool, If, Not, Or, Solver, sat

# Create boolean variables for who stole the car
ron_stole = Bool("ron_stole")
hermione_stole = Bool("hermione_stole")
harry_stole = Bool("harry_stole")

ron_told_truth = Bool("ron_told_truth")
hermione_told_truth = Bool("hermione_told_truth")
harry_told_truth = Bool("harry_told_truth")

# Create solver
solver = Solver()

# Constraint 1: Exactly one person stole the car
solver.add(Or(ron_stole, hermione_stole, harry_stole))
solver.add(If(ron_stole, And(Not(hermione_stole), Not(harry_stole)), True))
solver.add(If(hermione_stole, And(Not(ron_stole), Not(harry_stole)), True))
solver.add(If(harry_stole, And(Not(ron_stole), Not(hermione_stole)), True))

# Constraint 2: Only the guilty person told the truth
solver.add(If(ron_stole, ron_told_truth, Not(ron_told_truth)))
solver.add(If(hermione_stole, hermione_told_truth, Not(hermione_told_truth)))
solver.add(If(harry_stole, harry_told_truth, Not(harry_told_truth)))

# Constraint 3: Ron claimed the car was stolen by Hermione
solver.add(If(ron_told_truth, hermione_stole, Not(hermione_stole)))

if solver.check() == sat:
    model = solver.model()
    if model[ron_stole]:
        solver.add(Not(ron_stole))
        assert solver.check() != sat, "Another possible solution exists, which contradicts the problem statement."
        print("Ron stole the car.")
    elif model[hermione_stole]:
        solver.add(Not(hermione_stole))
        assert solver.check() != sat, "Another possible solution exists, which contradicts the problem statement."
        print("Hermione stole the car.")
    elif model[harry_stole]:
        solver.add(Not(harry_stole))
        assert solver.check() != sat, "Another possible solution exists, which contradicts the problem statement."
        print("Harry stole the car.")
else:
    print("No solution found.")
