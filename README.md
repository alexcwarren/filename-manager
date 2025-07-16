# filename-manager

**A batch renaming tool with user-defined rules.**  
Rename files in bulk using flexible patterns — ideal for developers, content creators, media managers, and data professionals.

## Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [CLI Options](#-cli-options)
- [Demo](#-demo)
- [Roadmap](#-roadmap)
- [Feedback or Suggestions?](#-feedback-or-suggestions)
- [Related Tools](#-related-tools)
- [License](#-license)

---

## 🚀 Features

- Rename files using custom string replacement rules
- Preview changes with a dry-run mode
- Works on multiple directories and file types
- Simple command-line interface (cross-platform)

---

## 🔧 Installation

```bash
git clone https://github.com/alexcwarren/filename-manager.git
cd filename-manager
python3 filename_manager.py --help
```

> 💡 You can also add this script to your system path for easier access.

---

## 📦 Usage

### Basic Example

```bash
python3 filename_manager.py ./photos --replace "IMG_" "Vacation_"
```

#### Before:

```
IMG_001.jpg
IMG_002.jpg
```

#### After:

```
Vacation_001.jpg
Vacation_002.jpg
```

### Preview Changes First (Dry Run)

```bash
python3 filename_manager.py ./photos --replace "IMG_" "Trip_" --dry-run
```

> No changes are made — just shows what would happen.

---

## 🪛 CLI Options

```bash
--replace        Specify the string to replace and the new string
--dry-run        Preview filename changes without modifying files
--extensions     Filter which file types to rename
--recursive      Apply renaming to subdirectories
--help           Show usage info
```

---

## 📷 Demo

TODO

---

## 🔄 Roadmap

Planned future features:
- Regex pattern matching
- Undo support
- Rule-based config files (JSON/YAML)
- GUI version

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
