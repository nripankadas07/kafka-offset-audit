# kafka-offset-audit

Classify missing, retained-out and ahead-of-end commits, explain hypothetical reset starts and quantify requested skip/replay offset distances.

## User and task

Streaming operators reviewing exported topic-partition bounds and consumer commits before an offset reset. A negative-looking lag can hide a commit ahead of the captured end; retention can invalidate a previously committed next offset.

## Install and first useful result

Python 3.10+ and pip. Git source install; no external-registry release is claimed.

```sh
git clone https://github.com/nripankadas07/kafka-offset-audit.git
cd kafka-offset-audit
python -m venv .venv
# POSIX: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install .
kafka-offset-audit example.json
```

The example committed next offset 20 is within [12,27], with offset distance 7 to the supplied end and no reset required. The example is synthetic. JSON goes to stdout. Exit0 means analyzed with no review findings; exit 1 means review findings; exit 2 means malformed/unsupported input or an IO error. Differences explicitly labeled informational do not alone trigger exit 1. Help: `kafka-offset-audit --help`.

## Input contract

Required keys: reset (earliest/latest/none) and partitions. Each partition requires topic, partition, log_start, log_end, committed (nonnegative next offset or null); requested is optional. Bounds are inclusive valid next positions, so committed==log_end is valid. Topics plus partition ids are unique. Partition ids fit signed32-bit nonnegative range; offsets fit signed64-bit nonnegative range. Out-of-range/missing commits remain findings even when a hypothetical reset start can be calculated. requested outside captured bounds is rejected; a changed/unknown requested position needs review.

Every object rejects unknown keys. CLI input is UTF-8 JSON, read with a 2 MiB cap before parsing; duplicate keys/nonfinite values fail. Default arrays allow at most 512 entries, strings1..256 characters and nonnegative integers up to2^63-1 except where a tighter/different bound is documented. The example shows the complete input shape. JSON output includes the supplied identities; review it before sharing sensitive inputs.

## Validate

```sh
python -m unittest -v
python -m compileall -q kafka_offset_audit.py
python -m pip wheel --no-deps --wheel-dir dist .
python -m venv /tmp/kafka-offset-audit-installed
/tmp/kafka-offset-audit-installed/bin/python -m pip install --no-index --no-deps dist/*.whl
python test_installed_cli.py /tmp/kafka-offset-audit-installed/bin/python
```

The last commands show the Linux/POSIX path; use the equivalent Scripts/python.exe path on Windows. Remote configured CI uses Linux Python 3.10/3.12/3.14. [Validation](VALIDATION.md) records actual preparation checks and limits; a workflow configuration is not itself proof of a passing run.

## Scope and limitations

Captured JSON only; no broker connection, consumer reset, group-membership check, leader-epoch validation or transaction/isolation behavior. log_end is the caller-supplied end boundary. Offset distance is not a record count: compaction, gaps, control records and transactions matter. Nonatomic captures may be inconsistent. No data-loss or replay guarantee is implied.

No runtime third-party packages. Setuptools is a build dependency. Original implementation developed with AI assistance, MIT licensed; no competitor code, prose or branding copied. [Research](RESEARCH.md), [contribution](CONTRIBUTING.md), [support](SUPPORT.md) and [security](SECURITY.md) guidance are included.
