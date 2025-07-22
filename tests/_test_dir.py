import pathlib
import random
from string import ascii_letters as alphabet

from file_extensions import FILE_EXTENSIONS
from nums import Nums


class _TestDir:
    def __init__(self, dir_path: str, seed: str | None = None):
        self.path: pathlib.Path = pathlib.Path(dir_path)

        # Remove test_dir if it exists
        if self.path.exists():
            self.cleanup()

        # Create test_dir
        self.path.mkdir()

        self.__nums = Nums()

        self.seed = seed
        random.seed(self.seed)

        self.__create_directories()

    def __create_directories(self, do_create_files: bool = True) -> None:
        """Create a random number of subdirectories [1,10] in given directory.

        For each subdirectory, files will also be created.
        """

        for _ in range(random.randint(1, 10)):
            # Create subdirectory path
            subdir = pathlib.Path(
                f"{self.path}/subdir{self.__nums.get_next_subdir_num()}"
            )

            # Create the actual directory
            subdir.mkdir()

            # Create files inside the subdirectory
            if do_create_files:
                self.__create_files(subdir)

    def __create_files(self, dir: pathlib.Path) -> None:
        """Create a random number of files in given directory.

        One to three files will be randomly created for each file extension.
        (Available file-extensions stored in FILE_EXTENSIONS list)
        """

        for ext in FILE_EXTENSIONS:
            for _ in range(3):
                # Get random filename with 50/50 chance of numbering
                filename: str = self.__random_filename(
                    number_filenames=(random.choice([True, False]))
                )
                file: pathlib.Path = dir.joinpath(f"{filename}.{ext}")
                file.touch()

    def __random_filename(
        self, word_length: int = 10, number_filenames: bool = True
    ) -> str:
        filename: str = (
            f"{self.__nums.get_next_file_num()}. " if number_filenames else ""
        )
        filename += "".join(random.choices(alphabet, k=word_length))
        return filename

    def cleanup(self) -> None:
        """Delete the temporary test directory."""

        self.__remove_dir_contents(self.path)
        self.path.rmdir()

    def __remove_dir_contents(self, dir: pathlib.Path) -> None:
        """Remove all contents (files/directories) in given directory."""

        for path_item in dir.iterdir():
            if path_item.is_dir():
                self.__remove_dir_contents(path_item)
                path_item.rmdir()
            else:
                path_item.unlink()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(dirpath = {self.path}, seed = {self.seed})"
        )
