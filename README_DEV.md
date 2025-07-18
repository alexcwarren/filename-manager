# filename-manager

Edit filenames in a given directory following user-defined rules.

## Usage

```shell
python filename_manager.py [-h] [-p PREFIX] [-s SUFFIX] [-o EXTOLD] [-n EXTNEW] [-r REGEX] [--sub SUB] <path>
```

`<path>` is the path to the directory containing the file(s) you want to modify.
If no other arguments are passed to tell `filename-manager` what/how to modify, no modification will occur.

### `PREFIX`

This is a string that will *prepend* all files contained in `<path>`.

`python filename_manager.py -p OLD_ ./my_folder` will *prepend* ALL the files in `my_folder` directory.
If there's initially a file in `my_folder` named `my_file.txt` this command will modify its name to become `OLDmy_file.txt`.

### `SUFFIX`

This is a string that will *append* all files contained in `<path>`.

`python filename_manager.py -s _OLD ./my_folder` will *append* ALL the files in `my_folder` directory.
If there's initially a file in `my_folder` named `my_file.txt` this command will modify its name to become `my_file_OLD.txt`.

### `EXTOLD` and `EXTNEW`

You can modify a specific file extension to another one.

`python filename_manager.py -o .txt -n .md ./my_folder` will change all files that end with a `.txt` and change that to `.md`.
If there's initially a file in `my_folder` named `my_file.txt` this command will modify its name to become `my_file.md`.

You can also modify ALL files to have a different extension.

`python filename_manager.py -o ALL -n .md ./my_folder` will change ALL files to have `.md` as its file extension.

> **NOTE:** You must provide BOTH `-o` and `-n` arguments. You cannot provide just one of them.

### `REGEX` and `SUB`

You can modify any file that matches a given pattern, `REGEX`, and replace the part of the file name that matches with the string `SUB`.

`python filename_manager.py -r "\d" --sub "X" ./my_folder` will change all files that contain a number in their file name to an `X`.
If there's initially a file in `my_folder` named `my_file01.txt` this command will modify its name to become `my_fileXX.txt`.

> **NOTE:** You must provide BOTH `-r` and `--sub` arguments. You cannot provide just one of them.

*** This functionality is particularly useful to *remove* matching patterns.

`python filename_manager.py -r "^\d+\. " "" ./my_folder` will change all files that **start** (`^`) with **one or more** (`+`) **number**s (`\d`) followed by a single **.** (`\.`) and a single space and remove that part.
If there's a file in `my_folder` named `31. My File.mp3` this command will modify its name to become `My File.mp3`.

> **WARNING**: This functionaliy may cause certain files to inadvertently be OVERRIDDEN.
>
> If your directory has a file named `file01.txt` and `file02.txt` this command will change both of these file names to the same value: `fileXX.txt`.
> This means one file will override the other as a result of the modification.
> In other words, as long as you have files with unique filenames (without the numbers, in this case) you shouldn't experience any problems.

*Check out [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) for more info on using **regex** in Python.*

*Also, try practicing **regex** at [regex101](https://regex101.com/) or at [Pythex](https://pythex.org/).*
