"""Filename Manager

This script contains functionality to modify all filenames within a given directory
path.

This file can also be imported as a module and contains the following functions:

    * modify_filenames
    * modify_filename
"""

import argparse
import pathlib
import sys

FORBIDDEN_CHARACTERS = '<>:"/\\|?*'


def modify_filenames(
    path: pathlib.Path,
    prefix: str = None,
    suffix: str = None,
    oldext: str = None,
    newext: str = None,
) -> None:
    """Modify all filenames contained in given directory path."""

    # Confirm path is a valid directory or file
    if path.is_file():
        modify_filename(path)
    elif not path.is_dir():
        raise NotADirectoryError(
            f"path provided is not a directory: '{path.absolute()}'"
        )

    no_files_found = True

    # Iterate through directory
    for path_item in path.iterdir():
        if path_item.is_file():
            no_files_found = False
            modify_filename(path_item, prefix, suffix, oldext, newext)
        elif path_item.is_dir():
            modify_filenames(path_item, prefix, suffix, oldext, newext)

    if no_files_found:
        print(f"No files found in path: '{path.absolute()}'")


def modify_filename(
    path: pathlib.Path,
    prefix: str = None,
    suffix: str = None,
    oldext: str = None,
    newext: str = None,
) -> None:
    """Modify given filename."""

    # Confirm existing arguments are valid
    for arg in (prefix, suffix, oldext, newext):
        if arg is not None and (
            not arg.isprintable() or any(ch in FORBIDDEN_CHARACTERS for ch in arg)
        ):
            raise ValueError(
                f"argument contains forbidden character: '{arg}'"
                + f"\n(forbidden characters = {FORBIDDEN_CHARACTERS})"
            )

    new_filepath: pathlib.Path = path

    # Verify both extension arguments exist if oldext is passed
    if oldext and not newext:
        raise TypeError(
            f"{modify_filename.__name__}() missing 1 argument: 'newext'"
        )

    # Replace extension if one is provided
    if newext:
        newext = newext.replace(".", "")

        if oldext:
            oldext = oldext.replace(".", "")

            # Replace only filenames with oldext
            if new_filepath.suffix == f".{oldext}":
                new_filepath = pathlib.Path(
                    f"{path.parent}/{new_filepath.stem}.{newext}"
                )

        # Replace all filenames' extensions
        else:
            new_filepath = pathlib.Path(f"{path.parent}/{new_filepath.stem}.{newext}")

    # Insert prefix if one is provided
    if prefix:
        new_filepath = pathlib.Path(f"{path.parent}/{prefix}{new_filepath.name}")

    # Insert suffix if one is provided
    if suffix:
        new_filepath = pathlib.Path(
            f"{path.parent}/{new_filepath.stem}{suffix}{new_filepath.suffix}"
        )

    # Replace old file with new
    path.replace(new_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FilenameManager",
        description="Modify all filenames in a given directory.",
    )
    parser.add_argument(
        "path", type=pathlib.Path, help="the path to directory of files to modify"
    )
    parser.add_argument(
        "-p", "--prefix", type=str, help="what to put before filenames"
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        help="what to put after filenames (but before extension)",
    )
    parser.add_argument(
        "-o", "--oldext", type=str, help="extension string to be replaced"
    )
    parser.add_argument(
        "-n", "--newext", type=str, help="extension string to replace with"
    )
    args = parser.parse_args()

    try:
        modify_filenames(args.path, args.prefix, args.suffix, args.oldext, args.newext)
    except (NotADirectoryError, ValueError):
        print(sys.exception())
    print()
