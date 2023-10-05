def safe_get_int(side: str) -> int:
    s = input(f"Сторона {side}: ")
    while True:
        try:
            return int(s)
        except ValueError:
            print("--- ERROR: нужно ввести число ---")
        s = input(f"Сторона {side}: ")


while True:
    a = safe_get_int("a")
    b = safe_get_int("b")

    if a < 0 or b < 0:
        print("--- ERROR: стороны прямоугольника должны быть положительным числом ---")
        continue

    print(f"P({a}, {b}) = {a * 2 + b * 2}")
    print(f"S({a}, {b}) = {a * b}")
    print(f"{'-'*25}\n")

    if input("Продолжить (Y/n): ").lower() == "n":
        break
