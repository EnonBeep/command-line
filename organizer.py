"""Copy files in a folder into category folders (images, documents, videos, other)."""

import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
}
OTHER = "other"
ALL_CATEGORIES = list(CATEGORIES) + [OTHER]


class OrganizerError(Exception):
    """Raised with a user-friendly message when the folder can't be used."""


def categorize(path):
    """R2/R3: return the category name for a file based on its extension."""
    ext = Path(path).suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return OTHER


def _unique_target(folder, name):
    """Pick a destination name that does not overwrite an existing file."""
    target = folder / name
    stem, suffix = Path(name).stem, Path(name).suffix
    n = 1
    while target.exists():
        target = folder / f"{stem}_{n}{suffix}"
        n += 1
    return target


def organize(folder):
    """R4/R5: copy each top-level file into <folder>/<category>/. Returns {category: count}."""
    source = Path(folder)
    if not source.exists():
        raise OrganizerError(f"Folder not found: {folder}")
    if not source.is_dir():
        raise OrganizerError(f"Not a folder: {folder}")
    try:
        files = [p for p in source.iterdir() if p.is_file()]
    except OSError as e:
        raise OrganizerError(f"Cannot access folder '{folder}': {e.strerror or e}") from e

    counts = {}
    for path in files:
        category = categorize(path)
        dest_dir = source / category
        try:
            dest_dir.mkdir(exist_ok=True)
            shutil.copy2(path, _unique_target(dest_dir, path.name))  # copy only; original untouched
        except OSError as e:
            raise OrganizerError(f"Cannot copy '{path.name}': {e.strerror or e}") from e
        counts[category] = counts.get(category, 0) + 1
    return counts


def main(argv=None):
    """R1: the folder to organize is a command-line argument."""
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Usage: python organizer.py <folder>", file=sys.stderr)
        return 2
    try:
        counts = organize(argv[0])
    except OrganizerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    if not counts:
        print("No files found to organize.")
    for category in ALL_CATEGORIES:
        if category in counts:
            print(f"{category}: {counts[category]} file(s) copied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
