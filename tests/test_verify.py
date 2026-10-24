"""Exercise the real verification command in a disposable source archive."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class VerificationCommand(unittest.TestCase):
    def test_empty_test_directory_is_a_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "archive"
            (root / "tools").mkdir(parents=True)
            (root / "tests").mkdir()
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            tools = Path(__file__).resolve().parents[1] / "tools"
            for name in ("verify.py", "check_docs.py"):
                shutil.copyfile(tools / name, root / "tools" / name)

            result = subprocess.run(
                [sys.executable, str(root / "tools" / "verify.py")],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no tests", result.stderr.lower())
        self.assertNotIn("Verification passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
