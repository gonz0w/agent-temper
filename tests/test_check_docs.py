"""Acceptance tests for the offline documentation checks."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from check_docs import check_repository


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.fixture = tempfile.TemporaryDirectory()
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def check(self):
        return "\n".join(check_repository(self.root))

    def test_archive_without_git_accepts_existing_files_and_directories(self):
        self.write("README.md", "# Example\n\n[Guide](docs/guide.md#usage)\n[Docs](docs/)\n![Art](art.svg)\n")
        self.write("docs/guide.md", "# Guide\n\n## Usage\n")
        self.write("art.svg", "<svg/>\n")
        self.assertEqual(self.check(), "")

    def test_missing_file_and_heading_are_reported_with_source_location(self):
        self.write("README.md", "# Example\n\n[Missing](absent.md)\n[Heading](guide.md#absent)\n")
        self.write("guide.md", "# Guide\n")
        diagnostics = self.check()
        self.assertIn("README.md:3", diagnostics)
        self.assertIn("absent.md", diagnostics)
        self.assertIn("README.md:4", diagnostics)
        self.assertIn("#absent", diagnostics)

    def test_inline_markup_unicode_duplicate_headings_and_escaped_spaces(self):
        self.write("README.md", "# Example\n\n[Guide](docs/My%20Guide.md#use-code-and-emphasis)\n[Repeat](docs/My%20Guide.md#r%C3%A9sum%C3%A9-1)\n[Space](<docs/My Guide.md>)\n")
        self.write("docs/My Guide.md", "# Guide\n\n## Use `code` and *emphasis*\n\n## Résumé\n\n## Résumé\n")
        self.assertEqual(self.check(), "")

    def test_underscore_emphasis_does_not_change_heading_anchor(self):
        self.write("README.md", "# Example\n\n[Heading](#use-emphasis-and-file_name)\n\n## Use _emphasis_ and `file_name`\n")
        self.assertEqual(self.check(), "")

    def test_code_examples_do_not_create_links_or_headings(self):
        self.write("README.md", "# Example\n\n`[Missing](absent.md)`\n\n```markdown\n# Example heading\n[Missing](absent.md)\n```\n\n~~~text\n[Missing](absent.md)\n~~~\n")
        self.assertEqual(self.check(), "")

    def test_fences_must_close_with_same_character_and_sufficient_length(self):
        self.write("README.md", "# Example\n\n````text\n```\n~~~\n")
        self.assertIn("unclosed code fence", self.check())

    def test_one_h1_and_no_trailing_whitespace(self):
        self.write("README.md", "# Example\n\n# Second\nText  \n")
        diagnostics = self.check()
        self.assertIn("exactly one H1", diagnostics)
        self.assertIn("README.md:4", diagnostics)
        self.assertIn("trailing whitespace", diagnostics)

    def test_missing_h1_is_reported(self):
        self.write("README.md", "## Example\n")
        self.assertIn("exactly one H1", self.check())

    def test_placeholders_are_allowed_only_in_templates(self):
        self.write("README.md", "# Example\n\nProject {{PROJECT_NAME}}\n\n```text\n{{COMMAND}}\n```\n")
        self.write("templates/README.md", "# {{PROJECT_NAME}}\n")
        diagnostics = self.check()
        self.assertIn("README.md:3", diagnostics)
        self.assertIn("README.md:6", diagnostics)
        self.assertIn("unresolved placeholder", diagnostics)
        self.assertNotIn("templates/README.md:", diagnostics)

    def test_external_links_are_not_fetched(self):
        self.write("README.md", "# Example\n\n[Web](https://example.invalid/a#b)\n[Mail](mailto:team@example.invalid)\n")
        self.assertEqual(self.check(), "")

    def test_inline_destinations_accept_balanced_parentheses_and_titles(self):
        self.write("README.md", '# Example\n\n[Guide](guide(1).md "Read this")\n')
        self.write("guide(1).md", "# Guide\n")
        self.assertEqual(self.check(), "")

    def test_reference_links_require_conversion_to_supported_inline_form(self):
        self.write("README.md", "# Example\n\n[Guide][guide]\n\n[guide]: guide.md\n")
        self.assertIn("use inline links", self.check())

    def test_template_link_placeholders_are_allowed(self):
        self.write("templates/README.md", "# {{PROJECT_NAME}}\n\n[Guide]({{GUIDE_PATH}})\n")
        self.assertEqual(self.check(), "")

    def test_absolute_file_paths_and_outside_traversal_are_rejected(self):
        self.write("README.md", "# Example\n\n[Absolute](/etc/passwd)\n[File](file:///etc/passwd)\n[Outside](../private.md)\n[Windows](C:\\private\\file.md)\n[Encoded](%2Fetc%2Fpasswd)\n")
        diagnostics = self.check()
        for line in range(3, 8):
            self.assertIn(f"README.md:{line}", diagnostics)
        self.assertIn("outside repository", diagnostics)

    def test_parent_relative_link_inside_repository_is_allowed(self):
        self.write("README.md", "# Example\n")
        self.write("docs/guide.md", "# Guide\n\n[Home](../README.md#example)\n")
        self.assertEqual(self.check(), "")

    def test_link_paths_require_exact_directory_and_filename_case(self):
        self.write(
            "README.md",
            "# Example\n\n[Directory](Docs/Guide.md)\n[File](docs/guide.md)\n",
        )
        self.write("docs/Guide.md", "# Guide\n")
        diagnostics = self.check()
        self.assertIn("README.md:3", diagnostics)
        self.assertIn("README.md:4", diagnostics)
        self.assertIn("case", diagnostics)

    def test_symlink_escape_is_rejected_without_reading_external_target(self):
        with tempfile.TemporaryDirectory() as outside:
            private = Path(outside) / "private.md"
            private.write_bytes(b"\xff")
            (self.root / "linked.md").symlink_to(private)
            self.write("README.md", "# Example\n\n[Escape](linked.md#secret)\n")
            diagnostics = self.check()
        self.assertIn("README.md:3", diagnostics)
        self.assertIn("outside repository", diagnostics)

    def test_git_metadata_is_excluded(self):
        self.write("README.md", "# Example\n")
        self.write(".git/hidden.md", "no heading {{VALUE}}  \n")
        self.assertEqual(self.check(), "")


if __name__ == "__main__":
    unittest.main()
