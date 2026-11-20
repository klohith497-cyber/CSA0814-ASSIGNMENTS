# PYTHON ASSIGNMENT - 2

import time
import sys
from functools import lru_cache

def task1():
    print("\n========== Q1: DECISIONS WITH MANY BOUNDARIES ==========")
    households = [
        ("H1", 100, False, 30),
        ("H2", 101, True, 40),
        ("H3", 101, False, 45),
        ("H4", 200, True, 65),
        ("H5", 200, False, 82),
        ("H6", 201, False, 81),
        ("H7", 201, True, 50),
        ("H8", 80, True, 85)
    ]

    def separate_ifs(units, has_ration_card, oldest_age):
        decisions = []
        if units <= 100:
            decisions.append("Full subsidy")
        if 101 <= units <= 200 and has_ration_card:
            decisions.append("Partial subsidy")
        if units > 200 and oldest_age > 80:
            decisions.append("Elderly exception subsidy")
        if not decisions:
            decisions.append("No subsidy")
        return decisions

    def if_elif_else(units, has_ration_card, oldest_age):
        if units <= 100:
            return "Full subsidy"
        elif 101 <= units <= 200 and has_ration_card:
            return "Partial subsidy"
        elif units > 200 and oldest_age > 80:
            return "Elderly exception subsidy"
        else:
            return "No subsidy"

    print("Household | Units | Ration card | Age | Separate-if result | If-elif-else result")
    for name, units, ration, age in households:
        separate = separate_ifs(units, ration, age)
        chained = if_elif_else(units, ration, age)
        print(f"{name:9} | {units:5} | {str(ration):11} | {age:3} | "
              f"{', '.join(separate):28} | {chained}")


def task2():
    print("\n========== Q2: LOOPS THAT COUNT ATTEMPTS ==========")
    correct_otp = "4821"
    max_attempts = 3

    def verify_with_while():
        wrong_attempts = 0
        while wrong_attempts < max_attempts:
            entered = input("Enter OTP (blank to skip): ").strip()
            if entered == "":
                print("Blank entry ignored.")
                continue
            if entered == correct_otp:
                print("OTP verified.")
                break
            wrong_attempts += 1
            print(f"Incorrect OTP. Attempts used: {wrong_attempts}")
        else:
            print("Account locked for 30 minutes.")

    def verify_with_for():
        wrong_attempts = 0
        for _ in range(max_attempts):
            entered = input("Enter OTP (blank to skip): ").strip()
            if entered == "":
                print("Blank entry ignored.")
                continue
            if entered == correct_otp:
                print("OTP verified.")
                break
            wrong_attempts += 1
            print(f"Incorrect OTP. Attempts used: {wrong_attempts}")
        else:
            print("Account locked for 30 minutes.")

    choice = input("Choose 1 for while or 2 for for: ").strip()
    if choice == "1":
        verify_with_while()
    elif choice == "2":
        verify_with_for()
    else:
        pass


def task3():
    print("\n========== Q3: VEHICLE REGISTRATION NUMBER VALIDATOR ==========")
    def normalise(text):
        return text.strip().replace(" ", "").replace("-", "").upper()

    def is_valid(reg):
        if len(reg) not in (9, 10):
            return False
        series_length = len(reg) - 8
        state = reg[:2]
        district = reg[2:4]
        series = reg[4:4 + series_length]
        number = reg[4 + series_length:]
        return (
            len(state) == 2 and state.isalpha()
            and len(district) == 2 and district.isdigit()
            and series_length in (1, 2) and series.isalpha()
            and len(number) == 4 and number.isdigit()
        )

    def format_registration(reg):
        if not is_valid(reg):
            return "INVALID"
        series_length = len(reg) - 8
        return (f"{reg[:2]} {reg[2:4]} "
                f"{reg[4:4 + series_length]} {reg[4 + series_length:]}")

    examples = [
        "tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234",
        "TN 22 1234 AB", "MH-12-XY-5678", "DL 05 C 4321"
    ]
    print("Predictions: first two valid; next two invalid; last two valid.")
    for raw in examples:
        reg = normalise(raw)
        status = "valid" if is_valid(reg) else "INVALID"
        print(f"{raw:15} -> {reg:11} {status:7} Receipt: {format_registration(reg)}")

    s = "TN09AB1234"
    short = "TN09A1234"
    print("10-char slices:", s[-4:], s[4:-4])
    print("9-char slices: ", short[-4:], short[4:-4])


