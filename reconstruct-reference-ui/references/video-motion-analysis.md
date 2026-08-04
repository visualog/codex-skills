# Video and Motion Analysis Protocol

Use this protocol for screen recordings, animated references, and interactions whose intermediate states affect fidelity.

## Inspect the source

Preserve the original video. Record its dimensions, duration, nominal frame rate, visible crop, playback speed, and whether the recording contains cursor movement or device chrome.

Extract frames into a temporary directory:

```bash
python3 <skill-directory>/scripts/extract_reference_frames.py reference.mp4 \
  --output-dir /tmp/reference-ui-frames \
  --fps 4 \
  --contact-sheet
```

For known event times, prefer explicit timestamps:

```bash
python3 <skill-directory>/scripts/extract_reference_frames.py reference.mp4 \
  --output-dir /tmp/reference-ui-frames \
  --timestamps 0,0.12,0.24,0.4,0.65,1.0 \
  --contact-sheet
```

Start with a low sampling rate that covers the whole interaction, then extract additional timestamps around fast transitions. Do not flood the context with every frame.

## Segment motion into events

Separate the recording into stable states and transitions. For each event, record:

| Field | Description |
| --- | --- |
| Trigger | Load, click, hover, scroll, drag, timer, or state change |
| Start and end | Reference timestamps and named UI states |
| Elements | Entering, exiting, moving, masking, or changing elements |
| Properties | Translation, scale, rotation, opacity, blur, clip, color, or layout |
| Timing | Delay, duration, overlap, and stagger |
| Easing | Measured curve, spring behavior, or best labeled approximation |
| Origin and path | Transform origin, trajectory, and spatial relationship |
| Interruption | Whether a repeated trigger reverses, retargets, queues, or restarts |

Describe compound motion explicitly. A transition that combines translation, scale, opacity, and blur is not a generic fade.

## Infer carefully

- Treat recording timestamps as evidence, not necessarily animation source durations; capture latency and playback speed may distort them.
- Distinguish camera or page scrolling from element motion.
- Check whether a moving element is fixed, sticky, absolutely positioned, or transformed inside a scrolling container.
- Infer easing from several intermediate frames, not only the endpoints.
- Identify motion that belongs to the browser, OS, cursor, video player, or device chrome and exclude it from app implementation.
- Preserve source behavior even when it conflicts with generic animation style guidance, unless it creates an accessibility or functional defect that the user asks to correct.

## Implement and compare

1. Match the stable start and end states before tuning motion.
2. Implement the simplest mechanism that reproduces the observed sequence within the existing stack.
3. Honor reduced-motion behavior without using it during a capture intended to match the normal reference.
4. Trigger the implementation from the same initial state.
5. Capture the same event timestamps or named states.
6. Compare corresponding frames with the static comparison protocol.
7. Tune path and transform origin before duration and easing; tune stagger and secondary effects last.

When deterministic timestamp capture is unavailable, compare reproducible named states and report the timing limitation. Never claim exact motion parity from endpoint screenshots alone.
