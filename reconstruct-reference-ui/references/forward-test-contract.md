# Forward-test contract

Use this contract only for real-usage validation and pre-installation checks. Keep the JSON in a temporary directory unless the user asks to preserve it.

```json
{
  "gate_context": "delivery",
  "reference": "path-or-url",
  "target": "route-or-component",
  "captures": [
    {
      "state": "initial",
      "reference": "/tmp/reference.png",
      "implementation": "/tmp/implementation.png",
      "dimensions_match": true,
      "reviewed": true
    }
  ],
  "interactions": [
    {
      "name": "Open preferences",
      "primary": true,
      "evidence": "observed",
      "status": "pass"
    }
  ],
  "discrepancies": [
    {
      "severity": "minor",
      "status": "open",
      "description": "One-pixel optical offset"
    }
  ],
  "console_errors": 0,
  "verdict": "pass"
}
```

For a skill pre-installation test, set `gate_context` to `skill-preinstallation` and add:

```json
{
  "independent_review": {
    "reviewer": "independent-agent-or-person",
    "status": "pass",
    "evidence": "Reviewed every matched capture and comparison artifact"
  }
}
```

Rules:

- `captures` must include every primary stable state and applicable motion timestamp.
- `evidence` is `observed`, `inferred`, or `unavailable`.
- `status` is `pass`, `fail`, or `blocked`.
- A primary interaction with `inferred` or `unavailable` evidence cannot pass without explicit user acceptance of that inference.
- Controls outside the available evidence must be disabled with a reason or excluded from the reconstruction scope; never leave them as cosmetic no-ops.
- `discrepancies` use `critical`, `major`, `moderate`, or `minor`, with `open` or `resolved` status.
- Set `verdict` to `pass` only after the validator succeeds. `fail` means work remains; `blocked` means required evidence or access is unavailable.
- `skill-preinstallation` requires an independent visual-review `pass`. Structural validation alone is not evidence that discrepancy severity was classified honestly.
