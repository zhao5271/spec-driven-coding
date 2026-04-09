#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import tomllib
from change_common import (
    ALLOWED_STATUSES,
    REQUIRED_FILES,
    load_meta,
    read_text,
    resolve_change_dir,
    validate_transition,
)
from task_common import extract_task_blocks, extract_task_ids, parse_depends_on, task_map


def validate_required_files(change_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (change_dir / name).exists():
            errors.append(f"missing required file: {name}")
    return errors


def validate_metadata(meta: dict[str, object]) -> list[str]:
    errors: list[str] = []
    status = meta.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"invalid status: {status!r}")
    return errors


def count_in_progress_tasks(tasks_text: str) -> int:
    return len(re.findall(r"^- Status:\s*in_progress\s*$", tasks_text, flags=re.MULTILINE))


def validate_tasks(tasks_text: str, current_status: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    in_progress_count = count_in_progress_tasks(tasks_text)
    if in_progress_count > 1:
        errors.append(f"multiple in_progress tasks found: {in_progress_count}")
    task_ids: set[str] = set()
    tasks = extract_task_blocks(tasks_text)
    tasks_by_id = {
        task["task_id"]: task
        for task in tasks
        if task["task_id"]
    }
    for task in tasks:
        heading = task["heading"]
        task_id = task["task_id"]
        goal = task["goal"]
        files = task["files"]
        verification = task["verification"]
        expected = task["expected_outcome"]
        status = task["status"]
        if not task_id:
            errors.append(f"{heading} is missing Task ID")
        elif task_id in task_ids:
            errors.append(f"duplicate Task ID found: {task_id}")
        else:
            task_ids.add(task_id)
        target = warnings if current_status in {"draft", "approved"} else errors
        if not goal:
            target.append(f"{heading} is missing Goal")
        if not files:
            target.append(f"{heading} is missing Files")
        if not verification:
            target.append(f"{heading} is missing Verification")
        if not expected:
            target.append(f"{heading} is missing Expected outcome")
        if status not in {"pending", "in_progress", "done", "blocked"}:
            errors.append(f"{heading} has invalid Status: {status or '(empty)'}")
        dependencies = parse_depends_on(task["depends_on"])
        for dependency in dependencies:
            if dependency not in tasks_by_id:
                errors.append(f"{heading} depends on unknown Task ID: {dependency}")
        if status in {"in_progress", "done"}:
            unmet_dependencies = [
                dependency
                for dependency in dependencies
                if tasks_by_id.get(dependency, {}).get("status") != "done"
            ]
            if unmet_dependencies:
                errors.append(
                    f"{heading} has unmet dependencies for status {status}: {', '.join(unmet_dependencies)}"
                )
    return errors, warnings


def validate_workflow_rules(meta: dict[str, object]) -> list[str]:
    errors: list[str] = []
    status = meta.get("status")
    approved = bool(meta.get("approved_by_user"))
    if not approved and status in {"in_progress", "verifying", "done"}:
        errors.append(f"status {status!r} requires approved_by_user=true")
    if status == "blocked" and not approved:
        errors.append("status 'blocked' requires approved_by_user=true")
    if approved and status == "draft":
        errors.append("approved_by_user=true conflicts with status 'draft'")
    if status == "done":
        if not str(meta.get("last_verification_command", "")).strip():
            errors.append("done status requires last_verification_command")
        if not str(meta.get("last_verification_result", "")).strip():
            errors.append("done status requires last_verification_result")
    if status == "in_progress" and not str(meta.get("current_task", "")).strip():
        errors.append("status 'in_progress' requires current_task")
    if status == "verifying" and not str(meta.get("last_verification_command", "")).strip():
        errors.append("status 'verifying' requires last_verification_command")
    return errors


def validate_task_linkage(meta: dict[str, object], tasks_text: str) -> list[str]:
    errors: list[str] = []
    task_ids = extract_task_ids(tasks_text)
    tasks_by_id = task_map(tasks_text)
    current_task = str(meta.get("current_task", "")).strip()
    next_task = str(meta.get("next_task", "")).strip()
    status = str(meta.get("status", "")).strip()

    if current_task and current_task not in task_ids:
        errors.append(f"current_task references unknown Task ID: {current_task}")
    if next_task and next_task not in task_ids:
        errors.append(f"next_task references unknown Task ID: {next_task}")
    if status == "in_progress" and current_task and task_ids and current_task not in task_ids:
        errors.append(f"in_progress status requires current_task to be one of: {', '.join(sorted(task_ids))}")
    if status == "in_progress" and current_task in tasks_by_id:
        unmet_dependencies = [
            dependency
            for dependency in parse_depends_on(tasks_by_id[current_task].get("depends_on", ""))
            if tasks_by_id.get(dependency, {}).get("status") != "done"
        ]
        if unmet_dependencies:
            errors.append(
                f"current_task {current_task} has unmet dependencies: {', '.join(unmet_dependencies)}"
            )
    return errors
def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a code_copilot change package.")
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", help="Specific change name to inspect")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    change_dir = resolve_change_dir(repo, args.change)

    errors = validate_required_files(change_dir)
    warnings: list[str] = []
    meta: dict[str, object] = {}
    if not errors:
        try:
            meta = load_meta(change_dir)
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"failed to parse change.toml: {exc}")

    tasks_text = read_text(change_dir / "tasks.md")
    if meta:
        errors.extend(validate_metadata(meta))
        errors.extend(validate_workflow_rules(meta))
        previous_status = str(meta.get("status", ""))
        transition_error = validate_transition(previous_status, previous_status)
        if transition_error:
            errors.append(transition_error)
    if tasks_text:
        task_errors, task_warnings = validate_tasks(tasks_text, str(meta.get("status", "draft")))
        errors.extend(task_errors)
        warnings.extend(task_warnings)
        if meta:
            errors.extend(validate_task_linkage(meta, tasks_text))

    payload = {
        "change": change_dir.name,
        "status": meta.get("status") if meta else None,
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("WARNINGS")
            for warning in warnings:
                print(f"- {warning}")
    else:
        print("VALID")
        for warning in warnings:
            print(f"- warning: {warning}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
