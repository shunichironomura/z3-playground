"""Who owns the fish?.

• Alice, Bob, Charlie の 3 人が一列に並んでいる。
• 3 人は犬、猫、魚のうちいずれかを 1 匹飼っており、同じペットを飼っている人はいない。
• 3 人はコーヒー、紅茶、牛乳のうちいずれかを 1 杯飲んでいる。同じ飲み物を飲んでいる人はいない。
• 以下の証拠から、誰が魚を飼っているかを特定せよ。
‣ アリスはコーヒーを飲んでいない。
‣ 犬を飼っている人は牛乳を飲んでいる。
‣ ボブは猫を飼っている。
‣ 紅茶を飲んでいる人は魚を飼っている人の隣にいる。
‣ チャーリーは真ん中に立っている。
"""

from enum import Enum

from z3 import Abs, Distinct, Implies, Int, Solver, sat


class Person(Enum):
    Alice = 0
    Bob = 1
    Charlie = 2


class Pet(Enum):
    Dog = 0
    Cat = 1
    Fish = 2


class Drink(Enum):
    Coffee = 0
    Tea = 1
    Milk = 2


class Position(Enum):
    Left = 0
    Middle = 1
    Right = 2


pet = {person: Int(f"{person}_pet") for person in Person}
drink = {person: Int(f"{person}_drink") for person in Person}
position = {person: Int(f"{person}_position") for person in Person}

s = Solver()
for person in Person:
    s.add(pet[person] >= 0, pet[person] < len(Pet))
    s.add(drink[person] >= 0, drink[person] < len(Drink))
    s.add(position[person] >= 0, position[person] < len(Position))

s.add(Distinct(*pet.values()))
s.add(Distinct(*drink.values()))
s.add(Distinct(*position.values()))

# ‣ アリスはコーヒーを飲んでいない。
s.add(drink[person.Alice] != Drink.Coffee.value)

# ‣ 犬を飼っている人は牛乳を飲んでいる。
for person in Person:
    s.add(Implies(pet[person] == Pet.Dog.value, drink[person] == Drink.Milk.value))

# ‣ ボブは猫を飼っている。
s.add(pet[person.Bob] == Pet.Cat.value)

# ‣ 紅茶を飲んでいる人は魚を飼っている人の隣にいる。
position_tea = Int("position_tea")
position_fish = Int("position_fish")
s.add(position_tea >= 0, position_tea < len(Position))
s.add(position_fish >= 0, position_fish < len(Position))
for person in Person:
    s.add(Implies(drink[person] == Drink.Tea.value, position[person] == position_tea))
    s.add(Implies(pet[person] == Pet.Fish.value, position[person] == position_fish))

s.add(Abs(position_tea - position_fish) == 1)

# ‣ チャーリーは真ん中に立っている。
s.add(position[Person.Charlie] == Position.Middle.value)

if s.check() == sat:
    print("satisfied")
    m = s.model()
    for person in Person:
        pet_val = Pet(m[pet[person]].as_long())
        drink_val = Drink(m[drink[person]].as_long())
        position_val = Position(m[position[person]].as_long())
        print(f"{person} owns pet {pet_val}, drinks {drink_val}, at position {position_val}")
