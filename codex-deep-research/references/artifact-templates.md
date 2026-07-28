# Durable research artifact templates

Use this reference only after the user requests that research be saved in the project. Replace bracketed text; keep entries concise and traceable.

## `README.md`

```md
# [Research topic]

- Decision: [decision this research informs]
- Scope: [included and excluded areas]
- As of: [date and time boundary]
- Status: [draft | reviewed | superseded]

See [report.md](report.md) for conclusions and [source-log.md](source-log.md) for provenance.
```

## `source-log.md`

```md
# Source log

| ID | Source | Publisher | Date | Supports or challenges | Independence / limits |
| --- | --- | --- | --- | --- | --- |
| S1 | [Title](https://example.com) | [Publisher] | YYYY-MM-DD | [claim] | [limit] |
```

Record one source per row. Give syndicated or derivative material its original source ID and do not count it as independent evidence.

## `report.md`

```md
# [Research topic] — report

## Conclusion

[Decision-ready answer, confidence, and strongest reason.]

## Findings

### Claim: [testable claim]

- **Finding:** [fact, inference, or recommendation label] [statement] ([S1](source-log.md#s1)).
- **Counterevidence / limit:** [what weakens or could reverse it].

## Open questions

- [Unresolved question and the evidence that would answer it.]

## Recommended next step

[Owner or action, if applicable; revisit trigger.]
```

Keep source links and citations valid. If Markdown table anchors are unreliable for the renderer, cite the source title or ID in plain text and link directly to the source URL.
