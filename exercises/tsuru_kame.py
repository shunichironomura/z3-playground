from z3 import Int, Not, Solver, sat

n_tsuru = Int("n_tsuru")
n_kame = Int("n_kame")

N_HEADS = 8
N_LEGS = 26

s = Solver()
s.add(n_tsuru >= 0)
s.add(n_kame >= 0)
s.add(n_tsuru + n_kame == N_HEADS)
s.add(n_tsuru * 2 + n_kame * 4 == N_LEGS)

if s.check() == sat:
    m = s.model()
    print(f"# of Tsuru's: {m[n_tsuru]}, # of Kame's: {m[n_kame]}.")

    s.add(Not(n_tsuru == m[n_tsuru], n_kame == m[n_kame]))
    if s.check() == sat:
        print("Another solution found")
    else:
        print("It was the only solution.")

else:
    print("No solution found.")
