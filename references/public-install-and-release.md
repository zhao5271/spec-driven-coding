# Public Install And Release

This note is for end users who want to install or pin `spec-driven-coding`.

## Install The Root Skill

Use GitHub install when you only want the main workflow skill:

```bash
npx skills add zhao5271/spec-driven-coding -g -y
```

## Install The Full Bundle

Use the repository bundle when you also want the companion skills shipped in this repo:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
./install.sh
```

## What Gets Installed

Root skill install:

- `spec-driven-coding`

Bundle install:

- `spec-driven-coding`
- `frontend-design`
- `api-design-principles`
- `postgresql-table-design`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

## Version Expectations

If you install directly from GitHub, you are effectively following the published repository state you choose to install from.

If you need a pinned version:

- install from a specific tag
- or pin your own internal install process to a known commit

## Release Notes

Check the repository tags, commit history, and GitHub releases if you want a human-readable summary of changes between versions.
