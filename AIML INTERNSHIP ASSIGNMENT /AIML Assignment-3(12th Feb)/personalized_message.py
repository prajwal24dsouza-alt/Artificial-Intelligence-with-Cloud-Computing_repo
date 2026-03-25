# Personalized Message Generator with Age Categorization

def get_age_category(age):
    """Categorize age into life stages using conditionals."""
    if age < 0:
        return "Invalid"
    elif age <= 12:
        return "Child"
    elif age <= 17:
        return "Teenager"
    elif age <= 25:
        return "Young Adult"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior"


def generate_message(name, age, hobby):
    """Generate a personalized message based on name, age, and hobby."""
    category = get_age_category(age)

    print("\n" + "=" * 50)
    print("PERSONALIZED MESSAGE ")
    print("=" * 50)
    print(f"\n  Hello, {name}! Welcome aboard! ")
    print(f"\n Your Details:")
    print(f"     • Name  : {name}")
    print(f"     • Age   : {age}")
    print(f"     • Hobby : {hobby}")
    print(f"\n   Age Category: {category}")

    # Personalized advice based on age category
    if category == "Invalid":
        print("\n   Please enter a valid age!")
    elif category == "Child":
        print(f"\n That's awesome, {name}! Enjoy your childhood!")
        print(f"     Keep exploring {hobby} — it's a great hobby at your age!")
    elif category == "Teenager":
        print(f"\n  Hey {name}, your teenage years are exciting!")
        print(f"     {hobby} is a wonderful way to express yourself!")
    elif category == "Young Adult":
        print(f"\n   Hi {name}, you're at a fantastic stage of life!")
        print(f"     Pursuing {hobby} can open amazing opportunities!")
    elif category == "Adult":
        print(f"\n   Hello {name}, great to see you staying active!")
        print(f"     Balancing life with {hobby} keeps things fun!")
    elif category == "Senior":
        print(f"\n   Welcome {name}, experience is your superpower!")
        print(f"     Enjoying {hobby} is a wonderful way to stay vibrant!")

    print("\n" + "=" * 50)


def main():
    """Main function to collect user input and display the message."""
    print("\n" + "=" * 50)
    print("   PERSONALIZED MESSAGE GENERATOR")
    print("=" * 50)

    # Collect user inputs
    name = input("\n  Enter your name  : ").strip()

    while True:
        try:
            age = int(input("  Enter your age   : "))
            break
        except ValueError:
            print("   Please enter a valid number for age.")

    hobby = input("  Enter your hobby : ").strip()

    # Generate and display the personalized message
    generate_message(name, age, hobby)


if __name__ == "__main__":
    main()

