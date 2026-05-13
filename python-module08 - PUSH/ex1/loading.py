import sys
import importlib


REQUIRED = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def check_dependencies() -> dict[str, str | None]:
    """Return {package_name: version_string or None if missing}."""
    versions: dict[str, str | None] = {}
    for pkg in REQUIRED:
        try:
            module = importlib.import_module(pkg)
            versions[pkg] = getattr(module, "__version__", "unknown")
        except ImportError:
            versions[pkg] = None
    return versions


def print_dependency_status(versions: dict[str, str | None]) -> bool:
    print("Checking dependencies:")
    all_ok = True
    for pkg, version in versions.items():
        description = REQUIRED[pkg]
        if version is None:
            print(f"[MISSING] {pkg} - {description} not ready")
            all_ok = False
        else:
            print(f"[OK] {pkg} ({version}) - {description} ready")
    return all_ok


def print_install_instructions() -> None:
    print()
    print("Missing dependencies. Install with:")
    print()
    print("With pip:")
    print("  pip install -r requirements.txt")
    print()
    print("With Poetry:")
    print("  poetry install")
    print()
    print("Note: pip uses requirements.txt (flat list of versions).")
    print("Poetry uses pyproject.toml (resolves dependency tree,")
    print("locks exact versions in poetry.lock for reproducibility).")


def run_analysis() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")  # backend non-interactif
    import matplotlib.pyplot as plt

    print()
    print("Analyzing Matrix data...")

    rng = np.random.default_rng(seed=42)
    n_points = 1000
    data = rng.normal(loc=0.0, scale=1.0, size=n_points)

    print(f"Processing {n_points} data points...")

    # Passage par pandas
    df = pd.DataFrame({"value": data})
    df["rolling_mean"] = df["value"].rolling(window=50).mean()

    print("Generating visualization...")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["value"], alpha=0.4, label="Raw signal")
    ax.plot(df.index, df["rolling_mean"], color="red", label="Rolling mean")
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend()
    fig.tight_layout()
    fig.savefig("matrix_analysis.png")
    plt.close(fig)

    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()

    versions = check_dependencies()
    all_ok = print_dependency_status(versions)

    if not all_ok:
        print_install_instructions()
        sys.exit(1)

    try:
        run_analysis()
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
