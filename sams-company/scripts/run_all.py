import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import update_employee
import writer
import checker
import informations
import content
import reporter


def main():
    steps = [
        ("Writer", writer.run),
        ("Checker", checker.run),
        ("informations", informations.run),
        ("Content", content.run),
        ("reporter", reporter.run),
    ]
    for name, func in steps:
        try:
            func()
        except Exception as e:
            update_employee(name, "error", f"حدث خطأ: {e}")
            traceback.print_exc()
            raise


if __name__ == "__main__":
    main()
