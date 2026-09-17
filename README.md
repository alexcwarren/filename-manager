# filename-manager

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

**A batch renaming tool with user-defined rules.**  
Rename files in bulk using flexible patterns — ideal for developers, content creators, media managers, and data professionals.

## Table of Contents

- [filename-manager](#filename-manager)
  - [Table of Contents](#table-of-contents)
  - [🚀 Features](#-features)
  - [🔧 Installation](#-installation)
  - [📦 Usage](#-usage)
    - [Basic CLI Example](#basic-cli-example)
      - [Before](#before)
      - [After](#after)
  - [🪛 CLI Options](#-cli-options)
  - [🎯 Advanced Examples](#-advanced-examples)
    - [✅ Add a prefix](#-add-a-prefix)
    - [✅ Add a suffix](#-add-a-suffix)
    - [✅ Change extension](#-change-extension)
    - [✅ Regex pattern replace](#-regex-pattern-replace)
  - [🧪 Testing \& Coverage](#-testing--coverage)
  - [📦 Build \& Distribute](#-build--distribute)
  - [📷 Demo](#-demo)
  - [🔄 Roadmap](#-roadmap)
  - [💬 Feedback or Suggestions?](#-feedback-or-suggestions)
  - [🔗 Related Tools](#-related-tools)
  - [📄 License](#-license)

---

## 🚀 Features

- Rename files using prefixes, suffixes, regex, or extension replacements
- Recursive renaming within nested folders
- Handles errors and edge cases with clear messages
- Built-in CLI interface (cross-platform)
- Lightweight and fast

---

## 🔧 Installation

```shell
git clone https://github.com/alexcwarren/filename-manager.git
cd filename-manager
pip install -e .
```

> 💡 You can also add this script to your system path for easier access.

---

## 📦 Usage

```shell
filename-manager <path> [options]
```

`<path>` is the directory of files to rename.
If no other arguments are passed, no modification will occur.

### Basic CLI Example

```shell
filename-manager ./photos -p Vacation_
```

#### Before

```shell
IMG_001.jpg
IMG_002.jpg
```

#### After

```shell
Vacation_IMG_001.jpg
Vacation_IMG_002.jpg
```

---

## 🪛 CLI Options

| Option | Description |
| --- | --- |
| `-p, --prefix` | String to prepend to filename |
| `-s, --suffix` | String to append to filename (before extension) |
| `--extold` | File extension to replace |
| `--extnew` | New file extension |
| `-r, --regex` | Regex pattern to find in filename |
| `--sub` | Substring to replace regex match |
| `-h, --help` | Show help message |

---

## 🎯 Advanced Examples

### ✅ Add a prefix

```shell
filename-manager ./my_folder -p OLD_
```

### ✅ Add a suffix

```shell
filename-manager ./my_folder -s _OLD
```

### ✅ Change extension

```shell
filename-manager ./my_folder --extold .txt --extnew .md
```

`my_file.txt` → `my_file.md`

```shell
filename-manager ./my_folder --extold ALL --extnew .md
```

Changes extension for all files to `.md`

### ✅ Regex pattern replace

```shell
filename-manager ./my_folder -r "\d" --sub "X"
```

`file01.txt` → `fileXX.txt`

```shell
filename-manager ./my_folder -r "^\d+\. " --sub ""
```

`31. My File.mp3` → `My File.mp3`

> ⚠️ Be cautious of overwrites when regex makes multiple filenames identical.

---

## 🧪 Testing & Coverage

```shell
pytest
```

🔍 Run tests and see coverage:

```shell
pytest --cov=src/filename_manager --cov-report=term-missing
```

Run only fast tests (default):

```shell
pytest -m "not full"
```

Run full suite:

```shell
pytest -m "full"
```

Run tests and output coverage to HTML file:

```bash
pytest --cov=src/filename_manager --cov-report=html
```

Open the generated `htmlcov/index.html` file in a browser to see coverage.

---

## 📦 Build & Distribute

To build a distribution:

```shell
python -m build
```

To publish to PyPI using Twine:

```shell
twine upload dist/*
```

To test upload (TestPyPI):

```shell
twine upload --repository testpypi dist/*
```

To remove `dist/` cleanly (for re-building):

Bash

```bash
rm -rf dist
```

PowerShell

```shell
Remove-Item -Recurse -Force dist
```

---

## 📷 Demo

📌 *Coming soon!*
(Screenshots, gifs, or terminal recordings will go here)

---

## 🔄 Roadmap

Planned future features:

- [ ] Dry-run support
- [ ] Undo/revert
- [ ] Regex preview mode
- [ ] Config file (YAML/JSON) support
- [ ] GUI interface

---

## 💬 Feedback or Suggestions?

Feel free to [open an issue](https://github.com/alexcwarren/filename-manager/issues) or [submit a pull request](https://github.com/alexcwarren/filename-manager/pulls). Feedback is always welcome!

---

## 🔗 Related Tools

- [replace-template](https://github.com/alexcwarren/replace-template)
- [image-manager](https://github.com/alexcwarren/image-manager)

---

## 📄 License

[MIT License](https://github.com/alexcwarren/filename-manager/blob/main/README.md)
