import pathlib
import random

import pytest

import src.filename_manager.filename_manager as filename_manager

TEST_DIR = "./.test"

FILE_EXTENSIONS = ["txt", "exe", "doc", "jpg", "png"]


class Nums:
    subdir_num = 0
    file_num = 0

    def get_next_subdir_num(self) -> int:
        num = self.subdir_num
        self.subdir_num += 1
        return num

    def get_next_file_num(self) -> int:
        num = self.file_num
        self.file_num += 1
        return num


nums = Nums()


@pytest.fixture(autouse=True)
def test_dir():
    # Create test_dir path
    test_dir_path = pathlib.Path(TEST_DIR)

    # Remove test_dir if it exists
    if test_dir_path.exists():
        cleanup(test_dir_path)

    # Create test_dir
    test_dir_path.mkdir()

    # Reset nums for file/directory naming
    nums.subdir_num = 0
    nums.file_num = 0

    # Create some test subdirectories and files
    create_directories(test_dir_path)

    return test_dir_path


# BEGIN TESTS


@pytest.mark.parametrize("bad_dir", ["a"])
def test_bad_path(bad_dir):
    assert_exception_caught(NotADirectoryError, pathlib.Path(bad_dir))


@pytest.mark.parametrize("prefix", ["pre_"])
def test_prefix_only(test_dir, prefix):
    assert_filenames(test_dir, lambda old: f"{prefix}{old.name}", prefix=prefix)


@pytest.mark.parametrize("suffix", ["_SUF"])
def test_suffix_only(test_dir, suffix):
    assert_filenames(
        test_dir, lambda old: f"{old.stem}{suffix}{old.suffix}", suffix=suffix
    )


@pytest.mark.parametrize("newext", ["md"])
def test_all_extensions_only(test_dir, newext):
    assert_filenames(test_dir, lambda old: f"{old.stem}.{newext}", newext=newext)


@pytest.mark.parametrize("oldext", FILE_EXTENSIONS)
@pytest.mark.parametrize("newext", ["md"])
def test_certain_extensions_only(test_dir, oldext, newext):
    assert_filenames(
        test_dir,
        lambda old: f"{old.stem}.{newext}",
        oldext=oldext,
        newext=newext,
        condition_pattern=lambda old: f".{oldext}" == old.suffix,
    )


@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("newext", ["EXT"])
def test_prefix_suffix_all_extensions(test_dir, prefix, suffix, newext):
    assert_filenames(
        test_dir,
        lambda old: f"{prefix}{old.stem}{suffix}.{newext}",
        prefix=prefix,
        suffix=suffix,
        newext=newext,
    )


@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("oldext", FILE_EXTENSIONS)
@pytest.mark.parametrize("newext", ["EXT"])
def test_prefix_suffix_certain_extensions(test_dir, prefix, suffix, oldext, newext):
    assert_filenames(
        test_dir,
        lambda old: f"{prefix}{old.stem}{suffix}.{newext}",
        prefix=prefix,
        suffix=suffix,
        oldext=oldext,
        newext=newext,
        condition_pattern=lambda old: f".{oldext}" == old.suffix,
    )


