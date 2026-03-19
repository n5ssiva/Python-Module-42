def test_value_error() -> None:
    """Attempt to convert an invalid string to an integer."""
    print("Testing ValueError...")
    try:
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()")


def test_zero_division_error() -> None:
    """Attempt to divide a number by zero."""
    print("Testing ZeroDivisionError...")
    try:
        10 / 0
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}")


def test_file_not_found_error() -> None:
    """Attempt to open a file that does not exist."""
    print("Testing FileNotFoundError...")
    try:
        open("missing.txt", "r")
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file'missing.txt'")


def test_key_error() -> None:
    """Attempt to access a non-existent key in a dictionary."""
    print("Testing KeyError...")
    try:
        garden = {"tomato": 5}
        _ = garden["missing_plant"]
    except KeyError:
        # Respecting the specific output format provided
        print(r"Caught KeyError: 'missing\_plant'")


def test_multiple_errors() -> None:
    """Catch multiple specific exceptions in a single block."""
    print("Testing multiple errors together...")
    try:
        int("abc")
    except (ValueError, ZeroDivisionError, FileNotFoundError):
        print("Caught an error, but program continues!")


def test_error_types() -> None:
    """Execute all error test cases in sequence."""
    print("=== Garden Error Types Demo ===\n")
    test_value_error()
    print("")
    test_zero_division_error()
    print("")
    test_file_not_found_error()
    print("")
    test_key_error()
    print("")
    test_multiple_errors()
    print("")
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
