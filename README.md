# Deployment Config Checker

Validate mock service deployment settings, aggregate resource budgets, and local probe configuration.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m deployment_lab --help
python -m deployment_lab examples/sample.json
python -m deployment_lab --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Input requires exactly service, replicas, resources, and health. Service names use lowercase letters, digits, and hyphens. Replicas are 1–50; per-instance CPU requests are 1–16000 millis and memory is 16–131072 MB, with exercise-wide totals capped at 64000 millis and 524288 MB. Health configuration requires a simple absolute path, interval, shorter timeout, and failure threshold. The configured failure window is only interval times threshold, not a measured readiness result. No service, scheduler, container, network probe, or deployment is started.

## Learning focus

The modeled 2015–2016 progression into deployment configuration and health-check validation around the roadmap's paasta/container learning themes. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `deployment_lab/core.py`: validated parsing, storage, or state transitions.
- `deployment_lab/cli.py`: JSON command interface.
- `deployment_lab/generate_fixtures.py`: original deterministic validation cases.
- `deployment_lab/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 366 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
