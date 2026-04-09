#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from change_common import list_changes, load_meta, meta_path, read_text, resolve_change_dir
from task_common import extract_task_blocks


STATUS_KEYS = (
    "Current phase",
    "Current task",
    "Next task",
    "Blockers",
    "Last touched files",
    "Last verification command",
    "Last verification result",
    "Last known failing point",
    "Next concrete command",
)


def read_change_meta(change_dir: Path) -> dict[str, object]:
    meta_file = meta_path(change_dir)
    if not meta_file.exists():
        return {}
    data = load_meta(change_dir)
    data["__path__"] = str(meta_file)
    return data


def extract_bullets(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in STATUS_KEYS:
        match = re.search(rf"^- {re.escape(key)}:\s*(.*)$", text, flags=re.MULTILINE)
        values[key] = match.group(1).strip() if match else ""
    return values


def extract_task_statuses(text: str) -> list[str]:
    task_summaries: list[str] = []
    for task in extract_task_blocks(text):
        label = task["task_id"] or task["heading"]
        status = task["status"] or "(empty)"
        depends_on = task["depends_on"] or "none"
        task_summaries.append(f"{label}: {status} (depends_on={depends_on})")
    return task_summaries
def last_session_heading(text: str) -> str:
    matches = re.findall(r"^###\s+(Session .+)$", text, flags=re.MULTILINE)
    return matches[-1] if matches else ""


def format_change_summary(change_dir: Path) -> str:
    spec = change_dir / "spec.md"
    tasks = change_dir / "tasks.md"
    log = change_dir / "log.md"
    meta = read_change_meta(change_dir)

    tasks_text = read_text(tasks)
    log_text = read_text(log)
    bullets = extract_bullets(tasks_text)
    task_statuses = extract_task_statuses(tasks_text)

    updated_at = datetime.fromtimestamp(change_dir.stat().st_mtime).isoformat(sep=" ", timespec="seconds")

    lines = [
        f"Change: {change_dir.name}",
        f"Path: {change_dir}",
        f"Updated: {updated_at}",
        "",
        "Files:",
        f"- change.toml: {meta.get('__path__', change_dir / 'change.toml')}",
        f"- spec.md: {spec}",
        f"- tasks.md: {tasks}",
        f"- log.md: {log}",
        "",
        "Current Status:",
    ]

    status_values = {
        "Current phase": str(meta.get("current_phase") or bullets.get("Current phase") or "(empty)"),
        "Current task": str(meta.get("current_task") or bullets.get("Current task") or "(empty)"),
        "Next task": str(meta.get("next_task") or bullets.get("Next task") or "(empty)"),
        "Blockers": _format_meta_value(meta.get("blockers")) or bullets.get("Blockers") or "(empty)",
    }

    for key in STATUS_KEYS[:4]:
        lines.append(f"- {key}: {status_values[key]}")

    lines.extend(
        [
            "",
            "Metadata:",
            f"- Status: {meta.get('status', '(missing)')}",
            f"- Approved by user: {meta.get('approved_by_user', '(missing)')}",
            "",
            "Resume Checklist:",
        ]
    )
    resume_values = {
        "Last touched files": _format_meta_value(meta.get("last_touched_files")) or bullets.get("Last touched files") or "(empty)",
        "Last verification command": str(meta.get("last_verification_command") or bullets.get("Last verification command") or "(empty)"),
        "Last verification result": str(meta.get("last_verification_result") or bullets.get("Last verification result") or "(empty)"),
        "Last known failing point": str(meta.get("last_known_failing_point") or bullets.get("Last known failing point") or "(empty)"),
        "Next concrete command": str(meta.get("next_concrete_command") or bullets.get("Next concrete command") or "(empty)"),
    }
    for key in STATUS_KEYS[4:]:
        lines.append(f"- {key}: {resume_values[key]}")

    lines.extend(
        [
            "",
            "Task Statuses:",
        ]
    )
    if task_statuses:
        lines.extend(f"- {entry}" for entry in task_statuses)
    else:
        lines.append("- (no task status lines found)")

    lines.extend(
        [
            "",
            "Latest Session:",
            f"- {last_session_heading(log_text) or '(no session headings found)'}",
        ]
    )
    return "\n".join(lines)


def _format_meta_value(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else ""
    if value is None:
        return ""
    return str(value)


def format_change_brief(change_dir: Path) -> str:
    meta = read_change_meta(change_dir)
    status = meta.get("status", "(missing)")
    current_task = meta.get("current_task", "")
    next_task = meta.get("next_task", "")
    return f"{change_dir.name}: status={status} current_task={current_task or '(empty)'} next_task={next_task or '(empty)'}"


def format_change_json(change_dir: Path) -> dict[str, object]:
    tasks = change_dir / "tasks.md"
    log = change_dir / "log.md"
    tasks_text = read_text(tasks)
    log_text = read_text(log)
    meta = read_change_meta(change_dir)
    return {
        "change": change_dir.name,
        "path": str(change_dir),
        "updated_at": datetime.fromtimestamp(change_dir.stat().st_mtime).isoformat(sep=" ", timespec="seconds"),
        "meta": {key: value for key, value in meta.items() if key != "__path__"},
        "task_statuses": extract_task_statuses(tasks_text),
        "tasks": extract_task_blocks(tasks_text),
        "latest_session": last_session_heading(log_text),
    }
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize active code_copilot changes for low-token session recovery."
    )
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", help="Specific change name to inspect")
    parser.add_argument("--list", action="store_true", help="List change packages only")
    parser.add_argument("--brief", action="store_true", help="Show one-line change summary")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    changes_dir = repo / "code_copilot" / "changes"
    changes = list_changes(changes_dir)

    if not changes:
        raise SystemExit(f"No change packages found under: {changes_dir}")

    if args.list:
        print("Available changes:")
        for path in changes:
            print(f"- {path.name}")
        return 0

    selected = resolve_change_dir(repo, args.change)

    if args.json:
        print(json.dumps(format_change_json(selected), ensure_ascii=False, indent=2))
    elif args.brief:
        print(format_change_brief(selected))
    else:
        print(format_change_summary(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
