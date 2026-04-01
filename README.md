# talon_rebecca

Personal Talon command set and compatibility layer on top of upstream Talon/community packages.

See `CONTRIBUTING.md` for placement rules, test expectations, and the current settings layout.

## Privacy Boundary

This repository is for shareable Talon commands, actions, and docs.

Local-only commands and data should live in `~/.talon/user/talon_rebecca_private/`, not in this repo. Talon will still auto-load that directory because it is under `~/.talon/user/`, but it is outside the `user/talon_rebecca/` git repository.

Keep the following out of `user/talon_rebecca/` unless they are intentionally public:

- custom prompt libraries and text snippets
- absolute local paths
- local vault roots and personal note locations
- personal bookmarks and project-specific URLs
- hardware-specific device names
- personal workflow notes that are not meant for publication

Examples:

- private prompts/snippets: `~/.talon/user/talon_rebecca_private/tools/prompts/`
- private text snippets: `~/.talon/user/talon_rebecca_private/core/text/`
- local path aliases: `user/talon_rebecca/settings/system_paths-mac.lan.talon-list`

When adding a new command, prefer this rule:

- if it is reusable and safe to publish, keep it in `user/talon_rebecca/`
- if it contains personal content or environment details, put it in `user/talon_rebecca_private/`

## Import And Test Conventions

Use `user.talon_rebecca...` as the canonical import path for shared modules in both runtime code and pytest.

- prefer `from user.talon_rebecca.core.platform_utils import ...` over repo-root imports like `from core.platform_utils import ...`
- avoid `try/except ImportError` fallbacks for internal repo modules; keep optional imports limited to external platform dependencies
- keep pure logic importable under pytest via the package path configured in `pyproject.toml`
