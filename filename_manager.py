import pathlib


class FilenameManager:
    def __init__(self):
        self.directory = pathlib.Path(self.__prompt_directory_path())
        prepend = self.__prompt_prepend()
        self.prepend_files(prepend)

    def prepend_files(self, prepend):
        for file in self.directory.iterdir():
            # Skip if it's a directory
            if file.is_dir():
                continue

            new_file = file.with_stem(prepend + file.stem)
            file.replace(new_file)

    def __prompt_directory_path(self):
        directory_path = input("Please enter directory path: ")
        return directory_path

    def __prompt_prepend(self):
        prepend = input("Please enter prepend string: ")
        return prepend


if __name__ == "__main__":
    filename_manager = FilenameManager()
