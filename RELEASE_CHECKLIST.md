# Release Checklist

Use this checklist before publishing a new version of the bundle.

## 1. Update The Main Skill

- [ ] Finish changes in `skills/spec-driven-coding/`
- [ ] Re-check `SKILL.md`, references, and scripts for consistency
- [ ] Validate the bundled main skill with your local `quick_validate.py` from the Codex `skill-creator` system skill
- [ ] Run:

```bash
python3 skills/spec-driven-coding/scripts/create_change.py --help
python3 skills/spec-driven-coding/scripts/scaffold_package.py --help
# Example:
# python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/spec-driven-coding
```

## 2. Verify Bundled Companion Skills

- [ ] Confirm each bundled skill is still needed:
  - [ ] `frontend-design`
  - [ ] `api-design-principles`
  - [ ] `postgresql-table-design`
  - [ ] `test-driven-development`
  - [ ] `systematic-debugging`
  - [ ] `verification-before-completion`
  - [ ] `requesting-code-review`
- [ ] Remove any bundled skill that is no longer part of the intended workflow
- [ ] Confirm bundled skill contents do not contain machine-specific absolute paths

## 3. Verify Installation Flow

- [ ] Run the installer into a temp directory:

```bash
TMPDIR=$(mktemp -d /tmp/spec-bundle-install.XXXXXX)
./install.sh --target "$TMPDIR"
find "$TMPDIR" -maxdepth 1 -mindepth 1 -type d | sort
```

- [ ] Confirm all expected skill folders are installed
- [ ] Re-run with `--force` if you changed overwrite behavior

## 4. Review README And Prompt Examples

- [ ] README still matches the actual bundle contents
- [ ] `1-Minute Install` commands still work
- [ ] Prompt cheat sheet still matches the intended workflow
- [ ] Repository layout section matches the real directory structure

## 5. Review License And Third-Party Notices

- [ ] Root `LICENSE` still reflects repository-owned files correctly
- [ ] `THIRD_PARTY_NOTICES.md` still matches the bundled skills
- [ ] Review whether any newly bundled third-party skill includes its own license file
- [ ] Re-check redistribution rights before public release

## 6. Git Hygiene

- [ ] Review changes:

```bash
git status
git diff --stat
```

- [ ] Commit with a clear message
- [ ] Push `main`

## 7. Optional Release Step

- [ ] Create a tag if this is a versioned release:

```bash
git tag v0.x.y
git push origin v0.x.y
```

- [ ] Draft GitHub release notes summarizing:
  - [ ] skill workflow changes
  - [ ] bundled skill changes
  - [ ] README or install changes
  - [ ] license or notice changes
