"""
Python-CSA0814: Combined executable solution for Tasks 1-6.
Run: python all_tasks.py
The script creates its own sample input files in ./python_tasks_demo/
and writes all generated reports under that folder.
"""

from pathlib import Path
import csv
import shutil

BASE = Path("python_tasks_demo")
INPUT = BASE / "input"
OUTPUT = BASE / "output"


def prepare_demo_files():
    """Create sample files so the program runs without manual setup."""
    if BASE.exists():
        shutil.rmtree(BASE)
    INPUT.mkdir(parents=True)
    OUTPUT.mkdir(parents=True)

    # Task 1: mess bill data
    (INPUT / "mess_oct.txt").write_text(
        "101,Ravi,1250.50\n"
        "102,Ram,1500.00\n"
        "103,John,1200.50\n"
        "104,Sam,Invalid\n",
        encoding="utf-8",
    )

    # Task 2 and Task 3: daily attendance data
    attendance = INPUT / "attendance"
    attendance.mkdir()
    (attendance / "attendance1.txt").write_text(
        "192311001,2026-10-08,P\n"
        "192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,L\n",
        encoding="utf-8",
    )
    (attendance / "attendance2.txt").write_text(
        "192311001,2026-10-09,P\n"
        "192311002,2026-10-09,P\n"
        "192311003,2026-10-09,A\n",
        encoding="utf-8",
    )

    # Task 4: daily returned-book files
    (INPUT / "day1.txt").write_text("Python\nJava\n", encoding="utf-8")
    (INPUT / "day2.txt").write_text("C\nC++\n", encoding="utf-8")
    (INPUT / "day3.txt").write_text("DBMS\nOperating Systems\n", encoding="utf-8")

    # Task 6: five department files
    (INPUT / "CSE.txt").write_text(
        "192311001,Ravi,CSE,ravi@gmail.com,Dance;Music\n"
        "192311002,Ram,CSE,ram@gmail.com,Singing\n"
        "192311003,John,CSE,john@gmail.com,Drama\n",
        encoding="utf-8",
    )
    (INPUT / "ECE.txt").write_text(
        "192311001,Sam,ECE,sam@gmail.com,Dance\n"
        "192311004,Arun,ECE,invalidemail,Singing\n"
        "192311005,Kiran,ECE,kiran@gmail.com,Music\n",
        encoding="utf-8",
    )
    for dept in ("EEE", "IT", "MECH"):
        (INPUT / f"{dept}.txt").write_text("", encoding="utf-8")


# ---------------------------------------------------------------------
# TASK 1 - File-processing design review: mess bill report
# ---------------------------------------------------------------------
def task1_mess_bill():
    print("\n" + "=" * 68)
    print("TASK 1 - MESS BILL FILE PROCESSING")
    print("=" * 68)

    filename = INPUT / "mess_oct.txt"
    total = 0.0
    report = []
    rejected = []

    try:
        with filename.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, 1):
                if not line.strip():
                    continue
                try:
                    parts = [part.strip() for part in line.strip().split(",")]
                    if len(parts) != 3:
                        raise ValueError("Invalid fields")
                    reg, name, amount_text = parts
                    amount = float(amount_text)
                    total += amount
                    report.append((reg, name, amount))
                except (ValueError, IndexError) as exc:
                    rejected.append((line_no, line.strip(), str(exc)))
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    print("Mess Bill Report")
    for reg, name, amount in report:
        print(f"{name} {amount}")
    print(f"Total Amount: {total:.1f}")
    print("Rejected Lines:", rejected)


