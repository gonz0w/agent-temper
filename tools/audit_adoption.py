#!/usr/bin/env python3
"""Optional inert-file adoption comparison; no policy or runtime qualification."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tomllib


BUNDLE_FILES = (
    'LICENSE', 'METHOD.md', 'docs/reference/documentation.md',
    'docs/reference/extensions.md', 'docs/reference/verification.md',
    'docs/reference/workflow.md', 'profiles/codex.md', 'profiles/github.md',
    'profiles/strict-test-first.md',
)
DIRECTORIES = {'docs', 'docs/reference', 'profiles'}
REPOSITORY = 'https://github.com/gonz0w/agent-temper'
FIELDS = ('name', 'description', 'developer_instructions', 'model',
          'model_reasoning_effort')
STANDARD_ROLES = {'temper_workflow', 'temper_product', 'temper_implementer',
                  'temper_analyst', 'temper_reviewer'}
MAX_BYTES = 1024 * 1024
MAX_ENTRIES = 32
NAME = re.compile(r'[a-zA-Z][a-zA-Z0-9_-]{0,63}\Z')
SETTING = re.compile(r'[a-zA-Z0-9][a-zA-Z0-9._:/-]{0,127}\Z')
MESSAGES = {
    'missing_file': 'Restore the required file or select the correct input copy.',
    'unexpected_entry': 'Inspect and reconcile unexpected bundle entries; names are withheld.',
    'unsafe_path': 'Use regular files and directories without symlinked inspected paths.',
    'unreadable_input': 'Check input availability and read permissions under local policy.',
    'file_too_large': 'Input exceeds the 1 MiB per-file limit.',
    'inventory_limit': 'Bundle directory exceeds the 32-entry inspection limit.',
    'invalid_text': 'Metadata must be valid UTF-8 text.',
    'invalid_manifest': 'Use one SHA-256 digest and exact allowed relative path per line.',
    'manifest_inventory': 'List all nine upstream files once; SOURCE.md is optional.',
    'digest_mismatch': 'File bytes differ from SHA256SUMS; investigate before updating.',
    'source_mismatch': 'Bundle bytes differ from the supplied source copy.',
    'invalid_provenance': 'Require one canonical Repository and one matching full Revision field.',
    'invalid_role_name': 'Select distinct role names matching letter then up to 63 letters, digits, _ or -.',
    'invalid_role': 'Check TOML, matching name, five nonempty string fields and model/effort identifiers.',
    'invalid_revision': 'Supply a full 40-character lowercase hexadecimal reviewed revision.',
}


class Audit:
    def __init__(self):
        self.errors = []

    def error(self, code, location, line=None):
        item = {'code': code, 'location': location, 'message': MESSAGES[code]}
        if line is not None:
            item['line'] = line
        if item not in self.errors:
            self.errors.append(item)

    def directory(self, path, location, optional=False):
        """Check all absolute path components without resolving symlinks."""
        try:
            for component in (*reversed(path.parents), path):
                mode = component.lstat().st_mode
                if not stat.S_ISDIR(mode):
                    self.error('unsafe_path', location)
                    return False
            return True
        except FileNotFoundError:
            if not optional:
                self.error('missing_file', location)
        except OSError:
            self.error('unreadable_input', location)
        return False

    def read(self, root, relative, location, optional=False):
        path = root / relative
        if not self.directory(path.parent, location, optional):
            return None
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode):
                self.error('unsafe_path', location)
                return None
            if info.st_size > MAX_BYTES:
                self.error('file_too_large', location)
                return None
            flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
            descriptor = os.open(path, flags)
            with os.fdopen(descriptor, 'rb') as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    self.error('unsafe_path', location)
                    return None
                data = stream.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                self.error('file_too_large', location)
                return None
            return data
        except FileNotFoundError:
            if not optional:
                self.error('missing_file', location)
        except OSError:
            self.error('unreadable_input', location)
        return None

    def text(self, data, location):
        if data is None:
            return None
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            self.error('invalid_text', location)
            return None

    def inventory(self, root, relative=''):
        location = 'bundle' + (f'/{relative}' if relative else '')
        if not self.directory(root / relative, location):
            return
        try:
            with os.scandir(root / relative) as entries:
                items = []
                for entry in entries:
                    if len(items) == MAX_ENTRIES:
                        self.error('inventory_limit', location)
                        break
                    items.append(entry.name)
            for name in sorted(items):
                child = f'{relative}/{name}' if relative else name
                if child in DIRECTORIES:
                    self.inventory(root, child)
                elif child in (*BUNDLE_FILES, 'SOURCE.md', 'SHA256SUMS'):
                    # The bounded read below checks regular-file type.
                    continue
                else:
                    self.error('unexpected_entry', location)
        except OSError:
            self.error('unreadable_input', location)

    def manifest(self, text):
        digests = {}
        if text is None:
            return digests
        for number, line in enumerate(text.splitlines(), 1):
            match = re.fullmatch(r'([0-9a-fA-F]{64}) [ *](.+)', line)
            if (not match or match[2] not in (*BUNDLE_FILES, 'SOURCE.md')
                    or match[2] in digests):
                self.error('invalid_manifest', 'bundle/SHA256SUMS', number)
                continue
            digests[match[2]] = match[1].lower()
        if set(digests) - {'SOURCE.md'} != set(BUNDLE_FILES):
            self.error('manifest_inventory', 'bundle/SHA256SUMS')
        return digests

    def provenance(self, text, revision):
        if text is None:
            return None
        fields = {}
        for line in text.splitlines():
            match = re.fullmatch(r'(?:- )?(Repository|Revision):\s*(.*?)\s*', line)
            if match:
                key, value = match.groups()
                if key in fields:
                    self.error('invalid_provenance', 'bundle/SOURCE.md')
                fields[key] = value
        declared = fields.get('Revision', '')
        if declared.startswith('`') and declared.endswith('`'):
            declared = declared[1:-1]
        repository = fields.get('Repository', '')
        if repository.startswith('`') and repository.endswith('`'):
            repository = repository[1:-1]
        if (repository != REPOSITORY or not re.fullmatch(r'[0-9a-f]{40}', declared)
                or declared != revision):
            self.error('invalid_provenance', 'bundle/SOURCE.md')
            return None
        return declared

    def role(self, root, relative, name, location, optional=False):
        data = self.text(self.read(root, relative, location, optional), location)
        if data is None:
            return None
        try:
            value = tomllib.loads(data)
        except (ValueError, RecursionError):
            self.error('invalid_role', location)
            return None
        if (any(not isinstance(value.get(key), str) or not value[key].strip()
                for key in FIELDS)
                or value['name'] != name
                or any(not SETTING.fullmatch(value[key])
                       for key in ('model', 'model_reasoning_effort'))):
            self.error('invalid_role', location)
            return None
        return value


def audit(consumer, source, revision, roles):
    check = Audit()
    report = {
        'schema_version': 1, 'bundle_files_compared': 0, 'declared_revision': None,
        'roles': [], 'runtime_routing': 'unverified', 'policy_conformance': 'unverified',
        'source_authenticity': 'unverified',
        'limits': [
            'Source bytes are caller-supplied; no Git identity, signature or trust verification.',
            'SOURCE.md Repository/Revision fields are declarations; other prose is not interpreted.',
            'Policy, profile selection, model availability, runtime routing and product behavior are not checked.',
            'Only explicitly selected roles are read; template differences may be intentional overrides.',
            'Inputs must remain unchanged during the audit; concurrent hostile filesystem changes are not supported.',
        ],
    }
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        check.error('invalid_revision', 'arguments')
    # Retain parents so physical checks see any symlink preceding a '..'.
    consumer = Path(consumer).absolute()
    source = Path(source).absolute()
    consumer_ok = check.directory(consumer, 'consumer')
    source_ok = check.directory(source, 'source')
    bundle = consumer / '.agent-temper'
    if consumer_ok and check.directory(bundle, 'bundle'):
        check.inventory(bundle)
        contents = {name: check.read(bundle, name, f'bundle/{name}')
                    for name in (*BUNDLE_FILES, 'SOURCE.md', 'SHA256SUMS')}
        manifest = check.manifest(check.text(contents['SHA256SUMS'], 'bundle/SHA256SUMS'))
        for name, digest in sorted(manifest.items()):
            data = contents[name]
            if data is not None and hashlib.sha256(data).hexdigest() != digest:
                check.error('digest_mismatch', f'bundle/{name}')
        report['declared_revision'] = check.provenance(
            check.text(contents['SOURCE.md'], 'bundle/SOURCE.md'), revision)
        if source_ok:
            for name in BUNDLE_FILES:
                upstream = check.read(source, name, f'source/{name}')
                if upstream is not None and contents[name] is not None:
                    report['bundle_files_compared'] += 1
                    if upstream != contents[name]:
                        check.error('source_mismatch', f'bundle/{name}')
    seen = set()
    if len(roles) > MAX_ENTRIES:
        check.error('invalid_role_name', 'arguments')
        roles = []
    for name in sorted(roles):
        if not NAME.fullmatch(name) or name in seen:
            check.error('invalid_role_name', 'arguments')
            continue
        seen.add(name)
        relative = f'.codex/agents/{name}.toml'
        local = check.role(consumer, relative, name, f'roles/{name}') if consumer_ok else None
        if local is None:
            continue
        observed = {key: local[key] for key in ('name', 'model', 'model_reasoning_effort')}
        observed.update(template_comparison='unavailable', different_fields=[],
                        additional_fields_changed=None)
        if source_ok:
            template = check.role(source, f'templates/codex/agents/{name}.toml', name,
                                  f'templates/{name}', optional=name not in STANDARD_ROLES)
            if template is not None:
                differences = [key for key in FIELDS if local[key] != template[key]]
                extra = {k: v for k, v in local.items() if k not in FIELDS}
                template_extra = {k: v for k, v in template.items() if k not in FIELDS}
                observed.update(
                    template_comparison='customized' if local != template else 'matches',
                    different_fields=sorted(differences),
                    additional_fields_changed=extra != template_extra,
                )
        report['roles'].append(observed)
    report['errors'] = sorted(check.errors, key=lambda item: (
        item['location'], item.get('line', 0), item['code']))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--consumer', required=True, help='Consumer root (inert file reads only)')
    parser.add_argument('--source', required=True, help='Trusted local source export/check-out root')
    parser.add_argument('--revision', required=True, help='Expected full reviewed upstream revision')
    parser.add_argument('--role', action='append', default=[], help='Explicit selected role; repeat, default none')
    args = parser.parse_args()
    result = audit(args.consumer, args.source, args.revision, args.role)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
