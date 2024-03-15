import pathlib
import random

import pytest

import src.filename_manager.filename_manager as filename_manager

TEST_DIR = "./.test"


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

    # Create some test subdirectories and files
    create_directories(test_dir_path)

    return test_dir_path


# BEGIN TESTS


@pytest.mark.parametrize("bad_dir", ["a"])
def test_bad_path(bad_dir):
    caught_not_directory_exception = False

    try:
        filename_manager.modify_filenames(pathlib.Path(bad_dir))
    except NotADirectoryError:
        caught_not_directory_exception = True

    assert caught_not_directory_exception


@pytest.mark.parametrize("prefix", ["pre_"])
def test_prefix_only(test_dir, prefix):
    old_filepaths: list[pathlib.Path] = collect_filepaths(test_dir)
    filename_manager.modify_filenames(test_dir, prefix)
    new_filenames: list[str] = [
        filepath.name for filepath in collect_filepaths(test_dir)
    ]

    assert len(old_filepaths) == len(new_filenames)
    for old in old_filepaths:
        assert f"{prefix}{old.name}" in new_filenames


@pytest.mark.parametrize("suffix", ["_SUF"])
def test_suffix_only(test_dir, suffix):
    old_filepaths: list[pathlib.Path] = collect_filepaths(test_dir)
    filename_manager.modify_filenames(test_dir, suffix=suffix)
    new_filenames: list[str] = [
        filepath.name for filepath in collect_filepaths(test_dir)
    ]

    assert len(old_filepaths) == len(new_filenames)
    for old in old_filepaths:
        assert f"{old.stem}{suffix}{old.suffix}" in new_filenames


# TODO
# def test_extension_only():


def test_prefix_suffix(test_dir):
    prefix = "PREFIX"
    suffix = "SUFFIX"

    old_filepaths: list[pathlib.Path] = collect_filepaths(test_dir)
    filename_manager.modify_filenames(test_dir, prefix, suffix)
    new_filenames: list[str] = [
        filepath.name for filepath in collect_filepaths(test_dir)
    ]

    assert len(old_filepaths) == len(new_filenames)
    for old in old_filepaths:
        assert f"{prefix}{old.stem}{suffix}{old.suffix}" in new_filenames


# TODO
# def test_prefix_extension():

# TODO
# def test_suffix_extension():

# TODO
# def test_prefix_suffix_extension():


@pytest.mark.parametrize(
    "bad_prefix", [f"pre{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_only(test_dir, bad_prefix):
    caught_value_exception = False

    try:
        filename_manager.modify_filenames(test_dir, bad_prefix)
    except ValueError:
        caught_value_exception = True

    assert caught_value_exception


@pytest.mark.parametrize(
    "bad_suffix", [f"suf{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_suffix_only(test_dir, bad_suffix):
    caught_value_exception = False

    try:
        filename_manager.modify_filenames(test_dir, suffix=bad_suffix)
    except ValueError:
        caught_value_exception = True

    assert caught_value_exception


# TODO
# def test_bad_extension_only():


@pytest.mark.parametrize(
    "bad_prefix", [f"pre{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_prefix_good_suffix(test_dir, bad_prefix):
    suffix = "SUFFIX"
    caught_value_exception = False

    try:
        filename_manager.modify_filenames(test_dir, bad_prefix, suffix)
    except ValueError:
        caught_value_exception = True

    assert caught_value_exception


# TODO
# def test_bad_prefix_good_extension():


@pytest.mark.parametrize(
    "bad_suffix", [f"suf{ch}" for ch in filename_manager.FORBIDDEN_CHARACTERS]
)
def test_bad_suffix_good_extension(test_dir, bad_suffix):
    prefix = "PREFIX"
    caught_value_exception = False

    try:
        filename_manager.modify_filenames(test_dir, prefix, bad_suffix)
    except ValueError:
        caught_value_exception = True

    assert caught_value_exception


# TODO
# def test_good_prefix_bad_suffix():

# TODO
# def test_good_prefix_bad_extension():

# TODO
# def test_good_suffix_bad_extension():

# TODO
# def test_good_prefix_good_suffix_bad_extension():

# TODO
# def test_good_prefix_bad_suffix_good_extension():

# TODO
# def test_good_prefix_bad_suffix_bad_extension():

# TODO
# def test_bad_prefix_good_suffix_good_extension():

# TODO
# def test_bad_prefix_good_suffix_bad_extension():

# TODO
# def test_bad_prefix_bad_suffix_good_extension():

# TODO
# def test_bad_prefix_bad_suffix_bad_extension():


# END TESTS


def create_directories(parent_dir: pathlib.Path):
    """Create a random number of subdirectories [1,10] in given directory.

    For each subdirectory, files will also be created.
    """

    for i in range(random.randint(1, 10)):
        # Create subdirectory path
        subdir = pathlib.Path(f"{parent_dir}/subdir{nums.get_next_subdir_num()}")

        # Create the actual directory
        subdir.mkdir()

        # Create files inside the subdirectory
        create_files(subdir)


def create_files(parent_dir: pathlib.Path):
    """Create a random number of files [1,10] in given directory.

    Each file will have a random file-extension.
    (Available file-extensions = txt, exe, doc, png)
    """

    file_extensions = ["txt", "exe", "doc", "png"]

    for i in range(random.randint(1, 10)):
        file = pathlib.Path(
            f"{parent_dir}"
            + f"/file{nums.get_next_file_num()}.{random.choice(file_extensions)}"
        )
        file.touch()


def cleanup(test_dir: pathlib.Path):
    """Delete the temporary test directory."""

    remove_dir_contents(test_dir)
    test_dir.rmdir()


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
