import glob
import os
import shutil
import sys

# Define common directories and files to clean up
DIRS_TO_CLEAN = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    ".hatch",  # Hatch's own environment cache, if you want to clean it
]

FILES_TO_CLEAN = [
    ".coverage",
    "coverage.xml",
]


# Function to safely remove a directory
def rmtree_safe(path: str) -> None:
    if os.path.exists(path) and os.path.isdir(path):
        print(f"Removing directory: {path}")
        try:
            shutil.rmtree(path)
        except OSError as e:
            print(f"Error removing directory {path}: {e}", file=sys.stderr)
    elif os.path.exists(path):
        print(f"Warning: {path} exists but is not a directory. Skipping rmtree.")


# Function to safely remove a file
def remove_file_safe(path: str) -> None:
    if os.path.exists(path) and os.path.isfile(path):
        print(f"Removing file: {path}")
        try:
            os.remove(path)
        except OSError as e:
            print(f"Error removing file {path}: {e}", file=sys.stderr)
    elif os.path.exists(path):
        print(f"Warning: {path} exists but is not a file. Skipping file removal.")


def main() -> None:
    print("Starting clean process...")

    # Remove specific directories
    for d in DIRS_TO_CLEAN:
        rmtree_safe(d)

    # Remove specific files
    for f in FILES_TO_CLEAN:
        remove_file_safe(f)

    # Clean up *.egg-info directories (often created by build processes)
    for egg_info_dir in glob.glob("*.egg-info"):
        rmtree_safe(egg_info_dir)

    # Clean up .pyc files across the project
    for root, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".pyc"):
                remove_file_safe(os.path.join(root, filename))

    print("Cleanup complete.")


if __name__ == "__main__":
    main()
