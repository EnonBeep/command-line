import unittest
import tempfile
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
import io

import organizer


def run_main(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = organizer.main(args)
    return code, out.getvalue(), err.getvalue()


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.files = {"a.jpg": b"img", "b.PDF": b"doc", "c.mp4": b"vid", "d.xyz": b"oth", "noext": b"x"}
        for name, data in self.files.items():
            (self.dir / name).write_bytes(data)

    def tearDown(self):
        self.tmp.cleanup()

    def test_r1_folder_from_command_line(self):
        code, out, _ = run_main([str(self.dir)])
        self.assertEqual(code, 0)
        self.assertTrue((self.dir / "images" / "a.jpg").exists())

    def test_r1_missing_argument(self):
        code, _, err = run_main([])
        self.assertNotEqual(code, 0)
        self.assertIn("Usage", err)

    def test_r2_extension_detection_case_insensitive(self):
        self.assertEqual(organizer.categorize("x.JPG"), "images")
        self.assertEqual(organizer.categorize("x.pdf"), "documents")
        self.assertEqual(organizer.categorize("x.MkV"), "videos")

    def test_r3_categories(self):
        self.assertEqual(organizer.categorize("a.png"), "images")
        self.assertEqual(organizer.categorize("a.docx"), "documents")
        self.assertEqual(organizer.categorize("a.mov"), "videos")
        self.assertEqual(organizer.categorize("a.xyz"), "other")
        self.assertEqual(organizer.categorize("noext"), "other")

    def test_r4_folders_created_and_files_copied(self):
        counts = organizer.organize(self.dir)
        self.assertEqual(counts, {"images": 1, "documents": 1, "videos": 1, "other": 2})
        self.assertEqual((self.dir / "images" / "a.jpg").read_bytes(), b"img")
        self.assertEqual((self.dir / "documents" / "b.PDF").read_bytes(), b"doc")
        self.assertEqual((self.dir / "videos" / "c.mp4").read_bytes(), b"vid")
        self.assertEqual((self.dir / "other" / "d.xyz").read_bytes(), b"oth")
        self.assertTrue((self.dir / "other" / "noext").exists())

    def test_r5_originals_untouched(self):
        organizer.organize(self.dir)
        for name, data in self.files.items():
            self.assertEqual((self.dir / name).read_bytes(), data)

    def test_r5_rerun_does_not_overwrite_or_delete(self):
        organizer.organize(self.dir)
        (self.dir / "images" / "a.jpg").write_bytes(b"changed")
        organizer.organize(self.dir)
        self.assertEqual((self.dir / "images" / "a.jpg").read_bytes(), b"changed")
        self.assertEqual((self.dir / "images" / "a_1.jpg").read_bytes(), b"img")
        self.assertEqual((self.dir / "a.jpg").read_bytes(), b"img")

    def test_r6_missing_folder(self):
        code, _, err = run_main([str(self.dir / "nope")])
        self.assertEqual(code, 1)
        self.assertIn("Folder not found", err)

    def test_r6_path_is_a_file(self):
        code, _, err = run_main([str(self.dir / "a.jpg")])
        self.assertEqual(code, 1)
        self.assertIn("Not a folder", err)


if __name__ == "__main__":
    unittest.main()
