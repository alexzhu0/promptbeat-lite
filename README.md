# Promptbeat Lite

Run lightweight prompt regression checks from JSON fixtures.

## Why

Prompt changes need cheap regression checks before teams invest in a heavier eval platform.

This is a flagship HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/promptbeat-lite.git
cd promptbeat-lite
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --fail-under 100
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --fail-under 100
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m promptbeat_lite --help`
- Main demo: `PYTHONPATH=src python3 -m promptbeat_lite examples/cases.json --fail-under 100`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- JSON fixture runner
- `must_contain`, `must_not_contain`, `must_equal`, and mined `expected` checks
- Pass-rate summary
- JUnit output for CI systems
- Threshold exit code with `--fail-under`
- Compatible with eval-case-miner promptbeat output

## API

The public Python surface is intentionally small:

```python
from promptbeat_lite.cli import run_suite
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It gives prompt engineers a tiny regression runner that fits in any repo.

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
