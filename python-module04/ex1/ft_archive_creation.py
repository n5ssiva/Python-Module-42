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
    content: str = ""

    try:
        ancient_fragment: typing.IO[str] = open(sys.argv[1], 'r')
        content = ancient_fragment.read()
        print("---\n")
        print(content)
        print("\n---")

        ancient_fragment.close()
        print(f"File '{sys.argv[1]}' closed.\n")

    except OSError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")

    lines = content.split("\n")
    new_lines = [line + "#" for line in lines]
    transformed_content: str = ""

    print("---\n")
    for line in new_lines:
        print(line)
        transformed_content += line + "\n"
    print("\n---")

    save: str = input("Enter a new file name (or empty): ")

    if not save:
        print("Not saving data.")
    else:
        print(f"Saving data to '{save}'.")
        try:
            new_archive: typing.IO[str] = open(save, 'w')
            new_archive.write(transformed_content)
            new_archive.close()
            print(f"Data saved in file '{save}'.")
        except OSError as e:
            print(f"Error saving file '{save}': {e}")


if __name__ == "__main__":
    main()
