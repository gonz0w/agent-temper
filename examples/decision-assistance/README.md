# Try optional decision assistance

Start with the offline example to exercise an adapter boundary without a model,
network connection, credential or installed package. It returns fixed fictional
advice. An optional Codex backend can classify supplied context after explicit
subscription-use selection. The existing lead-driven workflow remains the default;
neither path chooses real work or establishes productivity savings by itself.

The example uses Python 3.11+ and its standard library. No Agent Temper profile
activates it, and reading this page does not authorize inference or deployment.

## Run the fictional example

From the Agent Temper repository root, run:

```sh
python3 examples/decision-assistance/advice.py
```

The JSON array contains three results:

1. Fixed `inspect` advice with `status: ok` and `origin: fresh`.
2. The same recorded advice with `origin: replay`, without another backend call.
3. A `stale-record` fallback after a policy revision changes. Its route is
   `needs-review`; no replacement inference runs automatically.

The records are printed to stdout. The example does not write a cache or work
tracker. Do not put credentials, private source or personal information in a
request, backend configuration or saved result. Hashing identifies data; it does
not redact or authenticate it.

## Use the small interface

[advice.py](advice.py) exposes these operations:

| Operation | Result |
| --- | --- |
| `make_request(...)` | An owned JSON snapshot of evidence, identities, criteria, permitted routes and limits. Invalid construction raises `ValueError`. |
| `request_key(request)` | SHA-256 of the complete validated canonical JSON request. Object key order does not change the key. |
| `evaluate(request, backend)` | Mechanically validated advisory output, or a fallback to the lead. No action is dispatched. |
| `evaluate(request, replay=record)` | Reuse of matching successful recorded advice, labeled as replay. Invalid or stale records fall back without calling a backend. |
| `FakeBackend(route)` | A finite fixed-answer fixture with a call counter. It performs no inference. |

The version-1 request includes the evidence and its digest; source revisions;
policy and rubric revisions; criteria and permitted routes; backend/model/public
configuration identity; and response/deadline limits. These fields are ordinary
JSON, independent of any provider SDK. Callers must read canonical policy and
source before supplying their current identities. A matching key cannot establish
that an observation or permission is still current.

Fingerprinting uses this reference implementation's sorted, compact UTF-8 Python
JSON encoding. It is not an RFC 8785 implementation. Another language must share
the exact encoding or define a new versioned fingerprint contract; do not assume
that all JSON serializers produce the same bytes.

A backend is a trusted callable accepting `(request, deadline)`. The deadline is
an absolute value on the caller's monotonic clock. Its JSON answer contains
`request_key`, `status` and `route`, with optional `uncertainty` and `usage`.
Supported statuses are `ok`, `abstain` and `refused`. Only `ok` can carry a route;
the other statuses use `null`. The fake backend demonstrates this interface. The
separate Codex backend below uses the existing client; no local-model adapter is
included.

A successful record preserves the request key, source/policy/rubric/backend
provenance and available observations. `uncertainty` and `usage` are opaque,
provider-native JSON or `null` when unavailable. The example invents no confidence
value and compares no scores across providers. `latency_ms` measures the wrapper's
fresh callable execution, not whole-task effort. On replay, observations still
describe the recorded call; they are not fresh usage or latency measurements.

## Handle failures and replay deliberately

Only `status: ok` means the response passed these mechanical checks. It does not
establish that the advice is correct, that the named backend actually ran, or that
an action is permitted. The caller admits the backend and owns any evidence about
its actual configuration. Retain required tests, separate review and owner
decisions. Treat saved records as trusted evidence inputs; the fingerprint is not
a signature or a tamper-proof decision store.

| Condition | Fallback reason |
| --- | --- |
| Malformed request, mismatched evidence digest or exceeded input bound | `invalid-request` |
| No backend supplied | `unavailable` |
| Backend raises `BackendUnavailable` | `unavailable` |
| Backend raises an ordinary error | `backend-error` |
| Backend raises `TimeoutError`, or returns after the deadline | `timeout` |
| Backend changes its request snapshot | `request-mutated` |
| Malformed, stale, ambiguous or unsupported answer | `invalid-response` |
| Backend abstains or refuses | `abstained` or `refused` |
| Current request differs from the recorded request | `stale-record` |
| Failed or malformed recorded advice | `invalid-record` |

Fallback always returns `needs-review` to the existing lead. It grants no retry,
spending or permission. Backend exception text is excluded from result records.
Cancellation signals such as `KeyboardInterrupt` are not converted to advice.

