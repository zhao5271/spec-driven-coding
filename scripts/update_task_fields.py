#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from change_common import read_text, resolve_change_dir
from task_common import TASK_FIELD_NAMES, extract_task_ids, update_task_field


FIELD_NAME_MAP = {
    "task_id": "Task ID",
    "goal": "Goal",
    "files": "Files",
    "depends_on": "Depends on",
    "verification": "Verification",
    "expected_outcome": "Expected outcome",
    "status": "Status",
    "notes": "Notes",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Update fields for a task in tasks.md.")
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", required=True, help="Specific change name")
    parser.add_argument("--task-id", required=True, help="Task ID to update")
    parser.add_argument("--goal")
    parser.add_argument("--files")
    parser.add_argument("--depends-on")
    parser.add_argument("--verification")
    parser.add_argument("--expected-outcome")
    parser.add_argument("--status")
    parser.add_argument("--notes")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    change_dir = resolve_change_dir(repo, args.change)
    tasks_path = change_dir / "tasks.md"
    tasks_text = read_text(tasks_path)

    task_ids = extract_task_ids(tasks_text)
    if args.task_id not in task_ids:
        raise SystemExit(f"unknown task_id {args.task_id!r}; expected one of: {', '.join(sorted(task_ids))}")

    updates = {
        "goal": args.goal,
        "files": args.files,
        "depends_on": args.depends_on,
        "verification": args.verification,
        "expected_outcome": args.expected_outcome,
        "status": args.status,
        "notes": args.notes,
    }
    if not any(value is not None for value in updates.values()):
        raise SystemExit("no task field updates provided")

    updated = tasks_text
    for arg_name, value in updates.items():
        if value is None:
            continue
        field_name = FIELD_NAME_MAP[arg_name]
        if field_name not in TASK_FIELD_NAMES:
            raise SystemExit(f"unsupported task field: {field_name}")
        updated = update_task_field(updated, args.task_id, field_name, value)

    tasks_path.write_text(updated, encoding="utf-8")
    print(f"Updated task: {args.task_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
