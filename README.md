# Promptbeat Lite

Run local-first prompt and agent regression checks from JSON fixture files or suite folders.

For prompt engineers and agent builders who want a tiny CI gate before adopting a heavier eval platform.

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/suite --format junit --fail-under 100
```

## Why

Prompt and agent instruction changes often regress behavior before anyone notices. Full eval platforms are valuable, but many teams need a small, inspectable first gate that runs in any repo.

Promptbeat Lite is dependency-light, local-first, and CI-friendly. It accepts hand-written fixtures, golden files, and cases mined by `eval-case-miner`.

## Install

```bash
git clone https://github.com/alexzhu0/promptbeat-lite.git
cd promptbeat-lite
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/suite --format junit --fail-under 100
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --fail-under 100
```

Suite folder with golden files:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/suite --fail-under 100
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --format json
```

JUnit for CI:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/suite --format junit --fail-under 100
```

## CLI Reference

- `PYTHONPATH=src python3 -m promptbeat_lite --help`
- Main demo: `PYTHONPATH=src python3 -m promptbeat_lite examples/suite --format junit --fail-under 100`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- JSON fixture file and directory runner
- `must_contain`, `must_not_contain`, `must_equal`, and mined `expected` checks
- Golden file checks with `golden_file`
- Basic fixture schema validation
- Pass-rate summary
- JUnit output for CI systems
- Threshold exit code with `--fail-under`
- Compatible with eval-case-miner promptbeat output

## GitHub Actions

```yaml
- name: Prompt regression
  run: PYTHONPATH=src python3 -m promptbeat_lite examples/suite --format junit --fail-under 100
```

## API

The public Python surface is intentionally small:

```python
from promptbeat_lite.cli import run_suite
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

Star this if you want prompt regression tests that are simple enough to inspect in a pull request.

## Related Tools

- Feed it with `eval-case-miner` when real failures should become fixtures.
- Pair it with `prompt-drift-watch` to catch risky instruction edits before running the suite.
- Attach `agent-trace-summarizer` output when a regression comes from an agent run.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
