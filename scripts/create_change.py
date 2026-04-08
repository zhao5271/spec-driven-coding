#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
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

    spec = read_template(templates / "spec.md").replace("# Change Spec", f"# {args.title}")
    tasks = read_template(templates / "tasks.md").replace("# Tasks", f"# Tasks - {args.title}")
    log = read_template(templates / "log.md").replace("# Change Log", f"# Change Log - {args.title}")

    write(change_dir / "spec.md", spec)
    write(change_dir / "tasks.md", tasks)
    write(change_dir / "log.md", log)

    print(f"Created change package: {change_dir}")
    print(change_dir / "spec.md")
    print(change_dir / "tasks.md")
    print(change_dir / "log.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
