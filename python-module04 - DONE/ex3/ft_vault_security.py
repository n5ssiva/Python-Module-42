#!/usr/bin/env python3
"""Exercise 3 : Vault Security."""


def secure_archive(filename: str, mode: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:

        if mode == "read":
            with open(filename, "r") as f:
                content = f.read()
            return (True, content)

        elif mode == "write":
            with open(filename, "w") as f:
                f.write(content)
            return (True, 'Content successfully written to file')
        return (False, "Invalid mode")

    except OSError as e:

        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existent/file"))

    print("\nUsing 'secure_archive' to read from a inaccessible file:")
    print(secure_archive("/etc/master.passwd"))

    print("\nUsing 'secure_archive' to read from a regular file:")
    print(secure_archive("ancient_fragment.txt"))

    print("\nUsing 'secure_archive' to write previous content to a new file:")
    result = secure_archive("ancient_fragment.txt")
    print(secure_archive("ancient_fragment.txt", "write", result[1]))


if __name__ == "__main__":
    main()
