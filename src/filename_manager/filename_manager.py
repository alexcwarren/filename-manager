"""Filename Manager

This script contains functionality to modify all filenames within a given directory
path.

This file can also be imported as a module and contains the following functions:

    * modify_filenames
    * modify_filename
"""

from __future__ import annotations

import argparse
import logging
import pathlib
import re
import sys

logger: logging.Logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO, log_file: str | None = None) -> None:
    """
    Configures the root logger for console and optional file output.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)  # Set the minimum level for the root logger

    # Clear existing handlers to prevent duplicate messages if called multiple times
    # (Useful in testing or if setup_logging might be called more than once)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # --- Console Handler (for messages to stderr) ---
    console_handler = logging.StreamHandler(sys.stderr)
    # A concise formatter for console output
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)  # Ensure console handler respects the overall level
    root_logger.addHandler(console_handler)

    # --- Optional File Handler ---
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            # A more detailed formatter for file output
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(
                logging.DEBUG
            )  # Typically, file logs are more verbose (DEBUG)
            # regardless of console level, but can be same as 'level'
            root_logger.addHandler(file_handler)
        except Exception as e:
            # Log this error to console as the file handler setup failed
            root_logger.error(f"Could not set up log file '{log_file}': {e}")


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
        prog="filename-manager",
        description="Edit a batch of given filenames following user-defined rules.",
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
    # Add verbosity arguments for logging level
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity (e.g., -v for INFO, -vv for DEBUG).",
    )
    # Add argument for log file
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to a file where logs will be written (e.g., filename_manager.log).",
    )

    args = parser.parse_args()

    # Determine log level based on verbosity argument
    log_level = logging.WARNING  # Default log level if no -v
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:  # -vv or more
        log_level = logging.DEBUG
    # For very quiet output, you could add an --quiet option setting level to ERROR/CRITICAL

    # --- Configure Logging ---
    setup_logging(log_level, args.log_file)

    # Now you can use the logger globally or within this module
    logger.info(
        "Application started with log level: %s", logging.getLevelName(log_level)
    )
    if args.log_file:
        logger.info("Logging to file: %s", args.log_file)
    logger.debug("Detailed debug information enabled.")

    try:
        logger.info("Starting file processing...")
        modify_filenames(
            args.path,
            args.prefix,
            args.suffix,
            args.extold,
            args.extnew,
            args.regex,
            args.sub,
        )
        logger.info("File processing complete.")
    except NotADirectoryError as e:
        logger.error(
            f"Error: The specified source path is not a valid directory. Details: {e}"
        )
        logger.info("Please ensure the directory exists and you have read permissions.")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Error: Invalid input value or format encountered. Details: {e}")
        logger.info(
            "Please check the contents of your rules file or command-line arguments."
        )
        sys.exit(1)
    except Exception:
        logger.exception(
            "An unhandled error occurred during filename manager execution:"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
