#!/usr/bin/env python3
"""Create focused, legible evidence images from screenshots.

Requires Pillow. Set CUTTO_AI_VERIFY_FONT to a preferred TrueType/OpenType font.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


RED = (255, 59, 48)
BACKGROUND = (18, 17, 24)
PANEL = (40, 38, 52)
FOREGROUND = (247, 247, 248)
SECONDARY = (167, 165, 178)
ACCENT = (190, 154, 255)
PADDING = 28
LANCZOS = getattr(Image, "Resampling", Image).LANCZOS


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        box = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("box values must be integers") from error
    if len(box) != 4:
        raise argparse.ArgumentTypeError("box must be left,top,right,bottom")
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError("box right/bottom must exceed left/top")
    return left, top, right, bottom


def font_candidates() -> Iterable[str]:
    configured = os.environ.get("CUTTO_AI_VERIFY_FONT")
    if configured:
        yield configured
    yield from (
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    )


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in font_candidates():
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    warn("no suitable system font found; using Pillow's default font")
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> float:
    return draw.textlength(text, font=font)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    current = ""
    for character in text:
        if character == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + character
        if current and text_width(draw, candidate, font) > max_width:
            lines.append(current)
            current = character
        else:
            current = candidate
    if current or not lines:
        lines.append(current)
    return lines


def save(image: Image.Image, destination: str) -> None:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    print(f"saved {path} ({image.width}x{image.height})")


def crop_image(args: argparse.Namespace) -> None:
    source = Image.open(args.source).convert("RGB")
    left, top, right, bottom = args.box
    if not (0 <= left < right <= source.width and 0 <= top < bottom <= source.height):
        raise SystemExit(f"crop box {args.box} exceeds source size {source.size}")
    if right - left > 600:
        warn(f"crop is {right - left}px wide; narrower than 560px is usually easier to read")

    cropped = source.crop(args.box)
    resized = cropped.resize(
        (round(cropped.width * args.scale), round(cropped.height * args.scale)),
        LANCZOS,
    )
    draw = ImageDraw.Draw(resized)
    for rect in args.rect:
        x0, y0, x1, y1 = rect
        draw.rectangle(
            (
                round((x0 - left) * args.scale),
                round((y0 - top) * args.scale),
                round((x1 - left) * args.scale),
                round((y1 - top) * args.scale),
            ),
            outline=RED,
            width=args.line_width,
        )
    save(resized, args.destination)


def parse_panel(value: str) -> tuple[str, Path, bool]:
    label, separator, raw_path = value.partition("::")
    if not separator or not label or not raw_path:
        raise argparse.ArgumentTypeError("panel must be LABEL::IMAGE_PATH")
    emphasized = label.startswith("!")
    return label[1:] if emphasized else label, Path(raw_path), emphasized


def stack_images(args: argparse.Namespace) -> None:
    title_font = load_font(34)
    label_font = load_font(25)
    note_font = load_font(19)
    measuring = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    inner_width = args.width - PADDING * 2

    panels: list[tuple[list[str], Image.Image, bool]] = []
    height = PADDING
    title_lines = wrap_text(measuring, args.title, title_font, inner_width)
    height += len(title_lines) * 46 + 18

    for label, path, emphasized in args.panel:
        image = Image.open(path).convert("RGB")
        scale = min(inner_width / image.width, 1.6)
        if scale != 1:
            image = image.resize(
                (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
                LANCZOS,
            )
        label_lines = wrap_text(measuring, label, label_font, inner_width - 24)
        panels.append((label_lines, image, emphasized))
        height += len(label_lines) * 34 + 28 + image.height + 26

    note_lines = wrap_text(measuring, args.note, note_font, inner_width) if args.note else []
    height += len(note_lines) * 26 + PADDING

    output = Image.new("RGB", (args.width, height), BACKGROUND)
    draw = ImageDraw.Draw(output)
    y = PADDING
    for line in title_lines:
        draw.text((PADDING, y), line, font=title_font, fill=FOREGROUND)
        y += 46
    y += 18

    for label_lines, image, emphasized in panels:
        label_height = len(label_lines) * 34 + 18
        draw.rounded_rectangle(
            (PADDING, y, args.width - PADDING, y + label_height),
            radius=8,
            fill=RED if emphasized else PANEL,
        )
        line_y = y + 8
        for line in label_lines:
            draw.text(
                (PADDING + 12, line_y),
                line,
                font=label_font,
                fill=FOREGROUND if emphasized else ACCENT,
            )
            line_y += 34
        y += label_height + 10
        image_x = PADDING + (inner_width - image.width) // 2
        output.paste(image, (image_x, y))
        draw.rectangle(
            (image_x, y, image_x + image.width - 1, y + image.height - 1),
            outline=(60, 58, 72),
        )
        y += image.height + 26

    for line in note_lines:
        draw.text((PADDING, y), line, font=note_font, fill=SECONDARY)
        y += 26
    save(output, args.destination)


def join_images(args: argparse.Namespace) -> None:
    images = [Image.open(path).convert("RGB") for path in args.parts]
    width = sum(image.width for image in images) + args.gap * (len(images) - 1)
    height = max(image.height for image in images)
    output = Image.new("RGB", (width, height), PANEL)
    x = 0
    for image in images:
        output.paste(image, (x, (height - image.height) // 2))
        x += image.width + args.gap
    save(output, args.destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    crop = subparsers.add_parser("crop", help="crop, enlarge, and outline evidence")
    crop.add_argument("source")
    crop.add_argument("destination")
    crop.add_argument("--box", required=True, type=parse_box, help="left,top,right,bottom")
    crop.add_argument("--scale", type=float, default=2.4)
    crop.add_argument("--rect", action="append", default=[], type=parse_box)
    crop.add_argument("--line-width", type=int, default=5)
    crop.set_defaults(run=crop_image)

    stack = subparsers.add_parser("stack", help="stack labeled evidence vertically")
    stack.add_argument("destination")
    stack.add_argument("--title", required=True)
    stack.add_argument("--panel", required=True, action="append", type=parse_panel)
    stack.add_argument("--note", default="")
    stack.add_argument("--width", type=int, default=1200)
    stack.set_defaults(run=stack_images)

    join = subparsers.add_parser("hjoin", help="join small fragments from the same row")
    join.add_argument("destination")
    join.add_argument("parts", nargs="+")
    join.add_argument("--gap", type=int, default=14)
    join.set_defaults(run=join_images)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "crop" and args.scale <= 0:
        raise SystemExit("scale must be positive")
    if args.command == "stack" and args.width <= PADDING * 2:
        raise SystemExit("width is too small")
    args.run(args)


if __name__ == "__main__":
    main()
