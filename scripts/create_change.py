#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "new-change"


def read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def render_template(content: str, context: dict[str, str]) -> str:
    rendered = content
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def materialize_change(templates: Path, change_dir: Path, context: dict[str, str]) -> list[Path]:
    created: list[Path] = []
    for template in sorted(templates.rglob("*")):
        if not template.is_file():
            continue
        relative = template.relative_to(templates)
        if relative.parts and relative.parts[0] in {"examples", "task-examples"}:
            continue
        destination = change_dir / relative
        content = render_template(read_template(template), context)
        write(destination, content)
        created.append(destination)
    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new change package from code_copilot templates."
    )
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--name", required=True, help="Change slug or name")
    parser.add_argument("--title", required=True, help="Human-readable change title")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing change directory"
    )
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    root = repo / "code_copilot"
    templates = root / "changes" / "templates"
    change_name = slugify(args.name)
    change_dir = root / "changes" / change_name

    if change_dir.exists() and any(change_dir.iterdir()) and not args.force:
        raise SystemExit(f"Change already exists: {change_dir}")

    if not templates.exists():
        raise SystemExit(f"Templates directory not found: {templates}")

    context = {
        "change_name": change_name,
        "change_title": args.title,
        "timestamp": now_iso(),
    }
    created = materialize_change(templates, change_dir, context)

    print(f"Created change package: {change_dir}")
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
