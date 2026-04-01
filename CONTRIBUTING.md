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

## Imports And Tests

- Use `user.talon_rebecca...` as the canonical import path for internal shared modules.
- Put tests in `tests/`; extend `tests/stubs/talon/` only when a new Talon API must be mocked.
- For behavior-preserving refactors, run `python -m pytest tests/ -q` from the repo root and check `~/.talon/talon.log` for touched modules.

## Optional Local Tooling

- Install hooks with `python -m pip install pre-commit && pre-commit install`.
- The repo ships a minimal `.pre-commit-config.yaml` for `ruff`, merge-conflict checks, whitespace cleanup, and EOF normalization.