# ---------------------------------------------------------------------
# TASK 2 - Attendance file processor and monthly reports
# ---------------------------------------------------------------------
def task2_attendance_reports():
    print("\n" + "=" * 68)
    print("TASK 2 - ATTENDANCE REPORT DESIGN")
    print("=" * 68)

    folder = INPUT / "attendance"
    students = {}
    errors = []

    for path in sorted(folder.glob("*.txt")):
        try:
            with path.open("r", encoding="utf-8") as file:
                for line_no, line in enumerate(file, 1):
                    if not line.strip():
                        continue
                    try:
                        parts = [p.strip() for p in line.strip().split(",")]
                        if len(parts) != 3:
                            raise ValueError("Invalid fields")
                        reg, date, status = parts
                        if status not in ("P", "A"):
                            raise ValueError("Invalid status")
                        if not reg or not date:
                            raise ValueError("Missing register number or date")
                        if reg not in students:
                            students[reg] = [0, 0]  # present, absent
                        if status == "P":
                            students[reg][0] += 1
                        else:
                            students[reg][1] += 1
                    except ValueError as exc:
                        errors.append(f"{path.name},{line_no},{exc}")
        except OSError as exc:
            errors.append(f"{path.name},0,{exc}")

    report_lines = []
    below_lines = []
    for reg, (present, absent) in sorted(students.items()):
        total_days = present + absent
        percentage = (present / total_days) * 100 if total_days else 0.0
        report_lines.append(f"{reg} = {percentage:.2f}%")
        if percentage < 75:
            below_lines.append(reg)

    (OUTPUT / "attendance_report.txt").write_text(
        "\n".join(report_lines) + ("\n" if report_lines else ""), encoding="utf-8"
    )
    (OUTPUT / "below_75.txt").write_text(
        "\n".join(below_lines) + ("\n" if below_lines else ""), encoding="utf-8"
    )
    (OUTPUT / "damaged_lines.txt").write_text(
        "\n".join(errors) + ("\n" if errors else ""), encoding="utf-8"
    )

    print("Reports generated successfully")
    print("\nattendance_report.txt")
    print((OUTPUT / "attendance_report.txt").read_text(encoding="utf-8"), end="")
    print("\nbelow_75.txt")
    print((OUTPUT / "below_75.txt").read_text(encoding="utf-8"), end="")
    print("\ndamaged_lines.txt")
    print((OUTPUT / "damaged_lines.txt").read_text(encoding="utf-8"), end="")


# ---------------------------------------------------------------------
# TASK 3 - Custom exception and explicit exception handling
# ---------------------------------------------------------------------
class InvalidRecord(Exception):
    """Raised when an attendance record is malformed or has invalid status."""


def parse_attendance_line(line):
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{parts[2]}'")
    return tuple(parts)


def summarise_attendance(path):
    present = 0
    absent = 0
    errors = []

    try:
        with path.open("r", encoding="utf-8") as file:
            for number, line in enumerate(file, 1):
                if not line.strip():
                    continue
                try:
                    reg, date, status = parse_attendance_line(line)
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
                except InvalidRecord as exc:
                    errors.append((number, str(exc)))
    except FileNotFoundError as exc:
        print(f"File not found: {path.name}")
        raise RuntimeError(f"Cannot process attendance file: {path.name}") from exc
    except PermissionError as exc:
        print(f"Permission denied: {path}")
        raise
    finally:
        print("File processing completed")

    return present, absent, errors


def task3_error_handling():
    print("\n" + "=" * 68)
    print("TASK 3 - CUSTOM EXCEPTION HANDLING")
    print("=" * 68)

    path = INPUT / "attendance" / "attendance1.txt"
    result = summarise_attendance(path)
    print(result)


# ---------------------------------------------------------------------
# TASK 4 - Append-only returned-book log and error log
# ---------------------------------------------------------------------
def task4_library_returns():
    print("\n" + "=" * 68)
    print("TASK 4 - FILE AND EXCEPTION FORENSICS")
    print("=" * 68)

    log_path = OUTPUT / "returns.log"
    error_path = OUTPUT / "error.log"
    # Start a clean demonstration each time this combined script is run.
    log_path.write_text("", encoding="utf-8")
    error_path.write_text("", encoding="utf-8")

    def save_returns(books):
        try:
            with log_path.open("a", encoding="utf-8") as log:
                for book in books:
                    log.write(book.rstrip("\n") + "\n")
        except OSError as exc:
            with error_path.open("a", encoding="utf-8") as error:
                error.write(f"Could not write returns: {exc}\n")

    def process(day_file):
        try:
            with day_file.open("r", encoding="utf-8") as file:
                books = [line.strip() for line in file if line.strip()]
            save_returns(books)
        except FileNotFoundError:
            with error_path.open("a", encoding="utf-8") as error:
                error.write(f"{day_file.name} is missing\n")
        except OSError as exc:
            with error_path.open("a", encoding="utf-8") as error:
                error.write(f"{day_file.name}: {exc}\n")

    for day in ("day1.txt", "day2.txt", "day3.txt"):
        process(INPUT / day)

    print("Book records saved successfully")
    print("\nreturns.log")
    print(log_path.read_text(encoding="utf-8"), end="")


