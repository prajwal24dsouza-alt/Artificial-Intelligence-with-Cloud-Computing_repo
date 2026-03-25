# FizzBuzz Program: Print numbers 1–50 with Fizz/Buzz logic
# and count occurrences using loops and functions.


def fizzbuzz(n):
    """
    Determine the FizzBuzz value for a given number.
    - Returns 'FizzBuzz' if divisible by both 3 and 5
    - Returns 'Fizz'     if divisible by 3 only
    - Returns 'Buzz'     if divisible by 5 only
    - Returns the number itself otherwise
    """
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def print_fizzbuzz(start, end):
    """
    Print FizzBuzz results for numbers in the range [start, end]
    and return a list of results.
    """
    results = []
    for i in range(start, end + 1):
        result = fizzbuzz(i)
        results.append(result)
        print(f"{i:>3} → {result}")
    return results


def count_occurrences(results):
    """
    Count how many times 'Fizz', 'Buzz', 'FizzBuzz',
    and plain numbers appear in the results list.
    """
    fizz_count = 0
    buzz_count = 0
    fizzbuzz_count = 0
    number_count = 0

    for item in results:
        if item == "FizzBuzz":
            fizzbuzz_count += 1
        elif item == "Fizz":
            fizz_count += 1
        elif item == "Buzz":
            buzz_count += 1
        else:
            number_count += 1

    return fizz_count, buzz_count, fizzbuzz_count, number_count


def display_summary(fizz, buzz, fizzbuzz_c, numbers):
    """Display a formatted summary of occurrence counts."""
    total = fizz + buzz + fizzbuzz_c + numbers
    print("\n" + "=" * 35)
    print("       OCCURRENCE SUMMARY")
    print("=" * 35)
    print(f"  Fizz      : {fizz}")
    print(f"  Buzz      : {buzz}")
    print(f"  FizzBuzz  : {fizzbuzz_c}")
    print(f"  Numbers   : {numbers}")
    print("-" * 35)
    print(f"  Total     : {total}")
    print("=" * 35)


# ── Main execution ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 35)
    print("   FIZZBUZZ: Numbers 1 to 50")
    print("=" * 35)

    results = print_fizzbuzz(1, 50)

    fizz, buzz, fb, nums = count_occurrences(results)
    display_summary(fizz, buzz, fb, nums)
