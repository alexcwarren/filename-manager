import pathlib
import random
import filename_manager

import pytest


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


@pytest.mark.parametrize("prefix", [
    "pre_"
])
def test_prefix_only(test_dir, prefix):
    old_filenames = collect_filenames(test_dir)
    filename_manager.modify_filenames(test_dir, prefix)
    new_filenames = collect_filenames(test_dir)
    
    assert len(old_filenames) == len(new_filenames)
    for old in old_filenames:
        assert f"{prefix}{old}" in new_filenames

# TODO
# def test_suffix_only():

# TODO
# def test_extension_only():

# TODO
# def test_prefix_suffix():

# TODO
# def test_prefix_extension():

# TODO
# def test_suffix_extension():

# TODO
# def test_bad_prefixes():

# TODO
# def test_bad_suffixes():

# TODO
# def test_bad_extensions():

# TODO
# def test_bad_path():


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
        file = pathlib.Path(f"{parent_dir}/file{nums.get_next_file_num()}.{random.choice(file_extensions)}")
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


def collect_filenames(directory: pathlib.Path) -> list[str]:
    """Return list of filenames in given directory."""

    filenames = list()

    for path_item in directory.iterdir():
        if path_item.is_dir():
            filenames.extend(collect_filenames(path_item))
        elif path_item.is_file():
            filenames.append(path_item.name)
    
    return filenames
