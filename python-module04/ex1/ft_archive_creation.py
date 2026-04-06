#!/usr/bin/env python3
"""Exercise 2: Archive Creation - modified and saving a file."""
import sys
import typing


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{sys.argv[1]}'")

    try:
        ancient_fragment: typing.IO[str] = open(sys.argv[1], 'r')
        content = ancient_fragment.read()
        print("---\n")
        print(content)
        print("\n---")

        ancient_fragment.close()
        print(f"File '{sys.argv[1]}' closed.\n")

        lines = content.split("\n")
        new_lines = [line + "#" for line in lines]

        print("---\n")
        for line in new_lines:
            print(line)
        print("\n---")

    except OSError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")


if __name__ == "__main__":
    main()
