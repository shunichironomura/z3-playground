from z3 import Int, Solver, sat


def solve_two_numbers() -> None:
    """Solve the Two Numbers Riddle.

    Basic version: Find two numbers where sum = 10 and product = 21
    """
    s = Solver()  # ソルバーを作成
    x = Int("x")  # 整数変数xを作成
    y = Int("y")  # 整数変数yを作成
    s.add(x + y == 10)  # 足して10になる条件を追加
    s.add(x * y == 21)  # 掛けて21になる条件を追加
    s.add(x > 0, y > 0)  # 正の整数である条件を追加
    if s.check() == sat:  # 条件を満たす解が存在するか
        m = s.model()  # モデルを取得
        print(f"x = {m[x]}, y = {m[y]}")  # 解を表示
    else:
        print("No solution found")  # 解が存在しない場合


if __name__ == "__main__":
    solve_two_numbers()
