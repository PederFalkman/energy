# Conforming to this contract

An implementation conforms by answering every case in `fixtures/` the way the
contract says, and by satisfying the structural requirements in
[`../contract/CONTRACT.md`](../contract/CONTRACT.md) §1 that a fixture cannot
observe from outside.

## What a fixture cannot check

`fixtures/advice/cases.json` asks whether an *instance* of the forbidden cell can
be constructed. It cannot see §1.1's shape requirements: that the cell be
**occupied by a named uninhabited type** rather than left absent, that the pair be
unreachable through any factory or type table, and that a **new** type be unable
to claim it.

Fixtures check behaviour; a reviewer checks shape. Each implementation therefore
also carries a local test asserting that declaring the forbidden pair fails at
class-definition/compile time, and that its lesson type has no numeric field.
Those cannot be expressed as shared JSON, and the contract says so rather than
pretending the fixture set is complete. The same applies to §5's
no-date-literal rule: a fixture cannot scan a module's source, so each
implementation asserts it locally.

## Emitting results

Write a JSON object mapping `case_id` to the answer:

```json
{
  "contract_version": "1.1.0",
  "implementation": "markets",
  "results": {
    "advice/client-instrument-FORBIDDEN": {"constructible": false},
    "admit/method-note": {"admitted": true, "reason": null, "stale": false},
    "narrative/in-bare-integer": {"refused": true}
  }
}
```

Extra keys are ignored; only the fields in `COMPARED` are compared. A case with
no result is a **failure**, not a skip.

## Running

```sh
python conformance/check.py --results results.json --name markets
```

Exit 0 on agreement, 1 otherwise.
