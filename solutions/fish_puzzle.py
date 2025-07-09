"""Who Owns the Fish? (Simplified 3-person version).

Three people: Alice, Bob, Charlie
Three pets: Dog, Cat, Fish
Three drinks: Coffee, Tea, Milk

Clues:
1. Alice doesn't drink coffee
2. The dog owner drinks milk
3. Bob owns the cat
4. The tea drinker sits next to the fish owner
5. Charlie sits in the middle
"""

from z3 import Distinct, Implies, Int, Not, Or, Solver, sat

# Create solver
s = Solver()

# Define people, pets, drinks, and positions as integers
# People: Alice=0, Bob=1, Charlie=2
# Pets: Dog=0, Cat=1, Fish=2
# Drinks: Coffee=0, Tea=1, Milk=2
ALICE = DOG = COFFEE = LEFT = 0
BOB = CAT = TEA = MIDDLE = 1
CHARLIE = FISH = MILK = RIGHT = 2

# Variables: who owns which pet and drinks what
# pet[i] = j means person i owns pet j
pet = [Int(f"pet_{i}") for i in range(3)]
drink = [Int(f"drink_{i}") for i in range(3)]
positions = [Int(f"pos_{i}") for i in range(3)]

# Each person owns exactly one pet (0, 1, or 2)
for i in range(3):
    s.add(pet[i] >= 0, pet[i] <= 2)
    s.add(drink[i] >= 0, drink[i] <= 2)
    s.add(positions[i] >= 0, positions[i] <= 2)

# Each pet is owned by exactly one person
s.add(Distinct(pet))
s.add(Distinct(drink))
s.add(Distinct(positions))

# Clue 1: Alice (0) doesn't drink coffee (0)
s.add(drink[ALICE] != COFFEE)

# Clue 3: Bob (1) owns the cat (1)
s.add(pet[BOB] == CAT)

# Clue 2: The dog (0) owner drinks milk (2)
for i in range(3):
    s.add(Implies(pet[i] == DOG, drink[i] == MILK))

# Clue 4: Tea (1) drinker sits next to fish (2) owner
# In a row of 3, "next to" means adjacent positions
tea_drinker_pos = Int("tea_pos")
fish_owner_pos = Int("fish_pos")

# Find who drinks tea and who owns fish
for i in range(3):
    s.add(Implies(drink[i] == TEA, tea_drinker_pos == positions[i]))
    s.add(Implies(pet[i] == FISH, fish_owner_pos == positions[i]))

# Adjacent means difference of 1
s.add(Or(tea_drinker_pos - fish_owner_pos == 1, fish_owner_pos - tea_drinker_pos == 1))

# Solve and print results
if s.check() == sat:
    m = s.model()
    print("Solution found!\n")

    people = ["Alice", "Bob", "Charlie"]
    pets_names = ["Dog", "Cat", "Fish"]
    drinks_names = ["Coffee", "Tea", "Milk"]
    position_names = ["Left", "Middle", "Right"]

    for i in range(3):
        pet_val = m[pet[i]].as_long()
        drink_val = m[drink[i]].as_long()
        position_val = m[positions[i]].as_long()
        print(
            f"{people[i]}: owns {pets_names[pet_val]}, drinks {drinks_names[drink_val]},"
            f" at position {position_names[position_val]}",
        )

    # Answer the question
    for i in range(3):
        if m[pet[i]].as_long() == FISH:
            print(f"\n** {people[i]} owns the fish! **")
            fish_owner = i

    # Check other possibilities
    s.add(Not(pet[i] == FISH))
    if s.check() == sat:
        m = s.model()
        print("\nAnother solution found!\n")
        for i in range(3):
            pet_val = m[pet[i]].as_long()
            drink_val = m[drink[i]].as_long()
            position_val = m[positions[i]].as_long()
            print(
                f"{people[i]}: owns {pets_names[pet_val]}, drinks {drinks_names[drink_val]},"
                f" at position {position_names[position_val]}",
            )
    else:
        print("\nNo other solutions found after excluding the fish owner.")
else:
    print("No solution found!")
