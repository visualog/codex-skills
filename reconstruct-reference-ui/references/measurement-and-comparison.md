# Measurement and Comparison Protocol

Use this protocol for screenshot, image, and rendered-page references. Preserve source evidence and distinguish direct measurement from inference.

## Establish comparable inputs

Record a compact capture contract before comparing:

```yaml
reference_type: screenshot | image | video-frame | live-url
reference_source: path-or-url
reference_dimensions: width x height pixels
target_route: route-or-component
viewport: width x height CSS pixels
device_scale_factor: number-or-unknown
browser_zoom: 100 percent
state: initial | hover | open | scrolled | named-state
animation_timestamp_ms: number-or-not-applicable
fonts_ready: yes | no | unknown
dynamic_regions: list-of-x-y-width-height-rectangles
```

Do not assume that media pixel dimensions equal CSS viewport dimensions. A screenshot may be cropped, scaled, compressed, or captured at a device scale factor greater than one.

Use this evidence order:

1. Exact viewport and capture metadata supplied by the user or source tooling.
2. Live DOM, computed styles, media metadata, and original asset dimensions.
3. Geometric inference from repeated alignments and known device frames.
4. Visual estimation.

Label values from levels 1–2 as `measured`, level 3 as `inferred`, and level 4 as `estimated`.

## Measure the reference

Measure large relationships before individual details:

1. Identify the full page or component bounds and any crop.
2. Mark major horizontal and vertical alignment axes.
3. Measure container width, outer gutters, columns, gaps, and primary section heights.
4. Measure text blocks by bounding box, line count, baseline relationship, and wrapping before guessing font size.
5. Measure repeated components as a system; compare their shared dimensions and spacing.
6. Inspect colors, borders, shadows, blur, and radii after geometry is stable.
7. Record visible responsive clues without inventing unseen breakpoints.

Prefer ranges when compression or antialiasing prevents an exact reading. For example, record `31–33 px inferred` rather than `32 px measured`.

## Stabilize the implementation capture

Capture the implementation only after:

- the intended route and component state are visible
- document fonts report ready and fallback fonts are no longer swapping
- required images have loaded and layout shifts have stopped
- browser zoom is 100 percent
- viewport and device scale factor are documented
- scroll position matches the reference crop
- animations are at the intended start, intermediate, or end state
- dynamic regions are fixed or listed as masks
- relevant browser console errors have been checked

If exact environment parity is impossible, preserve the reference dimensions and report the mismatch rather than resizing an image to force alignment.

## Generate comparison evidence

For equal-size static images, run:

```bash
python3 <skill-directory>/scripts/compare_reference_renders.py \
  reference.png implementation.png \
  --output-dir /tmp/reference-ui-comparison
```

Ignore a dynamic rectangle only when it cannot be stabilized:

```bash
python3 <skill-directory>/scripts/compare_reference_renders.py \
  reference.png implementation.png \
  --output-dir /tmp/reference-ui-comparison \
  --mask 12,18,140,36 \
  --mask 980,24,220,180
```

The script writes:

- `overlay.png`: a 50/50 blend for spotting displaced edges and wrapping
- `difference.png`: amplified absolute RGB differences
- `metrics.json`: dimensions, threshold, masks, compared pixels, changed-pixel ratio, and mean absolute error

Treat changed-pixel ratio as a diagnostic measurement, not a similarity score. Antialiasing, font rendering, compression, shadows, and one-pixel displacement can change many pixels without representing equal perceptual impact.

## Review by perceptual impact

Inspect each comparison pass in this order:

| Priority | Inspect | Typical finding |
| --- | --- | --- |
| Critical | Structure and state | Missing section, wrong open state, broken interaction |
| Major | Proportions and typography | Wrong container, line wrap, font, asset, or component size |
| Moderate | Spacing and surfaces | Gap, color, shadow, border, blur, or radius mismatch |
| Minor | Optical finish | Subpixel alignment, antialiasing, tiny color drift |

Fix one related cluster at a time, recapture under the same contract, and retain the newest evidence. Recheck earlier priorities after any structural or typography change because downstream spacing may shift.

## Validate responsive behavior

Use the reference viewport first. Add widths only when the source or task requires them:

- an exact additional reference viewport
- a repository-defined breakpoint
- a user-requested mobile, tablet, or desktop target
- a boundary width where layout behavior visibly changes

At each width, test overflow, clipping, text wrapping, fixed and sticky elements, navigation state, touch-sized controls when relevant, and major interaction flows. Mark behavior without a source reference as an inference.
