#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from change_common import load_meta, now_iso, resolve_change_dir, validate_transition, write_meta
from change_common import read_text
from task_common import extract_task_ids, parse_depends_on, sync_tasks_text, task_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Update a code_copilot change status with transition checks.")
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", required=True, help="Specific change name to update")
    parser.add_argument("--status", required=True, help="Target status")
    parser.add_argument("--phase", help="Optional current_phase override")
    parser.add_argument("--current-task", help="Optional current_task override")
    parser.add_argument("--next-task", help="Optional next_task override")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    change_dir = resolve_change_dir(repo, args.change)
    meta = load_meta(change_dir)
    tasks_text = read_text(change_dir / "tasks.md")
    task_ids = extract_task_ids(tasks_text)
    tasks_by_id = task_map(tasks_text)

    current_status = str(meta.get("status", ""))
    target_status = args.status.strip()
    transition_error = validate_transition(current_status, target_status)
    if transition_error:
        raise SystemExit(transition_error)

    if not bool(meta.get("approved_by_user")) and target_status in {"in_progress", "blocked", "verifying", "done"}:
        raise SystemExit(f"status {target_status!r} requires approved_by_user=true")
    if target_status == "done":
        raise SystemExit("Use close_change.py to mark a change done.")
    current_task = args.current_task if args.current_task is not None else str(meta.get("current_task", ""))
    next_task = args.next_task if args.next_task is not None else str(meta.get("next_task", ""))
    if current_task and task_ids and current_task not in task_ids:
        raise SystemExit(f"unknown current_task {current_task!r}; expected one of: {', '.join(sorted(task_ids))}")
    if next_task and task_ids and next_task not in task_ids:
        raise SystemExit(f"unknown next_task {next_task!r}; expected one of: {', '.join(sorted(task_ids))}")
    if target_status == "in_progress" and not current_task:
        raise SystemExit("status 'in_progress' requires --current-task <Task ID>")
    if target_status == "in_progress" and current_task:
        task = tasks_by_id.get(current_task)
        if task is None:
            raise SystemExit(f"unknown current_task {current_task!r}; expected one of: {', '.join(sorted(task_ids))}")
        unmet_dependencies = [
            dependency
            for dependency in parse_depends_on(task.get("depends_on", ""))
            if tasks_by_id.get(dependency, {}).get("status") != "done"
        ]
        if unmet_dependencies:
            raise SystemExit(
                f"cannot start {current_task!r}; unmet dependencies: {', '.join(unmet_dependencies)}"
            )

    meta["status"] = target_status
    meta["updated_at"] = now_iso()
    if args.phase is not None:
        meta["current_phase"] = args.phase
    if args.current_task is not None:
        meta["current_task"] = args.current_task
    if args.next_task is not None:
        meta["next_task"] = args.next_task
    write_meta(change_dir, meta)
    synced_tasks = sync_tasks_text(
        tasks_text,
        phase=args.phase,
        current_task=current_task,
        next_task=next_task,
        target_status=target_status,
        status_task=current_task,
    )
    (change_dir / "tasks.md").write_text(synced_tasks, encoding="utf-8")

    print(f"Updated change: {args.change}")
    print(f"Status: {current_status} -> {target_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
