#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tomllib


META_FILENAME = "change.toml"
REQUIRED_FILES = ("spec.md", "tasks.md", "log.md", META_FILENAME)
ALLOWED_STATUSES = {
    "draft",
    "approved",
    "in_progress",
    "blocked",
    "verifying",
    "done",
    "archived",
}
ALLOWED_TRANSITIONS = {
    "draft": {"approved", "archived"},
    "approved": {"in_progress", "blocked", "verifying", "archived"},
    "in_progress": {"blocked", "verifying", "approved", "archived"},
    "blocked": {"approved", "in_progress", "archived"},
    "verifying": {"approved", "in_progress", "blocked", "done", "archived"},
    "done": {"archived"},
    "archived": set(),
}
ORDERED_META_KEYS = [
    "name",
    "title",
    "status",
    "owner",
    "created_at",
    "updated_at",
    "approved_by_user",
    "current_phase",
    "current_task",
    "next_task",
    "blockers",
    "last_touched_files",
    "last_verification_command",
    "last_verification_result",
    "last_known_failing_point",
    "next_concrete_command",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def meta_path(change_dir: Path) -> Path:
    return change_dir / META_FILENAME


def load_meta(change_dir: Path) -> dict[str, object]:
    with meta_path(change_dir).open("rb") as fh:
        return tomllib.load(fh)


def format_toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        inner = ", ".join(format_toml_value(item) for item in value)
        return f"[{inner}]"
    return f'"{str(value).replace(chr(34), chr(92) + chr(34))}"'


def write_meta(change_dir: Path, meta: dict[str, object]) -> None:
    lines = [f"{key} = {format_toml_value(meta[key])}" for key in ORDERED_META_KEYS if key in meta]
    meta_path(change_dir).write_text("\n".join(lines) + "\n", encoding="utf-8")


def resolve_change_dir(repo: Path, change: str | None) -> Path:
    changes_dir = repo / "code_copilot" / "changes"
    if change:
        change_dir = changes_dir / change
        if not change_dir.exists():
            raise SystemExit(f"Change not found: {change}")
        return change_dir
    candidates = list_changes(changes_dir)
    if not candidates:
        raise SystemExit(f"No change packages found under: {changes_dir}")
    return candidates[0]


def list_changes(changes_dir: Path) -> list[Path]:
    if not changes_dir.exists():
        return []
    return sorted(
        [path for path in changes_dir.iterdir() if path.is_dir() and path.name != "templates"],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def validate_transition(current: str, target: str) -> str | None:
    if current not in ALLOWED_STATUSES:
        return f"invalid current status: {current!r}"
    if target not in ALLOWED_STATUSES:
        return f"invalid target status: {target!r}"
    if current == target:
        return None
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        return f"invalid status transition: {current!r} -> {target!r}"
    return None
