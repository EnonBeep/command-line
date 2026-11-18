# Spec

Single-file Python program (`organizer.py`, standard library only). It copies the
top-level files of a folder into category subfolders created inside that folder.

| Req | How it is met | Test |
|-----|---------------|------|
| R1 | `main()` reads exactly one command-line argument (the folder). Wrong argument count prints usage and exits 2. | `test_r1_*` |
| R2 | `categorize()` lowercases `Path.suffix` and looks it up in the `CATEGORIES` extension table. | `test_r2_*` |
| R3 | Extensions map to `images`, `documents`, `videos`; anything else (including no extension) is `other`. | `test_r3_categories` |
| R4 | `organize()` creates `<folder>/<category>/` on demand and copies each file with `shutil.copy2`. Subfolders are not scanned, so category folders are not re-sorted on re-runs. | `test_r4_*` |
| R5 | Only `shutil.copy2` is used; no move/delete/write on originals. Existing files in category folders are never overwritten — a `_1`, `_2`… suffix is added. | `test_r5_*` |
| R6 | Missing path, non-directory path, unreadable folder, or copy failure raise `OrganizerError`; `main()` prints `Error: <message>` to stderr and exits 1. | `test_r6_*` |
