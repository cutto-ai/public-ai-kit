#!/usr/bin/env python3
"""Validate the repository's self-contained Skill packages."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{skill_file}: missing YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) != 3 or not parts[2].strip():
        fail(f"{skill_file}: frontmatter or body is incomplete")

    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z_]+):\s*(.+)", line)
        if not match:
            fail(f"{skill_file}: unsupported frontmatter line: {line}")
        key, value = match.groups()
        values[key] = value.strip().strip('"').strip("'")

    if set(values) != {"name", "description"}:
        fail(f"{skill_file}: frontmatter must contain only name and description")
    if not values["description"]:
        fail(f"{skill_file}: description cannot be empty")
    return values


def validate_links(skill_dir: Path, skill_file: Path) -> None:
    text = skill_file.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative_target = target.split("#", 1)[0]
        if relative_target and not (skill_dir / relative_target).exists():
            fail(f"{skill_file}: broken relative link: {target}")


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"{skill_dir}: missing SKILL.md")

    frontmatter = parse_frontmatter(skill_file)
    name = frontmatter["name"]
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        fail(f"{skill_file}: invalid Skill name: {name}")
    if name != skill_dir.name:
        fail(f"{skill_file}: name must match folder {skill_dir.name}")

    validate_links(skill_dir, skill_file)

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        metadata = openai_yaml.read_text(encoding="utf-8")
        if f"${name}" not in metadata:
            fail(f"{openai_yaml}: default prompt must mention ${name}")

    for script in (skill_dir / "scripts").glob("*") if (skill_dir / "scripts").exists() else []:
        if script.is_file() and not os.access(script, os.X_OK):
            fail(f"{script}: runnable Skill scripts must be executable")


def main() -> None:
    if not SKILLS_DIR.is_dir():
        fail("skills directory does not exist")

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        fail("no Skill packages found")

    for skill_dir in skill_dirs:
        validate_skill(skill_dir)

    print(f"Validated {len(skill_dirs)} Skill package(s).")


if __name__ == "__main__":
    main()
