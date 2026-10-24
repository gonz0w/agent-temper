#!/usr/bin/env python3
"""Run the same offline checks locally and in CI, including from an archive."""

from pathlib import Path
import sys
import unittest

from check_docs import check_repository


def main():
    if sys.version_info < (3, 11):
        print("Python 3.11 or newer is required.", file=sys.stderr)
        return 1
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(str(root / "tests"))
    if suite.countTestCases() == 0:
        print("Verification failed: no tests were discovered.", file=sys.stderr)
        return 1
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    diagnostics = check_repository(root)
    for diagnostic in diagnostics:
        print(diagnostic, file=sys.stderr)
    if not result.wasSuccessful() or diagnostics:
        print("Verification failed.", file=sys.stderr)
        return 1
    print("Verification passed: tests and offline documentation checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
