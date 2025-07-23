"""Filename Manager

This script contains functionality to modify all filenames within a given directory
path.

This file can also be imported as a module and contains the following functions:

    * modify_filenames
    * modify_filename
"""

import argparse
import pathlib
import re

FORBIDDEN_CHARACTERS: str = '<>:"/\\|?*'
ALL: str = "ALL"


def modify_filenames(
    path: pathlib.Path,
    prefix: str | None = None,
    suffix: str | None = None,
    extold: str | None = None,
    extnew: str | None = None,
    regex: str | None = None,
    sub: str | None = None,

) -> bool:
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
            modify_filename(path_item, prefix, suffix, extold, extnew, regex, sub)
        elif path_item.is_dir():
            no_files_found = modify_filenames(
                path_item, prefix, suffix, extold, extnew, regex, sub
            )

    if no_files_found:
        raise FileNotFoundError(f"No files found in path: '{path.absolute()}'")

    return no_files_found


def modify_filename(
    path: pathlib.Path,
    prefix: str | None = None,
    suffix: str | None = None,
    extold: str | None = None,
    extnew: str | None = None,
    regex: str | None = None,
    sub: str | None = None,
) -> None:
    """Modify given filename."""

    # Confirm existing arguments are valid
    for arg in (prefix, suffix, extold, extnew, sub):
        if arg is not None and (
            not arg.isprintable() or any(ch in FORBIDDEN_CHARACTERS for ch in arg)
        ):
            raise ValueError(
                f"argument contains forbidden character: '{arg}'"
                + f"\n(forbidden characters = {FORBIDDEN_CHARACTERS})"
            )

    new_filepath: pathlib.Path = path
    missing_arg: str = ""

    # Verify both extension arguments exist if one is provided
    extold_provided: bool = extold is not None
    extnew_provided: bool = extnew is not None
    if extold_provided ^ extnew_provided:
        missing_arg = "extnew" if extold_provided else "extold"
        raise TypeError(
            f'{modify_filename.__name__}() missing 1 argument: "{missing_arg}".'
        )

    # Verify both substring arguments exist if one is provided
    regex_provided: bool = regex is not None
    sub_provided: bool = sub is not None
    if regex_provided ^ sub_provided:
        missing_arg = "sub" if regex_provided else "regex"
        raise TypeError(
            f'{modify_filename.__name__}() missing 1 argument: "{missing_arg}".'
        )

    # Replace extension if provided
    if extold and extnew:
        extnew = extnew.replace(".", "")
        extold = extold.replace(".", "")

        # Replace only filenames with oldext (or ALL)
        if extold == ALL or new_filepath.suffix == f".{extold}":
            new_filepath = pathlib.Path(f"{path.parent}/{new_filepath.stem}.{extnew}")

    # Replace substrings if provided
    if regex_provided and sub_provided:
        new_filename: str = re.sub(regex or "", sub or "", new_filepath.name)
        new_filepath = new_filepath.with_name(new_filename)
        # new_filepath = pathlib.Path(re.sub(r"^\d+\.? ?", "", new_filepath))

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


def main() -> None:
    """Parse command-line arguments and invoke filename modification logic."""
    parser = argparse.ArgumentParser(
        prog="FilenameManager",
        description="Modify all filenames in a given directory.",
    )
    parser.add_argument(
        "path", type=pathlib.Path, help="the path to directory of files to modify"
    )
    parser.add_argument("-p", "--prefix", type=str, help="what to put before filenames")
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        help="what to put after filenames (but before extension)",
    )
    parser.add_argument("--extold", type=str, help="extension string to be replaced")
    parser.add_argument("--extnew", type=str, help="extension string to replace with")
    parser.add_argument(
        "-r", "--regex", type=str, help="regular expression to check in filenames"
    )
    parser.add_argument("--sub", type=str, help="substring to replace based on regex")
    args = parser.parse_args()

    try:
        modify_filenames(
            args.path,
            args.prefix,
            args.suffix,
            args.extold,
            args.extnew,
            args.regex,
            args.sub,
        )
    except (NotADirectoryError, ValueError) as e:
        print(e)
    print()


if __name__ == "__main__":
    main()
