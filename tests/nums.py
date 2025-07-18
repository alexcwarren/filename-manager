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
