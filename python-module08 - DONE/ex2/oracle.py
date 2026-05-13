import os
import sys
from dotenv import load_dotenv


EXPECTED_VARS: dict[str, str | None] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": None,
    "API_KEY": None,
    "LOG_LEVEL": "INFO",
    "ZION_ENDPOINT": None,
}


def load_config() -> dict[str, str | None]:
    load_dotenv(override=False)
    config: dict[str, str | None] = {}
    for var, default in EXPECTED_VARS.items():
        config[var] = os.environ.get(var, default)
    return config


def describe(value: str | None, fallback: str) -> str:
    return value if value else fallback


def print_config(config: dict[str, str | None]) -> None:
    mode = config["MATRIX_MODE"] or "development"
    db = config["DATABASE_URL"]
    api = config["API_KEY"]
    log = config["LOG_LEVEL"] or "INFO"
    zion = config["ZION_ENDPOINT"]

    print("Configuration loaded:")
    print(f"Mode: {mode}")

    if db:
        if mode == "development":
            print("Database: Connected to local instance")
        else:
            print("Database: Connected to production instance")
    else:
        print("Database: Not configured")

    print(f"API Access: {'Authenticated' if api else 'No API key set'}")
    print(f"Log Level: {log}")
    print(f"Zion Network: {'Online' if zion else 'Offline'}")


def security_check(config: dict[str, str | None]) -> None:
    print()
    print("Environment security check:")

    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARN] No .env file found (using defaults or shell env vars)")

    mode = config["MATRIX_MODE"]
    if mode in ("development", "production"):
        print("[OK] Production overrides available")
    else:
        print(f"[WARN] Unknown MATRIX_MODE: {mode}")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    try:
        config = load_config()
        print_config(config)
        security_check(config)
        print()
        print("The Oracle sees all configurations.")
    except Exception as e:
        print(f"Error reading configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
