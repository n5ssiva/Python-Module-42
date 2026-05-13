import sys
import os


def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def get_venv_name() -> str:
    venv_path = os.environ.get("VIRTUAL_ENV", "")
    if venv_path:
        return os.path.basename(venv_path)
    return os.path.basename(sys.prefix)


def get_site_packages() -> str:
    py_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(sys.prefix, "lib", py_version, "site-packages")


def main() -> None:
    if in_virtual_env():
        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {get_venv_name()}")
        print(f"Environment Path: {sys.prefix}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        print(get_site_packages())
    else:
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate    # On Unix")
        print("matrix_env\\Scripts\\activate    # On Windows")
        print()
        print("Then run this program again.")


if __name__ == "__main__":
    main()
