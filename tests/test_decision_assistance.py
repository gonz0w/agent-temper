"""Behavior contracts for the optional fictional decision-assistance example."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'examples/decision-assistance/advice.py'
spec = importlib.util.spec_from_file_location('decision_advice', MODULE)
advice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(advice)


def request(**changes):
    fields = dict(source_revisions={'fictional': 's1'}, policy_revision='p1',
                  rubric_revision='r1', criteria='Choose a permitted advisory route.',
                  routes=['inspect', 'implement', 'investigate'],
                  backend={'id': 'fake', 'model': 'fixed-v1', 'config': {}}, timeout_ms=1000)
    fields.update(changes)
    return advice.make_request({'summary': 'Fictional work item'}, **fields)


class DecisionAssistance(unittest.TestCase):
    def test_fresh_advice_is_bound_and_does_not_invent_uncertainty(self):
        req = request(); backend = advice.FakeBackend('inspect')
        result = advice.evaluate(req, backend)
        self.assertEqual((result['status'], result['route'], result['origin']), ('ok', 'inspect', 'fresh'))
        self.assertEqual(result['request_key'], advice.request_key(req))
        self.assertEqual(result['provenance']['policy_revision'], 'p1')
        self.assertIsNone(result['observation']['uncertainty'])
        self.assertIsNone(result['observation']['usage'])
        self.assertEqual(backend.calls, 1)

    def test_exact_replay_needs_no_backend_and_is_labeled(self):
        req = request(); backend = advice.FakeBackend('inspect')
        record = advice.evaluate(req, backend)
        replay = advice.evaluate(copy.deepcopy(req), None, replay=record)
        self.assertEqual((replay['status'], replay['origin']), ('ok', 'replay'))
        self.assertEqual(replay['observation'], record['observation'])
        self.assertEqual(backend.calls, 1)
        self.assertEqual(record['origin'], 'fresh')

    def test_each_changed_input_invalidates_replay_without_inference(self):
        req = request(); record = advice.evaluate(req, advice.FakeBackend('inspect'))
        changes = [request(source_revisions={'fictional': 's2'}), request(policy_revision='p2'),
                   request(rubric_revision='r2'), request(criteria='Changed criteria.'),
                   request(routes=['inspect', 'investigate']),
                   request(backend={'id': 'different', 'model': 'fixed-v1', 'config': {}}),
                   request(backend={'id': 'fake', 'model': 'fixed-v2', 'config': {}}),
                   request(backend={'id': 'fake', 'model': 'fixed-v1', 'config': {'mode': 'other'}}),
                   request(timeout_ms=500)]
        changed_evidence = copy.deepcopy(req)
        changed_evidence['evidence'] = {'summary': 'Another fictional work item'}
        changed_evidence['input_digest'] = advice.digest(changed_evidence['evidence'])
        changes.append(changed_evidence)
        for changed in changes:
            with self.subTest(changed=changed):
                backend = advice.FakeBackend('implement')
                result = advice.evaluate(changed, backend, replay=record)
                self.assertEqual((result['status'], result['reason'], result['route']),
                                 ('fallback', 'stale-record', 'needs-review'))
                self.assertEqual(backend.calls, 0)

    def test_malformed_request_fails_before_backend(self):
        for alter in [lambda r: r.update(policy_revision=''),
                      lambda r: r.update(contract_version=True),
                      lambda r: r['limits'].update(timeout_ms=True),
                      lambda r: r.update(input_digest='0' * 64),
                      lambda r: r.update(routes=['inspect', 'inspect']),
                      lambda r: r.update(extra='unrecognized'),
                      lambda r: r.update(evidence={'bad': float('nan')}),
                      lambda r: r['backend'].update(config={1: 'not a string key'})]:
            req = request(); alter(req); backend = advice.FakeBackend('inspect')
            self.assertEqual(advice.evaluate(req, backend)['reason'], 'invalid-request')
            self.assertEqual(backend.calls, 0)
        with self.assertRaises(ValueError):
            request(policy_revision='')

    def test_unsupported_stale_and_malformed_answers_fall_back(self):
        req = request()
        replies = [None, {'request_key': advice.request_key(req), 'status': 'ok', 'route': 'deploy'},
                   {'request_key': '0' * 64, 'status': 'ok', 'route': 'inspect'},
                   {'request_key': advice.request_key(req), 'status': 'maybe', 'route': 'inspect'},
                   {'request_key': advice.request_key(req), 'status': 'ok', 'route': 'inspect', 'extra': True}]
        for reply in replies:
            result = advice.evaluate(req, lambda *_: reply)
            self.assertEqual((result['status'], result['reason']), ('fallback', 'invalid-response'))

    def test_refusal_and_abstention_do_not_become_advice(self):
        for status, reason in [('refused', 'refused'), ('abstain', 'abstained')]:
            result = advice.evaluate(request(), advice.FakeBackend(None, status=status))
            self.assertEqual((result['status'], result['reason'], result['route']),
                             ('fallback', reason, 'needs-review'))

    def test_unavailable_error_and_timeout_are_distinct(self):
        req = request()
        self.assertEqual(advice.evaluate(req, None)['reason'], 'unavailable')
        def expired(*_): raise TimeoutError('private details')
        def broken(*_): raise RuntimeError('private details')
        self.assertEqual(advice.evaluate(req, expired)['reason'], 'timeout')
        result = advice.evaluate(req, broken)
        self.assertEqual(result['reason'], 'backend-error')
        self.assertNotIn('private details', str(result))
        times = iter([0.0, 1.001])
        self.assertEqual(advice.evaluate(req, advice.FakeBackend('inspect'), clock=lambda: next(times))['reason'], 'timeout')

    def test_backend_cannot_mutate_bound_request(self):
        req = request(); original = copy.deepcopy(req)
        def mutate(inner, _):
            inner['policy_revision'] = 'p2'
            return {'request_key': advice.request_key(inner), 'status': 'ok', 'route': 'inspect'}
        self.assertEqual(advice.evaluate(req, mutate)['reason'], 'request-mutated')
        self.assertEqual(req, original)

    def test_native_observations_are_preserved_without_comparison(self):
        req = request()
        def backend(inner, _):
            return {'request_key': advice.request_key(inner), 'status': 'ok', 'route': 'inspect',
                    'uncertainty': {'provider_score': 0.7, 'scale': 'fictional'}, 'usage': {'units': 3}}
        result = advice.evaluate(req, backend)
        self.assertEqual(result['observation']['uncertainty'], {'provider_score': 0.7, 'scale': 'fictional'})
        self.assertEqual(result['observation']['usage'], {'units': 3})

    def test_json_type_changes_cannot_evade_mutation_detection(self):
        for changed in [True, 1.0, float('nan'), object()]:
            req = request(backend={'id': 'fake', 'model': 'fixed-v1', 'config': {'value': 1}})
            original_key = advice.request_key(req)
            def mutate(inner, _, changed=changed):
                inner['backend']['config']['value'] = changed
                return {'request_key': original_key, 'status': 'ok', 'route': 'inspect'}
            with self.subTest(changed=changed):
                self.assertEqual(advice.evaluate(req, mutate)['reason'], 'request-mutated')

    def test_json_type_changes_in_recorded_provenance_are_rejected(self):
        req = request(backend={'id': 'fake', 'model': 'fixed-v1', 'config': {'value': 1}})
        record = advice.evaluate(req, advice.FakeBackend('inspect'))
        for changed in [True, 1.0]:
            forged = copy.deepcopy(record)
            forged['provenance']['backend']['config']['value'] = changed
            with self.subTest(changed=changed):
                self.assertEqual(advice.evaluate(req, replay=forged)['reason'], 'invalid-record')

    def test_replay_rejects_failed_forged_and_malformed_records(self):
        req = request(); record = advice.evaluate(req, advice.FakeBackend('inspect'))
        failed = advice.evaluate(req, None)
        forged = copy.deepcopy(record); forged['provenance']['policy_revision'] = 'p2'
        wrong_route = copy.deepcopy(record); wrong_route['route'] = 'deploy'
        for invalid in [failed, forged, wrong_route, {}, None]:
            if invalid is None: continue  # None means no replay was requested.
            backend = advice.FakeBackend('inspect')
            self.assertEqual(advice.evaluate(req, backend, replay=invalid)['status'], 'fallback')
            self.assertEqual(backend.calls, 0)

    def test_bounded_json_and_dictionary_order(self):
        req = request(); rearranged = dict(reversed(list(req.items())))
        self.assertEqual(advice.request_key(req), advice.request_key(rearranged))
        huge = request(); huge['evidence'] = 'x' * 40000; huge['input_digest'] = advice.digest(huge['evidence'])
        self.assertEqual(advice.evaluate(huge, advice.FakeBackend('inspect'))['reason'], 'invalid-request')
        def huge_reply(inner, _):
            return {'request_key': advice.request_key(inner), 'status': 'ok', 'route': 'inspect', 'uncertainty': 'x' * 5000}
        self.assertEqual(advice.evaluate(req, huge_reply)['reason'], 'invalid-response')

    def test_offline_demo_is_usable(self):
        result = subprocess.run([sys.executable, str(MODULE)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        import json
        demo = json.loads(result.stdout)
        self.assertEqual([x['origin'] for x in demo[:2]], ['fresh', 'replay'])
        self.assertEqual(demo[2]['reason'], 'stale-record')


if __name__ == '__main__':
    unittest.main()