@pytest.mark.parametrize(
    "bad_prefix", [f"pre{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_only(test_dir, bad_prefix):
    assert_exception_caught(ValueError, test_dir, prefix=bad_prefix)


@pytest.mark.parametrize(
    "bad_suffix", [f"suf{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_suffix_only(test_dir, bad_suffix):
    assert_exception_caught(ValueError, test_dir, suffix=bad_suffix)


@pytest.mark.parametrize(
    "bad_ext", [f"ext{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_extension_only(test_dir, bad_ext):
    assert_exception_caught(ValueError, test_dir, newext=bad_ext)


@pytest.mark.parametrize("oldext", ["md"])
def test_oldext_no_newext(test_dir, oldext):
    assert_exception_caught(TypeError, test_dir, oldext=oldext)


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_good_prefix_good_suffix_bad_extension(test_dir, prefix, suffix, badext):
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=suffix, newext=badext
    )


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("ext", ["EXT"])
def test_good_prefix_bad_suffix_good_extension(test_dir, prefix, badsuffix, ext):
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=badsuffix, newext=ext
    )


@pytest.mark.full
@pytest.mark.parametrize("prefix", ["PREFIX"])
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_good_prefix_bad_suffix_bad_extension(test_dir, prefix, badsuffix, badext):
    assert_exception_caught(
        ValueError, test_dir, prefix=prefix, suffix=badsuffix, newext=badext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize("ext", ["EXT"])
def test_bad_prefix_good_suffix_good_extension(test_dir, badprefix, suffix, ext):
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=suffix, newext=ext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("suffix", ["SUFFIX"])
@pytest.mark.parametrize(
    "badext", [f"EXT{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_good_suffix_bad_extension(test_dir, badprefix, suffix, badext):
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=suffix, newext=badext
    )


@pytest.mark.full
@pytest.mark.parametrize(
    "badprefix", [f"PREFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize(
    "badsuffix", [f"SUFFIX{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
@pytest.mark.parametrize("ext", ["EXT"])
def test_bad_prefix_bad_suffix_good_extension(test_dir, badprefix, badsuffix, ext):
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=badsuffix, newext=ext
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
def test_bad_prefix_bad_suffix_bad_extension(test_dir, badprefix, badsuffix, badext):
    assert_exception_caught(
        ValueError, test_dir, prefix=badprefix, suffix=badsuffix, newext=badext
    )


# END TESTS


def create_directories(parent_dir: pathlib.Path, do_create_files: bool = True):
    """Create a random number of subdirectories [1,10] in given directory.

    For each subdirectory, files will also be created.
    """

    for i in range(random.randint(1, 10)):
        # Create subdirectory path
        subdir = pathlib.Path(f"{parent_dir}/subdir{nums.get_next_subdir_num()}")

        # Create the actual directory
        subdir.mkdir()

        # Create files inside the subdirectory
        if do_create_files:
            create_files(subdir)


def create_files(parent_dir: pathlib.Path):
    """Create a random number of files in given directory.

    One to three files will be randomly created for each file extension.
    (Available file-extensions stored in FILE_EXTENSIONS list)
    """

    for ext in FILE_EXTENSIONS:
        for _ in range(3):
            file = pathlib.Path(f"{parent_dir}/file{nums.get_next_file_num()}.{ext}")
            file.touch()


def cleanup(directory: pathlib.Path):
    """Delete the temporary test directory."""

    remove_dir_contents(directory)
    directory.rmdir()


def remove_dir_contents(directory: pathlib.Path):
    """Remove all contents (files/directories) in given directory."""

    for path_item in directory.iterdir():
        if path_item.is_dir():
            remove_dir_contents(path_item)
            path_item.rmdir()
        else:
            path_item.unlink()


def collect_filepaths(directory: pathlib.Path) -> list[pathlib.Path]:
    """Return list of filenames in given directory."""

    filepaths = list()

    for path_item in directory.iterdir():
        if path_item.is_dir():
            filepaths.extend(collect_filepaths(path_item))
        elif path_item.is_file():
            filepaths.append(path_item)

    return filepaths


def assert_filenames(
    directory: pathlib.Path,
    filename_pattern,
    prefix: str = None,
    suffix: str = None,
    oldext: str = None,
    newext: str = None,
    condition_pattern=lambda x: True,
):
    """Assert that new filenames match the given pattern."""

    old_filepaths: list[pathlib.Path] = collect_filepaths(directory)
    filename_manager.modify_filenames(
        directory, prefix=prefix, suffix=suffix, oldext=oldext, newext=newext
    )
    new_filenames: list[str] = [
        filepath.name for filepath in collect_filepaths(directory)
    ]

    assert len(old_filepaths) == len(new_filenames)

    condition_pattern_met = False
    for old in old_filepaths:
        if condition_pattern(old):
            condition_pattern_met = True
            assert filename_pattern(old) in new_filenames

    if not condition_pattern_met:
        assert False


def assert_exception_caught(
    error,
    directory: pathlib.Path,
    prefix: str = None,
    suffix: str = None,
    oldext: str = None,
    newext: str = None,
):
    """Assert that the given exception is caught when calling modify_filenames()."""

    caught_exception = False

    try:
        filename_manager.modify_filenames(
            directory, prefix=prefix, suffix=suffix, oldext=oldext, newext=newext
        )
    except error:
        caught_exception = True

    assert caught_exception
