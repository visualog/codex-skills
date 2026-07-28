---
name: codex-deep-research
description: Conduct evidence-led deep research by framing claims, collecting authoritative sources, testing counterevidence, and delivering traceable conclusions. Use for decisions, competitive analysis, technical investigation, policy or market research, and any answer where source quality, recency, or uncertainty matters.
---

# Codex Deep Research

Turn an ambiguous question into a decision-ready, evidence-traceable research result. Use this skill whenever an answer needs more than a quick lookup: it must distinguish facts from inferences, account for recency, and actively look for evidence that could reverse the conclusion.

## Choose the research depth

- **Quick**: answer a narrow factual question with a small number of authoritative sources.
- **Evidence**: investigate a decision or comparison; construct a claim map and test material counterarguments.
- **Durable**: produce reusable research artifacts in the project after the user asks to save them. Read [artifact-templates.md](references/artifact-templates.md) before creating those files.

Do not impose a lengthy process for a simple question. Escalate to Evidence when the conclusion affects money, safety, compliance, architecture, roadmap, or reputation; when claims are disputed; or when information is likely to have changed.

## Research workflow

1. **Frame the decision.** State the question, decision it informs, target audience, scope, time boundary, and what would count as a useful answer. Make a reasonable scoped assumption when it is safe; identify it plainly.
2. **Build a claim map.** Break the expected conclusion into testable claims. Mark each claim as factual, analytical inference, or recommendation. Define the evidence needed and a plausible disconfirming condition.
3. **Plan the source mix.** Prefer primary sources: official documentation, regulations, original studies, filings, source code, datasets, or direct statements. Use reputable independent reporting and expert analysis for context and challenge. Do not count copied coverage of one original source as independent confirmation.
4. **Collect and record provenance.** Capture the source title, publisher, publication or update date, direct URL, relevant claim, and limitations. Verify time-sensitive facts live. Never invent a source, quote, date, or access that was not obtained.
5. **Search for counterevidence.** For each material conclusion, deliberately seek credible contradictory data, boundary cases, incentives, and methodological flaws. Report unresolved disagreement instead of forcing consensus.
6. **Synthesize by claim.** Put citations beside the claims they support. Separate established facts, reasoned inferences, and recommendations. Explain any inferential leap in one or two sentences.
7. **Audit before delivery.** Check coverage of decisive claims, source independence, recency, citation-to-claim fit, numerical consistency, and whether the answer directly serves the original decision.

## Reporting standard

Lead with the answer, confidence, and the key reason. Then present only the supporting detail the decision needs:

- **Conclusion:** clear answer and confidence level.
- **Evidence:** claim-level findings with adjacent links/citations.
- **Counterevidence and limits:** what could change the answer, what remains unknown, and any source conflicts.
- **Recommendation:** action, owner/next check when useful, and conditions for revisiting it.

Use calibrated wording: “confirms” only for direct evidence; “indicates” for strong but incomplete evidence; “suggests” for inference. Cite sources as direct Markdown links whenever external research was used.

## Durable research artifacts

Create project files only when the user requests saved research or when a project workflow explicitly requires it. Default to `docs/research/<YYYY-MM-DD>-<topic-slug>/` and avoid overwriting existing work. Include a brief `README.md`, `source-log.md`, and `report.md`; use the template guidance in [artifact-templates.md](references/artifact-templates.md).

When the repository has the `project-operating-system` skill and its research structure is already initialized, preserve that structure instead of creating a parallel taxonomy.

## Boundaries

- Treat access restrictions, missing primary sources, and unverified claims as explicit limitations.
- Do not bypass paywalls, logins, rate limits, or terms of service.
- For high-stakes medical, legal, financial, or security topics, prioritize current authoritative sources and state that the result is informational rather than professional advice.
- Preserve user-provided confidential material; do not send it to external services unless the user has placed that service and data exchange in scope.
