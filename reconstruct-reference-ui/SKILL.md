---
name: reconstruct-reference-ui
description: Reconstruct authorized web interfaces faithfully from screenshots, reference images, screen recordings, or live URLs by measuring the source, preserving the existing architecture, implementing the UI, rendering it in a real browser, comparing matched captures, and iterating on visible differences. Use when the user asks to clone, reproduce, match, rebuild, or achieve visual or motion parity with a concrete reference. Do not use for inspiration-only work, redesigns, or general frontend creation without a visual target.
---

# Reconstruct Reference UI

Treat the selected reference as the source of truth. Reproduce it as faithfully as the available evidence permits; do not modernize, simplify, embellish, or reinterpret it unless the user explicitly requests a redesign.

Scope this version to browser-rendered web interfaces. Route native iOS, Android, or desktop-app work through the appropriate platform workflow while preserving the same evidence and comparison principles.

## Establish the reconstruction contract

1. Resolve the exact reference and target page or component before editing.
2. For a live URL, confirm that the user owns it or has permission to reproduce it. Respect access controls and terms; do not bypass authentication, paywalls, or anti-bot controls.
3. Read repository instructions and inspect the existing framework, styling system, design tokens, components, fonts, icons, assets, motion libraries, and run commands.
4. Record the target viewport, device scale factor when known, visible state, interaction trigger, and reference timestamp for animated states.
5. Mark every value as `measured`, `inferred`, or `estimated`. State material uncertainty instead of presenting guesses as exact.
6. Inventory every visible control. Classify its outcome as `observed`, `inferred`, or `unavailable`. Never ship a control that changes only its selected styling while pretending the referenced outcome exists. Implement it from evidence, label an approved inference, or disable it with a concise reason.

Keep working analysis in a temporary directory or the conversation. Do not add analysis or QA documents to the target repository unless the user asks to preserve them.

## Route by reference type

- For an image or screenshot, read [measurement-and-comparison.md](references/measurement-and-comparison.md) and measure the source at its native resolution.
- For a screen recording or video, also read [video-motion-analysis.md](references/video-motion-analysis.md). Extract representative frames before implementing motion.
- For a live URL, inspect the rendered page, DOM, computed styles, responsive states, assets, and interactions with an available browser automation workflow. Capture only pages and states within the user's scope.
- When an installed image-to-code, URL-cloning, or browser-automation skill already supplies a sub-workflow, reuse it. This skill owns the reconstruction contract, measurement discipline, comparison passes, and completion evidence.

## Analyze before implementation

Produce a compact working specification proportional to the task. Include only applicable fields:

- viewport, page bounds, containers, grids, alignment axes, overflow, and stacking
- typography family, weight, size, line height, tracking, wrapping, and text width
- colors, borders, radii, shadows, opacity, blur, gradients, and blend modes
- component dimensions, internal spacing, repeated variants, and visible states
- assets, icons, fonts, and any unavailable source material
- responsive changes, interaction triggers, and motion events

Do not turn a small component task into a long documentation exercise. Do not start implementation while the primary structure, target viewport, or selected state remains ambiguous enough to change the approach materially.

## Implement for fidelity

1. Preserve the current project architecture unless a change is necessary for parity.
2. Reuse existing tokens, components, fonts, assets, icon libraries, and motion systems where they match the reference.
3. Implement static composition before motion. Correct structure, typography, wrapping, spacing, and assets before polishing effects.
4. Implement motion as explicit state transitions or timelines. Do not replace compound motion with a generic fade.
5. Add a dependency only after inspecting the existing stack. Prefer CSS for simple state changes and the project's current motion library for complex sequencing.
6. Do not create a new design system for one reconstructed screen. Do not invoke creative frontend guidance that conflicts with source fidelity.
7. Do not substitute emoji, generic gradients, stock illustrations, or approximate icons when the reference contains specific assets.

## Capture matched browser evidence

A successful build or HTTP response is not visual verification. Open the target route in a real browser and capture the rendered result.

Before each comparison capture:

- use the reference viewport and a documented device scale factor
- keep browser zoom at 100 percent
- wait for fonts, images, and layout to settle
- reproduce the same route, scroll position, UI state, and animation timestamp
- stabilize or mask clocks, cursors, ads, randomized content, video frames, and other dynamic regions
- preserve the reference crop instead of resizing one image to conceal a mismatch

Test additional widths only when the reference, repository requirements, or user scope calls for responsive behavior. Do not invent mobile behavior from a desktop-only reference without identifying it as an inference.

## Compare and iterate

Use the comparison protocol in [measurement-and-comparison.md](references/measurement-and-comparison.md). When two static captures have identical dimensions, run `scripts/compare_reference_renders.py` to produce an overlay, amplified difference image, and measurements. Use the artifacts as evidence, not as a substitute for visual judgment.

Review discrepancies in this order:

1. structure and missing regions
2. page proportions and primary positioning
3. typography scale, font, line breaks, and text width
4. spacing and component dimensions
5. assets, colors, borders, shadows, blur, and radii
6. interaction states and responsive behavior
7. motion timing, easing, path, stagger, and intermediate states
8. optical and subpixel polish

Classify discrepancies as `critical`, `major`, `moderate`, or `minor`. Fix critical and major items first, recapture, and repeat. Do not claim a percentage match or pixel-perfect result unless the measurement method and environment justify that claim.

## Enforce the forward-test gate

For a real-usage or pre-installation forward test, read [forward-test-contract.md](references/forward-test-contract.md), record the contract in a temporary JSON file, and run:

```bash
python3 <skill-directory>/scripts/validate_forward_test.py /tmp/reference-ui-forward-test.json
```

Treat `forward test executed` and `forward test passed` as different outcomes. Never report completion, install the skill globally, or publish it from a failed or blocked forward test. A pass requires matched captures, zero relevant console errors, no open critical or major discrepancy, and every primary observed interaction passing. Unobserved primary behavior is a blocker, not permission to invent it.

The JSON validator checks contract structure and declared outcomes; it cannot decide whether a visible mismatch was honestly classified. For `skill-preinstallation` tests, require an independent visual reviewer and include that verdict in the report. A self-authored `pass` cannot override an independent `fail` or `blocked` verdict. If the reviewer finds that timing alignment, component topology, or a primary state is globally different, record the discrepancy at the reviewer's severity and rerun the validator as an expected rejection.

Stop when:

- no critical or major discrepancy remains at the target state and viewport
- primary interactions reproduce the referenced behavior
- the target route renders without relevant console errors, clipping, or overflow
- another pass would address only minor differences, or progress is blocked by missing assets, fonts, dimensions, access, or source states

Report blockers and remaining differences explicitly; never hide them to claim completion.

## Deliver verifiable results

At completion, report:

- changed files and the implementation approach
- exact routes, viewports, device scale factors, states, and interactions tested
- comparison passes and generated evidence artifacts
- assumptions, inferred behavior, unavailable assets, and remaining differences
- whether the actual page was left open when the user requested a visible preview

Do not require multiple agents for routine execution. Use independent forward tests only when evaluating whether this skill generalizes across different reference types.
