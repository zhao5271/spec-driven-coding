#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from change_common import load_meta, now_iso, read_text, resolve_change_dir, validate_transition, write_meta
from task_common import sync_tasks_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and close a code_copilot change package.")
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", required=True, help="Specific change name to close")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    validate_script = Path(__file__).resolve().parent / "validate_change.py"
    result = subprocess.run(
        [sys.executable, str(validate_script), "--target", str(repo), "--change", args.change],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)

    change_dir = resolve_change_dir(repo, args.change)
    meta = load_meta(change_dir)

    if not bool(meta.get("approved_by_user")):
        raise SystemExit("Cannot close change before approval.")
    if not str(meta.get("last_verification_command", "")).strip():
        raise SystemExit("Cannot close change without last_verification_command.")
    if not str(meta.get("last_verification_result", "")).strip():
        raise SystemExit("Cannot close change without last_verification_result.")
    transition_error = validate_transition(str(meta.get("status", "")), "done")
    if transition_error:
        raise SystemExit(transition_error)

    current_task = str(meta.get("current_task", "")).strip()
    meta["status"] = "done"
    meta["current_phase"] = "done"
    meta["current_task"] = ""
    meta["next_task"] = ""
    meta["updated_at"] = now_iso()
    write_meta(change_dir, meta)
    tasks_path = change_dir / "tasks.md"
    synced_tasks = sync_tasks_text(
        read_text(tasks_path),
        phase="done",
        current_task="",
        next_task="",
        target_status="done",
        status_task=current_task,
    )
    tasks_path.write_text(synced_tasks, encoding="utf-8")

    print(f"Closed change: {args.change}")
    print("Status: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
