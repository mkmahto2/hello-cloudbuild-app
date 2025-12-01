"""Lightweight test runner to run the pytest-style tests without requiring pytest.

This script imports the `tests.test_client` module, discovers functions that
start with `test_` and runs them. It treats AssertionError as test failures.

This allows CI or local verification of the ADK scaffold even when pytest is
not installed.
"""
import importlib
import inspect
import sys
from pathlib import Path


def run_tests_module(module_name: str) -> int:
    module = importlib.import_module(module_name)
    functions = [
        (name, fn)
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if name.startswith("test_")
    ]
    fail_count = 0
    for name, fn in functions:
        try:
            fn()
            print(f"PASS: {module_name}.{name}")
        except AssertionError as e:
            fail_count += 1
            print(f"FAIL: {module_name}.{name} -> {e}")
        except Exception as e:
            fail_count += 1
            print(f"ERROR: {module_name}.{name} -> {e}")
    return fail_count


def discover_and_run_tests(tests_dir: str = "tests") -> int:
    """Discover test modules under the `tests` package and run them.

    Loads any file named `test_*.py` in the `tests` directory.
    """
    tests_path = Path(tests_dir)
    if not tests_path.exists():
        print("No tests directory found")
        return 0

    total_failures = 0
    for p in sorted(tests_path.glob("test_*.py")):
        module_name = f"{tests_dir}.{p.stem}"
        total_failures += run_tests_module(module_name)
    return total_failures


def main():
    total_failures = discover_and_run_tests()
    if total_failures:
        print(f"{total_failures} test(s) failed")
        sys.exit(1)
    print("All tests passed")


if __name__ == "__main__":
    main()
