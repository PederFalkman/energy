#!/usr/bin/env python3
"""
Conformance checker: does an implementation agree with the contract?

Each implementation runs the fixture set in `fixtures/` and writes a results
file mapping `case_id` to its own answer. This compares that to what the
contract says the answer is.

Language-neutral on purpose. The fixtures and the results are JSON, so an
implementation in any language conforms by producing the same JSON — nothing
here imports either implementation, and neither implementation imports this.

    python conformance/check.py --results results.json [--fixtures DIR]

Exit status is 0 on full agreement and 1 otherwise, so CI in each repo can call
it directly.

A MISSING case is a failure, not a skip. An implementation that silently omits
the forbidden-advice case would otherwise pass by not answering.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple

FIXTURE_FILES = ("advice/cases.json", "admission/cases.json", "narrative/cases.json")

# Compared per fixture kind. Only these keys matter; an implementation may
# report extra detail (timings, messages) without failing conformance.
COMPARED: Dict[str, Tuple[str, ...]] = {
    "advice_constructibility": ("constructible",),
    "lesson_admission": ("admitted", "reason"),
    "narrative_seam": ("refused",),
}
# Compared only when the fixture states an expectation for it.
OPTIONAL: Dict[str, Tuple[str, ...]] = {"lesson_admission": ("stale",)}


def load_fixtures(root: pathlib.Path) -> List[Dict[str, Any]]:
    cases = []
    for rel in FIXTURE_FILES:
        path = root / rel
        if not path.exists():
            raise SystemExit(f"missing fixture file: {path}")
        doc = json.loads(path.read_text())
        for c in doc["cases"]:
            cases.append({"kind": doc["kind"], **c})
    return cases


def check(cases: List[Dict[str, Any]], results: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for case in cases:
        cid = case["case_id"]
        kind = case["kind"]
        expected = case["expected"]
        got = results.get(cid)
        if got is None:
            failures.append(
                f"{cid}: NO RESULT REPORTED. A case the implementation did not "
                f"answer is a failure, not a skip — otherwise omitting the "
                f"forbidden-advice case would pass conformance.")
            continue
        keys = list(COMPARED[kind])
        keys += [k for k in OPTIONAL.get(kind, ()) if k in expected]
        for key in keys:
            if key not in expected:
                continue
            want, have = expected[key], got.get(key)
            if want != have:
                failures.append(
                    f"{cid}: {key} expected {want!r}, got {have!r}"
                    + (f"  ({case['note']})" if "note" in case else ""))
    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--fixtures", default=str(pathlib.Path(__file__).parent.parent / "fixtures"))
    ap.add_argument("--name", default="implementation")
    args = ap.parse_args()

    cases = load_fixtures(pathlib.Path(args.fixtures))
    results = json.loads(pathlib.Path(args.results).read_text())
    if isinstance(results, dict) and "results" in results:
        results = results["results"]

    failures = check(cases, results)
    if failures:
        print(f"CONFORMANCE FAILED — {args.name} disagrees with the contract "
              f"on {len(failures)} of {len(cases)} cases:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"conformance OK — {args.name} agrees with the contract on all "
          f"{len(cases)} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
