#!/usr/bin/env python3
"""Extract timestamped reference frames and an optional contact sheet from video."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn


GENERATED_FILES = ("contact-sheet.png", "frames-manifest.json")


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        fail(f"Required executable not found: {name}")
    return path


def parse_rate(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            return None
        return float(numerator) / denominator_value
    return float(value)


def probe_video(ffprobe: str, source: Path) -> dict[str, Any]:
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,width,height,avg_frame_rate,r_frame_rate",
        "-of",
        "json",
        str(source),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(completed.stdout)
    video_stream = next(
        (stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"),
        None,
    )
    if video_stream is None:
        fail(f"No video stream found in {source}")

    duration_raw = payload.get("format", {}).get("duration")
    duration = float(duration_raw) if duration_raw not in (None, "N/A") else None
    nominal_rate = parse_rate(video_stream.get("avg_frame_rate")) or parse_rate(
        video_stream.get("r_frame_rate")
    )
    return {
        "duration_seconds": duration,
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "nominal_frame_rate": nominal_rate,
    }


def parse_timestamps(raw: str) -> list[float]:
    values: list[float] = []
    seen: set[float] = set()
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            timestamp = float(item)
        except ValueError as exc:
            fail(f"Invalid timestamp: {item}")
            raise AssertionError from exc
        if not math.isfinite(timestamp) or timestamp < 0:
            fail(f"Timestamp must be a finite non-negative number: {item}")
        if timestamp not in seen:
            seen.add(timestamp)
            values.append(timestamp)
    if not values:
        fail("--timestamps must contain at least one number")
    return values


def prepare_output(output_dir: Path, force: bool) -> None:
    resolved = output_dir.expanduser().resolve()
    if resolved == Path(resolved.anchor):
        fail("Refusing to use a filesystem root as the output directory")
    resolved.mkdir(parents=True, exist_ok=True)

    existing = sorted(resolved.glob("frame-*.png"))
    existing.extend(path for name in GENERATED_FILES if (path := resolved / name).exists())
    if existing and not force:
        preview = ", ".join(path.name for path in existing[:5])
        fail(f"Generated artifacts already exist in {resolved}: {preview}. Use a fresh directory or --force.")
    if force:
        for path in existing:
            path.unlink()


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def extract_at_fps(
    ffmpeg: str,
    source: Path,
    output_dir: Path,
    fps: float,
    max_frames: int,
) -> list[dict[str, Any]]:
    pattern = output_dir / "frame-%05d.png"
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-map",
            "0:v:0",
            "-vf",
            f"fps={fps:.12g}",
            "-frames:v",
            str(max_frames),
            "-y",
            str(pattern),
        ]
    )
    frames = sorted(output_dir.glob("frame-*.png"))
    return [
        {"file": frame.name, "timestamp_seconds": round(index / fps, 6)}
        for index, frame in enumerate(frames)
    ]


def extract_at_timestamps(
    ffmpeg: str,
    source: Path,
    output_dir: Path,
    timestamps: list[float],
) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    for index, timestamp in enumerate(timestamps, start=1):
        milliseconds = round(timestamp * 1000)
        output = output_dir / f"frame-{index:04d}-{milliseconds:08d}ms.png"
        run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(source),
                "-ss",
                f"{timestamp:.6f}",
                "-map",
                "0:v:0",
                "-frames:v",
                "1",
                "-y",
                str(output),
            ]
        )
        if not output.exists():
            fail(f"ffmpeg did not produce a frame at {timestamp:.6f} seconds")
        frames.append({"file": output.name, "timestamp_seconds": timestamp})
    return frames


def create_contact_sheet(
    output_dir: Path,
    frames: list[dict[str, Any]],
    columns: int,
    thumbnail_width: int,
) -> Path:
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        fail("Pillow is required for --contact-sheet. Install it with: python3 -m pip install Pillow")

    label_height = 24
    prepared: list[tuple[Any, str]] = []
    maximum_height = 0
    for frame in frames:
        with Image.open(output_dir / frame["file"]) as image:
            image = image.convert("RGB")
            ratio = thumbnail_width / image.width
            height = max(1, round(image.height * ratio))
            resampling = getattr(Image, "Resampling", Image)
            thumbnail = ImageOps.contain(
                image,
                (thumbnail_width, height),
                method=resampling.LANCZOS,
            )
            prepared.append((thumbnail.copy(), f'{frame["timestamp_seconds"]:.3f}s'))
            maximum_height = max(maximum_height, thumbnail.height)

    if not prepared:
        fail("No frames were extracted")
    rows = math.ceil(len(prepared) / columns)
    sheet = Image.new(
        "RGB",
        (columns * thumbnail_width, rows * (maximum_height + label_height)),
        (18, 18, 18),
    )
    draw = ImageDraw.Draw(sheet)
    for index, (thumbnail, label) in enumerate(prepared):
        column = index % columns
        row = index // columns
        x = column * thumbnail_width
        y = row * (maximum_height + label_height)
        sheet.paste(thumbnail, (x, y))
        draw.text((x + 6, y + maximum_height + 5), label, fill=(240, 240, 240))

    output = output_dir / "contact-sheet.png"
    sheet.save(output)
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract frames from a reference video without modifying the source."
    )
    parser.add_argument("source", type=Path, help="Reference video path")
    parser.add_argument("--output-dir", required=True, type=Path, help="Artifact directory")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--fps", type=float, help="Uniform samples per second (default: 4)")
    selection.add_argument("--timestamps", help="Comma-separated timestamps in seconds")
    parser.add_argument("--max-frames", type=int, default=120, help="Extraction safety cap")
    parser.add_argument("--contact-sheet", action="store_true", help="Create contact-sheet.png")
    parser.add_argument("--columns", type=int, default=5, help="Contact sheet columns")
    parser.add_argument("--thumbnail-width", type=int, default=320, help="Contact sheet cell width")
    parser.add_argument("--force", action="store_true", help="Replace only artifacts generated by this script")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = args.source.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    if not source.is_file():
        fail(f"Reference video not found: {source}")
    if args.max_frames < 1:
        fail("--max-frames must be at least 1")
    if args.columns < 1 or args.thumbnail_width < 32:
        fail("--columns must be positive and --thumbnail-width must be at least 32")

    ffmpeg = require_tool("ffmpeg")
    ffprobe = require_tool("ffprobe")
    metadata = probe_video(ffprobe, source)
    timestamps = parse_timestamps(args.timestamps) if args.timestamps else None
    fps = args.fps if args.fps is not None else 4.0
    if timestamps is None and (not math.isfinite(fps) or fps <= 0):
        fail("--fps must be a finite positive number")
    if timestamps and len(timestamps) > args.max_frames:
        fail(f"Requested {len(timestamps)} timestamps, exceeding --max-frames {args.max_frames}")
    duration = metadata.get("duration_seconds")
    if timestamps and duration is not None:
        beyond_end = [value for value in timestamps if value > duration + 0.001]
        if beyond_end:
            fail(f"Timestamp exceeds video duration {duration:.3f}s: {beyond_end[0]:.3f}s")
    if timestamps is None and duration is not None:
        estimated = math.ceil(duration * fps)
        if estimated > args.max_frames:
            fail(
                f"Sampling would create about {estimated} frames, exceeding --max-frames "
                f"{args.max_frames}. Lower --fps or raise the cap explicitly."
            )

    prepare_output(output_dir, args.force)
    if timestamps is not None:
        frames = extract_at_timestamps(ffmpeg, source, output_dir, timestamps)
        sampling: dict[str, Any] = {"mode": "timestamps", "values_seconds": timestamps}
    else:
        frames = extract_at_fps(ffmpeg, source, output_dir, fps, args.max_frames)
        sampling = {"mode": "fps", "fps": fps}
    if not frames:
        fail("No frames were extracted")

    contact_sheet = None
    if args.contact_sheet:
        contact_sheet = create_contact_sheet(output_dir, frames, args.columns, args.thumbnail_width)

    manifest = {
        "source": str(source),
        "source_metadata": metadata,
        "sampling": sampling,
        "frame_count": len(frames),
        "frames": frames,
        "contact_sheet": contact_sheet.name if contact_sheet else None,
    }
    manifest_path = output_dir / "frames-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "frame_count": len(frames)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
