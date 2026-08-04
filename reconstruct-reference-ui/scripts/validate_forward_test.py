#!/usr/bin/env python3
"""Reject premature success claims for reference UI forward tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SEVERITIES = {"critical", "major", "moderate", "minor"}
STATUSES = {"pass", "fail", "blocked"}
EVIDENCE = {"observed", "inferred", "unavailable"}
GATE_CONTEXTS = {"delivery", "skill-preinstallation"}


def validate(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    gate_context = report.get("gate_context", "delivery")
    if gate_context not in GATE_CONTEXTS:
        errors.append(f"gate_context must be one of {sorted(GATE_CONTEXTS)}")
    if not report.get("reference"):
        errors.append("reference is required")
    if not report.get("target"):
        errors.append("target is required")

    captures = report.get("captures")
    if not isinstance(captures, list) or not captures:
        errors.append("at least one matched capture is required")
    else:
        for index, capture in enumerate(captures):
            prefix = f"captures[{index}]"
            if not capture.get("state"):
                errors.append(f"{prefix}.state is required")
            if not capture.get("reference") or not capture.get("implementation"):
                errors.append(f"{prefix} requires reference and implementation paths")
            if capture.get("dimensions_match") is not True:
                errors.append(f"{prefix} dimensions must match")
            if capture.get("reviewed") is not True:
                errors.append(f"{prefix} must be visually reviewed")

    interactions = report.get("interactions")
    if not isinstance(interactions, list) or not interactions:
        errors.append("at least one interaction result is required")
    else:
        for index, interaction in enumerate(interactions):
            prefix = f"interactions[{index}]"
            evidence = interaction.get("evidence")
            status = interaction.get("status")
            if evidence not in EVIDENCE:
                errors.append(f"{prefix}.evidence must be one of {sorted(EVIDENCE)}")
            if status not in STATUSES:
                errors.append(f"{prefix}.status must be one of {sorted(STATUSES)}")
            if interaction.get("primary") is True and (evidence != "observed" or status != "pass"):
                errors.append(f"{prefix} primary interaction must be observed and pass")

    discrepancies = report.get("discrepancies", [])
    if not isinstance(discrepancies, list):
        errors.append("discrepancies must be a list")
    else:
        for index, discrepancy in enumerate(discrepancies):
            prefix = f"discrepancies[{index}]"
            severity = discrepancy.get("severity")
            status = discrepancy.get("status")
            if severity not in SEVERITIES:
                errors.append(f"{prefix}.severity must be one of {sorted(SEVERITIES)}")
            if status not in {"open", "resolved"}:
                errors.append(f"{prefix}.status must be open or resolved")
            if severity in {"critical", "major"} and status == "open":
                errors.append(f"{prefix} has an open {severity} discrepancy")

    if report.get("console_errors") != 0:
        errors.append("console_errors must be 0")
    if gate_context == "skill-preinstallation":
        review = report.get("independent_review")
        if not isinstance(review, dict):
            errors.append("skill-preinstallation requires independent_review")
        else:
            if not review.get("reviewer"):
                errors.append("independent_review.reviewer is required")
            if not review.get("evidence"):
                errors.append("independent_review.evidence is required")
            if review.get("status") != "pass":
                errors.append("independent_review.status must be pass")
    if report.get("verdict") != "pass":
        errors.append("verdict must be pass")
    return errors


def self_test() -> int:
    passing = {
        "reference": "reference.mp4",
        "target": "http://127.0.0.1:4327/",
        "captures": [{"state": "initial", "reference": "a.png", "implementation": "b.png", "dimensions_match": True, "reviewed": True}],
        "interactions": [{"name": "Open preferences", "primary": True, "evidence": "observed", "status": "pass"}],
        "discrepancies": [{"severity": "minor", "status": "open", "description": "optical offset"}],
        "console_errors": 0,
        "verdict": "pass",
    }
    failing = json.loads(json.dumps(passing))
    failing["discrepancies"] = [{"severity": "major", "status": "open", "description": "missing interaction"}]
    preinstall_passing = json.loads(json.dumps(passing))
    preinstall_passing["gate_context"] = "skill-preinstallation"
    preinstall_passing["independent_review"] = {"reviewer": "reviewer", "status": "pass", "evidence": "matched captures reviewed"}
    preinstall_failing = json.loads(json.dumps(preinstall_passing))
    preinstall_failing["independent_review"]["status"] = "fail"
    if validate(passing):
        print("self-test failed: passing fixture was rejected")
        return 1
    if not validate(failing):
        print("self-test failed: failing fixture was accepted")
        return 1
    if validate(preinstall_passing):
        print("self-test failed: passing pre-installation fixture was rejected")
        return 1
    if not validate(preinstall_failing):
        print("self-test failed: failed independent review was accepted")
        return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.report is None:
        parser.error("report is required unless --self-test is used")
    report = json.loads(args.report.read_text(encoding="utf-8"))
    errors = validate(report)
    if errors:
        print("forward test rejected")
        for error in errors:
            print(f"- {error}")
        return 1
    print("forward test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
