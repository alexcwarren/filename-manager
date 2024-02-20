import pathlib


class FilenameManager:
    def __init__(self):
        directory = pathlib.Path(self.__prompt_directory_path())
        for file in directory.walk():
            print(file)

    def __prompt_directory_path(self):
        directory_path = input("Please enter directory path: ")
        print(f"You entered >>>{directory_path}<<<")
        return directory_path


if __name__ == "__main__":
    filename_manager = FilenameManager()
