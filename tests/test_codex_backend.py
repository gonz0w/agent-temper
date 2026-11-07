"""Offline transport contracts; this suite never invokes Codex or a model."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'examples/decision-assistance'
sys.path.insert(0, str(SOURCE))
try:
    import advice
    import codex_backend
finally:
    sys.path.pop(0)

FAKE = '''#!PYTHON
import json,os,sys,time,signal
def stray_child():
 read_fd,write_fd=os.pipe()
 child=os.fork()
 if child==0:
  os.close(read_fd);signal.signal(signal.SIGTERM,signal.SIG_IGN)
  for fd in (0,1,2):os.close(fd)
  os.write(write_fd,b'ready');os.close(write_fd)
  time.sleep(5);os._exit(0)
 os.close(write_fd);os.read(read_fd,5);os.close(read_fd)
if '--version' in sys.argv:
 if os.environ.get('TEMPER_FAKE_MODE')=='version-child':stray_child()
 print('codex-cli fixture-v1');sys.exit(0)
if 'login' in sys.argv:
 if os.environ.get('TEMPER_FAKE_MODE')=='auth-child':stray_child()
 print('Logged in using '+os.environ.get('TEMPER_FAKE_AUTH','ChatGPT'));sys.exit(0)
mode=os.environ.get('TEMPER_FAKE_MODE','ok')
if mode=='timeout':time.sleep(5)
if mode=='flood':
 print('x'*200000);sys.exit(0)
if mode=='error':sys.exit(2)
payload=json.loads(sys.stdin.read().split('\\n\\n',1)[1])
if mode=='argv':
 assert '--ignore-user-config' in sys.argv
 assert '--sandbox' in sys.argv and 'read-only' in sys.argv
 for setting in ['forced_login_method="chatgpt"','approval_policy="never"','features.shell_tool=false','features.apps=false','features.view_image=false','web_search="disabled"','features.multi_agent=false']:
  assert setting in sys.argv,setting
 assert not any(k in os.environ for k in ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL'])
 assert not os.path.exists('PROJECT.md')
 assert os.path.isfile('AGENTS.md')
result={'request_key':payload['request_key'],'status':'ok','route':'inspect'}
if mode=='malformed':result={'unexpected':True}
if mode=='stale':result['request_key']='0'*64
if mode=='refused':result.update(status='refused',route=None)
if mode=='tool':print(json.dumps({'type':'item.completed','item':{'type':'command_execution'}}))
if mode=='missing':sys.exit(0)
path=sys.argv[sys.argv.index('--output-last-message')+1]
with open(path,'w') as f:json.dump(result,f)
print(json.dumps({'type':'thread.started','thread_id':'fictional'}))
print(json.dumps({'type':'turn.completed','usage':{'input_tokens':11,'cached_input_tokens':3,'output_tokens':5}}))
'''


class CodexTransport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='temper-fake-cli-')
        self.addCleanup(self.temp.cleanup)
        self.executable = Path(self.temp.name) / 'fictional-codex'
        self.executable.write_text(FAKE.replace('PYTHON', sys.executable))
        self.executable.chmod(0o700)
        from unittest.mock import patch
        self.env = patch.dict(os.environ, {'TEMPER_FAKE_MODE': 'ok', 'TEMPER_FAKE_AUTH': 'ChatGPT'})
        self.env.start(); self.addCleanup(self.env.stop)

    def backend(self, **kwargs):
        return codex_backend.CodexBackend(executable=str(self.executable), **kwargs)

    def request(self, backend, timeout_ms=2000):
        return advice.make_request({'summary': 'Fictional inspection'}, source_revisions={'fixture': 's1'},
            policy_revision='p1', rubric_revision='r1', criteria='Inspect only.', routes=['inspect','implement'],
            backend=backend.identity, timeout_ms=timeout_ms)

    def test_explicit_opt_in_is_required(self):
        backend = self.backend(); req = self.request(backend)
        self.assertEqual(advice.evaluate(req, backend)['reason'], 'unavailable')
        self.assertFalse(backend.last_run.get('inference_started', False))

    def test_cost_efficient_default_and_no_silent_escalation(self):
        backend = self.backend(allow_inference=True)
        self.assertEqual(backend.identity['model'], 'gpt-6-luna')
        self.assertEqual(backend.identity['config']['effort'], 'medium')
        stronger = self.backend(model='gpt-6-astra', effort='high')
        self.assertNotEqual(backend.identity, stronger.identity)
        self.assertEqual(advice.evaluate(self.request(stronger), backend)['reason'], 'backend-error')
        self.assertFalse(backend.last_run.get('inference_started', False))

    def test_successful_fake_cli_and_native_usage(self):
        backend = self.backend(allow_inference=True)
        result = advice.evaluate(self.request(backend), backend)
        self.assertEqual((result['status'], result['route']), ('ok','inspect'))
        self.assertEqual(result['observation']['usage']['input_tokens'], 11)
        self.assertIsNone(result['observation']['uncertainty'])
        self.assertTrue(backend.last_run['local_cleanup_confirmed'])

    def test_per_invocation_isolation_and_api_environment_removal(self):
        os.environ.update(TEMPER_FAKE_MODE='argv', OPENAI_API_KEY='fictional', CODEX_API_KEY='fictional', OPENAI_BASE_URL='https://example.invalid')
        backend = self.backend(allow_inference=True)
        self.assertEqual(advice.evaluate(self.request(backend), backend)['status'], 'ok')

    def test_api_auth_is_refused_before_inference(self):
        os.environ['TEMPER_FAKE_AUTH']='API key'
        backend=self.backend(allow_inference=True)
        self.assertEqual(advice.evaluate(self.request(backend), backend)['reason'], 'unavailable')
        self.assertFalse(backend.last_run.get('inference_started',False))

    def test_missing_cli_is_unavailable(self):
        backend=codex_backend.CodexBackend(executable=str(Path(self.temp.name)/'absent'),allow_inference=True)
        self.assertEqual(advice.evaluate(self.request(backend),backend)['reason'],'unavailable')

    def test_protocol_and_process_errors_stop_further_calls(self):
        for mode in ['malformed','stale','error','tool','missing','flood']:
            with self.subTest(mode=mode):
                os.environ['TEMPER_FAKE_MODE']=mode
                backend=self.backend(allow_inference=True);req=self.request(backend)
                self.assertEqual(advice.evaluate(req,backend)['status'],'fallback')
                self.assertTrue(backend.stopped)
                self.assertTrue(backend.last_run['local_cleanup_confirmed'])
                os.environ['TEMPER_FAKE_MODE']='ok'
                self.assertEqual(advice.evaluate(req,backend)['status'],'fallback')

    def test_timeout_is_bounded_and_stops_instance(self):
        os.environ['TEMPER_FAKE_MODE']='timeout'
        backend=self.backend(allow_inference=True);req=self.request(backend,timeout_ms=300)
        start=time.monotonic();result=advice.evaluate(req,backend)
        self.assertEqual(result['reason'],'timeout')
        self.assertLess(time.monotonic()-start,3)
        self.assertTrue(backend.stopped)
        self.assertTrue(backend.last_run['local_cleanup_confirmed'])

    def test_refusal_is_not_successful_advice(self):
        os.environ['TEMPER_FAKE_MODE']='refused'
        backend=self.backend(allow_inference=True)
        self.assertEqual(advice.evaluate(self.request(backend),backend)['reason'],'refused')

    def test_uncertain_preflight_cleanup_never_reaches_inference(self):
        for mode in ['version-child','auth-child']:
            with self.subTest(mode=mode):
                os.environ['TEMPER_FAKE_MODE']='ok'
                backend=self.backend(allow_inference=True);req=self.request(backend)
                os.environ['TEMPER_FAKE_MODE']=mode
                self.assertEqual(advice.evaluate(req,backend)['status'],'fallback')
                self.assertTrue(backend.stopped)
                self.assertFalse(backend.last_run.get('inference_started',False))

    def test_stopped_instance_rejects_subprocesses(self):
        backend=self.backend(allow_inference=True);backend.stopped=True
        with self.assertRaises(advice.BackendUnavailable):
            backend._run([str(self.executable),'--version'],deadline=time.monotonic()+1)

    def test_replay_does_not_call_cli_inference(self):
        backend=self.backend(allow_inference=True);req=self.request(backend)
        record=advice.evaluate(req,backend)
        os.environ['TEMPER_FAKE_MODE']='error'
        self.assertEqual(advice.evaluate(req,replay=record)['origin'],'replay')
        changed=copy.deepcopy(req);changed['policy_revision']='p2'
        self.assertEqual(advice.evaluate(changed,backend,replay=record)['reason'],'stale-record')


if __name__=='__main__':unittest.main()
