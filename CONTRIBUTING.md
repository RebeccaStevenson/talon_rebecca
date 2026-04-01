# Contributing Notes

This repo is the public/shareable Talon package. Talon also auto-loads `~/.talon/user/talon_rebecca_personal/`; keep local-only commands and personal data there instead of in this repo.

## Placement Rules

- Put pure Python logic in feature helpers that are testable without Talon runtime state.
- Keep Talon-facing action modules thin; they should mostly validate inputs, call helpers, and invoke Talon APIs.
- Mirror `user/community/` structure when preserving or overriding community behavior.
- Use feature folders such as `notes/`, `tools/`, or `productivity/` for Rebecca-specific workflows that are not community overrides.
- Put personal prompts, snippets, bookmarks, vault roots, absolute paths, and other personal config in `~/.talon/user/talon_rebecca_personal/`.

## Settings Rules

- Keep `settings/system_paths-mac.lan.talon-list`, `settings/vocabulary.talon-list`, and `settings/words_to_replace.csv` as the active local settings files under this repo.
- Keep personal website and search-engine additions in `~/.talon/user/talon_rebecca_personal/settings/{websites,search_engines}.talon-list`.
- Do not reintroduce stale CSV copies for websites, search engines, or additional words; the active sources of truth are the `.talon-list` files above plus `words_to_replace.csv`.

## Repository Scope

This repository is for shareable Talon commands, actions, and docs.

Local-only commands and data should live in `~/.talon/user/talon_rebecca_personal/`, not in this repo. Talon still auto-loads that directory because it is under `~/.talon/user/`, but it is outside the `user/talon_rebecca/` git repository.

Keep the following out of `user/talon_rebecca/` unless they are intentionally public:

- custom prompt libraries and text snippets
- absolute local paths
- local vault roots and personal note locations
- personal bookmarks and project-specific URLs
- hardware-specific device names
- personal workflow notes that are not meant for publication

Examples:

- personal prompts/snippets: `~/.talon/user/talon_rebecca_personal/tools/prompts/`
- personal text snippets: `~/.talon/user/talon_rebecca_personal/core/text/`
- local path aliases: `user/talon_rebecca/settings/system_paths-mac.lan.talon-list`

When adding a new command, prefer this rule:

- if it is reusable and safe to publish, keep it in `user/talon_rebecca/`
- if it contains personal content or environment details, put it in `user/talon_rebecca_personal/`

## Imports And Tests

Use `user.talon_rebecca...` as the canonical import path for shared modules in both runtime code and pytest.

- prefer `from user.talon_rebecca.core.platform_utils import ...` over repo-root imports like `from core.platform_utils import ...`
- avoid `try/except ImportError` fallbacks for internal repo modules; keep optional imports limited to external platform dependencies
- keep pure logic importable under pytest via the package path configured in `pyproject.toml`
- Put tests in `tests/`; extend `tests/stubs/talon/` only when a new Talon API must be mocked.
- For behavior-preserving refactors, run `python -m pytest tests/ -q` from the repo root and check `~/.talon/talon.log` for touched modules.

## Optional Local Tooling

- Install hooks with `python -m pip install pre-commit && pre-commit install`.
- The repo ships a minimal `.pre-commit-config.yaml` for `ruff`, merge-conflict checks, whitespace cleanup, and EOF normalization.
