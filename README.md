# advisory-governance

The contract for advisory decision records, mechanical judges, and the lesson
admission gate — owned here, implemented by each producer.

Two implementations exist:

| Repo | Implementation |
|---|---|
| `markets` | `src/markets/decision/` |
| `ato-energy-platform` | `platform/shared/advisory_governance/` |

**Neither implementation depends on the other.** They depend on this contract,
which is the point: advice is not grid truth, and making `markets` import a
governance concern from `ato-energy-platform` would cut against the severability
rule those repos are built on. A shared contract is a dependency on a
specification; a cross-import is a dependency on someone else's release cycle.

## What is normative

- [`contract/CONTRACT.md`](contract/CONTRACT.md) — the rules, in prose. This is
  the document a regulator or assessor reads.
- [`schema/`](schema/) — JSON Schema for `Decision`, `Outcome`, `Lesson`.
- [`fixtures/`](fixtures/) — **the parity set.** Every implementation runs these
  and must produce identical decisions. A disagreement is a contract violation
  in one of them, and the fixture says which answer is correct.

## Running conformance

Each implementation emits a results file mapping `case_id` to its own answer,
then:

```sh
python conformance/check.py --results path/to/results.json
```

The checker is stdlib-only and language-neutral: an implementation in any
language conforms by producing the same JSON.

## Why this repo is not called `energy`

It was, and the name was wrong. A governance contract found in a repo called
`energy` reads as an energy library, and whoever finds it next would look for
grid code. What is here is the rule set for what advice may be constructed and
what may be learned from an outcome.
