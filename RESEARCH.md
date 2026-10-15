# Candidate brief and comparison — 15 October 2026

**User:** Streaming operators reviewing exported topic-partition bounds and consumer commits before an offset reset.

**Pain and smallest capability:** A negative-looking lag can hide a commit ahead of the captured end; retention can invalidate a previously committed next offset. Classify missing, retained-out and ahead-of-end commits, explain hypothetical reset starts and quantify requested skip/replay offset distances.

**Acceptance criteria:** Start/end boundaries are valid; retention gaps and ahead-of-end commits are distinguished; missing commits with reset=none stay unknown; requested moves identify skip/replay; duplicate partitions and booleans as offsets fail.

**Demand evidence:** Inferred operator/developer need, not a verified customer request. Current upstream READMEs, relevant docs/code and accessible issues were inspected. Issue titles below provide context about maintenance and operational work; they are not presented as requests for this tool. No claimed competitor absence is inferred from a successful example here.

**Discovery path:** Accurate repository description/topics, a runnable captured-input example and this evidence file; discoverable by `kafka; kafka monitoring` and the task-specific terms. No unsolicited outreach or activity manipulation.

## Relevant established alternatives found

Live GitHub searches used Most stars ordering; exact queries/URLs/observations are in research-provenance.json. Highest-star relevant comparable found for this bounded workflow: `apache/kafka`. Broader collections, tutorials, proxies or unrelated applications in broad results were excluded by relevance; this is not an exhaustive global ranking. Focused invoice-rounding and matrix queries were sparse and broader established tools were retained transparently.

| Comparable | Stars observed | Latest push observed | Archived | API license classification |
| --- | ---: | --- | --- | --- |
| [apache/kafka](https://github.com/apache/kafka) | 33954 | 2026-10-15T03:59:18Z | False | Apache-2.0 |
| [linkedin/Burrow](https://github.com/linkedin/Burrow) | 3965 | 2026-08-21T16:01:43Z | False | Apache-2.0 |
| [tchiotludo/akhq](https://github.com/tchiotludo/akhq) | 3860 | 2026-10-13T09:26:43Z | False | Apache-2.0 |

Observations are dated in research-provenance.json, including README blob hashes and accessible issue links. NOASSERTION means the API did not classify the license; upstream terms must be read before reuse. No upstream source was incorporated.

Kafka is the streaming platform; Burrow is a consumer-lag monitoring service; AKHQ provides a Kafka management GUI. This file-only preflight trades live monitoring and management for an explicit captured-input explanation. No claim that those alternatives lack offline exports or equivalent analysis. Kafka official consumer documentation defines commits as next positions; leader epochs and broker state remain outside this tool.

Installation and first-use paths were inspected in current documentation, not benchmarked. These alternatives provide broader workflows, operational reliability features, docs/examples and support communities. This tool offers a bounded file/JSON contract, explicit failure modes and runnable fixtures but lacks their broader product capabilities, adoption evidence and maintenance history. Our build/install example measures only our behavior. Competitor installs, time-to-first-result, reliability and technical performance were not measured; no superiority claim or numerical performance comparison is made. Stars inform discovery, not quality or speed.

## Portfolio and candidate distinctness

Distinct from eventbus-ts (in-process messaging), jsonl-seek (file lookup), retryback and traceweave: this reviews Kafka topic-partition recovery positions, not event delivery implementation or agent traces.

All 178 owned repository identities/descriptions and the current project index were compared. Related release-asset-matrix, table-reconcile, sqlite-rehearsal and traceweave READMEs were inspected. The five candidates have separate users/contracts: backup dependency preservation, Kafka recovery positions, tax allocation arithmetic, span ancestry/interval coverage and CI matrix inclusion provenance. They are independent tools, not renamed/forked/subdivided versions of one product. Shared JSON CLI and packaging scaffolding does not substitute for their distinct algorithms and tests.
