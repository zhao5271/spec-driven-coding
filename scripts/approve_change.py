#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from change_common import load_meta, now_iso, resolve_change_dir, validate_transition, write_meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve a code_copilot change package.")
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--change", required=True, help="Specific change name to approve")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    change_dir = resolve_change_dir(repo, args.change)
    meta = load_meta(change_dir)

    meta["approved_by_user"] = True
    if meta.get("status") == "draft":
        transition_error = validate_transition("draft", "approved")
        if transition_error:
            raise SystemExit(transition_error)
        meta["status"] = "approved"
    meta["updated_at"] = now_iso()
    write_meta(change_dir, meta)

    print(f"Approved change: {change_dir.name}")
    print(f"Status: {meta.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
