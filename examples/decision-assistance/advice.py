#!/usr/bin/env python3
"""Optional offline advisory contract and fictional fixed-answer backend.

No network, credentials, model, persistent cache or automatic actions are used.
A callable backend must enforce its own finite execution and cancellation.
"""

import copy
import hashlib
import json
import math
import time

VERSION = 1
MAX_REQUEST_BYTES = 32768
MAX_RESPONSE_BYTES = 4096
REQUEST_FIELDS = {'contract_version', 'evidence', 'input_digest', 'source_revisions',
                  'policy_revision', 'rubric_revision', 'criteria', 'routes', 'backend', 'limits'}
PROVENANCE_FIELDS = ('input_digest', 'source_revisions', 'policy_revision', 'rubric_revision', 'backend')
RECORD_FIELDS = {'contract_version', 'request_key', 'provenance', 'status', 'route',
                 'reason', 'origin', 'observation'}
OBSERVATION_FIELDS = {'uncertainty', 'usage', 'latency_ms'}


class BackendUnavailable(Exception):
    """The selected backend cannot run within the caller's current authority."""


def _json(value, limit=None):
    def check(item, depth=0):
        if depth > 12:
            raise ValueError('JSON nesting exceeds the example limit')
        if item is None or type(item) in (str, bool, int):
            return
        if type(item) is float and math.isfinite(item):
            return
        if type(item) is list:
            for child in item:
                check(child, depth + 1)
            return
        if type(item) is dict and all(type(key) is str for key in item):
            for child in item.values():
                check(child, depth + 1)
            return
        raise ValueError('Expected finite JSON values and string object keys')
    check(value)
    data = json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')
    if limit is not None and len(data) > limit:
        raise ValueError('JSON exceeds the example byte limit')
    return data


def digest(value):
    """Identify canonical JSON bytes; this is not authentication or redaction."""
    return hashlib.sha256(_json(value)).hexdigest()


def _text(value):
    return type(value) is str and bool(value.strip())


def _validate(request):
    _json(request, MAX_REQUEST_BYTES)
    if type(request) is not dict or set(request) != REQUEST_FIELDS:
        raise ValueError('Unexpected request fields')
    if type(request['contract_version']) is not int or request['contract_version'] != VERSION:
        raise ValueError('Unsupported contract version')
    for key in ('policy_revision', 'rubric_revision', 'criteria'):
        if not _text(request[key]):
            raise ValueError('Missing request identity or criteria')
    sources = request['source_revisions']
    if type(sources) is not dict or not sources or not all(_text(k) and _text(v) for k, v in sources.items()):
        raise ValueError('Missing source identities')
    routes = request['routes']
    if type(routes) is not list or not routes or not all(_text(r) for r in routes) or len(set(routes)) != len(routes):
        raise ValueError('Expected distinct permitted routes')
    backend = request['backend']
    if type(backend) is not dict or set(backend) != {'id', 'model', 'config'}:
        raise ValueError('Missing backend identity')
    if not _text(backend['id']) or not _text(backend['model']) or type(backend['config']) is not dict:
        raise ValueError('Invalid backend configuration')
    limits = request['limits']
    if type(limits) is not dict or set(limits) != {'timeout_ms', 'max_response_bytes'}:
        raise ValueError('Missing execution limits')
    if type(limits['timeout_ms']) is not int or not 0 < limits['timeout_ms'] <= 60000:
        raise ValueError('Invalid cooperative timeout')
    if type(limits['max_response_bytes']) is not int or not 0 < limits['max_response_bytes'] <= MAX_RESPONSE_BYTES:
        raise ValueError('Invalid response limit')
    if request['input_digest'] != digest(request['evidence']):
        raise ValueError('Evidence identity does not match')


def make_request(evidence, *, source_revisions, policy_revision, rubric_revision,
                 criteria, routes, backend, timeout_ms=1000):
    """Build an owned JSON snapshot; supply public configuration, never secrets."""
    request = dict(contract_version=VERSION, evidence=evidence, input_digest=digest(evidence),
                   source_revisions=source_revisions, policy_revision=policy_revision,
                   rubric_revision=rubric_revision, criteria=criteria, routes=routes,
                   backend=backend, limits={'timeout_ms': timeout_ms, 'max_response_bytes': MAX_RESPONSE_BYTES})
    _validate(request)
    return json.loads(_json(request))


def request_key(request):
    """Bind all request fields, including criteria, routes, configuration and limits."""
    _validate(request)
    return digest(request)


def _record(request, *, status='fallback', route='needs-review', reason,
            origin='none', uncertainty=None, usage=None, latency_ms=None):
    return dict(contract_version=VERSION,
                request_key=request_key(request) if request is not None else None,
                provenance={key: copy.deepcopy(request[key]) for key in PROVENANCE_FIELDS} if request is not None else None,
                status=status, route=route, reason=reason, origin=origin,
                observation={'uncertainty': uncertainty, 'usage': usage, 'latency_ms': latency_ms})


