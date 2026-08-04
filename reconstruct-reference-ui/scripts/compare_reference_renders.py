#!/usr/bin/env python3
"""Create visual comparison artifacts for two equal-size reference renders."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, NoReturn

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. Install it with: python3 -m pip install Pillow"
    ) from exc


OUTPUT_NAMES = ("overlay.png", "difference.png", "metrics.json")


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def parse_mask(value: str) -> tuple[int, int, int, int]:
    try:
        parts = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as exc:
        fail(f"Invalid mask '{value}'. Expected x,y,width,height integers.")
        raise AssertionError from exc
    if len(parts) != 4:
        fail(f"Invalid mask '{value}'. Expected x,y,width,height.")
    x, y, width, height = parts
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        fail(f"Invalid mask '{value}'. Coordinates must be non-negative and dimensions positive.")
    return x, y, width, height


def prepare_output(output_dir: Path, force: bool) -> None:
    resolved = output_dir.expanduser().resolve()
    if resolved == Path(resolved.anchor):
        fail("Refusing to use a filesystem root as the output directory")
    resolved.mkdir(parents=True, exist_ok=True)
    existing = [resolved / name for name in OUTPUT_NAMES if (resolved / name).exists()]
    if existing and not force:
        fail(
            "Comparison artifacts already exist: "
            + ", ".join(path.name for path in existing)
            + ". Use a fresh directory or --force."
        )
    if force:
        for path in existing:
            path.unlink()


def validate_masks(
    masks: list[tuple[int, int, int, int]], width: int, height: int
) -> None:
    for x, y, mask_width, mask_height in masks:
        if x + mask_width > width or y + mask_height > height:
            fail(
                f"Mask {x},{y},{mask_width},{mask_height} exceeds image bounds {width}x{height}"
            )


def masked_channel(channel: Any, include_mask: Any) -> Any:
    return Image.composite(channel, Image.new("L", channel.size, 0), include_mask)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare equal-size reference and implementation screenshots."
    )
    parser.add_argument("reference", type=Path)
    parser.add_argument("implementation", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--mask",
        action="append",
        default=[],
        metavar="X,Y,W,H",
        help="Ignore a dynamic rectangle; repeat as needed",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=16,
        help="Per-pixel maximum RGB delta counted as changed (0-255)",
    )
    parser.add_argument(
        "--amplify",
        type=float,
        default=4.0,
        help="Difference-image amplification factor",
    )
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    reference_path = args.reference.expanduser().resolve()
    implementation_path = args.implementation.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    for label, path in (("Reference", reference_path), ("Implementation", implementation_path)):
        if not path.is_file():
            fail(f"{label} image not found: {path}")
    if not 0 <= args.threshold <= 255:
        fail("--threshold must be between 0 and 255")
    if not math.isfinite(args.amplify) or args.amplify <= 0:
        fail("--amplify must be a finite positive number")

    masks = [parse_mask(value) for value in args.mask]
    with Image.open(reference_path) as source_reference:
        reference = source_reference.convert("RGB")
    with Image.open(implementation_path) as source_implementation:
        implementation = source_implementation.convert("RGB")
    if reference.size != implementation.size:
        fail(
            f"Image dimensions differ: reference {reference.size[0]}x{reference.size[1]}, "
            f"implementation {implementation.size[0]}x{implementation.size[1]}. "
            "Recapture under the same contract; do not resize to conceal the mismatch."
        )

    width, height = reference.size
    validate_masks(masks, width, height)
    prepare_output(output_dir, args.force)

    include_mask = Image.new("L", reference.size, 255)
    include_draw = ImageDraw.Draw(include_mask)
    for x, y, mask_width, mask_height in masks:
        include_draw.rectangle(
            (x, y, x + mask_width - 1, y + mask_height - 1), fill=0
        )
    compared_pixels = include_mask.histogram()[255]
    ignored_pixels = width * height - compared_pixels
    if compared_pixels == 0:
        fail("Masks exclude every pixel; leave at least one comparable region")

    difference = ImageChops.difference(reference, implementation)
    channels = difference.split()
    masked_channels = [masked_channel(channel, include_mask) for channel in channels]
    absolute_sum = 0
    maximum_channel_difference = 0
    for channel in masked_channels:
        histogram = channel.histogram()
        absolute_sum += sum(value * count for value, count in enumerate(histogram))
        extrema = channel.getextrema()
        maximum_channel_difference = max(maximum_channel_difference, extrema[1])
    mean_absolute_error = absolute_sum / (compared_pixels * 3)

    maximum_difference = ImageChops.lighter(
        ImageChops.lighter(masked_channels[0], masked_channels[1]), masked_channels[2]
    )
    changed_mask = maximum_difference.point(
        lambda value: 255 if value > args.threshold else 0
    )
    changed_mask = ImageChops.multiply(changed_mask, include_mask)
    changed_pixels = changed_mask.histogram()[255]

    overlay = Image.blend(reference, implementation, 0.5)
    overlay_draw = ImageDraw.Draw(overlay)
    for x, y, mask_width, mask_height in masks:
        overlay_draw.rectangle(
            (x, y, x + mask_width - 1, y + mask_height - 1),
            outline=(255, 208, 0),
            width=2,
        )
    overlay.save(output_dir / "overlay.png")

    amplification = args.amplify
    amplified = difference.point(lambda value: min(255, round(value * amplification)))
    ignored_fill = Image.new("RGB", reference.size, (48, 48, 48))
    amplified = Image.composite(amplified, ignored_fill, include_mask)
    amplified.save(output_dir / "difference.png")

    metrics = {
        "reference": str(reference_path),
        "implementation": str(implementation_path),
        "dimensions": {"width": width, "height": height},
        "threshold": args.threshold,
        "amplification": amplification,
        "masks": [
            {"x": x, "y": y, "width": mask_width, "height": mask_height}
            for x, y, mask_width, mask_height in masks
        ],
        "compared_pixels": compared_pixels,
        "ignored_pixels": ignored_pixels,
        "changed_pixels": changed_pixels,
        "changed_pixel_ratio": changed_pixels / compared_pixels,
        "mean_absolute_error_0_to_255": mean_absolute_error,
        "mean_absolute_error_normalized": mean_absolute_error / 255,
        "maximum_channel_difference": maximum_channel_difference,
        "interpretation": "Diagnostic measurements only; do not present them as a perceptual similarity score.",
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
