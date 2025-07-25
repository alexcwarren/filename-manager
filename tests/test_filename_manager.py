from __future__ import annotations

import pathlib
from typing import Callable

from file_extensions import FILE_EXTENSIONS
import pytest

import filename_manager.filename_manager as filename_manager

# BEGIN TESTS


@pytest.mark.parametrize("bad_dir", ["a"])
def test_bad_path(bad_dir: str) -> None:
    assert_exception_caught(NotADirectoryError, pathlib.Path(bad_dir))


@pytest.mark.parametrize("prefix", ["pre_"])
def test_prefix_only(test_dir: pathlib.Path, prefix: str) -> None:
    assert_filenames(test_dir, lambda old: f"{prefix}{old.name}", prefix=prefix)


@pytest.mark.parametrize("suffix", ["_SUF"])
def test_suffix_only(test_dir: pathlib.Path, suffix: str) -> None:
    assert_filenames(
        test_dir, lambda old: f"{old.stem}{suffix}{old.suffix}", suffix=suffix
    )


@pytest.mark.parametrize("extnew", ["md"])
def test_all_extensions_only(test_dir: pathlib.Path, extnew: str) -> None:
    assert_filenames(
        test_dir,
        lambda old: f"{old.stem}.{extnew}",
        extnew=extnew,
        extold=filename_manager.ALL,
    )


@pytest.mark.parametrize("extold", FILE_EXTENSIONS)
@pytest.mark.parametrize("extnew", ["md"])
def test_certain_extensions_only(
    test_dir: pathlib.Path, extold: str, extnew: str
) -> None:
    assert_filenames(
        test_dir,
        lambda old: f"{old.stem}.{extnew}",
        extold=extold,
        extnew=extnew,
        condition_pattern=lambda old: f".{extold}" == old.suffix,
    )


@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("extnew", ["EXT"])
def test_prefix_suffix_all_extensions(
    test_dir: pathlib.Path, prefix: str, suffix: str, extnew: str
) -> None:
    assert_filenames(
        test_dir,
        lambda old: f"{prefix}{old.stem}{suffix}.{extnew}",
        prefix=prefix,
        suffix=suffix,
        extnew=extnew,
        extold=filename_manager.ALL,
    )


@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("extold", FILE_EXTENSIONS)
@pytest.mark.parametrize("extnew", ["EXT"])
def test_prefix_suffix_certain_extensions(
    test_dir: pathlib.Path, prefix: str, suffix: str, extold: str, extnew: str
) -> None:
    assert_filenames(
        test_dir,
        lambda old: f"{prefix}{old.stem}{suffix}.{extnew}",
        prefix=prefix,
        suffix=suffix,
        extold=extold,
        extnew=extnew,
        condition_pattern=lambda old: f".{extold}" == old.suffix,
    )


@pytest.mark.parametrize(
    "bad_prefix", [f"pre{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_only(test_dir: pathlib.Path, bad_prefix: str) -> None:
    assert_exception_caught(ValueError, test_dir, prefix=bad_prefix)


@pytest.mark.parametrize(
    "bad_suffix", [f"suf{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_suffix_only(test_dir: pathlib.Path, bad_suffix: str) -> None:
    assert_exception_caught(ValueError, test_dir, suffix=bad_suffix)


@pytest.mark.parametrize(
    "bad_ext", [f"ext{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_extension_only(test_dir: pathlib.Path, bad_ext: str) -> None:
    assert_exception_caught(ValueError, test_dir, extnew=bad_ext)


@pytest.mark.parametrize("extold", ["md"])
def test_oldext_no_newext(test_dir: pathlib.Path, extold: str) -> None:
    assert_exception_caught(TypeError, test_dir, extold=extold)


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_good_prefix_good_suffix_bad_extension(
    test_dir: pathlib.Path, prefix: str, suffix: str, badext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=suffix, extnew=badext
    )


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("ext", ["EXT"])
def test_good_prefix_bad_suffix_good_extension(
    test_dir: pathlib.Path, prefix: str, badsuffix: str, ext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=badsuffix, extnew=ext
    )


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_good_prefix_bad_suffix_bad_extension(
    test_dir: pathlib.Path, prefix: str, badsuffix: str, badext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=badsuffix, extnew=badext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("ext", ["EXT"])
def test_bad_prefix_good_suffix_good_extension(
    test_dir: pathlib.Path, badprefix: str, suffix: str, ext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=suffix, extnew=ext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_good_suffix_bad_extension(
    test_dir: pathlib.Path, badprefix: str, suffix: str, badext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=suffix, extnew=badext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("ext", ["EXT"])
def test_bad_prefix_bad_suffix_good_extension(
    test_dir: pathlib.Path, badprefix: str, badsuffix: str, ext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=badsuffix, extnew=ext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_bad_suffix_bad_extension(
    test_dir: pathlib.Path, badprefix: str, badsuffix: str, badext: str
) -> None:
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=badsuffix, extnew=badext
    )


@pytest.mark.parametrize("regex", [""])
@pytest.mark.parametrize("sub", [""])
def test_regex_sub(test_dir: pathlib.Path, regex: str, sub: str) -> None:
    pass
    # assert_filenames(
    #    directory=test_dir,
    # )


# END TESTS


def collect_filepaths(directory: pathlib.Path) -> list[pathlib.Path]:
    """Return list of filenames in given directory."""

    filepaths = []

    for path_item in directory.iterdir():
        if path_item.is_dir():
            filepaths.extend(collect_filepaths(path_item))
        elif path_item.is_file():
            filepaths.append(path_item)

    return filepaths


def assert_filenames(
    directory: pathlib.Path,
    filename_pattern: Callable,
    suffix: str | None = None,
    prefix: str | None = None,
    extold: str | None = None,
    extnew: str | None = None,
    regex: str | None = None,
    sub: str | None = None,
    condition_pattern: Callable = lambda x: True,
) -> None:
    """Assert that new filenames match the given pattern."""

    # Make sure test directory exists
    assert directory.exists()

    # Retrieve all Path objects contained in `directory` before modification
    old_filepaths: list[pathlib.Path] = collect_filepaths(directory)

    # Confirm test directory isn't empty
    assert len(old_filepaths) > 0

    filename_manager.modify_filenames(
        directory,
        prefix=prefix,
        suffix=suffix,
        extold=extold,
        extnew=extnew,
        regex=regex,
        sub=sub,
    )
    # Retrieve all filenames of contents in `directory` after modification
    new_filenames: list[str] = [
        filepath.name for filepath in collect_filepaths(directory)
    ]

    assert len(old_filepaths) == len(new_filenames)

    condition_pattern_met = False
    for old in old_filepaths:
        if condition_pattern(old):
            condition_pattern_met = True
            assert filename_pattern(old) in new_filenames
        else:
            assert filename_pattern(old) not in new_filenames

    if not condition_pattern_met:
        pytest.fail()


def assert_exception_caught(
    error: type[Exception],
    directory: pathlib.Path,
    prefix: str | None = None,
    suffix: str | None = None,
    extold: str | None = None,
    extnew: str | None = None,
) -> None:
    """Assert that the given exception is caught when calling modify_filenames()."""

    caught_exception = False

    try:
        filename_manager.modify_filenames(
            directory, prefix=prefix, suffix=suffix, extold=extold, extnew=extnew
        )
    except error:
        caught_exception = True

    assert caught_exception
