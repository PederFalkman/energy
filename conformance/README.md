# Conforming to this contract

An implementation conforms by answering every case in `fixtures/` the way the
contract says, and by satisfying the structural requirements in
[`../contract/CONTRACT.md`](../contract/CONTRACT.md) §1 that a fixture cannot
observe from outside.

## What a fixture cannot check

`fixtures/advice/cases.json` asks whether the forbidden cell is constructible.
An implementation could answer `false` by catching an exception at call time and
still be **non-conformant**, because §1.1 requires that no type exists.

Fixtures check behaviour; a reviewer checks shape. Each implementation therefore
also carries a local test asserting that declaring the forbidden pair fails at
class-definition/compile time, and that its lesson type has no numeric field.
Those cannot be expressed as shared JSON, and the contract says so rather than
pretending the fixture set is complete.

## Emitting results

Write a JSON object mapping `case_id` to the answer:

```json
{
  "contract_version": "1.0.0",
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
