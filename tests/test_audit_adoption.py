"""Exercise the optional CLI against synthetic, inert adoption fixtures."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


FILES = (
    'LICENSE', 'METHOD.md', 'docs/reference/documentation.md',
    'docs/reference/extensions.md', 'docs/reference/verification.md',
    'docs/reference/workflow.md', 'profiles/codex.md', 'profiles/github.md',
    'profiles/strict-test-first.md',
)
REVISION = 'a' * 40
REPOSITORY = 'https://github.com/gonz0w/agent-temper'
ROLE = '''name = "temper_product"
description = "Synthetic task"
model = "synthetic-model"
model_reasoning_effort = "medium"
developer_instructions = "Inert synthetic instructions"
'''
SCRIPT = Path(__file__).resolve().parents[1] / 'tools/audit_adoption.py'


class AdoptionAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'source'
        self.consumer = self.root / 'consumer'
        self.bundle = self.consumer / '.agent-temper'
        for name in FILES:
            for parent in (self.source, self.bundle):
                path = parent / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f'Synthetic {name}\n', encoding='utf-8')
        (self.bundle / 'SOURCE.md').write_text(
            f'# Source\n\nRepository: {REPOSITORY}\n\nRevision: `{REVISION}`\n',
            encoding='utf-8',
        )
        for path in (
            self.source / 'templates/codex/agents/temper_product.toml',
            self.consumer / '.codex/agents/temper_product.toml',
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(ROLE, encoding='utf-8')
        self.manifest()

    def manifest(self, include_source=False):
        names = FILES + (('SOURCE.md',) if include_source else ())
        (self.bundle / 'SHA256SUMS').write_text(''.join(
            f'{hashlib.sha256((self.bundle / name).read_bytes()).hexdigest()}  {name}\n'
            for name in sorted(names)
        ), encoding='utf-8')

    def run_audit(self, roles=(), expected=0, extra=()):
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPT), '--consumer', str(self.consumer),
             '--source', str(self.source), '--revision', REVISION,
             *[arg for role in roles for arg in ('--role', role)], *extra],
            cwd=self.root, capture_output=True, text=True, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, '')
        report = json.loads(result.stdout)
        self.assertNotIn(str(self.root), result.stdout)
        self.assertEqual(report['runtime_routing'], 'unverified')
        self.assertEqual(report['policy_conformance'], 'unverified')
        self.assertEqual(report['source_authenticity'], 'unverified')
        return report

    def codes(self, report):
        return {item['code'] for item in report['errors']}

    def test_complete_bundle_no_roles_and_source_manifest_variant(self):
        for include_source in (False, True):
            self.manifest(include_source)
            report = self.run_audit()
            self.assertEqual(report['errors'], [])
            self.assertEqual(report['roles'], [])
            self.assertEqual(report['bundle_files_compared'], 9)
            self.assertEqual(report['declared_revision'], REVISION)
            self.assertTrue(report['limits'])

    def test_selected_role_subset_and_overrides_are_observations(self):
        path = self.consumer / '.codex/agents/temper_product.toml'
        path.write_text(ROLE.replace('synthetic-model', 'local-model') + 'custom = true\n')
        # Unselected malformed files and policy must never be parsed.
        (path.parent / 'unselected.toml').write_text('malformed[')
        (self.consumer / 'PROJECT.md').write_bytes(b'\xff')
        report = self.run_audit(('temper_product',))
        role = report['roles'][0]
        self.assertEqual(role['model'], 'local-model')
        self.assertEqual(role['model_reasoning_effort'], 'medium')
        self.assertEqual(role['template_comparison'], 'customized')
        self.assertEqual(role['different_fields'], ['model'])
        self.assertTrue(role['additional_fields_changed'])
        self.assertNotIn('Inert synthetic instructions', json.dumps(report))

    def test_renamed_local_role_has_explicit_comparison_limit(self):
        path = self.consumer / '.codex/agents/local_product.toml'
        path.write_text(ROLE.replace('temper_product', 'local_product'))
        role = self.run_audit(('local_product',))['roles'][0]
        self.assertEqual(role['template_comparison'], 'unavailable')

    def test_renamed_role_without_source_template_directory(self):
        path = self.consumer / '.codex/agents/local_product.toml'
        path.write_text(ROLE.replace('temper_product', 'local_product'))
        shutil.rmtree(self.source / 'templates')
        self.assertEqual(self.run_audit(('local_product',))['roles'][0]['template_comparison'],
                         'unavailable')

    def test_copied_standalone_script(self):
        copied = self.root / 'standalone.py'
        shutil.copyfile(SCRIPT, copied)
        result = subprocess.run(
            [sys.executable, '-B', str(copied), '--consumer', str(self.consumer),
             '--source', str(self.source), '--revision', REVISION],
            cwd=self.root, capture_output=True, text=True, check=False, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['errors'], [])

    def test_matching_role_and_deterministic_read_only_run(self):
        def snapshot():
            return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                    for p in self.root.rglob('*') if p.is_file()}
        before = snapshot()
        first = self.run_audit(('temper_product',))
        second = self.run_audit(('temper_product',))
        self.assertEqual(first, second)
        self.assertEqual(first['roles'][0]['template_comparison'], 'matches')
        self.assertEqual(before, snapshot())

    def test_missing_and_unexpected_files(self):
        (self.bundle / 'METHOD.md').unlink()
        (self.bundle / 'private-unexpected-name').write_text('private content')
        report = self.run_audit(expected=1)
        self.assertTrue({'missing_file', 'unexpected_entry'} <= self.codes(report))
        self.assertNotIn('private-', json.dumps(report))

    def test_manifest_drift_and_rehashed_bundle_source_drift(self):
        (self.bundle / 'METHOD.md').write_text('changed')
        self.assertIn('digest_mismatch', self.codes(self.run_audit(expected=1)))
        self.manifest()
        report = self.run_audit(expected=1)
        self.assertIn('source_mismatch', self.codes(report))
        self.assertNotIn('digest_mismatch', self.codes(report))

    def test_manifest_rejects_paths_digests_duplicates_and_omissions(self):
        path = self.bundle / 'SHA256SUMS'
        original = path.read_text()
        bad_lines = (
            f'{"0" * 64}  ../outside', f'{"0" * 64}  /private/outside',
            f'{"0" * 64}  docs/../METHOD.md', f'{"0" * 64}  C:\\outside',
            'invalid  METHOD.md', f'{"0" * 64}  unknown',
        )
        for line in bad_lines:
            with self.subTest(line=line):
                path.write_text(original + line + '\n')
                self.assertIn('invalid_manifest', self.codes(self.run_audit(expected=1)))
        path.write_text(original + original.splitlines()[0] + '\n')
        self.assertIn('invalid_manifest', self.codes(self.run_audit(expected=1)))
        path.write_text('\n'.join(original.splitlines()[1:]) + '\n')
        self.assertIn('manifest_inventory', self.codes(self.run_audit(expected=1)))

    def test_provenance_wrong_ambiguous_or_malformed(self):
        path = self.bundle / 'SOURCE.md'
        original = path.read_text()
        for text in (original.replace(REVISION, 'b' * 40),
                     original + f'Revision: `{REVISION}`\n',
                     original.replace(REPOSITORY, 'https://example.invalid'),
                     'no source fields', original.replace(REVISION, 'short')):
            with self.subTest(text=text):
                path.write_text(text)
                self.assertIn('invalid_provenance', self.codes(self.run_audit(expected=1)))

    def test_role_errors_and_invalid_selected_names(self):
        path = self.consumer / '.codex/agents/temper_product.toml'
        for text in ('malformed[', ROLE.replace('temper_product', 'other'),
                     ROLE.replace('model = "synthetic-model"', 'model = 4'),
                     ROLE.replace('description = "Synthetic task"', 'description = ""')):
            with self.subTest(text=text):
                path.write_text(text)
                self.assertIn('invalid_role', self.codes(self.run_audit(('temper_product',), 1)))
        path.unlink()
        self.assertIn('missing_file', self.codes(self.run_audit(('temper_product',), 1)))
        self.assertIn('invalid_role_name', self.codes(self.run_audit(('../escape',), 1)))

    def test_symlinked_bundle_file_directory_and_root_are_rejected(self):
        target = self.root / 'outside'
        target.write_text('sensitive outside content')
        path = self.bundle / 'METHOD.md'
        path.unlink()
        path.symlink_to(target)
        report = self.run_audit(expected=1)
        self.assertIn('unsafe_path', self.codes(report))
        self.assertNotIn('sensitive', json.dumps(report))
        path.unlink()
        path.write_text('restored')
        shutil.rmtree(self.bundle / 'profiles')
        (self.bundle / 'profiles').symlink_to(self.source / 'profiles', target_is_directory=True)
        self.assertIn('unsafe_path', self.codes(self.run_audit(expected=1)))
        link = self.root / 'linked-consumer'
        link.symlink_to(self.consumer, target_is_directory=True)
        self.assertIn('unsafe_path', self.codes(self.run_audit(expected=1, extra=('--consumer', str(link)))))

    def test_source_and_role_symlinks_are_rejected(self):
        for path in (self.source / 'METHOD.md',
                     self.source / 'templates/codex/agents/temper_product.toml',
                     self.consumer / '.codex/agents/temper_product.toml'):
            original = path.read_bytes()
            path.unlink()
            path.symlink_to(self.bundle / 'LICENSE')
            with self.subTest(path=path.name):
                self.assertIn('unsafe_path', self.codes(self.run_audit(('temper_product',), 1)))
            path.unlink()
            path.write_bytes(original)

    def test_special_file_and_oversized_or_non_utf8_metadata(self):
        path = self.bundle / 'SHA256SUMS'
        for content in (b'\xff', b'x' * (1024 * 1024 + 1)):
            path.write_bytes(content)
            self.assertTrue(self.codes(self.run_audit(expected=1)) & {'invalid_text', 'file_too_large'})
        path.unlink()
        os.mkfifo(path)
        self.assertIn('unsafe_path', self.codes(self.run_audit(expected=1)))

    def test_missing_source_and_invalid_source_template(self):
        (self.source / 'LICENSE').unlink()
        self.assertIn('missing_file', self.codes(self.run_audit(expected=1)))
        (self.source / 'LICENSE').write_text('Synthetic LICENSE\n')
        (self.source / 'templates/codex/agents/temper_product.toml').write_text('bad[')
        self.assertIn('invalid_role', self.codes(self.run_audit(('temper_product',), 1)))

    def test_manifest_and_role_directory_symlinks_and_nonregular_source(self):
        path = self.bundle / 'SHA256SUMS'
        original = path.read_bytes()
        target = self.root / 'saved-manifest'
        target.write_bytes(original)
        path.unlink()
        path.symlink_to(target)
        self.assertIn('unsafe_path', self.codes(self.run_audit(expected=1)))
        path.unlink()
        path.write_bytes(original)
        shutil.rmtree(self.consumer / '.codex')
        (self.consumer / '.codex').symlink_to(self.source / 'templates/codex', target_is_directory=True)
        self.assertIn('unsafe_path', self.codes(self.run_audit(('temper_product',), 1)))
        source_file = self.source / 'LICENSE'
        source_file.unlink()
        source_file.mkdir()
        self.assertIn('unsafe_path', self.codes(self.run_audit(expected=1)))

    def test_inventory_and_role_count_bounds(self):
        for index in range(40):
            (self.bundle / f'extra{index}').write_text('x')
        self.assertIn('inventory_limit', self.codes(self.run_audit(expected=1)))
        for path in self.bundle.glob('extra*'):
            path.unlink()
        self.assertIn('invalid_role_name', self.codes(self.run_audit(('temper_product',) * 33, 1)))

    def test_cli_usage_failure(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT)],
                                cwd=self.root, capture_output=True, text=True,
                                check=False, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn('required', result.stderr)


    def test_inspected_file_permission_failure_is_reported(self):
        # A subprocess permission test is meaningful for an unprivileged test user.
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            self.skipTest('root can read mode-000 files')
        path = self.bundle / 'LICENSE'
        path.chmod(0)
        try:
            self.assertIn('unreadable_input', self.codes(self.run_audit(expected=1)))
        finally:
            path.chmod(0o600)


if __name__ == '__main__':
    unittest.main()
