# ============================================================
#  Student Data Manager
#  -  Stores data for 5 students using dictionaries
#  -  Prints the topper (highest marks)
#  -  Calculates and prints the class average
#  -  Assigns letter grades to each student
# ============================================================


def assign_grade(marks):
    """Return a letter grade based on the student's marks."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def find_topper(students):
    """Return the dictionary entry of the student with the highest marks."""
    topper = max(students, key=lambda s: s["marks"])
    return topper


def class_average(students):
    """Calculate and return the average marks of all students."""
    total = sum(s["marks"] for s in students)
    return total / len(students)


def display_student_table(students):
    """Print a formatted table of all students with their grades."""
    header = f"{'Roll No':<10}{'Name':<20}{'Marks':<10}{'Grade':<10}"
    print(header)
    print("-" * len(header))
    for s in students:
        print(f"{s['roll_no']:<10}{s['name']:<20}{s['marks']:<10}{s['grade']:<10}")


def main():
    # ── Store data for 5 students using a list of dictionaries ──
    students = [
        {"roll_no": 101, "name": "Pavan ",   "marks": 92},
        {"roll_no": 102, "name": "Bob ",        "marks": 78},
        {"roll_no": 103, "name": "Charlie ",    "marks": 85},
        {"roll_no": 104, "name": "Diana Prince",     "marks": 64},
        {"roll_no": 105, "name": "Ethan Hunt",       "marks": 95},
    ]

    # ── Assign grades to each student ──
    for student in students:
        student["grade"] = assign_grade(student["marks"])

    # ── Display all students ──
    print("=" * 50)
    print("        STUDENT REPORT CARD")
    print("=" * 50)
    display_student_table(students)

    # ── Find and display the topper ──
    topper = find_topper(students)
    print("\n" + "=" * 50)
    print(f"🏆 Topper : {topper['name']} "
          f"(Roll No: {topper['roll_no']}) "
          f"with {topper['marks']} marks — Grade {topper['grade']}")

    # ── Calculate and display class average ──
    avg = class_average(students)
    print(f"📊 Class Average : {avg:.2f} marks")
    print("=" * 50)


if __name__ == "__main__":
    main()
