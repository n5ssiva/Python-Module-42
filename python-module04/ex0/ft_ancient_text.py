#!/usr/bin/env python3
"""Exercise 1: Ancient Text - open/read/close file."""
import sys
import typing


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{sys.argv[1]}'")

    try:
        ancient_text: typing.IO[str] = open(sys.argv[1], 'r')
        print("---\n")
        print(ancient_text.read())
        print("\n---")
        ancient_text.close()
        print(f"File '{sys.argv[1]}' closed.")
    except OSError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")


if __name__ == "__main__":
    main()