def task4():
    print("\n========== Q4: BUILDING LONG TEXT: + OR join() ==========")
    def make_items(n):
        return [f"Item{i}:Rs{i % 50}" for i in range(n)]

    def build_plus(parts):
        text_value = ""
        for part in parts:
            text_value += part + ";"
        return text_value

    def build_join(parts):
        return ";".join(parts) + ";"

    def build_fstring(parts):
        text_value = ""
        for part in parts:
            text_value += f"{part};"
        return text_value

    def measure(function, parts, repeats=3):
        times = []
        for _ in range(repeats):
            start = time.perf_counter()
            function(parts)
            times.append(time.perf_counter() - start)
        return sum(times) / len(times)

    for size in (1000, 10000, 200000):
        items = make_items(size)
        plus_time = measure(build_plus, items)
        join_time = measure(build_join, items)
        fstring_time = measure(build_fstring, items)
        result_text = build_join(items)
        same = result_text == build_plus(items) == build_fstring(items)
        print(f"\nLines: {size:,}")
        print(f"Same text: {same} | length: {len(result_text)}")
        print(f"+= average:      {plus_time:.6f} s")
        print(f"join average:    {join_time:.6f} s")
        print(f"f-string average: {fstring_time:.6f} s")


def task5():
    print("\n========== Q5: FUNCTIONS, PARAMETERS AND SCOPE ==========")
    def add_item_buggy(item, order=[]):
        order.append(item)
        return order

    print("Buggy call 1:", add_item_buggy("Tea"))
    print("Buggy call 2:", add_item_buggy("Vada"))
    print("Shared default:", add_item_buggy.__defaults__)

    def add_item(item, order=None):
        if order is None:
            order = []
        order.append(item)
        return order

    customer_1 = add_item("Tea")
    customer_2 = add_item("Vada")
    customer_3 = add_item("Coffee")
    print("Independent orders:", customer_1, customer_2, customer_3)

    def bill(subtotal, tax_rate=0.05):
        tax = subtotal * tax_rate
        total = subtotal + tax
        return total, tax

    total, gst = bill(1000)
    print(f"Total: {total:.2f}, GST: {gst:.2f}")

    shop_name = "Campus Cafe"
    def show_shop():
        shop_name = "Temporary Cafe"
        print("Inside function:", shop_name)

    show_shop()
    print("Outside function:", shop_name)

    def make_counter():
        count = 0
        def increment():
            nonlocal count
            count += 1
            return count
        return increment

    counter = make_counter()
    print("Counter:", counter(), counter())

    balance = 100
    def add_to_balance(amount):
        global balance
        balance += amount

    add_to_balance(25)
    print("Updated global balance:", balance)


def task6():
    print("\n========== Q6: RECURSION AND ITS LIMITS ==========")
    calls = 0
    def ways_naive(n):
        global calls
        calls += 1
        if n <= 1:
            return 1
        return ways_naive(n - 1) + ways_naive(n - 2)

    memo_calls = 0
    @lru_cache(maxsize=None)
    def ways_memo(n):
        global memo_calls
        memo_calls += 1
        if n <= 1:
            return 1
        return ways_memo(n - 1) + ways_memo(n - 2)

    def ways_loop(n):
        if n <= 1:
            return 1
        previous, current = 1, 1
        for _ in range(2, n + 1):
            previous, current = current, previous + current
        return current

    for n in range(1, 7):
        print(f"n={n}: {ways_loop(n)}")

    calls = 0
    print("naive:", ways_naive(25), "calls =", calls)
    memo_calls = 0
    ways_memo.cache_clear()
    print("memo:", ways_memo(25), "calls =", memo_calls)
    print("recursion limit:", sys.getrecursionlimit())

    try:
        print("memo n=1000:", ways_memo(1000))
    except RecursionError as error:
        print("memo n=1000:", type(error).__name__)

    print("loop n=1000:", ways_loop(1000))


def task7():
    print("\n========== Q7: DIAGNOSE, REDESIGN AND VALIDATE ==========")
    def ways_naive(n):
        if n <= 1:
            return 1
        return ways_naive(n - 1) + ways_naive(n - 2)

    @lru_cache(maxsize=None)
    def ways_memo(n):
        if n <= 1:
            return 1
        return ways_memo(n - 1) + ways_memo(n - 2)

    def ways_iterative(n):
        if n <= 1:
            return 1
        previous, current = 1, 1
        for _ in range(2, n + 1):
            previous, current = current, previous + current
        return current

    def timed_call(function, n):
        start = time.perf_counter()
        result = function(n)
        elapsed = time.perf_counter() - start
        return result, elapsed

    print("Correctness comparison:")
    for n in range(1, 11):
        assert ways_memo(n) == ways_iterative(n)
        print(f"n={n}: {ways_iterative(n)} ways")

    for n in (20, 25, 30):
        result, elapsed = timed_call(ways_naive, n)
        print(f"naive n={n}: {elapsed:.6f} s; digits={len(str(result))}")

    for n in (20, 25, 30, 1000):
        ways_memo.cache_clear()
        result, elapsed = timed_call(ways_memo, n)
        print(f"memo n={n}: {elapsed:.6f} s; digits={len(str(result))}")

    for n in (20, 25, 30, 1000):
        result, elapsed = timed_call(ways_iterative, n)
        print(f"iterative n={n}: {elapsed:.6f} s; digits={len(str(result))}")


if __name__ == "__main__":
    print("PYTHON ASSIGNMENT - 2")
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    print("\n========== ALL 7 TASKS COMPLETED ==========")
