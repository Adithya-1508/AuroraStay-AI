import subprocess
import sys


def run_command(args: list[str]) -> bool:
    """Executes system command and returns whether it completed successfully."""
    try:
        result = subprocess.run(args, capture_output=True, text=True)  # noqa: S603
        if result.returncode != 0:
            print(f"Error executing {' '.join(args)}:")
            print(result.stdout)
            print(result.stderr)
            return False
        return True
    except FileNotFoundError:
        print(f"Executable not found: {args[0]}")
        return False


def main() -> None:
    print("Executing all code quality checks...")
    ruff_check = run_command([sys.executable, "-m", "ruff", "check", "."])
    ruff_format = run_command([sys.executable, "-m", "ruff", "format", "--check", "."])
    mypy_check = run_command([sys.executable, "-m", "mypy", "shared", "tests"])

    if not (ruff_check and ruff_format and mypy_check):
        print("\nQuality checks FAILED. Please fix issues before committing.")
        sys.exit(1)
    else:
        print("\nAll quality checks PASSED successfully!")


if __name__ == "__main__":
    main()
