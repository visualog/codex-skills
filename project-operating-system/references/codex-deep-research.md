# Codex Deep Research

Use this workflow for an evidence-backed decision, not a quick fact lookup. Keep the canonical user question verbatim in `research-brief.md`; distinguish it from output format or file-location requirements.

## Run sequence

1. **Frame:** Define decision, audience, time boundary, deliverable, exclusions, and atomic claims/questions. Create a coverage matrix before searching.
2. **Collect:** Search primary sources first: official documents, datasets, filings, standards, original research, or source code. Add strong secondary analysis only for interpretation. Record source URL, publisher, date, source type, and the exact claim it supports in `source-register.md`.
3. **Challenge:** Run a separate counter-evidence search for each material conclusion: limitations, criticism, conflicting findings, corrections, retractions, and alternative explanations.
4. **Normalize:** Cluster reprints, syndicated articles, and pages that rely on the same press release or primary report. Treat a cluster as one independent source.
5. **Map:** Add every material report claim to `claim-map.md` with direct supporting sources, counter-evidence, confidence, and caveat. Do not cite a source that merely discusses the topic without supporting the sentence.
6. **Write:** Synthesize only what the mapped evidence supports. Separate observed fact, source-backed inference, and recommendation. Include unresolved questions.
7. **Gate:** Before delivery, verify date-sensitive facts, numerical claims, quote fidelity, source independence, and that any major counter-evidence is represented. Save the final report and a short handoff.

## Files per run

Create a dated slug under `docs/research/<YYYY-MM>-<topic>/`:

| File | Purpose |
| --- | --- |
| `research-brief.md` | Canonical question, scope, claim/coverage matrix |
| `source-register.md` | Sources, provenance, independence cluster, status |
| `evidence-digest.md` | Concise notes and exact evidence locations |
| `contradictions.md` | Conflicts, counter-evidence, unresolved questions |
| `claim-map.md` | Claim-to-evidence mapping and confidence |
| `final-report.md` | Decision-ready synthesis and citations |

Do not scrape paywalled or logged-in content by bypassing access controls. Ask the user to complete authentication when their session is needed; never automate CAPTCHAs, 2FA, or credential entry. Do not add embeddings, APIs, databases, or crawler packages without explicit approval.