def _replay(request, record):
    try:
        _json(record, MAX_REQUEST_BYTES + MAX_RESPONSE_BYTES)
        if type(record) is not dict or set(record) != RECORD_FIELDS:
            raise ValueError('Malformed record')
        if record['request_key'] != request_key(request):
            return _record(request, reason='stale-record')
        expected = {key: request[key] for key in PROVENANCE_FIELDS}
        if (type(record['contract_version']) is not int or record['contract_version'] != VERSION
                or record['status'] != 'ok' or record['reason'] != 'advisory'
                or record['origin'] not in ('fresh', 'replay') or _json(record['provenance']) != _json(expected)
                or record['route'] not in request['routes']):
            raise ValueError('Invalid recorded advice')
        observation = record['observation']
        if type(observation) is not dict or set(observation) != OBSERVATION_FIELDS:
            raise ValueError('Invalid observations')
        latency = observation['latency_ms']
        if type(latency) not in (int, float) or not math.isfinite(latency) or latency < 0:
            raise ValueError('Invalid recorded latency')
        result = copy.deepcopy(record)
        result['origin'] = 'replay'
        return result
    except (ValueError, TypeError, KeyError, OverflowError):
        return _record(request, reason='invalid-record')


def evaluate(request, backend=None, *, replay=None, clock=time.monotonic):
    """Validate advisory results; never dispatch work or retry a backend.

    Replay failure returns to the lead without a fresh backend call. Deadlines
    are cooperative: late answers are rejected, but a hung callable cannot be
    interrupted here. A live adapter must supply transport timeout/cancellation.
    """
    try:
        _validate(request)
        request = json.loads(_json(request))
    except (ValueError, TypeError, KeyError, OverflowError):
        return _record(None, reason='invalid-request')
    if replay is not None:
        return _replay(request, replay)
    if backend is None:
        return _record(request, reason='unavailable')
    start = clock()
    deadline = start + request['limits']['timeout_ms'] / 1000
    inner = copy.deepcopy(request)
    try:
        response = backend(inner, deadline)
    except BackendUnavailable:
        return _record(request, reason='unavailable')
    except TimeoutError:
        return _record(request, reason='timeout', origin='fresh')
    except Exception:
        return _record(request, reason='backend-error', origin='fresh')
    elapsed = clock() - start
    if elapsed >= request['limits']['timeout_ms'] / 1000:
        return _record(request, reason='timeout', origin='fresh', latency_ms=elapsed * 1000)
    try:
        changed = _json(inner, MAX_REQUEST_BYTES) != _json(request)
    except (ValueError, TypeError, OverflowError):
        changed = True
    if changed:
        return _record(request, reason='request-mutated', origin='fresh', latency_ms=elapsed * 1000)
    try:
        _json(response, request['limits']['max_response_bytes'])
        allowed = {'request_key', 'status', 'route', 'uncertainty', 'usage'}
        if type(response) is not dict or not {'request_key', 'status', 'route'} <= set(response) <= allowed:
            raise ValueError('Malformed response')
        if response['request_key'] != request_key(request):
            raise ValueError('Stale response')
        status, route = response['status'], response['route']
        if status in ('abstain', 'refused') and route is None:
            return _record(request, reason='abstained' if status == 'abstain' else 'refused', origin='fresh', latency_ms=elapsed * 1000)
        if status != 'ok' or route not in request['routes']:
            raise ValueError('Unsupported answer')
        return _record(request, status='ok', route=route, reason='advisory', origin='fresh',
                       uncertainty=copy.deepcopy(response.get('uncertainty')),
                       usage=copy.deepcopy(response.get('usage')), latency_ms=elapsed * 1000)
    except (ValueError, TypeError, KeyError, OverflowError):
        return _record(request, reason='invalid-response', origin='fresh', latency_ms=elapsed * 1000)


class FakeBackend:
    """Return a fixed fictional answer; no language judgment or model is involved."""
    def __init__(self, route='inspect', *, status='ok'):
        self.route, self.status, self.calls = route, status, 0

    def __call__(self, request, deadline):
        self.calls += 1
        return {'request_key': request_key(request), 'status': self.status, 'route': self.route}


def main():
    request = make_request({'summary': 'Fictional documentation task'},
                           source_revisions={'fictional': 's1'}, policy_revision='p1',
                           rubric_revision='r1', criteria='Choose a permitted advisory route.',
                           routes=['inspect', 'implement', 'investigate'],
                           backend={'id': 'fake', 'model': 'fixed-v1', 'config': {}})
    fresh = evaluate(request, FakeBackend('inspect'))
    replayed = evaluate(request, replay=fresh)
    changed = copy.deepcopy(request)
    changed['policy_revision'] = 'p2'
    stale = evaluate(changed, replay=fresh)
    print(json.dumps([fresh, replayed, stale], indent=2))


if __name__ == '__main__':
    main()