Changing evidence, source, policy, rubric, criteria, permitted routes, backend,
model, public configuration or limits changes the replay key. Reuse only unchanged
identified inputs. Inspect new canonical information before requesting fresh
advice; do not automatically call a model because reuse failed.

## Understand the execution limits

This example accepts at most 32 KiB of canonical request JSON, 4 KiB of backend
response JSON and 12 levels of nesting. Its cooperative timeout is a positive
integer of at most 60,000 milliseconds. These are example limits, not mandatory
limits for the method or measured model requirements.

The wrapper rejects late answers but cannot interrupt a hung callable. A live
adapter must enforce transport timeouts, resource bounds, cancellation and cleanup
before a project admits it. Do not use this wrapper as a process sandbox, resource
monitor or authorization boundary. The fixed fake backend is finite and offline.

## Check, adopt or remove the example

From the repository root, run:

```sh
python3 tools/verify.py
```

The behavior tests cover fresh advice, exact replay, changed identities, malformed
and unsupported answers, refusal, abstention, unavailable/error/timeout outcomes,
request mutation, native observations and the runnable fictional example. Passing
these tests does not evaluate a model's routing quality or whole-task cost.

For optional adoption, review and pin the example with the project's own source,
verification and authority rules. Copying it activates no service. Stop using and
remove the copied example and any owned saved records when it no longer serves
the project; removing the example does not change the core Temper method.

A live invocation, model installation, credential setup, spending or automatic
routing needs the project's selected authority and evaluation. Use the existing
[workflow comparison procedure](../../docs/reference/verification.md#compare-agent-workflows)
to compare it with the simpler lead-driven baseline. No live adapter or consumer
rollout is activated by copying the example.

## Select the Codex subscription backend

[codex_backend.py](codex_backend.py) implements the callable contract with the
installed Codex CLI on POSIX hosts. It needs an existing permitted ChatGPT sign-in;
it provisions no API key and installs nothing. Its defaults are `gpt-6-luna` and
`medium` effort for small advisory questions. Use the lead directly for trivial
choices. See the [optional routing profile](../../profiles/codex.md) for stronger
implementation, analysis and review assignments.

Construct a backend and use its current `identity` as the request's `backend`
field. Reading that property checks CLI version metadata without inference. The
identity also binds effort, adapter bytes and the global instruction-file digest.
Then call `evaluate` as before. Only constructing with `allow_inference=True`
permits a fresh model request. A replay can use `evaluate(request, replay=record)`
without constructing a live backend.

For an explicitly approved invocation from the repository root:

```sh
python3 examples/decision-assistance/codex_backend.py request.json --allow-subscription-use
```

`request.json` must follow the contract above, including the current backend
identity. Run the command with `--help` to inspect supported model/effort choices.
Selecting `--model gpt-6.1-sol --effort high`, or an explicitly justified Astra
choice, requires a matching request identity and the project's authority. There
is no automatic stronger-model fallback.

Each call forces ChatGPT authentication and removes API-key/base-URL environment
overrides for its child. The worker receives a disposable context directory and
the supplied request. Personal client configuration is ignored for that invocation;
command execution, images, web search, connectors, plugins, shell snapshots,
permissions requests, memory use/generation, bundled skills, automatic skill
instructions and multi-agent work are disabled by explicit client settings. Managed requirements
and execpolicy rules remain applicable. No project files are copied or repository
checks/hook requirements disabled. Required canonical reading belongs to the lead
before it supplies evidence and identities.

The adapter requests schema-constrained output and then validates the actual JSON,
request binding, status and route. Missing answers, unexpected tool events,
invalid JSON, excess output, failed processes and timeouts fail back to the lead.
After a transport failure, the instance stops accepting fresh calls. Native CLI
usage, when present, is preserved without converting subscription tokens to money.
No calibrated confidence is invented. `last_run` contains local diagnostic metadata;
keep private account, usage and path information out of public issue reports.

Process time and aggregate stdout/stderr are bounded; an owned process group is
terminated on failure. Local cleanup cannot prove cancellation at the inference
provider or account for escaped descendants. An uncertain cleanup result stops
the instance and requires lead reconciliation before another attempt. The adapter
is an optional trusted-client wrapper, not an OS security boundary.

CLI arguments establish the requested model and effort. They are not independent
provider attestation. Effective managed policy, hidden provider context, usage
definitions and model availability remain client-dependent. Refresh the request
identity and admission when the client or applicable policy changes.

The tests use a fictional CLI executable; the offline demo still uses `FakeBackend`.
A real model call needs separate permitted execution and does not occur during
`verify.py`. Keep a finite quality/usage question and stopping rule before a pilot.
No local-model download or runtime startup is performed when Codex is unavailable.
