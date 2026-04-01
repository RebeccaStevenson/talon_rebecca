# Preview Sync Workflow (Chrome + Localhost)

This workflow gives sentence-by-sentence read/highlight in Chrome preview pages and captures the current sentence to a sibling `*_notes/` directory.

## Components

- Chrome extension: `tools/preview_sync/preview_sync_chrome_extension/`
- Capture API service (localhost): `tools/preview_sync/capture_server.py`
- Talon server manager actions: `tools/preview_sync/preview_sync_server.py`

## Install extension

1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked**
4. Select `tools/preview_sync/preview_sync_chrome_extension`

## Talon commands (Chrome)

- `preview read start`
- `preview read premium`
- `preview read stop`
- `preview read capture`
- `read start`
- `read premium`
- `read stop`
- `read capture`
- `preview sync server start`
- `preview sync server stop`
- `preview sync server restart`

Default Chrome extension shortcuts:
- `cmd-shift-7`: start with macOS system voice (premium voice packs)
- `cmd-shift-8`: start with browser Web Speech
- `cmd-shift-9`: stop
- `cmd-shift-u`: capture current sentence

## Root mapping config

The capture service resolves source files from localhost URLs using:

- `~/.talon/user/talon_rebecca_private/settings/preview_sync_roots.json` (preferred)
- `user/talon_rebecca/settings/preview_sync_roots.json` (fallback)

Example:

```json
{
  "roots": [
    "/Users/rebec/localFiles"
  ]
}
```

For URL `/reports/paper.html`, resolver tries:
- `<root>/reports/paper.qmd`
- `<root>/reports/paper.md`
- `_site`-stripped variants as fallback

## Notes output

If source resolves to `.../paper.md` (or `.qmd`), captures append to:

- `.../paper_notes/paper_notes.md`

with blockquote format:

```markdown
> Captured sentence.
```

## Source pinning

The browser extension now pins the active source file per preview origin (for example
`http://localhost:6806`) before capture. This prevents captures from drifting into another
document's notes file when multiple previews are open.

## Debug log

Capture success/failure is logged to:

- `tools/preview_sync/preview_sync.log`

## Doctor script

Use the automated diagnostics/recovery script:

- `tools/preview_sync/preview_sync_doctor.sh all`
- `tools/preview_sync/preview_sync_doctor.sh health`
- `tools/preview_sync/preview_sync_doctor.sh fix`
- `tools/preview_sync/preview_sync_doctor.sh smoke`
- `tools/preview_sync/preview_sync_doctor.sh notes-path --source /path/to/file.md`
- `tools/preview_sync/preview_sync_doctor.sh capture-probe --source /path/to/file.md`
- `tools/preview_sync/preview_sync_doctor.sh debug`

Debug bundles are written to:

- `tools/preview_sync/debug/preview_sync_debug_YYYYmmdd_HHMMSS.txt`
