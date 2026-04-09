#!/usr/bin/env python3
from __future__ import annotations

import re


TASK_FIELD_NAMES = {
    "Task ID",
    "Goal",
    "Files",
    "Depends on",
    "Verification",
    "Expected outcome",
    "Status",
    "Notes",
}


def extract_task_blocks(tasks_text: str) -> list[dict[str, str]]:
    matches = list(re.finditer(r"^##\s+(Task.+)$", tasks_text, flags=re.MULTILINE))
    blocks: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tasks_text)
        block = tasks_text[start:end]
        blocks.append(
            {
                "heading": match.group(1).strip(),
                "task_id": extract_task_field(block, "Task ID"),
                "goal": extract_task_field(block, "Goal"),
                "files": extract_task_field(block, "Files"),
                "depends_on": extract_task_field(block, "Depends on"),
                "verification": extract_task_field(block, "Verification"),
                "expected_outcome": extract_task_field(block, "Expected outcome"),
                "status": extract_task_field(block, "Status"),
                "notes": extract_task_field(block, "Notes"),
            }
        )
    return blocks


def extract_task_field(block_text: str, field: str) -> str:
    match = re.search(rf"^- {re.escape(field)}:[ \t]*(.*)$", block_text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_task_ids(tasks_text: str) -> set[str]:
    return {task["task_id"] for task in extract_task_blocks(tasks_text) if task["task_id"]}


def parse_depends_on(value: str) -> list[str]:
    if not value:
        return []
    parts = [item.strip() for item in value.split(",")]
    return [item for item in parts if item]


def task_map(tasks_text: str) -> dict[str, dict[str, str]]:
    return {
        task["task_id"]: task
        for task in extract_task_blocks(tasks_text)
        if task["task_id"]
    }


def update_status_bullet(tasks_text: str, label: str, value: str) -> str:
    pattern = rf"^(- {re.escape(label)}:)[ \t]*(.*)$"
    replacement = rf"\1 {value}"
    updated, count = re.subn(pattern, replacement, tasks_text, count=1, flags=re.MULTILINE)
    return updated if count else tasks_text


def sync_tasks_text(
    tasks_text: str,
    *,
    phase: str | None = None,
    current_task: str | None = None,
    next_task: str | None = None,
    target_status: str,
    status_task: str | None = None,
) -> str:
    updated = tasks_text
    if phase is not None:
        updated = update_status_bullet(updated, "Current phase", phase)
    if current_task is not None:
        updated = update_status_bullet(updated, "Current task", current_task)
    if next_task is not None:
        updated = update_status_bullet(updated, "Next task", next_task)

    tasks = extract_task_blocks(updated)
    task_status_map = {
        task["task_id"]: (task["status"] or "pending")
        for task in tasks
        if task["task_id"]
    }
    active_task = status_task if status_task is not None else current_task
    if target_status == "in_progress" and active_task in task_status_map:
        for task_id, status in list(task_status_map.items()):
            if status == "in_progress":
                task_status_map[task_id] = "pending"
        task_status_map[active_task] = "in_progress"
    elif target_status == "blocked" and active_task in task_status_map:
        task_status_map[active_task] = "blocked"
    elif target_status in {"verifying", "done"} and active_task in task_status_map:
        task_status_map[active_task] = "done"

    for task_id, status in task_status_map.items():
        updated = update_task_field(updated, task_id, "Status", status)
    return updated


def update_task_field(tasks_text: str, task_id: str, field: str, value: str) -> str:
    if field not in TASK_FIELD_NAMES:
        raise ValueError(f"unsupported task field: {field}")
    matches = list(re.finditer(r"^##\s+(Task.+)$", tasks_text, flags=re.MULTILINE))
    if not matches:
        return tasks_text

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tasks_text)
        block = tasks_text[start:end]
        if f"- Task ID: {task_id}" not in block:
            continue
        pattern = rf"^(- {re.escape(field)}:)[ \t]*(.*)$"
        replacement = rf"\1 {value}"
        updated_block, count = re.subn(pattern, replacement, block, count=1, flags=re.MULTILINE)
        if not count:
            return tasks_text
        return tasks_text[:start] + updated_block + tasks_text[end:]
    return tasks_text