# ---------------------------------------------------------------------
# TASK 5 - Organising the same utility as script/modules/package
# ---------------------------------------------------------------------
def task5_organisation():
    print("\n" + "=" * 68)
    print("TASK 5 - FOUR PROGRAM ORGANISATIONS")
    print("=" * 68)

    # In this single-file runnable demonstration, these functions represent
    # the responsibilities that can be separated into modules or a package.
    def read_file():
        print("Reading attendance files")

    def percentage():
        print("Calculating attendance")

    def consecutive_absent(statuses):
        for index in range(len(statuses) - 2):
            if statuses[index:index + 3] == ["A", "A", "A"]:
                return True
        return False

    def generate_report():
        print("Generating attendance report")

    read_file()
    percentage()
    print("Checking three-day absence")
    print("Example consecutive absence:", consecutive_absent(["P", "A", "A", "A", "P"]))
    generate_report()

    print("\nOrganisation options described in the assignment:")
    print("1. One script: all functions in attendance.py")
    print("2. One module + main.py: attendance.py imported by main.py")
    print("3. Three modules: reader.py, stats.py, report.py")
    print("4. Package: attendance/__init__.py, reader.py, stats.py, report.py")


# ---------------------------------------------------------------------
# TASK 6 - College fest registration processing
# ---------------------------------------------------------------------
DEPARTMENTS = ("CSE", "ECE", "EEE", "IT", "MECH")
EVENTS = ("Dance", "Music", "Singing", "Drama")


def valid_email(email):
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def task6_college_fest():
    print("\n" + "=" * 68)
    print("TASK 6 - COLLEGE FEST REGISTRATION")
    print("=" * 68)

    seen = set()
    master = []
    event_participants = {event: [] for event in EVENTS}
    errors = []

    for department in DEPARTMENTS:
        path = INPUT / f"{department}.txt"
        try:
            with path.open("r", encoding="utf-8") as file:
                for line_no, line in enumerate(file, 1):
                    if not line.strip():
                        continue
                    try:
                        parts = [p.strip() for p in line.rstrip("\n").split(",")]
                        if len(parts) != 5:
                            raise ValueError("Invalid fields: expected 5")
                        reg, name, dept, email, chosen = parts
                        if not all((reg, name, dept, email, chosen)):
                            raise ValueError("Missing field")
                        if not valid_email(email):
                            raise ValueError("Invalid email")
                        if reg in seen:
                            raise ValueError("Duplicate registration")
                        selected_events = [event.strip() for event in chosen.split(";") if event.strip()]
                        if not selected_events:
                            raise ValueError("No events selected")
                        unknown = [event for event in selected_events if event not in EVENTS]
                        if unknown:
                            raise ValueError("Unknown event: " + ", ".join(unknown))

                        seen.add(reg)
                        record = (reg, name, dept, email, ";".join(selected_events))
                        master.append(record)
                        for event in selected_events:
                            event_participants[event].append((reg, name, dept))
                    except ValueError as exc:
                        errors.append(f"input/{path.name}, Line {line_no}: {exc}")
        except FileNotFoundError:
            errors.append(f"input/{path.name}: Missing department file")
        except OSError as exc:
            errors.append(f"input/{path.name}: {exc}")

    master_path = OUTPUT / "master.csv"
    with master_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["RegisterNumber", "Name", "Department", "Email", "Events"])
        writer.writerows(master)

    for event, participants in event_participants.items():
        (OUTPUT / f"{event}.txt").write_text(
            "".join(f"{reg},{name},{dept}\n" for reg, name, dept in participants),
            encoding="utf-8",
        )

    summary = [
        "College Fest Registration Summary",
        f"Valid Registrations: {len(master)}",
        f"Rejected Records: {len(errors)}",
    ]
    (OUTPUT / "summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    (OUTPUT / "error.log").write_text(
        "\n".join(errors) + ("\n" if errors else ""), encoding="utf-8"
    )

    print("Fest registration processing completed")
    print(f"Valid Registrations: {len(master)}")
    print(f"Rejected Records: {len(errors)}")
    print("\nmaster.csv")
    print(master_path.read_text(encoding="utf-8"), end="")
    print("\nerror.log")
    print((OUTPUT / "error.log").read_text(encoding="utf-8"), end="")


def main():
    prepare_demo_files()
    print("PYTHON-CSA0814 - COMBINED TASKS 1 TO 6")
    print(f"Demo inputs: {INPUT.resolve()}")
    print(f"Generated outputs: {OUTPUT.resolve()}")

    task1_mess_bill()
    task2_attendance_reports()
    task3_error_handling()
    task4_library_returns()
    task5_organisation()
    task6_college_fest()

    print("\n" + "=" * 68)
    print("ALL SIX TASKS EXECUTED SUCCESSFULLY")
    print(f"Check generated files in: {OUTPUT.resolve()}")
    print("=" * 68)


if __name__ == "__main__":
    main()
