from z3 import Int, Solver, sat


def tsuru_kame(head_count: int, leg_count: int) -> tuple[int, int]:
    """Solve the Tsuru and Kame problem.

    Args:
        head_count (int): Total number of heads.
        leg_count (int): Total number of legs.

    Returns:
        tuple[int, int]: Number of Tsuru and Kame.

    """
    # Define variables
    tsuru = Int("tsuru")
    kame = Int("kame")

    # Create a solver instance
    solver = Solver()

    # Add constraints
    solver.add(tsuru + kame == head_count)
    solver.add(2 * tsuru + 4 * kame == leg_count)

    # Check satisfiability
    if solver.check() == sat:
        model = solver.model()
        return model[tsuru].as_long(), model[kame].as_long()

    return -1, -1  # No solution found


if __name__ == "__main__":
    # Example usage
    heads = 8
    legs = 26
    tsuru_count, kame_count = tsuru_kame(heads, legs)

    if tsuru_count != -1 and kame_count != -1:
        print(f"Number of Tsuru: {tsuru_count}, Number of Kame: {kame_count}")
    else:
        print("No solution found")
