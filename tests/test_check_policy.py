"""Behavior tests for optional inert policy-selection inspection."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'tools/check_policy.py'
MANIFEST = '''schema_version = 1

[[modules]]
id = "execution"
path = "execution.md"
owner = "fictional-owner"

[[modules]]
id = "verification"
path = "verification.md"
owner = "fictional-owner"
requires = ["execution"]
conflicts = ["unselected-experimental"]
'''
EXCEPTION = '''
[[exceptions]]
id = "temporary-source"
path = "exception.md"
modules = ["verification"]
expires_on = 2030-01-01
ends_when = "private event description must not appear in report"
'''


class PolicySelection(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.project = self.root / 'project'
        self.project.mkdir()
        for name in ('execution.md', 'verification.md', 'exception.md'):
            (self.project / name).write_text('# Fictional inert policy\nPrivate prose stays here.\n')
        self.manifest = self.project / 'policy.toml'
        self.manifest.write_text(MANIFEST)

    def run_check(self, expected=0, manifest='policy.toml', as_of='2029-01-01', script=SCRIPT):
        result = subprocess.run(
            [sys.executable, '-B', str(script), '--root', str(self.project),
             '--manifest', manifest, '--as-of', as_of],
            cwd=self.root, capture_output=True, text=True, check=False, timeout=10)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, '')
        report = json.loads(result.stdout)
        self.assertNotIn(str(self.root), result.stdout)
        self.assertNotIn('Private prose', result.stdout)
        self.assertNotIn('private event description', result.stdout)
        for key in ('policy_conformance', 'selection_authority', 'execution_authority'):
            self.assertEqual(report[key], 'unverified')
        return report

    def codes(self, report):
        return {item['code'] for item in report['errors']}

    def test_valid_selection_and_unselected_conflict(self):
        report = self.run_check()
        self.assertEqual(report['errors'], [])
        self.assertEqual([m['id'] for m in report['modules']], ['execution', 'verification'])
        self.assertEqual(report['modules'][1]['requires'], ['execution'])
        self.assertTrue(report['limits'])

    def test_empty_selection_is_explicit_and_optional(self):
        self.manifest.write_text('schema_version = 1\nmodules = []\n')
        self.assertEqual(self.run_check()['modules'], [])

    def test_read_only_deterministic_and_standalone_copy(self):
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.project.iterdir()}
        first = self.run_check()
        second = self.run_check()
        self.assertEqual(first, second)
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                                  for p in self.project.iterdir()})
        copied = self.root / 'standalone.py'
        shutil.copyfile(SCRIPT, copied)
        self.assertEqual(first, self.run_check(script=copied))

    def test_duplicate_or_invalid_ids_and_owner(self):
        for text in (MANIFEST + '\n[[modules]]\nid="execution"\npath="execution.md"\nowner="owner"\n',
                     MANIFEST.replace('id = "execution"', 'id = "../private"'),
                     MANIFEST.replace('owner = "fictional-owner"', 'owner = ""')):
            with self.subTest(text=text):
                self.manifest.write_text(text)
                self.assertTrue(self.codes(self.run_check(1)) & {'duplicate_id', 'invalid_module'})

    def test_missing_dependency_and_selected_conflict(self):
        self.manifest.write_text(MANIFEST.replace('requires = ["execution"]', 'requires = ["missing"]'))
        self.assertIn('missing_dependency', self.codes(self.run_check(1)))
        self.manifest.write_text(MANIFEST.replace('conflicts = ["unselected-experimental"]', 'conflicts = ["execution"]'))
        self.assertIn('selected_conflict', self.codes(self.run_check(1)))

    def test_dependency_cycles_and_self_cycle(self):
        for addition in ('requires = ["verification"]\n', 'requires = ["execution"]\n'):
            self.manifest.write_text(MANIFEST.replace('path = "execution.md"', addition + 'path = "execution.md"'))
            self.assertIn('dependency_cycle', self.codes(self.run_check(1)))

    def test_unknown_keys_invalid_types_and_duplicate_lists(self):
        variants = (MANIFEST.replace('schema_version = 1', 'schema_version = true'),
                    MANIFEST + '\n[unexpected]\nvalue = "not echoed"\n',
                    'schema_version=1\nmodules="invalid"\n',
                    MANIFEST.replace('requires = ["execution"]', 'requires = ["execution", "execution"]'),
                    MANIFEST.replace('requires = ["execution"]', 'requires = [3]'),
                    MANIFEST.replace('owner = "fictional-owner"', 'owner = false'))
        for text in variants:
            with self.subTest(text=text):
                self.manifest.write_text(text)
                self.assertTrue(self.codes(self.run_check(1)) & {'invalid_manifest', 'invalid_module'})

    def test_safe_paths_and_missing_file(self):
        for path in ('../outside.md', '/private/outside.md', 'C:/private.md',
                     'folder\\\\outside.md', './execution.md', 'folder//execution.md',
                     'execution.md#anchor', 'execution.txt'):
            with self.subTest(path=path):
                self.manifest.write_text(MANIFEST.replace('path = "execution.md"', f'path = "{path}"'))
                self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        self.manifest.write_text(MANIFEST)
        (self.project / 'execution.md').unlink()
        self.assertIn('missing_reference', self.codes(self.run_check(1)))
        self.assertIn('unsafe_reference', self.codes(self.run_check(1, manifest='../policy.toml')))

    def test_symlinked_reference_directory_manifest_and_root(self):
        outside = self.root / 'outside.md'
        outside.write_text('sensitive outside prose')
        module = self.project / 'execution.md'
        module.unlink()
        module.symlink_to(outside)
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        module.unlink()
        module.write_text('# Inert\n')
        directory = self.project / 'linked'
        directory.symlink_to(self.root, target_is_directory=True)
        self.manifest.write_text(MANIFEST.replace('path = "execution.md"', 'path = "linked/outside.md"'))
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        self.manifest.unlink()
        self.manifest.symlink_to(outside)
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        self.manifest.unlink()
        self.manifest.write_text(MANIFEST)
        physical = self.project
        self.project = self.root / 'linked-root'
        self.project.symlink_to(physical, target_is_directory=True)
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))

    def test_root_parent_component_cannot_hide_a_symlink(self):
        elsewhere = self.root / 'elsewhere/child'
        elsewhere.mkdir(parents=True)
        linked = self.root / 'linked'
        linked.symlink_to(elsewhere, target_is_directory=True)
        original = self.project
        self.project = linked / '..' / 'project'
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        # Real parent components are checked physically and remain usable.
        self.project = original / '..' / 'project'
        self.assertEqual(self.run_check()['errors'], [])

    def test_date_expiry_is_inclusive_and_event_unverified(self):
        self.manifest.write_text(MANIFEST + EXCEPTION)
        for day in ('2029-01-01', '2030-01-01'):
            report = self.run_check(as_of=day)
            self.assertEqual(report['exceptions'][0]['expires_on'], '2030-01-01')
            self.assertEqual(report['exceptions'][0]['event_expiry'], 'unverified')
        self.assertIn('expired_exception', self.codes(self.run_check(1, as_of='2030-01-02')))
        self.manifest.write_text(MANIFEST + EXCEPTION.replace('expires_on = 2030-01-01\n', ''))
        self.assertEqual(self.run_check()['exceptions'][0]['event_expiry'], 'unverified')

    def test_invalid_and_ambiguous_exception_records(self):
        variants = (EXCEPTION.replace('modules = ["verification"]', 'modules = ["missing"]'),
                    EXCEPTION.replace('modules = ["verification"]', 'modules = []'),
                    EXCEPTION.replace('expires_on = 2030-01-01', 'expires_on = "2030-02-30"'),
                    EXCEPTION.replace('expires_on = 2030-01-01', 'expires_on = 2030-01-01T00:00:00Z'),
                    '[[exceptions]]\nid="no-end"\npath="exception.md"\nmodules=["execution"]\n',
                    EXCEPTION + EXCEPTION)
        for text in variants:
            with self.subTest(text=text):
                self.manifest.write_text(MANIFEST + text)
                self.assertTrue(self.codes(self.run_check(1)) & {'invalid_exception', 'unknown_exception_module', 'duplicate_id'})

    def test_malformed_toml_huge_integer_and_invalid_utf8(self):
        for data in (b'broken[', b'\xff', b'schema_version=' + b'7' * 5000):
            self.manifest.write_bytes(data)
            self.assertIn('invalid_manifest', self.codes(self.run_check(1)))

    def test_file_and_entry_bounds_and_special_files(self):
        self.manifest.write_bytes(b'x' * (64 * 1024 + 1))
        self.assertIn('input_too_large', self.codes(self.run_check(1)))
        self.manifest.write_text(MANIFEST)
        module = self.project / 'execution.md'
        module.write_bytes(b'x' * (256 * 1024 + 1))
        self.assertIn('input_too_large', self.codes(self.run_check(1)))
        module.unlink()
        os.mkfifo(module)
        self.assertIn('unsafe_reference', self.codes(self.run_check(1)))
        module.unlink()
        module.write_text('# Inert\n')
        many = '\n'.join(f'[[modules]]\nid="module{i}"\npath="execution.md"\nowner="owner"\n' for i in range(65))
        self.manifest.write_text('schema_version=1\n' + many)
        self.assertIn('invalid_manifest', self.codes(self.run_check(1)))

    def test_invalid_reference_utf8_and_unreadable_input(self):
        path = self.project / 'execution.md'
        path.write_bytes(b'\xff')
        self.assertIn('invalid_reference', self.codes(self.run_check(1)))
        path.write_text('# Inert\n')
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            self.skipTest('root can read mode-000 files')
        path.chmod(0)
        try:
            self.assertIn('unreadable_input', self.codes(self.run_check(1)))
        finally:
            path.chmod(0o600)

    def test_missing_manifest_is_a_failure(self):
        self.manifest.unlink()
        self.assertIn('missing_reference', self.codes(self.run_check(1)))

    def test_windows_game_fixture_has_three_compatible_modules(self):
        example = Path(__file__).resolve().parents[1] / 'examples/windows-game'
        self.project = self.root / 'windows-game'
        shutil.copytree(example, self.project)
        report = self.run_check()
        self.assertEqual(report['errors'], [])
        self.assertEqual([item['id'] for item in report['modules']],
                         ['execution', 'integration', 'verification'])
        self.assertEqual(report['exceptions'], [])

    def test_exception_string_date_unknown_keys_and_collection_bound(self):
        self.manifest.write_text(MANIFEST + EXCEPTION.replace('expires_on = 2030-01-01',
                                                            'expires_on = "2030-01-01"'))
        self.assertEqual(self.run_check()['exceptions'][0]['expires_on'], '2030-01-01')
        self.manifest.write_text(MANIFEST + EXCEPTION + 'unknown = true\n')
        self.assertIn('invalid_exception', self.codes(self.run_check(1)))
        many = ''.join(EXCEPTION.replace('temporary-source', f'exception{n}') for n in range(65))
        self.manifest.write_text(MANIFEST + many)
        self.assertIn('invalid_manifest', self.codes(self.run_check(1)))

    def test_cli_usage_and_bad_calendar_date(self):
        for args in ([], ['--root', str(self.project), '--manifest', 'policy.toml', '--as-of', '2030-02-30']):
            result = subprocess.run([sys.executable, '-B', str(SCRIPT), *args], cwd=self.root,
                                    capture_output=True, text=True, check=False, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertIn('usage:', result.stderr)


if __name__ == '__main__':
    unittest.main()
